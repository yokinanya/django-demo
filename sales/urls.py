from django.urls import path  # add this

from .views import ActivityListView, ActivityDeleteView, FactoryIndentCreateView, FactoryIndentListView, FactoryIndentDeleteView, \
    FeedBackIndentCreateView, FeedBackIndentListView, FeedBackIndentDeleteView, auto_employees, \
    auto_factory, CustomerIndentUpdateView, FactoryIndentUpdateView, FeedBackIndentUpdateView, auto_indent
from .views import CustomerIndentListView, CustomerIndentDeleteView, CustomerIndentCreateView, auto_customer, auto_good
from .views import CustomerListView, CustomerCreateView, CustomerDeleteView, CustomerUpdateView, CustomerDetailView
from .views import DataCenterView, download_data
from .views import EmployeeView, EmployeeDetailView, EmployeeUpdate
from .views import FactoryListView, FactoryCreateView, FactoryDeleteView, FactoryUpdateView
from .views import GoodListView, GoodUpdateView, GoodDetailView, GoodCreateView, GoodDeleteView
from .views import HomeView
from .views import NoticeListView, NoticeUpdateView
from .views import ProfileCreateView, ProfileDetailView, ProfileUpdateView
from .views import global_search

urlpatterns = [

    # HomePage
    path("", HomeView.as_view(), name='home'),
    # good
    path('good-list', GoodListView.as_view(), name="good_list"),
    path('good-create', GoodCreateView.as_view(), name="good_create"),
    path('good-update/<int:pk>/', GoodUpdateView.as_view(), name="good_update"),
    path('good-delete/<int:pk>/', GoodDeleteView.as_view(), name="good_delete"),
    path('good-detail/<int:pk>/', GoodDetailView.as_view(), name="good_detail"),

    # Factory
    path('factory-list', FactoryListView.as_view(), name="factory_list"),
    path('factory-create', FactoryCreateView.as_view(), name="factory_create"),
    path('factory-update/<int:pk>/', FactoryUpdateView.as_view(), name="factory_update"),
    path('factory-delete/<int:pk>/', FactoryDeleteView.as_view(), name="factory_delete"),

    # User Activity
    path('user-activity-list', ActivityListView.as_view(), name="user_activity_list"),
    path('user-activity-list/<int:pk>/', ActivityDeleteView.as_view(), name="user_activity_delete"),

    # Customer
    path('customer-list', CustomerListView.as_view(), name="customer_list"),
    path('customer-create', CustomerCreateView.as_view(), name="customer_create"),
    path('customer-delete/<int:pk>/', CustomerDeleteView.as_view(), name="customer_delete"),
    path('customer-update/<int:pk>/', CustomerUpdateView.as_view(), name="customer_update"),
    path('customer-detail/<int:pk>/', CustomerDetailView.as_view(), name="customer_detail"),

    # AutoComplete
    path('create-autocomplete-customer-name/', auto_customer, name="auto_customer_name"),
    path('create-autocomplete-good-name/', auto_good, name="auto_good_name"),
    path('create-autocomplete-employees-name/', auto_employees, name="auto_employees_name"),
    path('create-autocomplete-factory-name/', auto_factory, name="auto_factory_name"),
    path('create-autocomplete-indent-id/', auto_indent, name="auto_indent_id"),

    # Customer Indent CreateView
    path('customer-indent-create/', CustomerIndentCreateView.as_view(), name="customer_indent_create"),
    path('customer-indent-list/', CustomerIndentListView.as_view(), name="customer_indent_list"),
    path('customer-indent-update/<int:pk>/', CustomerIndentUpdateView.as_view(), name="customer_indent_update"),
    path('customer-indent-delete/<int:pk>/', CustomerIndentDeleteView.as_view(), name="customer_indent_delete"),

    # Factory Indent CreateView
    path('factory-indent-create/', FactoryIndentCreateView.as_view(), name="record_create_fac"),
    path('factory-indent-list/', FactoryIndentListView.as_view(), name="record_list_fac"),
    path('factory-indent-update/<int:pk>/', FactoryIndentUpdateView.as_view(), name="record_update_fac"),
    path('factory-indent-delete/<int:pk>/', FactoryIndentDeleteView.as_view(), name="record_delete_fac"),

    # Feedback Indent CreateView
    path('feedback-indent-create/', FeedBackIndentCreateView.as_view(), name="record_create_fed"),
    path('feedback-indent-list/', FeedBackIndentListView.as_view(), name="record_list_fed"),
    path('feedback-indent-update/<int:pk>/', FeedBackIndentUpdateView.as_view(), name="record_update_fed"),
    path('feedback-indent-delete/<int:pk>/', FeedBackIndentDeleteView.as_view(), name="record_delete_fed"),

    # Data center
    path('data-center/', DataCenterView.as_view(), name="data_center"),
    path('data-download/<str:model_name>/', download_data, name="data_download"),

    # Global Search
    path('global-search/', global_search, name="global_search"),

    # UserProfile
    path('user/profile-create/', ProfileCreateView.as_view(), name="profile_create"),
    path('user/<int:pk>/profile/', ProfileDetailView.as_view(), name="profile_detail"),
    path('user/<int:pk>/profile-update/', ProfileUpdateView.as_view(), name="profile_update"),

    # Employee
    path('employees/', EmployeeView.as_view(), name="employees_list"),
    path('employees-detail/<int:pk>', EmployeeDetailView.as_view(), name="employees_detail"),
    path('employees-update/<int:pk>', EmployeeUpdate, name='employee_update'),

    # Notice
    path('notice-list/', NoticeListView.as_view(), name='notice_list'),
    path('notice-update/', NoticeUpdateView.as_view(), name='notice_update'),
]
