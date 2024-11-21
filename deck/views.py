from random import choice

from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
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

CARDS_PAGINATION_LIMIT = 15

sample_deck = {
    'deck_id': 1,
    'deck_name': 'Рофлан Колода',
    'card_list': {
        'ligma',
        'sugma',
        'sugondese'
    }
}


class CardListView(ListView):
    model = Card
    template_name = 'deck/card_list.html'
    paginate_by = CARDS_PAGINATION_LIMIT

    def get_queryset(self):
        deck = get_object_or_404(
            Deck,
            pk=self.kwargs['deck_id'],
            user=self.request.user
        )

        qs = Card.objects.filter(deck=deck)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = CardForm()
        context['deck'] = get_object_or_404(
            Deck,
            pk=self.kwargs['deck_id'],
            user=self.request.user
        )
        context['card_count'] = context['deck'].cards.count()

        return context


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    form_class = CardForm
    template_name = 'deck/card_list.html'
    paginate_by = CARDS_PAGINATION_LIMIT

    def form_valid(self, form):
        form.instance.deck = get_object_or_404(
            Deck,
            id=self.kwargs['deck_id'],
            user=self.request.user
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        # Тут вручную передаем то же, что передается в CardListView
        context = super().get_context_data(*args, **kwargs)
        context['deck'] = get_object_or_404(
            Deck,
            pk=self.kwargs['deck_id'],
            user=self.request.user
        )
        context['card_count'] = context['deck'].cards.count()

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

    if request.method == 'GET':
        cards_to_review = list(Card.objects.filter(
            in_queue=True,
            deck__id=deck_id
        ))

        if len(cards_to_review) == 0:
            return render(
                request,
                template_name='deck/review_no_cards_in_queue.html'
            )

        context = {
            'reviewed_card': choice(cards_to_review)    # random.choice
        }

        return render(
            request,
            template_name='deck/review.html',
            context=context
        )
    # Здесь дописать функционал когда метод POST
    # Лучше наверное сделать для проверки отдельную вьюшку с кард_ид в аргах


def review_check(request, card_id):
    print(request.POST) # Желательно получить ответ без bootstrap_form

    return render(
            request,
            template_name='deck/review_success.html',
        )
