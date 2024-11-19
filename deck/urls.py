from django.urls import path
from . import views

app_name = 'deck'

urlpatterns = [
    path('<int:deck_id>/', views.card_list, name='card_list'),
    path('<int:deck_id>/review/', views.review, name='review'),
    # мэйби 'create/' - как страница создания новой колоды
]
