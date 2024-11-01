from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Deck, Card

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Deck)
admin.site.register(Card)
