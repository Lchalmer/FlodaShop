from django import template

register = template.Library()


# 根据商品原价及折扣，计算折后价格
@register.filter(name='final_price')
def fina_price(value, arg):
    """
    value: 要进行过滤的值 price 商品原价
    arg:    传递的参数 discount 折扣
    """
    return "%.2f" % (float(value) * float((1 - arg)))


@register.filter(name='discount')
def discount(value):
    """
    value: 折扣
    """
    return "%.2f%%" % (value * 100)


@register.filter(name='multiply_by')
def multiply_by(value, arg):
    return float(value) * float(arg)