# accounts/templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Adds a CSS class to a form field
    Usage in template: {{ form.field|add_class:"my-class" }}
    """
    css_classes = value.field.widget.attrs.get('class', '')
    # Only add the class if it's not already present
    if css_classes:
        if arg not in css_classes:
            css_classes = f'{css_classes} {arg}'
    else:
        css_classes = arg
    return value.as_widget(attrs={'class': css_classes})