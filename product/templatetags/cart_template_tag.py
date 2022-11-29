from product.models import Order, Profile
from django import template



register = template.Library()

@register.filter()
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user = user, ordered = False)
        if qs.exists():
            return qs[0].items.count()
    return 0


@register.simple_tag()
def image_user_tag(user):
    pass
