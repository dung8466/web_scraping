from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from .models import *
from dataclasses import dataclass
from rich import print
import time
from django.db.models import Q
import sqlite3
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from .combine_search import *
from .forms import *
from decimal import Decimal
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from random import randint
from datetime import datetime, timedelta

# @dataclass
# class Item:
#     url: str
#     name: str
#     current_price: Decimal
#     prev_price: str
#     place: str
#     img: str
#     date_add: datetime.datetime

def form_view(request):
    newForm = ProductNameForm()
    # instantiate the ModelForm
    filterForm = FilterForm()
    # Return the form.html, passing the form into its context
    return render(request, "form.html", {"filterForm": filterForm, "form": newForm})

@login_required(login_url="/login")
def products_view(request):
    try:
        price = request.GET.get("price", None) # Get the submitted value for price
        search_name = request.GET.get('name', None)
        products = Product.objects.all()
        favourite = Favourite.objects.get(user=request.user)
        favourite_items = FavouriteItem.objects.filter(favourite=favourite)
        print(favourite_items)
        if search_name == "":
            if price == "A":
                products = Product.objects.order_by('current_price')
            elif price == "B":
                products = Product.objects.order_by('-current_price')
        else:
            if price == "A":
                products = Product.objects.filter(Q(name__icontains=search_name)).order_by('current_price')
            elif price == "B":
                products = Product.objects.filter(Q(name__icontains=search_name)).order_by('-current_price')
        # Use Q object in filtering the queryset
        # products = Product.objects.filter(Q(place=place))
        newForm = ProductNameForm()
        filterForm = FilterForm()
        filterForm.fields['name'].initial = search_name
        filterForm.fields['price'].initial = price
        # Return the products and the form to the form, but include products into its context
        return render(request, "form.html", {"product_list": products, "form": newForm, "filterForm": filterForm, "favourite": favourite_items})
    except ObjectDoesNotExist:
        return render(request, "form.html", {"product_list": [], "form": newForm, "filterForm": filterForm})

def search_result(request):
    context = {}
    lists = []
    name = request.POST.get('name', None)
    newForm = ProductNameForm()
    context['name'] = name
    products1 = cellphones(name)
    products2 = media_mart(name)
    products3 = nguyen_kim(name)
    products4 = gg_shopping(name)
    for product in products1:
        lists.append(product)
    for p in products2:
        lists.append(p)
    for p in products3:
        lists.append(p)
    for p in products4:
        lists.append(p)
    newForm.fields['name'].initial = name
    return render(request, 'search_result.html', {'lists':lists, 'context':context, 'form':newForm})

def search(request):
    if request.method == 'POST':
        form = ProductNameForm(request.POST)
        if form.is_valid() and place.is_valid():
            form.save()
            form = ProductNameForm()
            # return HttpResponseRedirect('/search_result/')
            # return HttpResponseRedirect(reverse('search_result'))
            return redirect('/search_result')
    form = ProductNameForm()
    return render(request, 'search_form.html', {'form':form})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

@login_required(login_url="/login")
def add_to_favourite(request, product_id):
    name = request.POST.get('name', None)
    product = Product.objects.get(pk=product_id)
    favourite = Favourite.objects.get_or_create(user=request.user)[0]
    favourite_item = FavouriteItem.objects.get_or_create(favourite=favourite, product=product)[0]
    print(name)

    return redirect('/favourite')

@login_required(login_url='/login')
def remove_from_favourite(request, product_id):
    product = Product.objects.get(pk=product_id)
    favourite = Favourite.objects.get(user=request.user)
    try:
        favourite_item = favourite.favouriteitem_set.get(product=product)
        favourite_item.delete()
    except FavouriteItem.DoesNotExist:
        pass

    return HttpResponseRedirect('/favourite')

@login_required(login_url='/login')
def view_favourite(request):
    try:
        newForm = ProductNameForm()
        favourite = request.user.favourite
        favourite_items = FavouriteItem.objects.filter(favourite=favourite)
        products = Product.objects.filter(id__in=favourite_items.values_list('product', flat=True))
        return render(request, 'favourite.html', {'favourite_items': products, 'form':newForm})
    except ObjectDoesNotExist:
        return render(request, 'favourite.html', {'favourite_items': [], 'form':newForm})

def compare(request):
    form = ProductNameForm()
    if request.method == 'POST':
        compare_form = CompareForm(request.POST)
        if compare_form.is_valid():
            compare_form.save()
            compare_form = CompareForm()
            # return HttpResponseRedirect('/search_result/')
            # return HttpResponseRedirect(reverse('search_result'))
            return redirect('/compare/result')
    compare_form = CompareForm()
    return render(request, 'compare.html', {'form':form, 'compare_form':compare_form})

def compare_result(request):
    lists = []
    name = request.POST.get('name', None)
    product1 = cellphones_one(name)
    lists.append(product1[0])
    product2 = media_mart_one(name)
    lists.append(product2[0])
    product3 = nguyen_kim_one(name)
    lists.append(product3[0])
    product4 = gg_shopping(name)
    product1_price = Decimal(product1[0]['current_price'])
    product2_price = Decimal(product2[0]['current_price'])
    product3_price = Decimal(product3[0].current_price)
    # Create a list of items with their prices
    lists = [
        {'item': product1[0], 'price': product1_price},
        {'item': product2[0], 'price': product2_price},
        {'item': product3[0], 'price': product3_price},
    ]
    excluded_keywords = {"Cellphones", "Media Mart", "Nguyễn Kim"}
    encountered_names = set()
    for p in product4:
        if p.name not in encountered_names:
            is_excluded = False
            for keyword in excluded_keywords:
                if keyword.lower() in p.place.lower():
                    is_excluded = True
                    break  # Exit the keyword loop if a match is found
            if not is_excluded:
                if p not in lists:
                    # Extract the 'current_price' attribute from the model object
                    product4_price = p.current_price
                    # Create a dictionary with the item and price
                    lists.append({'item': p, 'price': product4_price})
                    encountered_names.add(p.name)
                    # lists.append(p)
                    # encountered_names.add(p.name)

        # else:
        #     places_to_exclude.append(p.place)
    # product = Product.objects.all();
    # Find the lowest-priced item
    # lowest_price_item = min(lists, key=lambda p: Decimal(p['current_price']))
    lowest_price_item = min(lists, key=lambda p: p['price'])
    # Create a list of other products (excluding the lowest-priced item)
    other_products = [p for p in lists if p != lowest_price_item]
    # print(product);
    form = ProductNameForm()
    compare_form = CompareForm()  
    # return render(request, 'compare_result.html', {'form':form, 'compare_form':compare_form, 'product':product})
    return render(request, 'compare_result.html', {'form':form, 'compare_form':compare_form, 'lists':lists, 'lowest_price_item': lowest_price_item, 'other_products': other_products})

def is_excluded_place(place):
    excluded_keywords = ["Cellphones", "Media Mart", "Nguyễn Kim"]
    for keyword in excluded_keywords:
        if keyword.lower() in place.lower():
            return True
    return False


# def price_history(request, product_id):
#     form = ProductNameForm()
#     product = Product.objects.get(pk=product_id)
#     price_history = product.pricehistory_set.all()
#     price_history_data = [
#         {'timestamp': entry.timestamp, 'price': entry.price}
#         for entry in price_history
#     ]
#     return render(request, 'price_history.html', {'product': product, 'price_history_data': price_history_data, 'form':form})

def price_history(request, product_id):
    form = ProductNameForm()
    product = Product.objects.get(pk=product_id)

    # Create some dummy price history data for testing
    price_history_data = []
    today = datetime.now()
    for i in range(1, 11):  # Generate data for the last 10 days
        date = today - timedelta(days=i)
        price = float(product.current_price - (randint(1, 10) * 10))  # Convert Decimal to float  # Example: Randomly decrease price
        price_history_data.append({
            'timestamp': date.strftime('%Y-%m-%d'),
            'price': price,
        })

    return render(request, 'price_history.html', {'product': product, 'price_history_data': price_history_data, 'form':form})

def price_history_data(request, product_id):
    product = Product.objects.get(pk=product_id)

    # Create some dummy price history data for testing (similar to the previous view)
    price_history_data = []
    today = datetime.now()
    for i in range(1, 11):
        date = today - timedelta(days=i)
        price = product.current_price - (randint(1, 10) * 10)
        price_history_data.append({
            'timestamp': date.strftime('%Y-%m-%d'),
            'price': price,
        })

    return JsonResponse({'price_history_data': price_history_data})

@login_required(login_url='/login')
def add_review(request, product_id):
    product = Product.objects.get(pk=product_id)
    nameForm = ProductNameForm()
    reviewForm = ReviewForm()
    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['user'] = request.user.id
        form_data['product'] = product_id
        form = ReviewForm(form_data)
        # form = ReviewForm(request.POST)
        # print(form)
        if form.is_valid():
            review = form.save(commit=False)
            print(review)
            # review.user = request.user  # Set the user
            # review.product = product   # Set the product
            review.save()
            product.average_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
            product.save()
            form = ReviewForm()
            print("Form is valid")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            print(form.errors)

    return render(request, 'add_review.html', {'form': nameForm, 'product': product, 'reviewForm': reviewForm})

def view_reviews(request, product_id):
    form = ProductNameForm()
    product = Product.objects.get(pk=product_id)
    reviews = Review.objects.filter(product=product)

    return render(request, 'view_reviews.html', {'product': product, 'reviews': reviews, 'form':form})