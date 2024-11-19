from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from .models import Card, Deck

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


def card_list(request, deck_id):
    return render(
        request,
        template_name='deck/deck_card_list.html',
        context={
            'deck': sample_deck
        }
    )


def review(request, deck_id):
    return render(
        request,
        template_name='deck/review.html',
        context={
            'deck': sample_deck
        }
    )
