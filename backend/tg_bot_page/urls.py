from django.urls import path
from . import views

app_name = 'tg_bot_page'

urlpatterns = [
    path('', views.ApiTokenPageView.as_view(), name='tg_bot_page_view'),
    path('create_api_token/', views.create_api_token, name='create_api_token'),
    path('delete_api_token/', views.delete_api_token, name='delete_api_token'),

]
