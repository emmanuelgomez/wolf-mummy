from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import list_route
from .models import Todo, Investor
from .serializers import TodoSerializer,InvestorSerializer,MummySerializer


class APIRoot(APIView):
    """
    API root view listing all routes.
    """
    def get(self, request):
        return Response({
            'todos': reverse('todo-list-view', request=request),
            'investors': reverse('investors-list-view', request=request),
            'dashboard': reverse('dashboard-view', request=request)
        })

class InvestorList(APIView):
    """
    List all investors or create a new one.
    """
    def get(self, request, format=None):
        investors = Investor.objects.all()
        serializer = InvestorSerializer(investors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = InvestorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvestorItem(APIView):
    """
    Retrieve, delete, update or update partially a investor instance.
    """
    def get(self, request, pk, format=None):
        investor = get_object_or_404(Investor, id=pk)
        serializer = InvestorSerializer(investor)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        investor = get_object_or_404(Investor, id=pk)
        serializer = InvestorSerializer(investor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        investor = get_object_or_404(Investor, id=pk)
        investor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        investor = get_object_or_404(Investor, id=pk)
        serializer = InvestorSerializer(investor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardItem(APIView):
    """
        Dashboard methods
        """
    queryset = Investor.objects.all()

    serializer_class = MummySerializer

    @list_route()
    def get(self, request):
        queryset = Investor.objects.filter(parent=None)
        serializer = MummySerializer(queryset, many=True)
        return Response({serializer.data})


