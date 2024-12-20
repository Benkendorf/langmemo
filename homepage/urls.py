from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path(
        'create_deck/',
        views.DeckCreateView.as_view(),
        name='create_deck'
    ),
    path(
        '<int:deck_id>/delete_deck/',
        views.DeckDeleteView.as_view(),
        name='delete_deck'
    ),
    path('', views.DeckListView.as_view(), name='index'),

]
