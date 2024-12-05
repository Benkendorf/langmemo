from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count, Q
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from deck.models import Card, Deck
from deck.forms import DeckForm
from deck.views import SRS_LEVELS_DICT

from deck.views import refresh_queue

DECKS_PAGINATION_LIMIT = 9
DECK_BAD_WINRATE_LIMIT = 50


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
        context['form'] = DeckForm()
        context['deck_bad_winrate'] = DECK_BAD_WINRATE_LIMIT

        return context


class DeckCreateView(LoginRequiredMixin, CreateView):
    """Класс, отвечающий за создание колоды."""
    model = Deck
    form_class = DeckForm
    template_name = 'homepage/index.html'

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