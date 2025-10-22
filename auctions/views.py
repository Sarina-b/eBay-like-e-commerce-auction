from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Comment, Watchlist, Watchlist_Items
from .models import List_Auctions


def index(request):
    all_auctions = List_Auctions.objects.all()
    user_watchlist = Watchlist.objects.get(user=request.user)
    user_watchlist_items = Watchlist_Items.objects.filter(watchlist=user_watchlist)
    number_of_watchlist_items = user_watchlist_items.count()
    return render(request, "auctions/index.html",
                  {"all_auctions": all_auctions,
                   "user_watchlist": user_watchlist, "user_watchlist_items": user_watchlist_items,
                   "number_of_watchlist_items": number_of_watchlist_items})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
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


def create_listing(request):
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
    in_watchlist_items = False
    requested_auction = List_Auctions.objects.get(pk=auction_id, title=auction_title)
    if request.user == requested_auction.user:
        owner_of_auction = True
    watchlist = Watchlist.objects.get(user=request.user)
    if requested_auction.Watchlist_Items.filter(watchlist=watchlist, auction=requested_auction).exists():
        in_watchlist_items = True
    return render(request, 'auctions/auction.html',
                  {"requested_auction": requested_auction,
                   "owner_of_auction": owner_of_auction,
                   "in_watchlist_items": in_watchlist_items})


@login_required
def bid_and_comment(request, requested_auction_id):
    requested_auction = List_Auctions.objects.get(pk=requested_auction_id)
    if request.method == "POST":
        comment = request.POST["comment"]
        now = timezone.now()
        bid = request.POST["bid"]
        if bid:
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
    auction.save()
    return redirect(reverse("show_auctions", args=[auction.id, auction.title]))


def show_watchlist(request):
    user_watchlist = Watchlist.objects.get(user=request.user)
    if Watchlist_Items.objects.filter(watchlist=user_watchlist).exists():
        watchlist = List_Auctions.objects.filter(Watchlist_Items__watchlist=user_watchlist)
    else:
        watchlist = None
    return render(request, 'auctions/watchlist.html',
                  {"watchlist": watchlist})


def watchlist_add_or_delete(request, auction_id):
    auction = List_Auctions.objects.get(pk=auction_id)
    user_watchlist = Watchlist.objects.get(user=request.user)
    if Watchlist_Items.objects.filter(auction=auction, watchlist=user_watchlist).exists():
        target_watchlist_Items = Watchlist_Items.objects.get(auction=auction, watchlist=user_watchlist)
        target_watchlist_Items.delete()
        return redirect(reverse("show_auctions", args=[auction.id, auction.title]))
    new_watchlist_items = Watchlist_Items.objects.create(watchlist=user_watchlist, auction=auction)
    new_watchlist_items.save()
    return redirect(reverse("show_auctions", args=[auction.id, auction.title]))


def categories(request):
    all_categories = List_Auctions.objects.values_list('category', flat=True).distinct()
    if request.method == 'POST':
        requested_category = request.POST["category"]
        if requested_category not in all_categories:
            messages.error(request, "Invalid category.")
            return redirect("categories")
        auctions_with_requested_category = List_Auctions.objects.filter(category=requested_category)
        return render(request, 'auctions/index.html', {
            "requested_category": requested_category,
            "all_auctions": auctions_with_requested_category ,
            "from_home_or_category": True
        })
    return render(request, 'auctions/categories.html',{
        "all_categories": all_categories
    })
