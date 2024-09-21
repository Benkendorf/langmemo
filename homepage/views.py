from django.shortcuts import render


placeholder_decks = [
    {'name': 'English',
     'cards_qty': 120,
     'winrate': 0.78},

    {'name': 'French',
     'cards_qty': 156,
     'winrate': 0.63},
]

def index(request):
    return render(
        request,
        template_name='homepage/index.html',
        context={'decks': placeholder_decks})
