from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .models import Company
from .serializers import CompanySerializer
# from api.coronavstech.companies.models import Company
# from api.coronavstech.companies.serializers import CompanySerializer
# Create your views here.


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination
