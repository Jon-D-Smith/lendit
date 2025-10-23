from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("api/items/", views.get_all_items, name="items_json_list"),
    path("items/", views.item_list_view, name="item_list")
]
