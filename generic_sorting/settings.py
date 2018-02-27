from django.conf import settings
from .utils import sanity_check, security_check


BASE_TEMPLATE = getattr(
    settings, 'DYNAMIC_SORTING_BASE_TEMPLATE',
    'generic_sorting/generic_sorting_base.html'
)

TEMPLATE_PREFIX = getattr(
    settings, 'DYNAMIC_SORTING_TEMPLATE_PREFIX', ''
)

CHECKS = getattr(
    settings, 'DYNAMIC_SORTING_CHECKS', (security_check, sanity_check)
)
