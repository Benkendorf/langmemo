from django.utils import timezone
from datetime import timedelta
from random import choice
from sys import maxsize

from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from .models import Card, Deck
from .forms import CardForm
from .utils import damerau_levenshtein_distance as dam_lev_dist

CARDS_PAGINATION_LIMIT = 15
CARD_BAD_WINRATE_LIMIT = 50
DAM_LEV_DIST_LIMIT = 1
SRS_LEVELS_DICT = {
    0: {'xp_to_next_lvl': 3, 'time_interval_hrs': 6},
    1: {'xp_to_next_lvl': 5, 'time_interval_hrs': 24},
    2: {'xp_to_next_lvl': 5, 'time_interval_hrs': 48},
    3: {'xp_to_next_lvl': 10, 'time_interval_hrs': 72},
    4: {'xp_to_next_lvl': None, 'time_interval_hrs': 120}
}


def refresh_queue(user, deck_list):
    """Функция, актуализирующая статус in_queue всех карт пользователя"""
    cards = Card.objects.filter(
            #Q(datetime_reviewed=None) | Q(timezone.now() - F('datetime_reviewed') > timedelta(hours=SRS_LEVELS_DICT[F('srs_level')]['time_interval_hrs'])),
            deck__user__id=user.pk,
            deck__in=deck_list,
            in_queue=False
        )
    # Нужно сделать один запрос, апдейтящий все нужные карты,
    # а не много запросов, каждый апдейтящий одну карту.
    cards_to_update = []
    for card in cards:
        if (card.datetime_reviewed is None) or (timezone.now() - card.datetime_reviewed > timedelta(hours=SRS_LEVELS_DICT[card.srs_level]['time_interval_hrs'])):
            card.in_queue = True
            cards_to_update.append(card)

    cards.bulk_update(cards_to_update, fields=['in_queue'])
    """
    for card in cards:
        if not card.in_queue and ((card.datetime_reviewed is None) or (timezone.now() - card.datetime_reviewed > timedelta(hours=SRS_LEVELS_DICT[card.srs_level]['time_interval_hrs']))):
            card.in_queue = True
            card.save(update_fields=['in_queue'])
    """


class CardListView(ListView):
    """Класс, отвечающий за отображение списка карт на странице колоды."""
    model = Card
    template_name = 'deck/card_list.html'
    paginate_by = CARDS_PAGINATION_LIMIT

    def get_queryset(self):
        self.deck = get_object_or_404(
            Deck,
            pk=self.kwargs['deck_id'],
            user=self.request.user
        )

        # Для корректной отображения ответов только у кард не в очереди
        refresh_queue(user=self.request.user, deck_list=(self.deck,))

        qs = Card.objects.filter(deck=self.deck)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = CardForm()
        context['deck'] = self.deck
        context['card_count'] = context['deck'].cards.count()
        context['card_bad_winrate'] = CARD_BAD_WINRATE_LIMIT

        return context


class CardCreateView(LoginRequiredMixin, CreateView):
    """Класс, отвечающий за создание карты."""
    model = Card
    form_class = CardForm
    template_name = 'deck/card_list.html'
    paginate_by = CARDS_PAGINATION_LIMIT

    def form_valid(self, form):
        self.deck = get_object_or_404(
            Deck,
            id=self.kwargs['deck_id'],
            user=self.request.user
        )
        # Для корректной отображения ответов только у кард не в очереди
        refresh_queue(user=self.request.user, deck_list=(self.deck,))
        form.instance.deck = self.deck
        return super().form_valid(form)

    def form_invalid(self, form):
        self.deck = get_object_or_404(
            Deck,
            id=self.kwargs['deck_id'],
            user=self.request.user
        )
        # Для корректной отображения ответов только у кард не в очереди
        refresh_queue(user=self.request.user, deck_list=(self.deck,))
        return super().form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        # Тут вручную передаем то же, что передается в CardListView
        context = super().get_context_data(*args, **kwargs)
        context['deck'] = self.deck
        context['card_count'] = context['deck'].cards.count()
        context['card_bad_winrate'] = CARD_BAD_WINRATE_LIMIT

        paginator = Paginator(
            Card.objects.filter(deck=context['deck']),
            self.paginate_by
        )
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context

    def get_success_url(self):
        return reverse_lazy('deck:card_list',
                            kwargs={'deck_id': self.kwargs['deck_id']})


class CardDeleteView(UserPassesTestMixin, DeleteView):
    """Класс, отвечающий за удаление карты."""
    model = Card

    def test_func(self):
        object = self.get_object()
        return object.deck.user == self.request.user

    def get_object(self, queryset=None):
        return get_object_or_404(
            Card,
            id=self.kwargs['card_id'],
            deck__id=self.kwargs['deck_id']
        )

    def get_success_url(self):
        return reverse('deck:card_list',
                       kwargs={'deck_id': self.kwargs['deck_id']})


class DeckDeleteView(UserPassesTestMixin, DeleteView):
    """Класс, отвечающий за удаление колоды."""
    model = Deck

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user

    def get_object(self, queryset=None):
        return get_object_or_404(
            Deck,
            id=self.kwargs['deck_id']
        )

    def get_success_url(self):
        return reverse('homepage:index')


def review_display(request, deck_id):
    """Функция, отображающая очередную карту для ревью."""

    deck = get_object_or_404(
        Deck,
        id=deck_id
    )
    refresh_queue(user=request.user, deck_list=(deck,))

    cards_to_review = list(Card.objects.filter(
        in_queue=True,
        deck__id=deck_id
    ))

    if len(cards_to_review) == 0:
        return redirect(reverse('homepage:index'))

    context = {
        'reviewed_card': choice(cards_to_review)    # random.choice
    }

    return render(
        request,
        template_name='deck/review.html',
        context=context
    )


def review_check(request, card_id):
    """Функция, проверяющая ответ на ревью."""

    update_fields = ['in_queue', 'datetime_reviewed', 'srs_xp', 'srs_level']

    reviewed_card = get_object_or_404(
        Card,
        id=card_id,
        deck__user=request.user
    )
    if not reviewed_card.in_queue:
        template_name = 'deck/review_not_in_queue.html'
    else:
        min_dist = maxsize
        for ans in (reviewed_card.answer_1,
                    reviewed_card.answer_2,
                    reviewed_card.answer_3):
            if ans is not None:
                min_dist = min(
                    min_dist,
                    dam_lev_dist(
                        str.lower(request.POST['answer']),
                        str.lower(ans)
                    )
                )
        if min_dist <= DAM_LEV_DIST_LIMIT:
            template_name = 'deck/review_success.html'
            reviewed_card.right_guesses += 1
            update_fields.append('right_guesses')
            if reviewed_card.srs_level < 4:
                reviewed_card.srs_xp += 1
                # По-хорошему, "больше" быть не может, но на всякий случай учтем и этот случай.
                if reviewed_card.srs_xp >= SRS_LEVELS_DICT[reviewed_card.srs_level]['xp_to_next_lvl']:
                    reviewed_card.srs_level += 1
                    reviewed_card.srs_xp = 0
        else:
            template_name = 'deck/review_failure.html'
            reviewed_card.wrong_guesses += 1
            update_fields.append('wrong_guesses')
            reviewed_card.srs_xp = 0
            if reviewed_card.srs_level > 0:
                reviewed_card.srs_level -= 1

        reviewed_card.datetime_reviewed = timezone.now()
        reviewed_card.in_queue = False
        reviewed_card.save(update_fields=update_fields)

    return render(
            request,
            template_name=template_name,
            context={
                'reviewed_card': reviewed_card
            }
        )
