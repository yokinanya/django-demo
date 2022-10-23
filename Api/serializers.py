from django.contrib.auth.models import User, Group
from rest_framework import serializers

from sales.models import CustomerModel, FactoryModel, GoodsModel, CustomerIndent, FeedBackIndent, FactoryIndent


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


# Factory Serializer


class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FactoryModel
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(FactorySerializer, self).to_representation(instance)
        return representation


# Good Serializer
class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsModel
        fields = (
            'name',
            'price',
            'factory',
            'types',
            'brand',
            'specs',
            'color'
        )

    def to_representation(self, instance):
        representation = super(GoodSerializer, self).to_representation(instance)

        return representation


# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = (
            'name',
            'sex',
            'phone',
            'birthdate',
            'address',
            'vip_level'
        )

    def to_representation(self, instance):
        representation = super(CustomerSerializer, self).to_representation(instance)

        return representation


# Indent Serializer
class CustomerIndentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerIndent
        fields = (
            'customer',
            'good',
            'employees',
            'factory',
            'number',
            'track_num',
            'income',
            'status'
        )

    def to_representation(self, instance):
        representation = super(CustomerIndentSerializer, self).to_representation(instance)
        representation['created'] = instance.created_at.strftime("%Y/%m/%d")
        return representation


class FactoryIndentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactoryIndent
        fields = (
            'good',
            'employees',
            'factory',
            'payment_id',
            'numbers',
            'status'
        )

    def to_representation(self, instance):
        representation = super(FactoryIndentSerializer, self).to_representation(instance)
        representation['created'] = instance.created_at.strftime("%Y/%m/%d")
        return representation


class FeedBackIndentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBackIndent
        fields = (
            'customer_indent',
            'employees',
            'text',
            'status'
        )

        def to_representation(self, instance):
            representation = super(FeedBackIndentSerializer, self).to_representation(instance)
            representation['created'] = instance.created_at.strftime("%Y/%m/%d")
            return representation
