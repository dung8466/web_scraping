from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    # current_price = models.CharField(max_length=50)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    place = models.CharField(max_length=50)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    url = models.CharField(max_length=50)
    img = models.CharField(max_length=50)
    date_add = models.DateTimeField(default=timezone.now)

    # Add a ForeignKey field to relate Product to its PriceHistory
    # price_history = models.ForeignKey('PriceHistory', on_delete=models.SET_NULL, null=True, blank=True)
    price_history = models.ForeignKey('PriceHistory', on_delete=models.SET_NULL, null=True, blank=True, related_name='product_price_history')
    
    class Meta:
        db_table = "scrape_product"

    def __str__(self):
        return self.name

    def add_price_to_history(self):
        price_history = PriceHistory.objects.create(product=self, price=self.current_price)
        self.price_history = price_history
        self.save()

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=False, null=False) # Validators should be a list
    is_shop = models.BooleanField(default=False)
    shop_name = models.CharField(max_length=50, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)

    class Meta:
        db_table = "scrape_customuser"

CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'

class ProductName(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

price_choices = (
    ("A", "Giá thấp > cao"),
    ("B", "Giá cao > thấp")
)
class ProductFilter(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.CharField(max_length=50, choices=price_choices, null=True, blank=True)

class Favourite(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='FavouriteItem')
    
    class Meta:
        db_table = "scrape_favourite"

class FavouriteItem(models.Model):
    favourite = models.ForeignKey(Favourite, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "scrape_favouriteitem"

class CompareName(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "scrape_pricehistory"

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()  # You can add a rating field if needed
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "scrape_review"

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"



