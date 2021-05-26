from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.db.models import Count
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from .models import Channel, Post, Category, Tag
from .forms import PostForm
import markdown
from markdown.extensions.toc import TocExtension
import re

class BaseView(ListView):
  model = Channel
  template_name = 'base.html'
  context_object_name = 'channel_list'

class IndexView(BaseView):
  template_name = 'blog/index.html'


class BlogView(BaseView):
  """BlogView 视图将为所有基于 post 的视图提供 blog 模板"""
  template_name = 'blog/blog.html'
  paginate_by = 1

class ChannelView(BlogView):
  # 下面这段代码将使导航栏只包含本 channel，而无法显示并跳转到其他 channel
  # def get_queryset(self):
  #   return Channel.objects.filter(pk=self.kwargs.get('pk'))

  # 同时将文章及其类别列表传入 blog.html，然后按照 channel 的参数对 category 和 post 进行分组
  # https://stackoverflow.com/questions/31133963/multiple-models-generic-listview-to-template
  def get_context_data(self, **kwargs):
    context = super(ChannelView, self).get_context_data(**kwargs)
    # 先传入 channel 本身
    context['channel'] = get_object_or_404(Channel, pk=self.kwargs.get('pk'))

    queried_category = Category.objects.filter(channel__id=self.kwargs.get('pk'))
    # 统计各类别中文章的数量，如果为0，则不显示
    # num_posts 的用法：https://www.facebook.com/notes/institute-of-applied-ai-engineers/python-django-summary-aggregate-or-custom-quries-in-template/494230914271780/
    context['category_list'] = queried_category.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    
    # 跨表查询，通过已经筛选的 category 进一步筛选 post
    # https://stackoverflow.com/questions/50431810/the-queryset-value-for-an-exact-lookup-must-be-limited-to-one-result-using-slici
    context['post_list'] = Post.objects.filter(category__id__in=queried_category.all())

    return context


class CategoryView(ChannelView):
  def get_context_data(self, **kwargs):
    context = super(CategoryView, self).get_context_data(**kwargs)
    queried_category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
    context['post_list'] = Post.objects.filter(category=queried_category)
    context['category'] = queried_category
    return context

  # 侧边栏不出现“分类”


class TagView(ChannelView):
  def get_context_data(self, **kwargs):
    context = super(TagView, self).get_context_data(**kwargs)
    queried_tags = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
    context['post_list'] = Post.objects.filter(tags=queried_tags)
    return context

class PostDetailView(DetailView):
  model = Post
  template_name = 'blog/detail.html'
  context_object_name = 'post'

  def get(self, request, *args, **kwargs):
    response = super(PostDetailView, self).get(request, *args, **kwargs)
    self.object.increase_views()
    return response

  def get_context_data(self, **kwargs):
    # 将 channel listview 嵌入 post detailview，是导航栏正常显示
    # https://stackoverflow.com/questions/41287431/django-combine-detailview-and-listview
    context = super(PostDetailView, self).get_context_data(**kwargs)
    context['channel_list'] = Channel.objects.all()
    return context

  def get_object(self, queryset=None):
    post = super().get_object(queryset=None)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return post

class AboutView(ChannelView):
  template_name = 'blog/about.html'

