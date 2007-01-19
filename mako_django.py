from django.conf import settings
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.template.context import Context
from django.template.loaders.app_directories import app_template_dirs
from mako.lookup import TemplateLookup
from mako.template import Template
from mako.exceptions import TopLevelLookupException

template_dirs = settings.TEMPLATE_DIRS + app_template_dirs
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
