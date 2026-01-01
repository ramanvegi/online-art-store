from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


import qrcode
from django.conf import settings
import os
from django.shortcuts import render



def index(request):
    products = Product.objects.all()
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render(request, "index.html", {
        "products": products,
        "cart": cart,
        "total": total
    })


@login_required(login_url='/login/')
def add_to_cart(request, pid):
    product = Product.objects.get(id=pid)
    cart = request.session.get('cart', [])
    cart.append({"name": product.name, 
                 "price": product.price
                })
    request.session['cart'] = cart
    return redirect('/')

def register_user(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('/login/')
    return render(request, "register.html")

def login_user(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect('/')

def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
    request.session['cart'] = cart
    return redirect('/')

def buy_now(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)

    # Dummy UPI/payment data
    data = f"upi://pay?pa=artstore@upi&pn=ArtStore&am={total}&cu=INR"

    qr_path = os.path.join(settings.BASE_DIR, 'static', 'qr.png')
    img = qrcode.make(data)
    img.save(qr_path)

    return render(request, "buy.html", {"total": total})

