from django.shortcuts import render


def start_review(request):
    return render(
        request,
        template_name='review/review.html'
    )
