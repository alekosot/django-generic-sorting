from django.conf.urls import url
from .views import generic_sorting


app_name = 'generic_sorting'


urlpatterns = [
    url(r'(?P<content_type_pk>[\w]+)/(?P<order_by_field>[\w]+)/(?P<primary_keys>[\w,]+)/',
        generic_sorting,
        name='generic_sorting'),
]
