from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from PIL import Image
import markdown

class Channel(models.Model):
  CHANNEL_CHOICES = (
    ('SaaS', 'SaaS'),
    ('Insights', '洞察'),
    ('Resources', '资源'),
  )

  # name = models.CharField(max_length=20, default='Your channel name here.')
  # https://www.liujiangblog.com/course/django/104
  name = models.CharField(max_length=32, choices=CHANNEL_CHOICES, default='洞察')
  desc = models.CharField(max_length=200, default='Your channel description here.')

  class Meta:
    verbose_name = '版块'
    verbose_name_plural = verbose_name

  def __str__(self):
    return self.name

class Category(models.Model):
  name = models.CharField(max_length=32, unique=True)
  channel = models.ForeignKey(Channel, verbose_name='版块', on_delete=models.CASCADE, default='insights')

  class Meta:
    verbose_name = '类别'
    verbose_name_plural = verbose_name

  def __str__(self):
    return self.name

class Tag(models.Model):
  name = models.CharField(max_length=20, unique=True)

  class Meta:
    verbose_name = '标签'
    verbose_name_plural = verbose_name

  def __str__(self):
    return self.name

class Post(models.Model):
  title = models.CharField('标题', max_length=70)
  subtitle = models.CharField('副标题', max_length=70, blank=True)
  body = models.TextField('正文')
  created_time = models.DateTimeField('创建时间', auto_now_add=True)
  modified_time = models.DateTimeField('修改时间', auto_now=True)
  elapsed_time = models.IntegerField('阅读时长', default=5, blank=True)

  # 使用图床显示标题图
  avatar = models.URLField('标题图', max_length=400, blank=True)

  # 可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
  excerpt = models.CharField('摘要', max_length=300, blank=True)

  # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章
  category = models.ForeignKey(Category, verbose_name='类别', on_delete=models.CASCADE, blank=False)

  # 对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章
  tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

  # 我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章
  # 这里 User 是从 django.contrib.auth.models 导入的
  author = models.ForeignKey(User, default='Grit', verbose_name='作者', on_delete=models.CASCADE)

  # 记录阅读量
  views = models.PositiveIntegerField(default=0, editable=False)

  class Meta:
    verbose_name = '文章'
    verbose_name_plural = verbose_name
    ordering = ['-created_time']

  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse("blog:post_detail", kwargs={"pk": self.pk})
  
  def save(self, *args, **kwargs):
    self.modified_time = timezone.now()

    # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
    # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
    ])

    # 先将 Markdown 文本渲染成 HTML 文本
    # strip_tags 去掉 HTML 文本的全部 HTML 标签
    # 从文本摘取前 54 个字符赋给 excerpt
    self.excerpt = strip_tags(md.convert(self.body))[:200]

    super().save(*args, **kwargs)

  def increase_views(self):
    self.views += 1
    self.save(update_fields=['views'])
