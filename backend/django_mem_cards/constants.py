CARDS_PAGINATION_LIMIT = 15
CARD_BAD_WINRATE_LIMIT = 50
DAM_LEV_DIST_LIMIT = 1
SRS_LEVELS = {
    0: {'xp_to_next_lvl': 3, 'time_interval_hrs': 6},
    1: {'xp_to_next_lvl': 5, 'time_interval_hrs': 24},
    2: {'xp_to_next_lvl': 5, 'time_interval_hrs': 48},
    3: {'xp_to_next_lvl': 10, 'time_interval_hrs': 72},
    4: {'xp_to_next_lvl': None, 'time_interval_hrs': 120}
}

REVIEW_SUCCESS_MESSAGE = 'Правильно!'
REVIEW_FAILURE_MESSAGE = 'Неправильно!'
REVIEW_NOT_PERFECT_SUCCESS_MESSAGE = 'Принято! Хотя есть неточность.'
REVIEW_NOT_IN_QUEUE_MESSAGE = 'Упс! Карты уже нет в очереди!'

DECKS_PAGINATION_LIMIT = 9
DECK_BAD_WINRATE_LIMIT = 50
WEEKDAYS_RUS = ['Понедельник', 'Вторник', 'Среда',
                'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
TOTAL_CALENDAR_DAYS = 5

API_TOKEN_LENGTH = 30
TG_USER_ID_MAX_LENGTH = 50
TG_BOT_USERNAME = '<PLACEHOLDER>'
TG_ERROR_CODES_MESSAGES = {
    'token_not_found':
        ('Пользователя с таким токеном не найдено!'
         ' Проверьте корректность токена.'),

    'token_already_in_use_by_other_chat_id':
        ('Токен уже привязан к другому Telegram-аккаунту.'
         ' Если вы хотите привязать этот аккаунт, удалите старый токен на'
         ' сайте, создайте новый и пришлите его сюда.'),

    'token_already_in_use_by_current_chat_id':
        ('Вы уже добавили этот токен.'
         ' Все в порядке, добавлять токен повторно не нужно.'),

    'tg_chat_id_already_in_use':
        ('Telegram уже привязан к другому аккаунту LangMemo.'
         ' Если вы хотите привязать новый аккаунт LangMemo,'
         ' удалите токен из старого аккаунта,'
         ' создайте токен в новом и пришлите его.'),
}
