from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^adhesion$', views.adhesion, name='adhesion'),
    url(r'^benevole$', views.benevole, name='benevole'),
    url(r'^militant$', views.militant, name='militant'),
    # ex: /member/5/
    url(r'^(?P<member_id>[0-9]+)/$', views.get_member, name='detail'),

]