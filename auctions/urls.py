from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_auction", views.create_listing, name="create_listing"),
    path("auctions/<int:auction_id>/<str:auction_title>", views.show_auctions, name="show_auctions"),
    path("auctions/bid-on/<int:requested_auction_id>", views.place_bid, name="place_bid"),
    path("auctions/comment-on/<int:requested_auction_id>", views.place_comment, name="place_comment"),
    path("auctions/close-auction/<int:auction_id>", views.close_auction, name="close_auction"),
    path("auctions/", views.show_watchlist, name="show_watchlist"),
    path('watchlist/<int:auction_id>', views.watchlist_add_or_delete, name="watchlist_add_or_delete"),
    path('auctions/categories/', views.categories, name="categories"),
    path('not_authenticated', views.not_login, name="not_login"),
    path('deny_owner<int:requested_auction_id>', views.deny_owner, name="deny_owner"),
    path("stats", views.zabbix_stats, name="stats")

]
