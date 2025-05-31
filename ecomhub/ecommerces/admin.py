from django.contrib import admin
from django.db.models import Sum

from .models import Product, ProductImage, Shop, Inventory, Cart, CartDetail, Order, OrderDetail, Payment, Category, Comment, CommentLike
from datetime import datetime

# Register your models here.

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    inlines = [ProductInline, ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ['image']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'shop']
    search_fields = ['name', 'price']
    list_filter = ['price']
    inlines = [ProductImageInline, ]


class InventoryAdmin(admin.ModelAdmin):
    list_display = ['quantity', 'product']
    list_filter = ['quantity']


class CartDetailInline(admin.TabularInline):
    model = CartDetail


class CartAdmin(admin.ModelAdmin):
    list_display = ['total', 'user']
    inlines = [CartDetailInline, ]


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total', 'shipping_address']
    inlines = [OrderDetailInline, PaymentInline]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_method', 'total', 'status']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'star', 'content', 'image', 'comment_parent']


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment']


class ShopStatsAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'user', 'total_products', 'products_this_year', 'products_this_quarter']

    def total_products(self, obj):
        return obj.products.count()
    total_products.short_description = 'Tổng sản phẩm'

    def products_this_year(self, obj):
        year = datetime.now().year
        return obj.products.filter(created_date__year=year).count()
    products_this_year.short_description = 'Sản phẩm năm nay'

    def products_this_quarter(self, obj):
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        return obj.products.filter(
            created_date__year=now.year,
            created_date__month__in=[(quarter - 1) * 3 + 1, (quarter - 1) * 3 + 2, (quarter - 1) * 3 + 3]
        ).count()
    products_this_quarter.short_description = 'Sản phẩm quý này'


class ProductStatsAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'shop', 'price', 'quantity_sold']

    def quantity_sold(self, obj):
        result = obj.orderdetails.aggregate(total_sold=Sum('quantity'))['total_sold']
        return result if result else 0
    quantity_sold.short_description = 'Đã bán'


# admin.site.register(Shop, ShopAdmin)
# admin.site.register(Product, ProductAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
admin.site.register(Shop, ShopStatsAdmin)
admin.site.register(Product, ProductStatsAdmin)
admin.site.site_header = "EcomSale Admin"