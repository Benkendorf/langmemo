from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Deck(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='decks'
    )
    deck_name = models.CharField(
        'Название колоды',
        max_length=50,
    )

    def __str__(self):
        return self.deck_name

    class Meta:
        ordering = ('-pk',)


class Card(models.Model):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name='cards'
    )
    question = models.CharField(
        'Текст вопроса',
        max_length=50,
    )
    # В формах методом clean() валидируем,
    # что хотя бы один из ответов не пустой
    answer_1 = models.CharField(
        'Первый ответ',
        max_length=50,
        null=True,
        blank=True
    )
    answer_2 = models.CharField(
        'Второй ответ',
        max_length=50,
        null=True,
        blank=True
    )
    answer_3 = models.CharField(
        'Третий ответ',
        max_length=50,
        null=True,
        blank=True
    )
    right_guesses = models.PositiveSmallIntegerField(
        'Количество правильных ответов',
        default=0
    )
    wrong_guesses = models.PositiveSmallIntegerField(
        'Количество неправильных ответов',
        default=0
    )
    # Автоматически рассчитывается в переопределенном методе модели save()
    winrate = models.FloatField(
        'Доля успеха',
        default=None,
        null=True,
        blank=True
    )
    # Автоматически устанавливается при создании карты
    datetime_created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    # Лучше не делать авто, т.к. дата будет ставиться и при сохранении после
    # редактирования
    datetime_reviewed = models.DateTimeField(
        'Дата последнего ревью',
        default=None,
        null=True,
        blank=True
    )
    in_queue = models.BooleanField(
        'В очереди на ревью',
        default=True
    )
    srs_level = models.PositiveSmallIntegerField(
        'Уровень SRS',
        default=0
    )
    srs_xp = models.PositiveSmallIntegerField(
        'Опыт SRS',
        default=0
    )

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        try:
            self.winrate = (100 * self.right_guesses
                            / (self.right_guesses + self.wrong_guesses))
        except ZeroDivisionError:
            self.winrate = None

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-datetime_created',)
