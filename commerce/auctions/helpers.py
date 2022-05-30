from .models import Bid, Comment
from .forms import BidForm

def update_watchlist(request, listing):
    """Update watchlist for a specific user"""
    watchlist_val = request.POST.get('watchlist', None)
    if watchlist_val == "Add to Watchlist":
        request.user.watchlist.add(listing)
    elif watchlist_val == "Remove from Watchlist":
        request.user.watchlist.remove(listing)

def place_bid(request, listing):
    """
    Place a bid if its greater than the starting price or current bid, 
    otherwise display an error message.
    """
    bid_form = BidForm(request.POST or None)
    bid_amount = None
    if bid_form.is_valid():
        bid_amount = bid_form.cleaned_data['bid']

        bid = Bid()
        bid.listing = listing
        bid.bid = bid_amount
        bid.bidder = request.user
        bid.save()

        message = None
        if listing.current_bid is not None:
            if bid_amount <= float(listing.current_bid.bid):
                message = "Bid rejected: your bid must be greater than the current value"
            else:
                listing.current_bid = bid
        else:
            if bid_amount < float(listing.start_price):
                message = "Bid rejected: your bid must be greater than the start value"
            else:
                listing.current_bid = bid

        request.user.bids.add(bid)
        listing.save()
        return message

def post_comment(request, listing):
    """Post a comment to the current listing's page."""
    text = request.POST.get('text', None)
    comment = Comment()
    if text is not None:
        comment.listing = listing
        comment.text = text
        comment.commenter = request.user
        comment.save()
        listing.comments.add(comment)