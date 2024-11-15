from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages

from .models import *
from .forms import *


def index(request):
    return render(request, "auctions/index.html", {"auction_list":auction_list.objects.all()})


def productdetails(request,auction_id):
    user=request.user
    product=auction_list.objects.get(pk=auction_id)
    comment=product.comments.all()
    owner=product.owner
    a=False
    if owner==user:
        a=True


    if product in user.watchlist.all():
        
        return render(request,"auctions/productdetails.html",{"product":auction_list.objects.get(pk=auction_id),"in_watchlist":True,"form":CommentForm(),"comments":comment,"form_b":BidsForm(),"a":a})
    return render(request,"auctions/productdetails.html",{"product":auction_list.objects.get(pk=auction_id),"in_watchlist":False,"form":CommentForm(),"comments":comment,"form_b":BidsForm(),"a":a})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def watchlist(request):
    if request.POST:

        product_id=request.POST["product"]
        product=auction_list.objects.get(pk=product_id)
        user=request.user
        user.watchlist.add(product)
    watchlist=request.user.watchlist.all()

    return render(request, "auctions/watchlist.html", {"watchlist": watchlist})

    

def cats(request):
    categories=Category.objects.all()
    return render(request, "auctions/catogeries.html", {"catogeries":categories})

def register_product(request):
    if request.method=="POST":
        form=AuctionForm(request.POST)
        if form.is_valid():

            auction=form.save(commit=False)
            auction.owner=request.user
            auction.save()
            return redirect('index')
    else:
        form=AuctionForm()
        
            
    return render(request,"auctions/create.html", {"form":form})

def cat_product(request,category_id):
    category=Category.objects.get(pk=category_id)
    product=category.auctions.all()
    return render(request,"auctions/category_product.html",{"auction_list":product})

def remove_watchlist(request,remove_id):
    if request.method=="POST":
        id=request.POST["product_to_remove"]
        product_to_remove=auction_list.objects.get(pk=id)
        user=request.user
        user.watchlist.remove(product_to_remove)
        return HttpResponseRedirect(reverse('index'))

def add_comment(request):
    if request.method=="POST":
        user=request.user
        product_id=request.POST["product_commented"]
        product=auction_list.objects.get(pk=product_id)
        form=CommentForm(request.POST)
        if form.is_valid():
            commentss=form.save(commit=False)
            commentss.person=user
            commentss.item=product
            commentss.save()
            return redirect("auction_detail", auction_id=product_id)
        return redirect("auction_detail", auction_id=product_id)
    return redirect('index')


def update_bid(request):
    if request.method == "POST":
        user=request.user
        product_id=request.POST["product_bidded"]
        product=auction_list.objects.get(pk=product_id)
        form=BidsForm(request.POST)
        price=product.starting_bid

        if form.is_valid():
            bid_amount=form.cleaned_data['price']

            if bid_amount > price:
                product.starting_bid=bid_amount
                product.winner=user
                product.save()
                new_bid=form.save(commit=False)
                new_bid.user=user
                new_bid.list_item=product
                new_bid.save()
                list(messages.get_messages(request))
                messages.success(request, "Bid placed successfully!")

            else:
                list(messages.get_messages(request))
                messages.error(request, "Your bid must be higher than previous price")
    return redirect('auction_detail', auction_id=product_id)

def stop_bid(request):
    auction_id=request.POST['product_stop']
    product=auction_list.objects.get(pk=auction_id)
    product.is_active=False
    product.save()
    return redirect('auction_detail', auction_id=auction_id)



