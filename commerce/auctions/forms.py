from django.forms import ModelForm
from .models import Listing, Bid, Comment

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'start_price', 'image', 'category']

class CreateBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']