from re import X
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category
from .forms import CreateBidForm, CreateListingForm, CreateCommentForm

def index(request):
    "Display homepage with all active listings"
    return render(request, "auctions/index.html", {
        "listings": reversed(Listing.objects.filter(is_active=True)),
        "title": "Active Listings",
        "empty_message": "There are no active listings."
    })


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

def categories(request):
    """View proudct categories."""
    categories = [category[0] for category in Category.choices]
    print(categories)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    """Display all listings in a given category"""
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": category,
        "empty_message": "No items in category."
    })

def create_listing(request):
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

def listing(request, listing_id):
    """View a specific listing."""
    listing = Listing.objects.get(id=listing_id)
    if request.method == "GET":
        return render_listing(request, listing, None)
    else:
        watchlist_val = request.POST.get('watchlist', None)
        bid = request.POST.get('bid', None)
        comment = request.POST.get('comment', None)
        message = None
        if watchlist_val == "Add to Watchlist":
            request.user.watchlist.add(listing)
        elif watchlist_val == "Remove from Watchlist":
            request.user.watchlist.remove(listing)
        if bid is not None:
            bid = float(bid)
            print(f"BID: {bid}")
            print(listing.current_bid)
            if listing.current_bid is not None:
                if bid <= float(listing.current_bid):
                    message = "Error: bid must be greater than current bid"
                else:
                    listing.current_bid = bid
            else:
                if bid < float(listing.start_price):
                    message = "Error: bid must be greater than start price"
                else:
                    listing.current_bid = bid
            listing.save()
        if comment is not None:
            listing.comments = comment
        return render_listing(request, listing, message)
 
def render_listing(request, listing, message):
    """Render listings page with any new context."""
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": message,
            "on_watchlist": listing in request.user.watchlist.all(),
            "bid_form": CreateBidForm(),
            "comment_form": CreateCommentForm()
        })

def watchlist(request):
    """Display all listings in watchlist."""
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlist.all(),
        "title": "Watchlist",
        "empty_message": "No items in watchlist."
    })