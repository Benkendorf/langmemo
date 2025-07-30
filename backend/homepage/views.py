from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count, Q, Sum
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from deck.models import Card, Deck
from deck.forms import DeckForm

from deck.views import refresh_queue

from django_mem_cards.constants import (SRS_LEVELS,
                                        DECKS_PAGINATION_LIMIT,
                                        DECK_BAD_WINRATE_LIMIT,
                                        WEEKDAYS_RUS,
                                        TOTAL_CALENDAR_DAYS)


def get_total_queue_end_of_day(plus_days, user):
    """Функция, возвращающая суммарное количество карт, которые
    будут находится в очереди в 23:59:59 в день сегодня+plus_days.
    """

    cards = Card.objects.filter(
        deck__user=user
    )
    total = 0
    for card in cards:
        if (card.datetime_reviewed is None) or (timezone.make_aware(datetime(year=timezone.now().year, month=timezone.now().month, day=timezone.now().day, hour=23, minute=59, second=59) + timedelta(days=plus_days)) - card.datetime_reviewed > timedelta(hours=SRS_LEVELS[card.srs_level]['time_interval_hrs'])):
            total += 1
    return total


class DeckListView(ListView):
    """Класс, отвечающий за отображение списка колод на главной."""

    model = Deck
    paginate_by = DECKS_PAGINATION_LIMIT
    template_name = 'homepage/index.html'

    def get_queryset(self):
        qs = Deck.objects.filter(
            user__id=self.request.user.pk
        ).annotate(
            card_count=Count('cards')
        ).annotate(
            winrate=Avg('cards__winrate')
        ).annotate(
            cards_in_queue=Count('cards', filter=Q(cards__in_queue=True))
        )

        refresh_queue(user=self.request.user, deck_list=qs)

        return qs.order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cards_total_now = self.get_queryset().aggregate(Sum("cards_in_queue"))['cards_in_queue__sum']
        if cards_total_now is None:
            cards_total_now = 0

        if self.request.user.is_authenticated:
            end_of_day_totals = [
                get_total_queue_end_of_day(plus_days=i, user=self.request.user)
                for i in range(TOTAL_CALENDAR_DAYS)
            ]
            calendar = [
                {'weekday': 'Сегодня',
                 'diff': end_of_day_totals[0] - cards_total_now,
                 'end_of_day': end_of_day_totals[0]},
            ] + [
                {'weekday': WEEKDAYS_RUS[(timezone.now().weekday() + i) % 7],
                 'diff': end_of_day_totals[i] - end_of_day_totals[i - 1],
                 'end_of_day': end_of_day_totals[i]}
                for i in range(1, TOTAL_CALENDAR_DAYS)
            ]
        else:
            calendar = []

        context['form'] = DeckForm()
        context['deck_bad_winrate'] = DECK_BAD_WINRATE_LIMIT
        context['cards_total_now'] = cards_total_now
        context['calendar'] = calendar

        return context


class DeckCreateView(LoginRequiredMixin, CreateView):
    """Класс, отвечающий за создание колоды."""

    model = Deck
    form_class = DeckForm
    template_name = 'homepage/index.html'

    def get(self, *args, **kwargs):
        return redirect(reverse_lazy('homepage:index'))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('deck:card_list',
                            kwargs={'deck_id': self.object.id})


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
