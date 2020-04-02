from django import template

register = template.Library()


@register.filter
def my_range(value):
    return [0] * value


@register.filter
def my_pages(value, total):
    value = int(value)
    total = int(total)
    if value == 1:
        end = (value + 4) if total > (value + 4) else total + 1
        return [i for i in range(value, end)]
    elif value == 2:
        end = (value + 3) if total > (value + 3) else total + 1
        return [i for i in range(1, end)]
    else:
        end = (value + 3) if total > (value + 3) else total + 1
        return [i for i in range(value - 2, end)]


@register.filter
def into_str(value):
    return str(value)


@register.filter
def into_int(value):
    return int(value)


@register.filter
def into_list(value):
    value = value.split(',')
    return value


@register.filter
def add(value, add):
    return int(value) + int(add)


@register.filter
def sub(value, add):
    return int(value) - int(add)


@register.filter
def label(value):
    value = value.capitalize().split('_')
    value = ' '.join(value)
    return value


@register.filter
def test(value):
    print(type(value))
    # return value
