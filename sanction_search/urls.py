from django.conf.urls import url,include
from . import views


urlpatterns = [
url(r'^$' , views.index, name = 'index'),
url(r'doj/' , views.doj_search, name = 'doj'),
url(r'ofac/' , views.ofac_search, name = 'ofac'),
url(r'actionUrl_doj' , views.doj_search, name = 'doj_button'),
url(r'actionUrl_ofac' , views.ofac_search, name = 'ofac_button'),
url(r'ofac_name' , views.ofac_search_name, name = 'ofac_name'),
url(r'doj_name' , views.doj_search_name, name = 'doj_name')


]


