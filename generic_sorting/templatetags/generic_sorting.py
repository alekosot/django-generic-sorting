from django import template
from django.template.loader import get_template

from generic_sorting import settings as conf
from generic_sorting.utils import generic_sorting_url


register = template.Library()

register.simple_tag(generic_sorting_url)


@register.simple_tag
def generic_sorting_partial_template(model):
    app_label = model._meta.app_label
    model_name = model._meta.model_name
    tpl = '{}{}/{}/partials/generic_sorting.html'.format(
        conf.TEMPLATE_PREFIX, app_label, model_name
    )
    try:
        get_template(tpl)
    except template.TemplateDoesNotExist:
        tpl = 'generic_sorting/partials/generic_sorting.html'

    return tpl
