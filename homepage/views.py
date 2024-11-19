from django.db.models import Avg, Count, Q
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.shortcuts import render

from deck.models import Deck

DECKS_PAGINATION_LIMIT = 10


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

        return qs.order_by('pk')
