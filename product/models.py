from unicodedata import category
from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('CPU', 'Central Processing Unit'),
    ('RAM', 'Random Access Memory'),
    ('GPU', 'Graphics Processing Unit')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)



class Item(models.Model):
    tittle = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits=5, decimal_places= 0)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length = 5)
    label = models.CharField(choices = LABEL_CHOICES, max_length = 5)
    slug = models.SlugField()

    def __str__(self):
        return self.tittle

    def get_absolute_url(self):
        return reverse("product:product", kwargs={
            'slug': self.slug
        } )


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


    def __str__(self):
        return self.tittle

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.username