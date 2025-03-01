from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

UserModel = get_user_model()


class ApiTokenView(LoginRequiredMixin, ListView):
    model = UserModel
    template_name = 'tg_bot_page/tg_bot_page.html'

    def get_queryset(self):
        return self.request.user
