from product.models import Profile
from django import template


register = template.Library()

@register.simple_tag()
def image_user_tag(user):
    return user
    # if user == Profile.username:
    #     return Profile.image



