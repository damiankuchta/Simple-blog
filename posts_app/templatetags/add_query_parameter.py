from django import template

register = template.Library()

@register.simple_tag
def add_query_parameter(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()