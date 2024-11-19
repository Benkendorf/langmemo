from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('create_deck/', views.DeckCreateView.as_view(), name='create_deck'),
    path('', views.DeckListView.as_view(), name='index'),

]
