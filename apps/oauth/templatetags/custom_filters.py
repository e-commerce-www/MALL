from django import template

register = template.Library()

@register.filter
def calculate_index(page_number, per_page, counter):
    return counter + (per_page * (page_number -1))