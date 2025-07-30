import random
import string

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from django_mem_cards.constants import API_TOKEN_LENGTH


UserModel = get_user_model()


class description(TemplateView):
    template_name = 'pages/description.html'


class tutorial(LoginRequiredMixin, TemplateView):
    template_name = 'pages/tutorial.html'


class ApiTokenPageView(LoginRequiredMixin, ListView):
    model = UserModel
    template_name = 'pages/tg_bot_page.html'

    def get_queryset(self):
        return self.request.user


@login_required
def create_api_token(request):
    current_user = request.user
    if current_user.api_token is not None:
        return redirect(reverse_lazy('pages:tg_bot_page_view'))

    all_users = UserModel.objects.all()
    all_tokens = [user.api_token for user in all_users if user.api_token is not None]

    new_token = ''.join(random.choices(
        string.ascii_letters + string.digits, k=API_TOKEN_LENGTH)
    )
    while new_token in all_tokens:
        new_token = ''.join(random.choices(
            string.ascii_letters + string.digits, k=API_TOKEN_LENGTH)
        )
    current_user.api_token = new_token
    current_user.save(update_fields=['api_token'])
    return redirect(reverse('pages:tg_bot_page_view'))


@login_required
def delete_api_token(request):
    current_user = request.user
    if current_user.api_token is not None:
        current_user.api_token = None
    if current_user.telegram_chat_id is not None:
        current_user.telegram_chat_id = None    # Удаляем также и связь с ТГ
    current_user.save(update_fields=['api_token', 'telegram_chat_id'])
    return redirect(reverse('pages:tg_bot_page_view'))


# При создании токена, если токен уже есть у пользователя - редиректить на страницу tg_bot_page
