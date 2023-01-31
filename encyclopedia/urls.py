from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("Add", views.add_page, name="add"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("randoms", views.randoms, name="randoms"),
    path("search", views.search, name="search"),
    path("edit/<str:title>", views.edit_page, name="edit")
]
