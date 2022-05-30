from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("categories/all", views.categories_view, name="categories"),
    path("categories/<str:category>", views.category_view, name="category"),
    path("create_listing", views.create_listing_view, name="create_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("watchlist", views.watchlist_view, name="watchlist")
]
