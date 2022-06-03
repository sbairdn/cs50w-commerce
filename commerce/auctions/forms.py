from django.forms import ModelForm, Textarea
from .models import Listing, Bid, Comment

class CreateListingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
        add_bootstrap(self)

    class Meta:
        model = Listing
        fields = ['title', 'description', 'start_price', 'image', 'category']
        widgets = {
            'description': Textarea(attrs={'rows': 2, 'cols': 20})
        }

class BidForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""  # Remove ':' from form label
        add_bootstrap(self)

    class Meta:
        model = Bid
        fields = ['bid']
        

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        add_bootstrap(self)

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'rows': 2, 'cols': 20})
        }

def add_bootstrap(form):
    for visible in form.visible_fields():
        visible.field.widget.attrs['class'] = 'form-control'