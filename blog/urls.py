from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('article/edit/<slug:slug>', views.UpdatePostView.as_view(), name='update_post'),
    path('article/delete/<slug:slug>', views.DeletePostView.as_view(), name='delete_post'),
    path('like/<slug:slug>', views.LikeView, name='like_post'),
    path('<int:pk>/profile/', views.ProfileView.as_view(), name='profile'),
    path('<int:id>/edit_account/', views.edit_account, name='edit_account'),
]