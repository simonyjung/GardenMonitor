from django.shortcuts import render
from django.http import HttpResponse

from . import models


def index(request):
    plants = models.Plant.objects.all()
    context = {'plants': plants}
    return render(request, 'index.html', context)
