from django.conf import settings
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.template.context import Context
from genshi.template import MarkupTemplate, TemplateLoader
from genshi.template.loader import TemplateNotFound

import os
from common import app_dirs

'''
configuration:
    GENSHI_TEMPLATE_DIRS:
        specify directories in which to find the genshi template files.
'''

app_template_dirs = []
for app_dir in app_dirs:
    template_dir = os.path.join(app_dir, 'genshi_templates')
    if os.path.isdir(template_dir):
        app_template_dirs.append(template_dir)

template_dirs = getattr(settings, 'GENSHI_TEMPLATE_DIRS', None) or ('genshi_templates',)
template_dirs += tuple(app_template_dirs)

loader = TemplateLoader(template_dirs, auto_reload=settings.DEBUG)

def select_template(template_name_list):
    for template_name in template_name_list:
        try:
            return loader.load(template_name)
        except TemplateNotFound:
            pass

    raise TemplateDoesNotExist, 'genshi templates: '+', '.join(template_name_list)

def get_template(template_name):
    try:
        return loader.load(template_name)
    except TemplateNotFound:
        raise TemplateDoesNotExist, 'genshi templates: '+template_name

def render_to_response(template_name, dictionary=None,
        context_instance=None):
    if isinstance(template_name, (list, tuple)):
        template = select_template(template_name)
    else:
        template = get_template(template_name)

    dictionary = dictionary or {}
    if context_instance is None:
        context_instance = Context(dictionary)
    else:
        context_instance.update(dictionary)
    data = {}
    [data.update(d) for d in context_instance]
    stream = template.generate(**data)
    return HttpResponse(stream.render('xhtml'))
