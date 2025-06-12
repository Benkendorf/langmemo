from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.description.as_view(), name='description'),

]
