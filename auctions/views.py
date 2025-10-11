from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Comment
from .models import List_Auctions


def index(request):
    all_auctions = List_Auctions.objects.all()
    return render(request, "auctions/index.html", {"all_auctions": all_auctions})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_auction(request):
    if request.method == "POST":
        start_date = timezone.now()
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        image_url = request.POST["image_url"]
        start_bid = request.POST["start_bid"]
        new_auction = List_Auctions.objects.create(user=user, title=title, description=description,
                                                   photo=image_url, category=category,
                                                   start_bid=start_bid, start_date=start_date)
        new_auction.save()
        return redirect(reverse("show_auctions", args=[new_auction.id, title]))
    else:
        return render(request, 'auctions/create_auction.html')


def show_auctions(request, auction_id, auction_title):
    owner_of_auction = False
    requested_auction = List_Auctions.objects.get(pk=auction_id, title=auction_title)
    if request.user == requested_auction.user:
        owner_of_auction = True
    return render(request, 'auctions/auction.html',
                  {"requested_auction": requested_auction},
                  {"owner_of_auction": owner_of_auction})


@login_required
def bid_and_comment(request, requested_auction_id):
    requested_auction = List_Auctions.objects.get(pk=requested_auction_id)
    if request.method == "POST":
        comment = request.POST["comment"]
        now = timezone.now()
        bid = request.POST["bid"]
        if bid.strip() != "":
            bid = float(bid)
            if bid > requested_auction.start_bid:
                requested_auction.start_bid = bid
                requested_auction.save()
                return redirect(reverse("show_auctions", args=[requested_auction.id, requested_auction.title]))
            else:
                messages.error(request, "Your suggested bid should be more than the latest bid.")
        if comment.strip() != "":
            new_comment = Comment.objects.create(user=request.user, auction=requested_auction, text=comment,
                                                 written_at=now)
            new_comment.save()
            return redirect(reverse("show_auctions", args=[requested_auction.id, requested_auction.title]))
    else:
        messages.error(request, "Comment or bid is empty.")


def close_auction(request, auction_id):
    auction = List_Auctions.objects.get(pk=auction_id)

    auction.active = False
