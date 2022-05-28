from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
from .forms import CreateListingForm

def index(request):
    "Display homepage with all active listings"
    return render(request, "auctions/index.html", {
        "listings": reversed(Listing.objects.filter(is_active=True))
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
            form.current_price = request.POST['start_price']
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
        return rerender_listing(request, listing)
    else:
        form = request.POST
        if form["watchlist"] == "Add to Watchlist":
            request.user.watchlist.add(listing)
        elif form["watchlist"] == "Remove from Watchlist":
            request.user.watchlist.remove(listing)
        return rerender_listing(request, listing)

def rerender_listing(request, listing):
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "on_watchlist": listing in request.user.watchlist.all()
        })
