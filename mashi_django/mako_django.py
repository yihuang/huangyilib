from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.template.context import Context
from mako.lookup import TemplateLookup
from mako.template import Template
from mako.exceptions import TopLevelLookupException
import os

app_template_dirs = []
for app in settings.INSTALLED_APPS:
    i = app.rfind('.')
    if i == -1:
        m, a = app, None
    else:
        m, a = app[:i], app[i+1:]
    try:
        if a is None:
            mod = __import__(m, {}, {}, [])
        else:
            mod = getattr(__import__(m, {}, {}, [a]), a)
    except ImportError, e:
        raise ImproperlyConfigured, 'ImportError %s: %s' % (app, e.args[0])
    template_dir = os.path.normpath(
            os.path.join(os.path.dirname(mod.__file__), 'mako_templates'))
    if os.path.isdir(template_dir):
        app_template_dirs.append(template_dir)

template_dirs = settings.MAKO_TEMPLATE_DIRS + tuple(app_template_dirs)
lookup = TemplateLookup(directories=template_dirs,
            module_directory='templates')

def select_template(template_name_list):
    for template_name in template_name_list:
        try:
            return lookup.get_template(template_name)
        except TopLevelLookupException:
            pass

    raise TemplateDoesNotExist, ', '.join(template_name_list)

def get_template(template_name):
    try:
        return lookup.get_template(template_name)
    except TopLevelLookupException:
        raise TemplateDoesNotExist, template_name

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
    return HttpResponse(template.render(**data))