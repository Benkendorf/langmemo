from django.urls import path
from . import views

app_name = 'tg_bot_page'

urlpatterns = [
    path('', views.ApiTokenView.as_view(), name='tg_bot_page_view'),

]
