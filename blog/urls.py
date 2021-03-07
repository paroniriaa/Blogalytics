from . import views
from django.urls import path
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from django.views import static

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('article/edit/<slug:slug>', views.UpdatePostView.as_view(), name='update_post'),
    path('article/delete/<slug:slug>', views.DeletePostView.as_view(), name='delete_post'),
    path('like/<slug:slug>', views.LikeView, name='like_post'),
    path('<int:pk>/profile/', views.ProfileView.as_view(), name='profile'),
    path('<int:id>/edit_account/', views.edit_account, name='edit_account'),
    url(r'analytics/$', csrf_exempt(views.store_coordinates), name='store_coordinates'),
    url(r'analytics/heatmap/(?P<id>(\w*-*\w*))/$', views.generate_heatmap, name='generate_heatmap'),
    url(r'analytics/elements/(?P<id>\d{1,6})/$', views.retrieve_html_elements, name='retrieve_html_elements'),
    url(r'analytics/page/(?P<id>\d{1,6})/$', views.retrieve_heatmap_information, name='retrieve_heatmap_information'),
    url(r'analytics/html/(?P<path>.*)$', static.serve, {'document_root': '.'})
]