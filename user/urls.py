from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.dash_board, name="dashboard"),
    path("withdraw-funds/", views.withdrawal_, name="withdrawal"),
    path("transactions/", views.transactions_, name="transactions_"),
    path("account-settings/", views.settings_, name="settings_"),
    path("change-password/", views.change_password_view, name="change_password"),
]
