from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2',)
