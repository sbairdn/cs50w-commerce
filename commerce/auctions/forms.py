from django.forms import ModelForm
from .models import Listing, Bid, Comment

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'start_price', 'image', 'category']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']