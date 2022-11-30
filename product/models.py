from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('CPU', 'CPU'),
    ('RAM', 'RAM'),
    ('GPU', 'GPU')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model):
    tittle = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500, null=True)
    price = models.DecimalField(max_digits=10, decimal_places= 0)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length = 5)
    label = models.CharField(choices = LABEL_CHOICES, max_length = 5, null=True, blank= True)
    slug = models.SlugField()
    img = models.ImageField(upload_to='products/', null=True)
    

    def __str__(self):
        return self.tittle

    def get_absolute_url(self):
        return reverse("product:product", kwargs={
            'slug': self.slug
        } )

    def get_add_to_cart_url(self):
        return reverse("product:add_to_cart", kwargs={
            'slug': self.slug
        } )


    def get_delte_url(self):
        return reverse("product:delete", kwargs={
            'slug': self.slug
        } )

    def get_remove_from_cart_url(self):
        return reverse("product:remove_from_cart", kwargs={
            'slug': self.slug
        } )

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null= True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity= models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.item.tittle}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.DecimalField(decimal_places=0, max_digits=10, null=True, blank=True)
    description = models.CharField(max_length = 300, null= True, blank=True)
    image = models.ImageField(upload_to='profile/', blank=True, default='/uploads/profile/default.jpg', null=True)


    def __str__(self):
        return self.username.username

    def get_profile_url(self):
        return reverse("product:edit_profile", kwargs={
            'username': self.username.username
        } )

