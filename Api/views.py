# Create your views here.
from django.http import Http404
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView, status

from sales.groups_permissions import check_user_group
from sales.models import CustomerModel, FactoryModel, GoodsModel, FactoryIndent, FeedBackIndent, CustomerIndent
from .permissions import IsOwnerOrReadOnly
from .serializers import CustomerSerializer, FactorySerializer, GoodSerializer, FactoryIndentSerializer, FeedBackIndentSerializer, \
    CustomerIndentSerializer


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def apiOverview(request):
    check_user_group(request.user, 'api')
    api_urls = {
        'Customer Indent List': '/customer-indent-list/',
        'Customer Indent Create': '/customer-indent-create/',
        'Customer Indent Delete': '/customer-indent-delete/<int:pk>/',
        'Customer Indent Update': '/customer-indent-update/<int:pk>/',
        'Factory Indent List': '/factory-indent-list/',
        'Factory Indent Create': '/factory-indent-create/',
        'Factory Indent Delete': '/factory-indent-delete/<int:pk>/',
        'Factory Indent Update': '/factory-indent-update/<int:pk>/',
        'FeedBack Indent List': '/feedBack-indent-list/',
        'FeedBack Indent Create': '/feedBack-indent-create/',
        'FeedBack Indent Delete': '/feedBack-indent-delete/<int:pk>/',
        'FeedBack Indent Update': '/feedBack-indent-update/<int:pk>/',
        'Factory List': '/factory-list/',
        'Factory Create': '/factory-create/',
        'Factory Update': '/factory-update/<int:pk>/',
        'Factory Delete': '/factory-delete/<int:pk>/',
        'Good List': '/good-list/',
        'Good Detail': '/good-detail/<int:pk>/',
        'Good Create': '/good-create/',
        'Good Update': '/good-update/<int:pk>/',
        'Good Delete': '/good-delete/<int:pk>/',
        'Customer List': '/customer-list/',
        'Customer Detail': '/customer-detail/<int:pk>/',
        'Customer Create': '/customer-create/',
        'Customer Update': '/customer-update/<int:pk>/',
        'Customer Delete': '/customer-delete/<int:pk>/',
    }

    return Response(api_urls)


# Factory API View

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def FactoryList(request):
    facs = FactoryModel.objects.all().order_by('-name')
    serializer = FactorySerializer(facs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def FactoryCreate(request):
    serializer = FactorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def FactoryDetail(request, pk):
    fac = FactoryModel.objects.get(id=pk)
    serializer = FactorySerializer(fac, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def FactoryDelete(request, pk):
    fac = FactoryModel.objects.get(id=pk)
    fac.delete()
    return Response(f'{fac.name} successfully delete!')


# Good Api View
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def GoodList(request):
    goods = GoodsModel.objects.all().order_by('-id')
    serializer = GoodSerializer(goods, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def GoodCreate(request):
    serializer = GoodSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def GoodDetail(request, pk):
    good = GoodsModel.objects.get(id=pk)
    serializer = GoodSerializer(good, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def GoodUpdate(request, pk):
    good = GoodsModel.objects.get(id=pk)
    serializer = GoodSerializer(instance=good, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def GoodDelete(request, pk):
    good = GoodsModel.objects.get(id=pk)
    good.delete()
    return Response(f'{good.name} succsesfully delete!')


# Customer API

class CustomerList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        members = CustomerModel.objects.all()
        serializer = CustomerSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return CustomerModel.objects.get(pk=pk)
        except CustomerModel.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        member = self.get_object(pk)
        serializer = CustomerSerializer(member)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        member = self.get_object(pk)
        serializer = CustomerSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        member = self.get_object(pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# User Api

# Factory Indent API View

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def FactoryIndentList(request):
    faci = FactoryIndent.objects.all().order_by('-name')
    serializer = FactoryIndentSerializer(faci, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def FactoryIndentCreate(request):
    serializer = FactoryIndentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def FactoryIndentDetail(request, pk):
    fac = FactoryIndent.objects.get(id=pk)
    serializer = FactoryIndentSerializer(fac, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def FactoryIndentDelete(request, pk):
    fac = FactoryIndent.objects.get(id=pk)
    fac.delete()
    return Response(f'{fac.id} successfully delete!')


# Feedback Indent API View

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def FeedBackIndentList(request):
    faci = FeedBackIndent.objects.all().order_by('-name')
    serializer = FeedBackIndentSerializer(faci, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def FeedBackIndentCreate(request):
    serializer = FeedBackIndentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def FeedBackIndentDetail(request, pk):
    fac = FeedBackIndent.objects.get(id=pk)
    serializer = FeedBackIndentSerializer(fac, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def FeedBackIndentDelete(request, pk):
    fdb = FeedBackIndent.objects.get(id=pk)
    fdb.delete()
    return Response(f'{fdb.id} successfully delete!')


# Customer Indent API View

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def CustomerIndentList(request):
    ci = CustomerIndent.objects.all().order_by('-name')
    serializer = CustomerIndentSerializer(ci, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def CustomerIndentCreate(request):
    serializer = CustomerIndentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def CustomerIndentDetail(request, pk):
    fac = CustomerIndent.objects.get(id=pk)
    serializer = CustomerIndentSerializer(fac, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def CustomerIndentDelete(request, pk):
    ci = CustomerIndent.objects.get(id=pk)
    ci.delete()
    return Response(f'{ci.id} successfully delete!')
