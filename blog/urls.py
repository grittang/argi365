from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('blog/', views.BlogView.as_view(), name='blog'),
  path('c<int:pk>', views.ChannelView.as_view(), name='channel'),
  path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
  path('category/<int:pk>', views.CategoryView.as_view(), name='category'),
  path('tag/<int:pk>', views.TagView.as_view(), name='tag'),
  path('about', views.AboutView.as_view(), name='about'),
]