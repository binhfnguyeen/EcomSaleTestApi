from django.template.defaulttags import comment
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from unicodedata import category

from .models import Category, Product, Inventory, ProductImage, Shop, Cart, CartDetail, Comment, Order, \
    OrderDetail, Payment, User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'is_shop_owner', 'avatar', 'phone','is_superuser','is_approved']

        extra_kwargs = {
            'is_superuser': {
                'read_only': True
            },
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u

    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar')

        if isinstance(avatar, str):
            instance.avatar = avatar
        elif avatar:
            instance.avatar = avatar

        instance.save()
        return instance


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name','user']


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image','product']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = instance.image.url
        return data


class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'shop', 'category', 'price', 'images']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['shop'] = {
            'id': instance.shop.id,
            'name': instance.shop.name,
            'user': {
                'id': instance.shop.user.id,
                'username': instance.shop.user.username,
                'first_name': instance.shop.user.first_name,
                'last_name': instance.shop.user.last_name
            }
        }
        representation['category'] = instance.category.__str__()
        return representation



class CommentSerializer(ModelSerializer):
    like_count = serializers.SerializerMethodField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(instance.user).data
        return data

    def get_like_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'star', 'content', 'image', 'comment_parent', 'product', 'like_count']

        extra_kwargs = {
            'product': {
                'write_only': True
            }
        }

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_method', 'total', 'status', 'order']


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'active', 'user', 'total', 'shipping_address', 'phone', 'status']


class OrderDetailWithProductSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        fields = ['id', 'product', 'quantity']


class CartDetailSerializer(ModelSerializer):
    class Meta:
        model = CartDetail
        fields = ['id', 'quantity', 'product', 'cart']


class CartSerializer(ModelSerializer):
    details = CartDetailSerializer(many=True, read_only=True)  # Error here without read_only or source

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total', 'details']
