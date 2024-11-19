from django.db.models import Count, Avg
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.shortcuts import render

from deck.models import Deck

PAGINATION_LIMIT = 10


placeholder_decks = [
    {'name': 'English',
     'cards_qty': 120,
     'winrate': 0.78,
     'in_queue': 28},

    {'name': '日本語',
     'cards_qty': 243,
     'winrate': 0.64,
     'in_queue': 0},

    {'name': 'Français',
     'cards_qty': 156,
     'winrate': 0.43,
     'in_queue': 45},

    {'name': 'Deutsch',
     'cards_qty': 349,
     'winrate': 0.69,
     'in_queue': 32},
]


def index(request):
    return render(
        request,
        template_name='homepage/index.html',
        context={'decks': placeholder_decks})


class DeckListView(ListView):
    model = Deck
    paginate_by = PAGINATION_LIMIT
    template_name = 'homepage/index.html'

    def get_queryset(self):
        qs = Deck.objects.filter(
            user__id=self.request.user.pk
        ).annotate(
            card_count=Count('cards')
        ).annotate(
            winrate=Avg('cards__right_guesses') * 100
            / (Avg('cards__right_guesses') + Avg('cards__wrong_guesses'))
        )

        return qs.order_by('pk')
