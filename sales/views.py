import json
import logging

import pandas as pd
from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import messages
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView

# from .utils import get_n_days_ago,create_clean_dir,change_col_format
from util.useful import get_n_days_ago
from .forms import FactoryCreateEditFrom, GoodsCreateEditFrom, CustomerCreateEditFrom, CustomerIndentCreateFrom, CustomerIndentEditFrom, \
    ProfileForm, FeedBackIndentCreateEditFrom, FactoryIndentCreateFrom, FactoryIndentEditFrom
from .groups_permissions import check_user_group, user_groups, SuperUserRequiredMixin, allowed_groups
from .models import FactoryModel, GoodsModel, CustomerModel, FactoryIndent, CustomerIndent, Profile, FeedBackIndent, UserActivity
from .notification import send_notification

logger = logging.getLogger(__name__)

TODAY = get_n_days_ago(0, "%Y%m%d")
PAGINATOR_NUMBER = 5
allowed_models = ['Category', 'Publisher', 'Book', 'Member', 'UserActivity', 'BorrowRecord']


# HomePage

class HomeView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "index.html"
    context = {}

    def get(self, request, *args, **kwargs):
        indent_count = CustomerIndent.objects.filter(status=0).count
        data_count = {"good": GoodsModel.objects.all().count(),
                      "customer": CustomerModel.objects.all().count(),
                      "factory": FactoryModel.objects.all().count(),
                      "indent": indent_count}

        self.context['data_count'] = data_count

        return render(request, self.template_name, self.context)


# Global Search
@login_required(login_url='login')
def global_search(request):
    search_value = request.POST.get('global_search')
    if search_value == '':
        return HttpResponseRedirect("/")

    r_factory = FactoryModel.objects.filter(Q(name__icontains=search_value))
    r_employees = Profile.objects.filter(Q(name__icontains=search_value) | Q(phone_number__icontains=search_value))
    r_good = GoodsModel.objects.filter(
        Q(name__icontains=search_value) | Q(factory__name__icontains=search_value) | Q(types__icontains=search_value))
    r_customer = CustomerModel.objects.filter(Q(name__icontains=search_value) | Q(phone__icontains=search_value))
    r_customer_indent = CustomerIndent.objects.filter(
        Q(customer__name__icontains=search_value) | Q(good__name__icontains=search_value) | Q(id__icontains=search_value) | Q(
            factory__name__icontains=search_value))

    context = {
        'factory': r_factory,
        'employees': r_employees,
        'good': r_good,
        'customer': r_customer,
        'customer_indent': r_customer_indent,
    }

    return render(request, 'sales/global_search.html', context=context)


# Goods
class GoodListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = GoodsModel
    context_object_name = 'goods'
    template_name = 'goods/goods_list.html'
    search_value = ""
    order_field = "-id"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")

        if order_by:
            all_books = GoodsModel.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_books = GoodsModel.objects.all().order_by(self.order_field)

        if search:
            all_books = all_books.filter(
                Q(name__icontains=search) | Q(author__icontains=search)
            )
            self.search_value = search
        self.count_total = all_books.count()
        paginator = Paginator(all_books, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        goods = paginator.get_page(page)
        return goods

    def get_context_data(self, *args, **kwargs):
        context = super(GoodListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        return context


class GoodDetailView(LoginRequiredMixin, DetailView):
    model = GoodsModel
    context_object_name = 'goods'
    template_name = 'goods/goods_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_goods_name = self.get_object().name
        logger.info(f'Goods <<{current_goods_name}>> retrieved from db')
        return context


class GoodCreateView(LoginRequiredMixin, CreateView):
    model = GoodsModel
    login_url = 'login'
    form_class = GoodsCreateEditFrom
    template_name = 'goods/goods_create.html'

    def get_form(self):
        form = super().get_form()
        return form

    def form_valid(self, form):
        selected_factory = FactoryModel.objects.get(name=form.cleaned_data['factory'])
        form.save()
        selected_factory.save()
        good_name = self.request.POST['name']

        messages.success(self.request, f" 'Create <<{good_name}>>")
        UserActivity.objects.create(created_by=self.request.user.username,
                                    target_model=self.model.__name__,
                                    detail=f" 'Create <<{good_name}>>")

        return super(GoodCreateView, self).form_valid(form)


class GoodUpdateView(LoginRequiredMixin, UpdateView):
    model = GoodsModel
    login_url = 'login'
    form_class = GoodsCreateEditFrom
    template_name = 'goods/goods_update.html'

    def post(self, request, *args, **kwargs):
        current_good = self.get_object()
        current_good.save()
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="warning",
                                    target_model=self.model.__name__,
                                    detail=f"Update {self.model.__name__} << {current_good.name} >>")
        return super(GoodUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        name = form.cleaned_data['name']
        messages.warning(self.request, f"Update << {name} >> success")
        return super().form_valid(form)


class GoodDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        good_pk = kwargs["pk"]
        delete_good = GoodsModel.objects.get(pk=good_pk)
        model_name = delete_good.__class__.__name__
        messages.error(request, f"Book << {delete_good.name} >> Removed")
        delete_good.delete()
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="danger",
                                    target_model=model_name,
                                    detail=f"Delete {model_name} << {delete_good.name} >>")
        return HttpResponseRedirect(reverse("book_list"))


# Factory

class FactoryListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = FactoryModel
    context_object_name = 'factory'
    template_name = 'goods/factory_list.html'
    count_total = 0
    search_value = ''
    order_field = "-name"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        if order_by:
            all_factories = FactoryModel.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_factories = FactoryModel.objects.all().order_by(self.order_field)
        if search:
            all_factories = all_factories.filter(
                Q(name__icontains=search) | Q(phone__icontains=search)
            )
            self.search_value = search

        self.count_total = all_factories.count()
        paginator = Paginator(all_factories, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        factories = paginator.get_page(page)
        return factories

    def get_context_data(self, *args, **kwargs):
        context = super(FactoryListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        return context


class FactoryCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = FactoryModel
    form_class = FactoryCreateEditFrom
    template_name = 'goods/factory_create.html'
    success_url = reverse_lazy('factory_list')

    def form_valid(self, form):
        new_fac = form.save(commit=False)
        new_fac.save()
        send_notification(self.request.user, new_fac, verb=f'Add New Factory << {new_fac.name} >>')
        logger.info(f'{self.request.user} created Factory {new_fac.name}')
        UserActivity.objects.create(created_by=self.request.user.username,
                                    target_model=self.model.__name__,
                                    detail=f"Create {self.model.__name__} << {new_fac.name} >>")
        return super(FactoryCreateView, self).form_valid(form)


class FactoryDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        fac_pk = kwargs["pk"]
        delete_fac = FactoryModel.objects.get(pk=fac_pk)
        model_name = delete_fac.__class__.__name__
        messages.error(request, f"Factory << {delete_fac.name} >> Removed")
        delete_fac.delete()
        send_notification(self.request.user, delete_fac, verb=f'Delete Category << {delete_fac.name} >>')
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="danger",
                                    target_model=model_name,
                                    detail=f"Delete {model_name} << {delete_fac.name} >>")

        logger.info(f'{self.request.user} delete Factory {delete_fac.name}')

        return HttpResponseRedirect(reverse("factory_list"))


class FactoryUpdateView(LoginRequiredMixin, UpdateView):
    model = FactoryModel
    login_url = 'login'
    form_class = FactoryCreateEditFrom
    template_name = 'goods/factory_update.html'

    def post(self, request, *args, **kwargs):
        current_factory = self.get_object()
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="warning",
                                    target_model=self.model.__name__,
                                    detail=f"Update {self.model.__name__} << {current_factory.name} >>")
        return super(FactoryUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        name = form.cleaned_data['name']
        messages.warning(self.request, f"Update << {name} >> success")
        return super().form_valid(form)


@method_decorator(allowed_groups(group_name=['logs']), name='dispatch')
class ActivityListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = UserActivity
    context_object_name = 'activities'
    template_name = 'goods/user_activity_list.html'
    count_total = 0
    search_value = ''
    created_by = ''
    order_field = "-created_at"
    all_users = User.objects.values()
    user_list = [x['username'] for x in all_users]

    # def dispatch(self, *args, **kwargs):
    #     return super(ActivityListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        data = self.request.GET.copy()
        search = self.request.GET.get("search")
        filter_user = self.request.GET.get("created_by")

        all_activities = UserActivity.objects.all()

        if filter_user:
            self.created_by = filter_user
            all_activities = all_activities.filter(created_by=self.created_by)

        if search:
            self.search_value = search
            all_activities = all_activities.filter(Q(target_model__icontains=search))

        self.search_value = search
        self.count_total = all_activities.count()
        paginator = Paginator(all_activities, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        try:
            response = paginator.get_page(page)
        except PageNotAnInteger:
            response = paginator.get_page(1)
        except EmptyPage:
            response = paginator.get_page(paginator.num_pages)
        return response

    def get_context_data(self, *args, **kwargs):
        context = super(ActivityListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['user_list'] = self.user_list
        context['created_by'] = self.created_by
        return context


@method_decorator(allowed_groups(group_name=['logs']), name='dispatch')
class ActivityDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        log_pk = kwargs["pk"]
        delete_log = UserActivity.objects.get(pk=log_pk)
        messages.error(request, f"Activity Removed")
        delete_log.delete()

        return HttpResponseRedirect(reverse("user_activity_list"))


# Customer
class CustomerListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = CustomerModel
    context_object_name = 'customer'
    template_name = 'goods/customer_list.html'
    count_total = 0
    search_value = ''
    order_field = "-id"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        if order_by:
            all_members = CustomerModel.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_members = CustomerModel.objects.all().order_by(self.order_field)
        if search:
            all_members = all_members.filter(
                Q(name__icontains=search) | Q(phone__icontains=search)
            )
        else:
            search = ''
        self.search_value = search
        self.count_total = all_members.count()
        paginator = Paginator(all_members, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        members = paginator.get_page(page)
        return members

    def get_context_data(self, *args, **kwargs):
        context = super(CustomerListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        return context


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = CustomerModel
    login_url = 'login'
    form_class = CustomerCreateEditFrom
    template_name = 'goods/customer_create.html'

    def post(self, request, *args, **kwargs):
        super(CustomerCreateView, self).post(request)
        new_customer_name = request.POST['name']
        messages.success(request, f"New Member << {new_customer_name} >> Added")
        UserActivity.objects.create(created_by=self.request.user.username,
                                    target_model=self.model.__name__,
                                    detail=f"Create {self.model.__name__} << {new_customer_name} >>")
        return redirect('customer_list')

    def form_valid(self, form):
        self.object = form.save()
        send_notification(self.request.user, self.object, f'Add new Customer {self.object.name}')

        return HttpResponseRedirect(self.get_success_url())


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomerModel
    login_url = 'login'
    form_class = CustomerCreateEditFrom
    template_name = 'goods/customer_update.html'

    def post(self, request, *args, **kwargs):
        current_customer = self.get_object()
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="warning",
                                    target_model=self.model.__name__,
                                    detail=f"Update {self.model.__name__} << {current_customer.name} >>")
        return super(CustomerUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        customer_name = form.cleaned_data['name']
        messages.warning(self.request, f"Update << {customer_name} >> success")
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        member_pk = kwargs["pk"]
        delete_customer = CustomerModel.objects.get(pk=member_pk)
        model_name = delete_customer.__class__.__name__
        messages.error(request, f"Member << {delete_customer.name} >> Removed")
        delete_customer.delete()
        send_notification(self.request.user, delete_customer, f'Delete member {delete_customer.name} ')

        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="danger",
                                    target_model=model_name,
                                    detail=f"Delete {model_name} << {delete_customer.name} >>")
        return HttpResponseRedirect(reverse("customer_list"))


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = CustomerModel
    context_object_name = 'customer'
    template_name = 'goods/customer_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_customer_name = self.get_object().name
        related_records = CustomerIndent.objects.filter(customer=current_customer_name)
        context['related_records'] = related_records
        return context


# Customer Indent Records

class CustomerIndentCreateView(LoginRequiredMixin, CreateView):
    model = CustomerIndent
    template_name = 'indent_records/create.html'
    form_class = CustomerIndentCreateFrom
    login_url = 'login'
    context_object_name = 'customer-indent-create'

    def get_form(self):
        form = super().get_form()
        return form

    def form_valid(self, form):
        selected_customer = get_object_or_404(CustomerModel, name=form.cleaned_data['customer'])
        selected_good = GoodsModel.objects.get(name=form.cleaned_data['good'])

        price = selected_good.price
        vip_level = selected_customer.vip_level
        if vip_level == 4:
            price = price * 0.8
        elif vip_level == 3:
            price = price * 0.85
        elif vip_level == 2:
            price = price * 0.9
        elif vip_level == 1:
            price = price * 0.95
        else:
            price = price

        form.instance.customer = selected_customer.name
        form.instance.good = selected_good.name
        form.instance.employees = self.request.user.username
        form.instance.number = form.cleaned_data['number']
        form.instance.income = price * form.instance.number
        form.instance.status = 0
        form.instance.track_num = form.cleaned_data['track_num']
        form.save()

        # Create Log
        customer_name = selected_customer.name
        good_name = selected_good.name

        messages.success(self.request, f" '为 {customer_name}' 提交 <<{good_name}>> 的订单成功")
        UserActivity.objects.create(created_by=self.request.user.username,
                                    target_model=self.model.__name__,
                                    detail=f" '{customer_name}' buy <<{good_name}>>")

        return super(CustomerIndentCreateView, self).form_valid(form)


@login_required(login_url='login')
def auto_customer(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        member_names = CustomerModel.objects.filter(name__icontains=query)
        results = []
        for m in member_names:
            results.append(m.name)
        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


@login_required(login_url='login')
def auto_good(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        good_names = GoodsModel.objects.filter(name__icontains=query)
        results = [g.name for g in good_names]
        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


@login_required(login_url='login')
def auto_factory(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        factory_name = FactoryModel.objects.filter(name__icontains=query)
        results = [f.name for f in factory_name]
        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


@login_required(login_url='login')
def auto_employees(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        employees_name = Profile.objects.filter(name__icontains=query)
        results = [e.name for e in employees_name]
        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


@login_required(login_url='login')
def auto_indent(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        indent_num = CustomerIndent.objects.filter(id__icontains=query)
        results = [i.id for i in indent_num]
        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


class CustomerIndentDetailView(LoginRequiredMixin, DetailView):
    model = CustomerIndent
    context_object_name = 'indent'
    template_name = 'indent_records/detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(CustomerIndentDetailView, self).get_context_data(**kwargs)
        related_customer = CustomerModel.objects.get(name=self.get_object().name)
        context['related_customer'] = related_customer
        return context


class CustomerIndentListView(LoginRequiredMixin, ListView):
    model = CustomerIndent
    template_name = 'indent_records/list.html'
    login_url = 'login'
    context_object_name = 'indent'
    count_total = 0
    search_value = ''
    order_field = "-id"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        if order_by:
            all_records = CustomerIndent.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_records = CustomerIndent.objects.all().order_by(self.order_field)
        if search:
            all_records = CustomerIndent.objects.filter(
                Q(customer__icontains=search) | Q(good__icontains=search)
            )
        else:
            search = ''
        self.search_value = search
        self.count_total = all_records.count()
        paginator = Paginator(all_records, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        records = paginator.get_page(page)
        return records

    def get_context_data(self, *args, **kwargs):
        context = super(CustomerIndentListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        return context


class CustomerIndentDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        record_pk = kwargs["pk"]
        delete_record = CustomerIndent.objects.get(pk=record_pk)
        model_name = delete_record.__class__.__name__
        messages.error(request, f"删除订单 {delete_record.id} 成功")
        delete_record.delete()
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="danger",
                                    target_model=model_name,
                                    detail=f"Delete {model_name} {delete_record.customer}")
        return HttpResponseRedirect(reverse("customer_indent_list"))


class CustomerIndentUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomerIndent
    login_url = 'login'
    form_class = CustomerIndentEditFrom
    template_name = 'indent_records/update.html'

    def post(self, request, *args, **kwargs):
        current_ci = self.get_object()
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="warning",
                                    detail=f"<< {current_ci.id} >>已更新")
        return super(CustomerIndentUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        current_ci = self.get_object()
        messages.warning(self.request, f"更新订单 << {current_ci.id} >> 成功")
        return super().form_valid(form)


# Factory Indent Records

class FactoryIndentCreateView(LoginRequiredMixin, CreateView):
    model = FactoryIndent
    template_name = 'indent_records/fac-create.html'
    form_class = FactoryIndentCreateFrom
    login_url = 'login'

    def get_form(self):
        form = super().get_form()
        return form

    def form_valid(self, form):
        selected_good = GoodsModel.objects.get(name=form.cleaned_data['good'])
        selected_factory = FactoryModel.objects.get(name=form.cleaned_data['factory'])

        form.instance.good = selected_good.name
        form.instance.employees = self.request.user.username
        form.instance.factory = selected_factory.name
        form.instance.numbers = form.cleaned_data['numbers']
        form.instance.payment_id = form.cleaned_data['payment_id']
        form.instance.status = 0
        form.save()

        # Create Log
        factory_name = selected_factory.name
        good_name = selected_good.name

        messages.success(self.request, f" '<< {good_name} >>' submit to {factory_name} ")
        UserActivity.objects.create(created_by=self.request.user.username,
                                    target_model=self.model.__name__,
                                    detail=f" ' '<< {good_name} >>' submit to {factory_name} ")

        return super(FactoryIndentCreateView, self).form_valid(form)


class FactoryIndentDetailView(LoginRequiredMixin, DetailView):
    model = FactoryIndent
    context_object_name = 'indent_fac'
    template_name = 'indent_records/fac-detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(FactoryIndentDetailView, self).get_context_data(**kwargs)
        related_member = FactoryModel.objects.get(name=self.get_object().name)
        context['related_member'] = related_member
        return context


class FactoryIndentListView(LoginRequiredMixin, ListView):
    model = FactoryIndent
    template_name = 'indent_records/fac-list.html'
    login_url = 'login'
    context_object_name = 'indent_fac'
    count_total = 0
    search_value = ''
    order_field = "-id"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        if order_by:
            all_records = FactoryIndent.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_records = FactoryIndent.objects.all().order_by(self.order_field)
        if search:
            all_records = FactoryIndent.objects.filter(
                Q(factory__icontains=search) | Q(good__icontains=search)
            )
        else:
            search = ''
        self.search_value = search
        self.count_total = all_records.count()
        paginator = Paginator(all_records, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        records = paginator.get_page(page)
        return records

    def get_context_data(self, *args, **kwargs):
        context = super(FactoryIndentListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        return context


class FactoryIndentDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        record_pk = kwargs["pk"]
        delete_record = FactoryIndent.objects.get(pk=record_pk)
        model_name = delete_record.__class__.__name__
        messages.error(request, f"Record {delete_record.borrower} => {delete_record.book} Removed")
        delete_record.delete()
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="danger",
                                    target_model=model_name,
                                    detail=f"Delete {model_name} {delete_record.borrower}")
        return HttpResponseRedirect(reverse("record_list_fac"))


class FactoryIndentUpdateView(LoginRequiredMixin, UpdateView):
    model = FactoryIndent
    login_url = 'login'
    form_class = FactoryIndentEditFrom
    template_name = 'indent_records/fac-update.html'

    def post(self, request, *args, **kwargs):
        current_ci = self.get_object()
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="warning",
                                    detail=f"订单 << {current_ci.id} >> 已更新")
        return super(FactoryIndentUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        current_ci = self.get_object()
        messages.warning(self.request, f"Update << {current_ci.id} >> success")
        return super().form_valid(form)


# FeedBack Indent Records

class FeedBackIndentCreateView(LoginRequiredMixin, CreateView):
    model = FeedBackIndent
    template_name = 'indent_records/fed-create.html'
    form_class = FeedBackIndentCreateEditFrom
    login_url = 'login'

    def get_form(self):
        form = super().get_form()
        return form

    def form_valid(self, form):
        form.instance.good = form.cleaned_data['customer_indent']
        form.instance.employees = self.request.user.username
        form.instance.text = form.cleaned_data['text']
        form.instance.status = 0
        form.save()

        # Create Log
        employees = self.request.user.username

        messages.success(self.request, f" '<< {employees} >>' submit  ")
        UserActivity.objects.create(created_by=self.request.user.username,
                                    target_model=self.model.__name__,
                                    detail=f" ' '<< {employees} >>' submit  ")

        return super(FeedBackIndentCreateView, self).form_valid(form)


class FeedBackIndentDetailView(LoginRequiredMixin, DetailView):
    model = FeedBackIndent
    context_object_name = 'indent_fed'
    template_name = 'indent_records/fed-detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(FeedBackIndentDetailView, self).get_context_data(**kwargs)
        related_id = FeedBackIndent.objects.get(name=self.get_object().id)
        context['related_id'] = related_id
        return context


class FeedBackIndentListView(LoginRequiredMixin, ListView):
    model = FeedBackIndent
    template_name = 'indent_records/fed-list.html'
    login_url = 'login'
    context_object_name = 'indent_fed'
    count_total = 0
    search_value = ''
    order_field = "-id"

    def get_queryset(self):
        search = self.request.GET.get("search")
        order_by = self.request.GET.get("orderby")
        if order_by:
            all_records = FeedBackIndent.objects.all().order_by(order_by)
            self.order_field = order_by
        else:
            all_records = FeedBackIndent.objects.all().order_by(self.order_field)
        if search:
            all_records = FeedBackIndent.objects.filter(
                Q(customer_indent__id__icontains=search) | Q(status__icontains=search)
            )
        else:
            search = ''
        self.search_value = search
        self.count_total = all_records.count()
        paginator = Paginator(all_records, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        records = paginator.get_page(page)
        return records

    def get_context_data(self, *args, **kwargs):
        context = super(FeedBackIndentListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['objects'] = self.get_queryset()
        return context


class FeedBackIndentDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        record_pk = kwargs["pk"]
        delete_record = FeedBackIndent.objects.get(pk=record_pk)
        model_name = delete_record.__class__.__name__
        messages.error(request, f"Record {delete_record.borrower} => {delete_record.book} Removed")
        delete_record.delete()
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="danger",
                                    target_model=model_name,
                                    detail=f"Delete {model_name} {delete_record.borrower}")
        return HttpResponseRedirect(reverse("feedback_indent_list"))


class FeedBackIndentUpdateView(LoginRequiredMixin, UpdateView):
    model = FeedBackIndent
    login_url = 'login'
    form_class = FeedBackIndentCreateEditFrom
    template_name = 'indent_records/fed-update.html'

    def post(self, request, *args, **kwargs):
        current_ci = self.get_object()
        UserActivity.objects.create(created_by=self.request.user.username,
                                    operation_type="warning",
                                    detail=f"<< {current_ci.id} >>已更新")
        return super(FeedBackIndentUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        name = form.cleaned_data['name']
        messages.warning(self.request, f"Update << {name} >> success")
        return super().form_valid(form)


# Data center
@method_decorator(allowed_groups(group_name=['download_data']), name='dispatch')
class DataCenterView(LoginRequiredMixin, TemplateView):
    template_name = 'goods/download_data.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        # check_user_group(request.user,"download_data")
        data = {m.objects.model._meta.db_table:
                    {"source": pd.DataFrame(list(m.objects.all().values())),
                     "path": f"{str(settings.BASE_DIR)}/datacenter/{m.__name__}_{TODAY}.csv",
                     "file_name": f"{m.__name__}_{TODAY}.csv"} for m in apps.get_models() if m.__name__ in allowed_models}

        count_total = {k: v['source'].shape[0] for k, v in data.items()}
        return render(request, self.template_name, context={'model_list': count_total})


@login_required(login_url='login')
@allowed_groups(group_name=['download_data'])
def download_data(request, model_name):
    check_user_group(request.user, "download_data")

    download = {m.objects.model._meta.db_table:
                    {"source": pd.DataFrame(list(m.objects.all().values())),
                     "path": f"{str(settings.BASE_DIR)}/datacenter/{m.__name__}_{TODAY}.csv",
                     "file_name": f"{m.__name__}_{TODAY}.csv"} for m in apps.get_models() if m.__name__ in allowed_models}

    download[model_name]['source'].to_csv(download[model_name]['path'], index=False, encoding='utf-8')
    download_file = pd.read_csv(download[model_name]['path'], encoding='utf-8')
    response = HttpResponse(download_file, content_type="text/csv")
    response = HttpResponse(open(download[model_name]['path'], 'r', encoding='utf-8'), content_type="text/csv")
    response['Content-Disposition'] = f"attachment;filename={download[model_name]['file_name']}"
    return response


# Handle Errors

def page_not_found(request, exception):
    context = {}
    response = render(request, "errors/404.html", context=context)
    response.status_code = 404
    return response


def server_error(request, exception=None):
    context = {}
    response = render(request, "errors/500.html", context=context)
    response.status_code = 500
    return response


def permission_denied(request, exception=None):
    context = {}
    response = render(request, "errors/403.html", context=context)
    response.status_code = 403
    return response


def bad_request(request, exception=None):
    context = {}
    response = render(request, "errors/400.html", context=context)
    response.status_code = 400
    return response


# Employees
# @method_decorator(user_passes_test(lambda u: check_superuser(u)), name='dispatch')
class EmployeeView(SuperUserRequiredMixin, ListView):
    login_url = 'login'
    model = User
    context_object_name = 'employees'
    template_name = 'goods/employees.html'

    # def get(self, request):
    #     # check_superuser(request.user)
    #     return super(EmployeeView, self).get(self,request)


# @method_decorator(user_passes_test(lambda u: check_superuser(u)), name='dispatch')
class EmployeeDetailView(SuperUserRequiredMixin, DetailView):
    model = User
    context_object_name = 'employee'
    template_name = 'goods/employee_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = user_groups
        return context


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def EmployeeUpdate(request, pk):
    current_user = User.objects.get(pk=pk)
    if request.method == 'POST':
        chosen_groups = [g for g in user_groups if "on" in request.POST.getlist(g)]
        current_user.groups.clear()
        for each in chosen_groups:
            group = Group.objects.get(name=each)
            current_user.groups.add(group)
        messages.success(request, f"Group for  << {current_user.username} >> has been updated")
        return redirect('employees_detail', pk=pk)


# Notice

class NoticeListView(SuperUserRequiredMixin, ListView):
    context_object_name = 'notices'
    template_name = 'notice_list.html'
    login_url = 'login'

    # 未读通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.unread()


class NoticeUpdateView(SuperUserRequiredMixin, View):
    """Update Status of Notification"""

    # 处理 get 请求
    def get(self, request):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        # 更新单条通知
        if notice_id:
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect('factory_list')
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice_list')


# Profile View

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile/profile_detail.html'
    login_url = 'login'

    def get_context_data(self, *args, **kwargs):
        current_user = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        context['current_user'] = current_user
        return context


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = 'profile/profile_create.html'
    login_url = 'login'
    form_class = ProfileForm

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.name_id = self.request.user.id
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    login_url = 'login'
    form_class = ProfileForm
    template_name = 'profile/profile_update.html'
