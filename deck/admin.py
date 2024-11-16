from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Deck, Card

admin.site.register(Deck)
admin.site.register(Card)
