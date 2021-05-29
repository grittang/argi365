from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
  # path('base/', views.BaseView.as_view(), name='base'),
  path('', views.IndexView.as_view(), name='index'),
  path('blog/', views.BlogView.as_view(), name='blog'),
  path('C<int:pk>', views.ChannelView.as_view(), name='channel'),
  path('posts/<int:pk>', views.PostDetailView.as_view(), name='detail'),
  path('categories/<int:pk>', views.CategoryView.as_view(), name='category'),
  path('tags/<int:pk>', views.TagView.as_view(), name='tag'),
  path('about', views.AboutView.as_view(), name='about'),

  # form urls
  path('posts/create/', views.posts_create, name='posts_create'),
]