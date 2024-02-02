from django.contrib import admin
from .models import Smartphone, Smartwatch,BlogPost,Testimonial

admin.site.register(Smartphone)
admin.site.register(Smartwatch)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published', 'category', 'author')
    search_fields = ('title', 'category', 'author__username')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('quote', 'rating', 'author_name')    