from django.contrib import admin
from .models import Product, Category, BlogPost, Testimonial,OrderItem,Order,CartItem





admin.site.register(CartItem)






@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)



@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published', 'category', 'author')
    search_fields = ('title', 'category', 'author__username')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('quote', 'rating', 'author_name')    