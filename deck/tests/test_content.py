from django.urls import reverse

from deck.forms import CardForm


def test_card_list_contains_form(deck_owner_client, deck_id_for_args):
    url = reverse('deck:card_list', args=deck_id_for_args)
    response = deck_owner_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CardForm)


def test_cards_are_in_deck_list(deck_owner_client, deck_id_for_args, cards):
    url = reverse('deck:card_list', args=deck_id_for_args)
    response = deck_owner_client.get(url)
    page_obj = response.context['object_list']
    card_count = page_obj.count()
    first_winrate = page_obj[0].winrate
    second_winrate = page_obj[1].winrate

    assert card_count == len(cards)
    assert card_count == response.context['card_count']

    # На странице карты отсортированы по принципу "сначала новые"
    assert first_winrate == 100 * cards[1].right_guesses / (cards[1].right_guesses + cards[1].wrong_guesses)
    assert second_winrate == 100 * cards[0].right_guesses / (cards[0].right_guesses + cards[0].wrong_guesses)

    assert page_obj[1].question == cards[0].question
    assert page_obj[1].answer_1 == cards[0].answer_1
    assert page_obj[1].answer_2 == cards[0].answer_2
    assert page_obj[1].answer_3 == cards[0].answer_3

    assert page_obj[0].question == cards[1].question
    assert page_obj[0].answer_1 == cards[1].answer_1
    assert page_obj[0].answer_2 == cards[1].answer_2
    assert page_obj[0].answer_3 == cards[1].answer_3


def test_cards_order_in_deck_list(deck_owner_client, deck_id_for_args, cards):
    url = reverse('deck:card_list', args=deck_id_for_args)
    response = deck_owner_client.get(url)
    page_obj = response.context['object_list']
    sorted_page_obj = sorted(
        page_obj,
        key=lambda card: card.datetime_created,
        reverse=True
    )

    print(page_obj)
    print(sorted_page_obj)
    assert list(page_obj) == sorted_page_obj
