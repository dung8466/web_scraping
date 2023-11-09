from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'current_price', 'place', 'url', 'img', 'date_add')
    list_filter = ('place',)