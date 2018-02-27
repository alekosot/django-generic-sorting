from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelformset_factory
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.encoding import force_text

from . import settings as conf


def generic_sorting(request, content_type_pk, order_by_field, primary_keys):
    ctype = get_object_or_404(ContentType, pk=content_type_pk)
    Class = ctype.model_class()
    primary_keys = primary_keys.split(',')
    objects = Class._base_manager \
        .filter(pk__in=primary_keys) \
        .order_by(order_by_field)  # TODO: What about desc ordering?
    FormSet = modelformset_factory(
        Class, fields=(order_by_field,), extra=0,
        widgets={order_by_field: forms.HiddenInput()}
    )

    tpl = '{}{}/{}/generic_sorting_base.html'.format(
        conf.TEMPLATE_PREFIX,
        Class._meta.app_label,
        Class._meta.model_name
    )
    templates = (tpl, conf.BASE_TEMPLATE)

    if not all(check(request, ctype, order_by_field, objects, primary_keys)
               for check in conf.CHECKS):
        # NOTE: The HTTP status could be different, but this is good enough
        return HttpResponseNotFound()

    if request.method == 'POST':
        formset = FormSet(request.POST)
        if formset.is_valid():
            formset.save()
            url = getattr(
                settings, 'GENERIC_SORTING_SUCCESS_URL', request.path
            )
            return HttpResponseRedirect(force_text(url))
    else:
        formset = FormSet(queryset=objects)

    context = {
        'model': Class,
        'model_name': Class._meta.verbose_name,
        'model_name_plural': Class._meta.verbose_name_plural,
        'formset': formset,
        'order_by_field': order_by_field
    }

    return render(request, templates, context)
