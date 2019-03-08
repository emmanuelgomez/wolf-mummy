from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import list_route
from .models import Investor
from .serializers import InvestorSerializer,MummySerializer
import random
from django.db.models import Avg
from django.db.models import Q
from .manager import Manager

class APIRoot(APIView):
    """
    API root view listing all routes.
    """
    def get(self, request):
        return Response({
            'investors': reverse('investors-list-view', request=request),
            'dashboard': reverse('dashboard-view', request=request)
        })

class InvestorList(APIView):
    """
    List all investors or create a new one.
    """
    def get(self, request, format=None):
        candidates = Investor.objects.all().filter(parent=None).filter(is_mummy=False)
        try:
            mummy = Investor.objects.select_related('parent').get(is_mummy=True)
        except :
            mummy = Investor(innocence=random.random(), experience=random.random(),charisma=random.random(),is_mummy=True,money=0,week=0,parent=None)
            mummy.save()
        if len(mummy.GetChildrens()) == 0:
            if len(candidates) > 0:
                candidates[0].parent = mummy
            else:
                candidate = Investor(innocence=random.random(), experience=random.random(),charisma=random.random(),is_mummy=False,money=0,week=0,parent=mummy)
                candidate.save()
        if len(candidates) == 0:
            Manager.GenerateInvestors(100)

        Manager().IterateTree(mummy)
        investors = Investor.objects.all().filter(~Q(parent=None)).filter(is_mummy=False)
        candidates = Investor.objects.all().filter(parent=None).filter(is_mummy=False)

        return Response({
            'mummyId':mummy.id,
            'totalPopulation': Investor.objects.all().filter(parent=None).count(),
            'totalMembers': Investor.objects.count(),
            'mummyMoney': Investor.objects.get(is_mummy=True).money,
            'avgMoney': Investor.objects.all().filter(~Q(parent=None)).aggregate(Avg('money')),
            'investors': InvestorSerializer(investors, many=True).data,
            'candidates': InvestorSerializer(candidates, many=True).data
        })

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
        newCandidates = []
        for x in range(0, 10):
            newCandidates.append(Investor(innocence = random.random(),experience = random.random(),
                                          charisma=random.random()))
        candidates = InvestorSerializer(newCandidates, many=True)
        return Response({
            'totalPopulation': Investor.objects.count() + 10,
            'totalMembers': Investor.objects.count(),
            'mummyMoney': Investor.objects.get(parent=None).money,
            'avgMoney': Investor.objects.all().filter(~Q(parent=None)).aggregate(Avg('money')),
            'tree':  serializer.data,
            'candidates': candidates.data
        })
