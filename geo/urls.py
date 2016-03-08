from django.conf.urls import include, url
import views

urlpatterns = [
  url(r'list/map/', views.ListMap.as_view(), name="listMap"),
  url(r'list/data.json', views.ListNull.as_view(), name="ListNull"),
  url(r'form/(?P<pk>\d+)/', views.GeoForm.as_view(), name="geoform"),
]