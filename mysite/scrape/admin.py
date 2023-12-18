from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import User

# admin.site.register(CustomUser, UserAdmin)
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'current_price', 'place', 'url', 'img', 'date_add')
    list_filter = ('place',)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_shop', 'products')
    def products(self, obj):
        return "\n".join([p.name for p in obj.products.all()])

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'text', 'created_at')

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'date')
