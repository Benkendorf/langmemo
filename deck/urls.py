from django.urls import path
from . import views

app_name = 'deck'

urlpatterns = [
    path('<int:deck_id>/', views.CardListView.as_view(), name='card_list'),
    path('<int:deck_id>/review/', views.review, name='review'),
    path(
        '<int:deck_id>/delete/<int:card_id>/',
        views.CardDeleteView.as_view(),
        name='delete_card'
    ),
    path(
        '<int:deck_id>/delete_deck/',
        views.DeckDeleteView.as_view(),
        name='delete_deck'
    ),
    # мэйби 'create/' - как страница создания новой колоды
]
