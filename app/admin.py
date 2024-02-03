from django.contrib import admin
from .models import Product, Category, BlogPost, Testimonial,OrderItem,Order





class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_total_quantity', 'get_total_price', 'created_at']
    inlines = [OrderItemInline]

    def get_total_quantity(self, obj):
        return obj.total_quantity()

    def get_total_price(self, obj):
        return obj.total_price()

    get_total_quantity.short_description = 'Total Quantity'
    get_total_price.short_description = 'Total Price'

admin.site.register(Order, OrderAdmin)





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