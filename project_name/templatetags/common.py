import json
from os.path import join

from django import template
from django.contrib.staticfiles import finders

register = template.Library()


@register.inclusion_tag(file_name='inc/javascripts.html', takes_context=True)
def devel_js_scripts(context, group='common'):
    fn = finders.find(join('_dev', 'build.json'))
    with open(fn, 'r') as fp:
        json_data = json.load(fp)

    context['scripts'] = json_data[group]
    return context
