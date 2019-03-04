from django.conf.urls import url
from rest_demo import views

urlpatterns = [
    url(r'^books/', views.BookView.as_view()),
    url(r'^book/(\d+)', views.BookDetailView.as_view()),

    url(r'^authors/', views.AuthorView.as_view()),
    url(r'^author/(?P<pk>\d+)/', views.AuthorDetailView.as_view()),

    url(r'^publishes/', views.PublishView.as_view()),
    url(r'^publish/(?P<pk>\d+)/', views.PublishDetailView.as_view()),

    url(r'^publishs/$', views.PublishViewSet.as_view({"get": "list","post": "create"})),
    url(r'^publishs/(?P<pk>\d+)/$', views.PublishViewSet.as_view({"get": "retrieve","put": "update","delete": "destroy"})),
]