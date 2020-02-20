from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

""" truncatechars is not available in Django 1.3, so we define our own
	Maybe try to upgrade to 1.4 to get the official truncatechars 
	good practice to try and build this myself"""

@register.filter(name='truncatechars')
@stringfilter
def truncatechars(value, size):
    if len(value) > size:
    	# why size -3 and not just size? -3 is to make space for ellipsis
    	# truncates everything *starting* at value[size-3] and then "..."
        return value[:(size-3)] + '...'
    else:
        return value
