from django.shortcuts import render


def description(request):
    return render(
        request,
        template_name='about/description.html'
    )
