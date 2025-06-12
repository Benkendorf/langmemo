from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.description.as_view(), name='description'),
    path('tg/', views.ApiTokenPageView.as_view(), name='tg_bot_page_view'),
    path('tg/create_api_token/', views.create_api_token, name='create_api_token'),
    path('tg/delete_api_token/', views.delete_api_token, name='delete_api_token'),

]
