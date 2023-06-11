from django.shortcuts import render


def home_page(request):
    return render(request, 'home_page.html')


def base_page(request):
    return render(request, 'base.html', {
        'user': request.user,
    })