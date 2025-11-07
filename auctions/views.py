from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .URL_to_image import url_to_image
from .models import User, Comment, Watchlist, Watchlist_Items, Bids
from .models import List_Auctions
from .forms import create_auction_form


def index(request):
    all_auctions = List_Auctions.objects.all()
    if not request.user.is_authenticated:
        return render(request, "auctions/index.html", {
            "all_auctions": all_auctions
        })
    else:
        user_watchlist = Watchlist.objects.get(user=request.user)
        return render(request, "auctions/index.html",
                      {"all_auctions": all_auctions,
                       "number_of_watchlist_items": user_watchlist.count_items})


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


@login_required
def create_listing(request):
    if request.method == "POST":
        form = create_auction_form(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.start_date = timezone.now()
            print(form.cleaned_data['photo'])
            auction.photo = url_to_image(form.cleaned_data['photo'])
            print(auction.photo)
            auction.save()
            return redirect(reverse("show_auctions", args=[auction.id, auction.title]))
        else:
            return render(request, 'auctions/create_auction.html')
    else:
        form = create_auction_form(request.POST)
        return render(request, 'auctions/create_auction.html', {'form': form})


def show_auctions(request, auction_id, auction_title):
    owner_of_auction = False
    in_watchlist_items = False
    requested_auction = List_Auctions.objects.get(pk=auction_id, title=auction_title)
    if request.user.is_authenticated:
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
def place_bid(request, requested_auction_id):
    requested_auction = List_Auctions.objects.get(pk=requested_auction_id)
    if request.method == "POST":
        if request.user == requested_auction.user:
            return redirect(reverse('deny_owner', args=[requested_auction_id]))
        else:
            bid = request.POST["bid"]
            if bid:
                bid = float(bid)
                if bid > requested_auction.start_bid:
                    requested_auction.number_of_bids += 1
                    requested_auction.start_bid = bid
                    requested_auction.save()
                    new_bid = Bids.objects.create(user=request.user, auction=requested_auction, amount=bid,
                                                  written_at=timezone.now())
                    new_bid.save()
                else:
                    messages.error(request, "Your suggested bid should be more than the latest bid")
            else:
                messages.error(request, "Please enter a bid")
    return redirect(reverse("show_auctions", args=[requested_auction.id, requested_auction.title]))


@login_required
def place_comment(request, requested_auction_id):
    requested_auction = List_Auctions.objects.get(pk=requested_auction_id)
    if request.method == "POST":
        if request.user == requested_auction.user:
            return redirect(reverse('deny_owner', args=[requested_auction_id]))
        else:
            comment = request.POST["comment"]
            now = timezone.now()
            if comment:
                new_comment = Comment.objects.create(user=request.user, auction=requested_auction, text=comment,
                                                     written_at=now, author_name=request.user.username)
                new_comment.save()
            else:
                messages.error(request, "Please enter a comment")
    return redirect(reverse("show_auctions", args=[requested_auction.id, requested_auction.title]))


def deny_owner(request, requested_auction_id):
    requested_auction = List_Auctions.objects.get(pk=requested_auction_id)
    messages.error(request, "Owner cant place bid and comment")
    return redirect(reverse("show_auctions", args=[requested_auction.id, requested_auction.title]))


def close_auction(request, auction_id):
    auction = List_Auctions.objects.get(pk=auction_id)
    final_bid = auction.start_bid
    the_bid = Bids.objects.filter(auction=auction, amount=final_bid).first()
    auction.winner = the_bid.user
    auction.active = False
    auction.end_date = timezone.now()
    auction.save()
    return redirect(reverse("show_auctions", args=[auction.id, auction.title]))


@login_required
def show_watchlist(request):
    user_watchlist = Watchlist.objects.get(user=request.user)
    if Watchlist_Items.objects.filter(watchlist=user_watchlist).exists():
        watchlist = List_Auctions.objects.filter(Watchlist_Items__watchlist=user_watchlist)
    else:
        watchlist = None
    return render(request, 'auctions/watchlist.html',
                  {"watchlist": watchlist, "number_of_watchlist_items": user_watchlist.count_items})


@login_required
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
    all_categories = (
        List_Auctions.objects.exclude(category__isnull=True).exclude(category__exact="")
        .values_list('category', flat=True).distinct())
    if request.user.is_authenticated:
        user_watchlist = Watchlist.objects.get(user=request.user)
        number_of_watchlist_items = user_watchlist.count_items
    else:
        number_of_watchlist_items = 0
    if request.method == 'POST':
        requested_category = request.POST["category"]
        if requested_category not in all_categories:
            messages.error(request, "Category is not chosen")
            return redirect("categories")
        auctions_with_requested_category = List_Auctions.objects.filter(category=requested_category)
        return render(request, 'auctions/index.html', {
            "requested_category": requested_category,
            "all_auctions": auctions_with_requested_category,
            "from_home_or_category": True,
            "number_of_watchlist_items": number_of_watchlist_items
        })
    return render(request, 'auctions/categories.html', {
        "all_categories": all_categories,
        "number_of_watchlist_items": number_of_watchlist_items
    })


def not_login(request):
    return render(request, 'auctions/not_login.html')
