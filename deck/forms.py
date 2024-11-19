from django import forms
from django.core.exceptions import ValidationError

from .models import Card, Deck


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('question',
                  'answer_1',
                  'answer_2',
                  'answer_3',
                  )

    def clean(self):
        ans1 = self.cleaned_data['answer_1']
        ans2 = self.cleaned_data['answer_2']
        ans3 = self.cleaned_data['answer_3']

        if not (ans1 or ans2 or ans3):
            raise ValidationError('Введите хотя бы один вариант ответа!')


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ('deck_name',)
