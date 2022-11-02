from django.urls import path
from product.views import HomeView, log_in, log_out, sign_up,ItemDetailView, about


app_name = 'product'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', log_out),
    path('signup/', sign_up),
    path('login/', log_in),
    path('product/<slug>/', ItemDetailView.as_view(), name="product"),
    path('about/', about),
]