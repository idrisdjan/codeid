from django.shortcuts import render


def index(request):
    data = {
        'title': 'Главная страница',
        'values': ['Some', 'Hello', '123']
    }
    return render(request, 'main/index.html', {'title': 'Главная страница'})

def about(request):
    return render(request, 'main/about.html')