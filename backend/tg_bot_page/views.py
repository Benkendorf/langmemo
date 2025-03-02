import random
import string

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView

from django_mem_cards.constants import API_TOKEN_LENGTH


UserModel = get_user_model()


class ApiTokenPageView(LoginRequiredMixin, ListView):
    model = UserModel
    template_name = 'tg_bot_page/tg_bot_page.html'

    def get_queryset(self):
        return self.request.user


@login_required
def create_api_token(request):
    current_user = request.user
    if current_user.api_token is not None:
        return redirect(reverse_lazy('tg_bot_page:tg_bot_page_view'))
    current_user.api_token = ''.join(random.choices(
        string.ascii_letters + string.digits, k=API_TOKEN_LENGTH)
    )
    current_user.save(update_fields=['api_token'])
    return redirect(reverse('tg_bot_page:tg_bot_page_view'))


@login_required
def delete_api_token(request):
    current_user = request.user
    if current_user.api_token is not None:
        current_user.api_token = None
        current_user.save(update_fields=['api_token'])
    return redirect(reverse('tg_bot_page:tg_bot_page_view'))


# При создании токена, если токен уже есть у пользователя - редиректить на страницу tg_bot_page
