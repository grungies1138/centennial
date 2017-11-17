# URL patterns for the character app

from django.conf.urls import url
from web.characterview.views import sheet

urlpatterns = [
    url(r'^sheet/(?P<object_id>\d+)/$', sheet, name="sheet")
]