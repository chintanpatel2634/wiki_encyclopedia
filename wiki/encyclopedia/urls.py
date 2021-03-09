from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:name>", views.entry, name="entry"),
    path("newentry", views.newentry, name="newentry")
]
