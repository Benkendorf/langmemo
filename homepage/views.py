from django.shortcuts import render


placeholder_decks = [
    {'name': 'English',
     'cards_qty': 120,
     'winrate': 0.78,
     'in_queue': 28},

    {'name': '日本語',
     'cards_qty': 243,
     'winrate': 0.64,
     'in_queue': 0},

    {'name': 'Français',
     'cards_qty': 156,
     'winrate': 0.43,
     'in_queue': 45},

    {'name': 'Deutsch',
     'cards_qty': 349,
     'winrate': 0.69,
     'in_queue': 32},
]


def index(request):
    return render(
        request,
        template_name='homepage/index.html',
        context={'decks': placeholder_decks})
