from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from .models import Card, Deck
from .forms import CardForm, DeckForm

CARDS_PAGINATION_LIMIT = 20

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

        return context


class CardCreateView(CreateView):
    model = Card
    form_class = CardForm
    template_name = 'deck/card_list.html'

    def form_valid(self, form):
        form.instance.deck = get_object_or_404(
            Deck,
            id=self.kwargs['deck_id'],
            user=self.request.user
        )
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['deck'] = get_object_or_404(
            Deck,
            pk=self.kwargs['deck_id'],
            user=self.request.user
        )

        return context

    def get_success_url(self):
        return reverse_lazy('deck:card_list',
                            kwargs={'deck_id': self.kwargs['deck_id']})


class CardDeleteView(DeleteView, UserPassesTestMixin):
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


class DeckDeleteView(DeleteView, UserPassesTestMixin):
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


def review(request, deck_id):
    return render(
        request,
        template_name='deck/review.html',
        context={
            'deck': sample_deck
        }
    )
