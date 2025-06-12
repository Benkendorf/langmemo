from django.conf import settings
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
from .views import RegistrationView

urlpatterns = [
    path('', include('homepage.urls', namespace='homepage')),
    path('pages/', include('pages.urls', namespace='pages')),
    #path('about/', include('about.urls', namespace='about')),
    path('tg_bot_page/', include('tg_bot_page.urls', namespace='tg_bot_page')),
    path('deck/', include('deck.urls', namespace='deck')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        RegistrationView.as_view(),
        name='registration',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
