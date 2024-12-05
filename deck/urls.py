from django.urls import path
from . import views

app_name = 'deck'

urlpatterns = [
    path('<int:deck_id>/review/', views.review_display, name='review_display'),
    path('review_check/<int:card_id>/', views.review_check, name='review_check'),
    path(
        '<int:deck_id>/create_card/',
        views.CardCreateView.as_view(),
        name='create_card'
    ),
    path(
        '<int:deck_id>/delete_card/<int:card_id>/',
        views.CardDeleteView.as_view(),
        name='delete_card'
    ),
    path('<int:deck_id>/', views.CardListView.as_view(), name='card_list'),
    # мэйби 'create/' - как страница создания новой колоды
]
