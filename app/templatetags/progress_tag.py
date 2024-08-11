from django import template
import math
register = template.Library()


@register.simple_tag

def cal_avg (price,discount):
    if discount is None or discount is 0:
        return price
    sell_price = price
    sell_price = price - (price*discount/100)
    return math.floor(sell_price)



@register.simple_tag

def progress_bar(total_quantity,availability):
    progress_bar = availability
    progress_bar = availability * (100/total_quantity)

    return math.floor(progress_bar)




