from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType


def sanity_check(request, content_type, order_by_field, objects, primary_keys):
    # Fetched objects should be as many as the primary keys
    if len(objects) != len(primary_keys):
        return False

    Class = content_type.model_class()
    fields = [f.name for f in Class._meta.fields]

    if order_by_field not in fields:
        return False

    return True


def security_check(request, content_type, order_by_field, objects,
                   primary_keys):
    model_name = content_type.model_class().__name__.lower()
    permission_name = '{}.change_{}'.format(
        content_type.app_label, model_name
    )
    return request.user.has_perm(permission_name)


def generic_sorting_url(queryset, order_by_field=None):
    ctype = ContentType.objects.get_for_model(queryset.model)
    primary_keys_qs = queryset.values_list('pk', flat=True)
    primary_keys = ','.join([str(pk) for pk in primary_keys_qs])

    if not order_by_field:
        try:
            order_by_field = ctype.model_class().Meta.ordering()[0]
        except (AttributeError, IndexError) as e:
            raise e()

    kwargs = {
        'content_type_pk': str(ctype.pk),
        'order_by_field': order_by_field,
        'primary_keys': primary_keys
    }

    return reverse_lazy('generic_sorting:generic_sorting', kwargs=kwargs)
