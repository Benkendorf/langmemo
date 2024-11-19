from django.shortcuts import render


sample_deck = {
    'deck_id': 1,
    'deck_name': 'Рофлан Колода',
    'card_list': {
        'ligma',
        'sugma',
        'sugondese'
    }
}

def card_list(request, deck_id):
    return render(
        request,
        template_name='deck/deck_card_list.html',
        context={
            'deck': sample_deck
        }
    )


def review(request, deck_id):
    return render(
        request,
        template_name='deck/review.html',
        context={
            'deck': sample_deck
        }
    )
