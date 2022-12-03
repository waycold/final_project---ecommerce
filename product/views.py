from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.db import IntegrityError
from django.db.models import Q
from product.models import Item, OrderItem, Order, Profile, Comments
from product.forms import profile_edit_form, comments_form
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
# home render




class HomeView(ListView):
    model = Item
    template_name = "home.html"
    paginate_by= 8


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def products(request, slug):
    input = "-"
    output = " "
    change = str.maketrans(input, output)
    id = slug
    modifed_slug = id.translate(change)
    modifed_slug = modifed_slug.capitalize()
    items = Item.objects.filter(
        tittle__icontains = modifed_slug
    )
    comments = Comments.objects.filter(
        url = request.path
    )
    if "submit" in request.POST:
        date_adedd = timezone.now()
        Comments.objects.create(
            user = request.user,
            body = request.POST['body'],
            date_adedd = date_adedd,
            url = request.path
        )
        context = {
            'items': items,
            'comments': comments,
            'form': comments_form,
        }
        return render(request, 'product.html', context)
    context = {
        'items': items,
        'comments': comments,
        'form': comments_form,
    }
    return render(request, 'product.html', context)


# sign up function

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                new_profile = Profile.objects.create(username = user)
                new_profile.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'User already exists'})
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'})


# log out function

def log_out(request):
    logout(request)
    return redirect('/')


# log in function

def log_in(request):
    if request.method == 'GET':
        return render(request, 'login.html',{
        'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html',{
            'form': AuthenticationForm, 
            'error': 'User or password is incorrect'})
        else:
            login(request, user)
            return redirect('/')

def about(request):
    context = {
        'items': Item.objects.all(),
        'orderitems': OrderItem.objects.all(),
        'profile': Profile.objects.all()
    }
    return render(request, 'about.html', context)


def store(request):
    order_qs = OrderItem.objects.filter(
        user = request.user,
        ordered = False
    )
    qs = request.POST.get("delete")
    if "delete" in request.POST:
        items = order_qs.delete()
        context = {
            'orderitems': items
        }
        return redirect('/checkout/')
    if "buy" in request.POST and order_qs.count() >= 1:
        print(order_qs)
        items = order_qs.delete()
        context = {
            'orderitems': items
        }
        messages.info(request, "Your purchase has been successful!")
        return redirect ('/')
    context = {
        'items': Item.objects.all(),
        'orderitems': order_qs,
        'comments': Comments.objects.all()
    }
    return render(request, 'checkout.html', context)


def profile(request):
    form = profile_edit_form
    profile1 = Profile.objects.all()
    profile2 = Profile.user
    image_form = request.POST.get("image")
    if image_form:
        image_form = profile_edit_form(request.POST, request.FILES , instance=profile)
        image_form.save()
        context = {
            'items': Item.objects.all(),
            'profile': Profile.objects.all(),
            'form': form,
            'image_form': image_form,
        }
        return render(request, 'profile.html', context)
    context = {
        'items': Item.objects.all(),
        'profile': Profile.objects.all(),
        'form': form,
        'image_form': image_form,
        }
    return render(request, 'profile.html', context)


def edit_profile(request, username):
    user = request.user
    profile = get_object_or_404(Profile, username = user)
    form = profile_edit_form(instance=profile)
    if request.method == "GET":
        context = {
                'items': Item.objects.all(),
                'profile': Profile.objects.all(),
                'form': form,
            }
        return render(request, 'edit_profile.html', context)
    else:
        try:
            form = profile_edit_form(request.POST, request.FILES , instance=profile)
            form.save()
            return redirect("/profile")
        except ValueError:
            messages.info(request, "Error updating data.")

            context = {
                'items': Item.objects.all(),
                'profile': Profile.objects.all(),
                'form': form,
            }
            return render(request, 'edit_profile.html', context)


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        # check if the order item is in the order
        
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")

        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            Item.objects.update()

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user= request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        Item.objects.update(in_cart=True)
        messages.info(request, "This item was added to your cart")
    return redirect("product:product", slug=slug
    )


def remove_single_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        print(f"a {order_qs} a  ")
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity -= 1
            order_item.save()
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item quantity was update!")
            return redirect("product:product", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product:product", slug=slug)

def home(request):
    qs = request.POST.get("search")
    items = Item.objects.all()
    if qs:
        items = Item.objects.filter(
            Q(category__icontains = qs) |
            Q(tittle__icontains = qs)
        ).distinct()
    if "CPU" in request.POST:
        items = Item.objects.filter(
            category = 'CPU' 
        )
    if "GPU" in request.POST:
        items = Item.objects.filter(
            category = 'GPU' 
        )
    if "RAM" in request.POST:
        items = Item.objects.filter(
            category = 'RAM' 
        )
    context = {
        'items': items,
        'search': qs
    }
    return render(request, 'home.html', context)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("product:checkout")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product:product", slug=slug)


# def delete(request, slug):
#     item = get_object_or_404(Item, slug=slug)
#     order_qs = Order.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__slug=item.slug).exists():
#             order_item = OrderItem.objects.filter(
#                 item=item,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             order.items.remove(order_item)
#             order_item.delete()
#             messages.info(request, "This item was removed from your cart.")
#             return redirect("product:checkout")
#         else:
#             messages.info(request, "This item was not in your cart")
#             return redirect("product:checkout", slug=slug)
#     else:
#         messages.info(request, "You do not have an active order")
#         return redirect("product:checkout", slug=slug)

def delete(request):
    order_qs = OrderItem.objects.filter(
        user = request.user,
        ordered = False
    )
    qs = request.POST.get("delete")
    print("work2")
    if qs:
        print("work")
        items1 = order_qs.remove()
        items2 = order_qs.delete()
        context = {
            'orderitems': items2
        }
        return render(request, "checkout.html", context)