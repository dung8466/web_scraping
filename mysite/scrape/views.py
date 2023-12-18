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
# from datetime import datetime, timedelta
from django.urls import reverse
from threading import Thread
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from random import randint  # For generating random codes
import telegram
import json
from django.views.decorators.csrf import csrf_exempt
import logging
import asyncio
import schedule



# @dataclass
# class Item:
#     url: str
#     name: str
#     current_price: Decimal
#     prev_price: str
#     place: str
#     img: str
#     date_add: datetime.datetime

BOT_TOKEN = '6709719100:AAFL_KC-vpkitkkxdvDGgGmihW0Hr4cVPZI'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

def form_view(request):
    user = request.user
    newForm = ProductNameForm()
    # instantiate the ModelForm
    filterForm = FilterForm()
    # Return the form.html, passing the form into its context
    return render(request, "form.html", {"filterForm": filterForm, "form": newForm, "user": user})

@login_required(login_url="/login")
def products_view(request):
    newForm = ProductNameForm()
    filterForm = FilterForm()
    try:
        price = request.GET.get("price", None) # Get the submitted value for price
        search_name = request.GET.get('name', None)
        products = Product.objects.all()
        favourite = Favourite.objects.get(user=request.user)
        favourite_items = FavouriteItem.objects.filter(favourite=favourite)
        # if search_name == "":
        #     if price == "A":
        #         products = Product.objects.order_by('current_price')
        #     elif price == "B":
        #         products = Product.objects.order_by('-current_price')
        # else:
        if search_name:
            if price == "A":
                products = Product.objects.filter(Q(name__icontains=search_name)).order_by('current_price')
            elif price == "B":
                products = Product.objects.filter(Q(name__icontains=search_name)).order_by('-current_price')
            else:
                products = Product.objects.filter(Q(name__icontains=search_name))
        else:
            if price == "A":
                products = Product.objects.order_by('current_price')
            elif price == "B":
                products = Product.objects.order_by('-current_price')
        # Use Q object in filtering the queryset
        # products = Product.objects.filter(Q(place=place))
        filterForm.fields['name'].initial = search_name
        filterForm.fields['price'].initial = price
        user = request.user
        # Return the products and the form to the form, but include products into its context
        return render(request, "form.html", {"product_list": products, "form": newForm, "filterForm": filterForm, "favourite": favourite_items, "user": user})
    except ObjectDoesNotExist:
        user = request.user
        return render(request, "form.html", {"product_list": [], "form": newForm, "filterForm": filterForm, "user": user})

def search_result(request):
    context = {}
    lists = []
    name = request.POST.get('name', None)
    newForm = ProductNameForm()
    context['name'] = name
    shop_users = CustomUser.objects.filter(is_shop=True)
    for user in shop_users:
        # For each shop user, get their products
        products = user.products.filter(Q(name__icontains=name))
        if products:
            for product in products:
                lists.append(product)
    products1 = cellphones(name)
    products2 = media_mart(name)
    products3 = nguyen_kim(name)
    products4 = gg_shopping(name)
    products5 = scrape_fake_product(name)
    if products5 != []:
        for p in products5:
            lists.append(p)
            PriceHistory.objects.create(product=p, price=p.current_price)
    if products1 != []:
        for product in products1:
            lists.append(product)
            PriceHistory.objects.create(product=product, price=product.current_price)
    if products2 != []:
        for p in products2:
            lists.append(p)
            PriceHistory.objects.create(product=p, price=p.current_price)
    if products3 != []:
        for p in products3:
            lists.append(p)
            PriceHistory.objects.create(product=p, price=p.current_price)
            print(p)
    if products4 != []:
        for p in products4:
            lists.append(p)
            PriceHistory.objects.create(product=p, price=p.current_price)
    newForm.fields['name'].initial = name
    user = request.user
    return render(request, 'search_result.html', {'lists':lists, 'context':context, 'form':newForm, 'user': user})

def search(request):
    shop_users = CustomUser.objects.filter(is_shop=True)
    shop_data = []
    
    for user in shop_users:
        # For each shop user, get their products
        products = user.products.all()
        shop_data.append({'user': user, 'products': products})
        print(shop_data)
    # try:
    #     favourite = Favourite.objects.get_or_create(user=request.user)[0]
    #     favourite_items = FavouriteItem.objects.filter(favourite=favourite)
    #     products_to_check = [fav_item.product for fav_item in favourite_items]
    #     print(products_to_check)
    #     # Start a single thread to check all products
    #     thread = Thread(target=price_check_timer, args=(products_to_check,))
    #     thread.start()
    # except:
    #     pass
    if request.method == 'POST':
        form = ProductNameForm(request.POST)
        if form.is_valid() and place.is_valid():
            form.save()
            form = ProductNameForm()
            # return HttpResponseRedirect('/search_result/')
            # return HttpResponseRedirect(reverse('search_result'))
            return redirect('/search_result')
    form = ProductNameForm()
    return render(request, 'search_form.html', {'form':form, 'shop_data': shop_data})

def sign_up(request):
    if request.method == 'POST':
        # form = RegisterForm(request.POST)
        form = RegularUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            referring_url = request.POST.get('next', None)
            if  referring_url:
                return redirect(referring_url)
            else:
                return redirect('/')
            # return render(request, 'registration/verify_code.html', {'user': user})
    else:
        form = RegularUserForm()
    return render(request, 'registration/sign_up.html', {"form": form})

# Function to send a message to a specific chat ID
def send_message(chat_id, text):
    send_text = TELEGRAM_API_URL + f'sendMessage?chat_id={chat_id}&text={text}'
    response = requests.get(send_text)
    return response.json()

# Function to send a verification code to a user
def send_verification_code(chat_id):
    verification_code = str(random.randint(100000, 999999))
    send_message(chat_id, f"Your verification code: {verification_code}")
    return verification_code

def get_id():
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    bot = telegram.Bot(token=token)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['ok']:
            latest_update = data['result'][-1]['update_id']
            last_id = Id.objects.lastest()  # Assuming you have an UpdateId model
            if last_id:
                if last_id.id < latest_update:
                    last_id.id = latest_update
                    last_id.save()
                    return latest_update
            else:
                Id.objects.create(id=latest_update)
                return latest_update

def verify_code(request):
    
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('/')
    else:
        form = VerifyCodeForm()
    return render(request, 'registration/verify_code.html', {'form': form})

def price_check_timer(products):
    print("Thread started")
    try:
        while True:
            for product in products:
                if product.place == "Fake":
                    latest = scrape_fake_product_one(product.name)
                    PriceHistory.objects.update_or_create(
                        product=product,
                        defaults={
                            'price':latest[0].current_price,
                            'date':datetime.datetime.now(tz=timezone.utc)
                        }   
                    )
                    if latest[0].current_price < product.current_price:
                        send_price_drop_notification(product, latest[0])
                        print("Notification sent")
                elif product.place == "Cellphones":
                    latest = cellphones_one(product.name)
                    PriceHistory.objects.update_or_create(
                        product=product,
                        defaults={
                            'price':latest[0].current_price,
                            'date':datetime.datetime.now(tz=timezone.utc)
                        }   
                    )
                    if latest[0].current_price < product.current_price:
                        send_price_drop_notification(product, latest[0])
                        print("Notification sent")
                elif product.place == "Media Mart":
                    latest = media_mart_one(product.name)
                    PriceHistory.objects.update_or_create(
                        product=product,
                        defaults={
                            'price':latest[0].current_price,
                            'date':datetime.datetime.now(tz=timezone.utc)
                        }   
                    )
                    if latest[0].current_price < product.current_price:
                        send_price_drop_notification(product, latest[0])
                        print("Notification sent")
                elif product.place == "Nguyen Kim":
                    latest = nguyen_kim_one(product.name)
                    PriceHistory.objects.update_or_create(
                        product=product,
                        defaults={
                            'price':latest[0].current_price,
                            'date':datetime.datetime.now(tz=timezone.utc)
                        }   
                    )
                    if latest[0].current_price < product.current_price:
                        send_price_drop_notification(product, latest[0])
                        print("Notification sent")
                elif product.place == "GG Shopping":
                    print(product.name)
            time.sleep(10)
    except Exception as e:
        # Log the exception, you might want to use a logging library
        print(f"Exception in background thread: {e}")

def send_price_drop_notification(product, latest_item):
    favorite_users = Favourite.objects.filter(product=product)
    if favorite_users:
        subject = f'Price Drop Alert for {product.name}'
        message = f'The price for {product.name} has dropped to {latest_item.current_price}.\nCheck it out now!'
        from_email = 'emailtam1231@gmail.com'
        
        recipient_list = [favorite.user.email for favorite in favorite_users]
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print(f"From: {from_email}")
        print(f"To: {recipient_list}")
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False,)     
        except BadHeaderError as e:
            print(f"BadHeaderError: {e}")
            # Handle BadHeaderError or other exceptions
        except Exception as e:
            print(f"Exception occurred while sending email: {e}")


@login_required(login_url="/login")
def add_to_favourite(request, product_id):
    name = request.POST.get('name', None)
    product = Product.objects.get(pk=product_id)
    favourite = Favourite.objects.get_or_create(user=request.user)[0]
    favourite_item = FavouriteItem.objects.get_or_create(favourite=favourite, product=product)[0]
    favourite_items = FavouriteItem.objects.filter(favourite=favourite)
    products_to_check = [fav_item.product for fav_item in favourite_items]
    print(products_to_check)
    # Start a single thread to check all products
    thread = Thread(target=price_check_timer, args=(products_to_check,))
    thread.start()
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
    newForm = ProductNameForm()
    try:
        
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
    if product1 != []:
        product1_price = Decimal(product1[0].current_price)
        lists.append({'item': product1[0], 'price': product1_price})   
    product2 = media_mart_one(name)
    if product2 != []:
        product2_price = Decimal(product2[0].current_price)
        lists.append({'item': product2[0], 'price': product2_price})
    product3 = nguyen_kim_one(name)
    if product3 != []:
        product3_price = Decimal(product3[0].current_price)
        lists.append({'item': product3[0], 'price': product3_price})
    product4 = gg_shopping(name)
    # Create a list of items with their prices
    # lists = [
    #     {'item': product1[0], 'price': product1_price},
    #     {'item': product2[0], 'price': product2_price},
    #     {'item': product3[0], 'price': product3_price},
    # ]
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
    try:
        product = Product.objects.get(pk=product_id)
        price_history_data = get_price_history(product)
        form = ProductNameForm()  # Assuming you have a form called ProductNameForm
        return render(request, 'price_history.html', {'product': product, 'price_history_data': price_history_data, 'form': form})
    except Product.DoesNotExist:
        # Handle product not found error
        pass

def get_price_history(product):
    try:
        price_history = PriceHistory.objects.filter(product=product).values('price', 'date')
        return list(price_history)
    except PriceHistory.DoesNotExist:
        return []
# def price_history_data(request, product_id):
#     product = Product.objects.get(pk=product_id)

#     # Create some dummy price history data for testing (similar to the previous view)
#     price_history_data = []
#     today = datetime.now()
#     for i in range(1, 11):
#         date = today - timedelta(days=i)
#         price = product.current_price - (randint(1, 10) * 10)
#         price_history_data.append({
#             'timestamp': date.strftime('%Y-%m-%d'),
#             'price': price,
#         })

#     return JsonResponse({'price_history_data': price_history_data})


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
            # review.user = request.user  # Set the user
            # review.product = product   # Set the product
            review.save()
            product.average_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
            product.save()
            form = ReviewForm()
            referring_url = request.POST.get('next', None)
            print(referring_url)
            if referring_url:
                return redirect(referring_url)
            else:
                # If 'next' is not provided, go to the product details page
                return redirect(reverse('view_reviews', args=[product_id]))
            
            # return render(request, 'view_reviews.html', {'product': product, 'reviews': Review.objects.filter(product=product), 'form':nameForm})
        else:
            print(form.errors)

    return render(request, 'add_review.html', {'form': nameForm, 'product': product, 'reviewForm': reviewForm, 'user': request.user})

def view_reviews(request, product_id):
    form = ProductNameForm()
    product = Product.objects.get(pk=product_id)
    reviews = Review.objects.filter(product=product)

    return render(request, 'view_reviews.html', {'product': product, 'reviews': reviews, 'form':form, 'user': request.user})


def shop_user_signup(request):
    if request.method == 'POST':
        form = ShopUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_shop = True
            user.save()
            form = ProductNameForm()
            login(request, user)
            return redirect('/')
            # return render(request, 'search_form.html', {'user': user, 'form':form})
    else:
        form = ShopUserForm()
    return render(request, 'shop_user_signup.html', {'form': form})

def add_product(request):
    form = ProductNameForm()
    user = request.user
    if request.method == 'POST':
        newForm = ProductForm(request.POST)
        if newForm.is_valid():
            product = newForm.save(commit=False)
            product.place = user.shop_name or 'N/A'
            product.average_rating = 0
            product.date_add = datetime.datetime.now(tz=timezone.utc)
            product.save()
            PriceHistory.objects.create(product=product, price=product.current_price, date=datetime.datetime.now(tz=timezone.utc))
            print(product)
            user.products.add(product)
            user.save()
            referring_url = request.POST.get('next', None)
            products = user.products.all()
            # return redirect('/')
            if referring_url:
                return redirect(referring_url)
            else:
                # If 'next' is not provided, go to the product details page
                return redirect(reverse('/', args=[products]))
    else:
        newForm = ProductForm()
        form = ProductNameForm()
    return render(request, 'add_product.html', {'form': form, 'newForm': newForm})

def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    user = request.user
    product.delete()


    return HttpResponseRedirect('/shop')

def change_product(request, product_id):
    form = ProductNameForm()
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        newForm = ProductForm(request.POST, instance=product)
        if newForm.is_valid():
            newForm.save()

            return redirect('shop')  # Redirect to a specific page after successful update
    else:
        form = ProductNameForm()
        newForm = ProductForm(instance=product)
    return render(request, 'change_product.html', {'form': form, 'product': product, 'newForm': newForm})

@login_required(login_url='/login')
def shop(request):
    form = ProductNameForm()
    user = request.user
    products = user.products.all()
    return render(request, 'shop.html', {'products': products, 'user': user, 'form':form})

