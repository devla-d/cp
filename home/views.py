from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def plans(request):
    return render(request, "plan.html")


def blog(request):
    return render(request, "blog.html")


def contact(request):
    return render(request, "contact.html")


def privacy(request):
    return render(request, "privacy.html")


def rules(request):
    return render(request, "rules.html")
