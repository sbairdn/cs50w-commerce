from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category
from .forms import BidForm, CreateListingForm, CommentForm
from .helpers import update_watchlist, place_bid, post_comment, close_auction

def index_view(request):
    "Display homepage with all active listings."
    return render(request, "auctions/index.html", {
        "listings": reversed(Listing.objects.filter(is_active=True)),
        "title": "Active Listings",
        "empty_message": "There are no active listings."
    })


def login_view(request):
    "Display login page."
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
    """Return user to default homepage when they log out."""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    "Display account registration page."
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

def categories_view(request):
    """View proudct categories."""
    categories = [category[0] for category in Category.choices]
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_view(request, category):
    """Display all active listings in a given category"""
    listings = Listing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": category,
        "empty_message": "No items in category."
    })

def create_listing_view(request):
    """Create a listing to post."""
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "form": CreateListingForm()
        })
    else:
        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.poster = request.user
            form.save()
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
        return HttpResponseRedirect(reverse("index"))

def listing_view(request, listing_id):
    """View a specific listing."""
    listing = Listing.objects.get(id=listing_id)
    if request.method == "GET":
        return render_listing(request, listing, None)
    else:
        update_watchlist(request, listing)
        message = place_bid(request, listing)
        post_comment(request, listing)
        close_auction(request, listing)
        return render_listing(request, listing, message)


def render_listing(request, listing, message):
    """Render listings page with any new context."""
    on_watchlist = False
    if request.user.is_authenticated:
        on_watchlist = listing in request.user.watchlist.all()
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": message,
            "on_watchlist": on_watchlist,
            "bid_form": BidForm(),
            "comment_form": CommentForm(),
            "comments": listing.comments.all()
        })


def watchlist_view(request):
    """Display all listings in watchlist."""
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlist.all(),
        "title": "Watchlist",
        "empty_message": "No items in watchlist."
    })