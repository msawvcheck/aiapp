from django.conf.urls import url
from . import views


def index(request):
    return HttpResponse("<h2>HEY!</h2>")


urlpatterns = [
url(r'^$' , views.index, name = 'index')
]

# Create your views here.
