from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user/(?P<user_id>\d+)$', views.user),
    url(r'^registration$', views.registration),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^points$', views.points),
    url(r'^home$', views.home),
    url(r'^', views.index)
]