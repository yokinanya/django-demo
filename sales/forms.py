from django import forms
from flatpickr import DatePickerInput

from .models import FactoryModel, GoodsModel, CustomerModel, FactoryIndent, CustomerIndent, FeedBackIndent, Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('namex',
                  'sex',
                  'phone_number',
                  'base_pay',
                  'job'
                  )


class UserCreateEditFrom(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name',
            'sex',
            'phone_number',
            'base_pay',
            'job'
        )


class FactoryCreateEditFrom(forms.ModelForm):
    class Meta:
        model = FactoryModel
        fields = (
            'name',
            'address',
            'phone'
        )


class GoodsCreateEditFrom(forms.ModelForm):
    factory = forms.CharField(label='工厂名', widget=forms.TextInput(attrs={'placeholder': 'Search Factory...'}))

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


class CustomerCreateEditFrom(forms.ModelForm):
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
        widgets = {
            'birthdate': DatePickerInput(options={"dateFormat": "Y-m-d", }),
        }


class CustomerIndentCreateFrom(forms.ModelForm):
    customer = forms.CharField(label='客户姓名', widget=forms.TextInput(attrs={'placeholder': 'Search Customer...'}))
    good = forms.CharField(label='商品名', widget=forms.TextInput(attrs={'placeholder': 'Search Goods...'}))

    class Meta:
        model = CustomerIndent
        fields = (
            'customer',
            'good',
            'number',
            'track_num',
        )


class CustomerIndentEditFrom(forms.ModelForm):
    customer = forms.CharField(label='客户姓名', widget=forms.TextInput(attrs={'placeholder': 'Search Customer...'}))
    good = forms.CharField(label='商品名', widget=forms.TextInput(attrs={'placeholder': 'Search Goods...'}))

    class Meta:
        model = CustomerIndent
        fields = (
            'customer',
            'good',
            'number',
            'track_num',
            'status'
        )


class FactoryIndentCreateFrom(forms.ModelForm):
    good = forms.CharField(label='商品名', widget=forms.TextInput(attrs={'placeholder': 'Search Goods...'}))
    factory = forms.CharField(label='工厂名', widget=forms.TextInput(attrs={'placeholder': 'Search Factory...'}))

    class Meta:
        model = FactoryIndent
        fields = (
            'good',
            'factory',
            'payment_id',
            'numbers',
        )


class FactoryIndentEditFrom(forms.ModelForm):
    good = forms.CharField(label='商品名', widget=forms.TextInput(attrs={'placeholder': 'Search Goods...'}))
    factory = forms.CharField(label='工厂名', widget=forms.TextInput(attrs={'placeholder': 'Search Factory...'}))

    class Meta:
        model = FactoryIndent
        fields = (
            'good',
            'factory',
            'payment_id',
            'numbers',
            'status'
        )


class FeedBackIndentCreateEditFrom(forms.ModelForm):
    # customer_indent = forms.CharField(label='客户订单编号', widget=forms.TextInput(attrs={'placeholder': 'Search Customer Indent...'}))

    class Meta:
        model = FeedBackIndent
        fields = (
            'customer_indent',
            # 'employees',
            'text',
            'status'
        )
