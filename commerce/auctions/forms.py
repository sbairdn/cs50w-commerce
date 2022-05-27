from django.forms import ModelForm
from .models import Listing

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'start_price', 'image', 'category']