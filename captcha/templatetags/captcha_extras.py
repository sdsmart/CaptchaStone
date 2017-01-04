from django import template

register = template.Library()

@register.filter(name = 'addstr')
def addstr(arg1, arg2): #From http://stackoverflow.com/questions/4386168/how-to-concatenate-strings-in-django-templates
    return str(arg1) + str(arg2)