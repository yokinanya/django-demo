from django.urls import include, path
from rest_framework import routers
from Api import views
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [

    #Home
    path('', views.apiOverview, name="api-overview"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Category API
    path('factory-list/', views.FactoryList, name="api_factory_list"),
    path('factory-create/', views.FactoryCreate, name="api_factory_create"),
    path('factory-detail/<int:pk>/', views.FactoryDetail, name="api_factory_detail"),
    path('factory-delete/<int:pk>/', views.FactoryDelete, name="api_factory_delete"),

    # Good API
    path('good-list/', views.GoodList, name="api_good_list"),
    path('good-create/', views.GoodCreate, name="api_good_create"),
    path('good-detail/<int:pk>/', views.GoodDetail, name="api_good_detail"),
    path('good-update/<int:pk>/', views.GoodUpdate, name="api_good_update"),
    path('good-delete/<int:pk>/', views.GoodDelete, name="api_good_delete"),


    # Customer API
    path('customer/', views.CustomerList.as_view()),
    path('customer/<int:pk>', views.CustomerDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
