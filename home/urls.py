from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("plans/", views.plans, name="plans"),
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy, name="privacy"),
    path("rules/", views.rules, name="rules"),
]
