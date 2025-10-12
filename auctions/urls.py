from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_auction", views.create_auction, name="create_auction"),
    path("auctions/<int:auction_id>/<str:auction_title>", views.show_auctions, name="show_auctions"),
    path("auctions/<int:requested_auction_id>", views.bid_and_comment, name="bid_and_comment"),
    path("auctions/close auction<int:auction_id>", views.close_auction, name="close_auction")

]
