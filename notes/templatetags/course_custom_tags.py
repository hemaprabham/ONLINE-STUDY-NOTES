from django import template
import math

from notes.models import UserCourse , Course ,Payment
register = template.Library()

# 100 -> 10% --> mrp  - ( mrp * discount * 0.01 ) = selprice
@register.simple_tag
def cal_sellprice(price , discount):
    if discount is None or discount == 0:
        return price
    sellprice = price
    sellprice = price - ( price * discount * 0.01 )
    return math.floor(sellprice)


@register.filter
def rupee(price):
    return f'₹{price}'




@register.simple_tag
def is_enrolled(request , course):
   
    username = None
    if not request.username.is_authenticated:
        return False
        # i you are enrooled in this course you can watch every video
    username = request.username
    try:
        user_course = UserCourse.objects.get(username = username  , course = course)
        return True
    except:
        return False

