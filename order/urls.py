from django.conf.urls import url
from .views import *
urlpatterns = [
    url('^addorder/', addorder, name='add_order'),
]
