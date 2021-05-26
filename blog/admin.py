from django.contrib import admin
from .models import Channel, Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
  list_display = ['title', 'created_time', 'modified_time', 'category', 'avatar', 'author', 'elapsed_time']
  fields = ['title', 'body', 'excerpt', 'category', 'tags', 'avatar', 'elapsed_time']

  def save_model(self, request, obj, form, change):
    obj.author = request.user
    super().save_model(request, obj, form, change)

class CategoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'channel']
  fields = ['name', 'channel']

  def save_model(self, request, obj, form, change):
    obj.author = request.user
    super().save_model(request, obj, form, change)

class ChannelAdmin(admin.ModelAdmin):
  list_display = ['name', 'desc']
  fields = ['name', 'desc']

  def save_model(self, request, obj, form, change):
    obj.author = request.user
    super().save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
