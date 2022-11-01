from django.contrib import admin
from django.urls import path
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('logout/', views.log_out),
    path('login/', views.log_in),
]
