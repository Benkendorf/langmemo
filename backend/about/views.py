from django.shortcuts import render


def description(request):
    """Страница описания проекта."""
    return render(
        request,
        template_name='about/description.html'
    )
