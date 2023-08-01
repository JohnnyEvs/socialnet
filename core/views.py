from django.shortcuts import render, HttpResponse

# Create your views here.
def homepage(request):
    return HttpResponse("Hello world!")

def contacts(request):
    return HttpResponse("Наши контакты")

def about_us(request):
    return HttpResponse("Информация о нас!")



