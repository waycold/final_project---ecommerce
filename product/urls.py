from django.urls import path
from product.views import log_in, log_out, sign_up, ItemDetailView, about, add_to_cart, remove_from_cart, store, HomeView, profile, edit_profile, home, remove_single_cart


app_name = 'product'

urlpatterns = [
    path('', home),
    path('logout/', log_out),
    path('signup/', sign_up),
    path('login/', log_in),
    path('profile/', profile),
    path('edit_profile/<username>/', edit_profile, name="edit_profile"),
    path('product/<slug>/', ItemDetailView.as_view(), name="product"),
    path('about/', about),
    path('checkout/', store),
    path('add_to_cart/<slug>/', add_to_cart, name="add_to_cart" ),
    path('remove_single_cart/<slug>/', remove_single_cart, name="remove_from_cart" ),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
]