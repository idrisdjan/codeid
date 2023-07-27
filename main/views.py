from django.shortcuts import render
from django.http import HttpResponse


def index():
    return HttpResponse("<h4>Проверка работы</h4>")