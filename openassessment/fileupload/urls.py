from django.conf.urls import url

from openassessment.fileupload import views_django_storage, views_filesystem, views_s3

urlpatterns = [
    url(r'^django/(?P<key>.+)/$', views_django_storage.django_storage, name='openassessment-django-storage'),
    url(r'^s3/(?P<key>.+)/$', views_s3.s3_storage, name='openassessment-s3-storage'),
    url(r'^(?P<key>.+)/$', views_filesystem.filesystem_storage, name='openassessment-filesystem-storage'),
]
