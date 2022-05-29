from django.contrib.auth.models import AbstractUser
from django.db import models
from requests import request
from django.core.validators import MaxValueValidator, MinValueValidator

MAX_PRICE = 9_999.99
MAX_PRICE_DIGITS = 6

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlisters")
    bids = models.ManyToManyField('Bid', blank=True, related_name="bidders")

class Category(models.TextChoices):
    ART = 'Art'
    ELECTRONICS = 'Electronics'
    FASHION = 'Fashion'
    HOME = 'Home'
    TOYS = 'Toys'

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=1000)
    start_price = models.DecimalField(max_digits=MAX_PRICE_DIGITS, validators=[MaxValueValidator(MAX_PRICE), MinValueValidator(0)], decimal_places=2, null=True)
    current_bid = models.DecimalField(max_digits=MAX_PRICE_DIGITS, validators=[MaxValueValidator(MAX_PRICE), MinValueValidator(0)], decimal_places=2, blank=True)
    image = models.ImageField(upload_to="images", blank=True)
    category = models.CharField(choices=Category.choices, max_length=50, null=True)
    is_active = models.BooleanField(default=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postings", null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        string = ""
        string += "Active" if self.is_active else "Inactive"
        return f" listing: '{self.title}' by {self.poster} for ${self.current_bid} at {self.datetime}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", null=True)
    bid = models.DecimalField(max_digits=MAX_PRICE_DIGITS, validators=[MaxValueValidator(MAX_PRICE), MinValueValidator(0)], decimal_places=2, null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)
    comment = models.CharField(max_length=500, blank=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="comments")
    datetime = models.DateTimeField(auto_now_add=True, null=True)

