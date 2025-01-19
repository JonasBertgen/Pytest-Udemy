from django.contrib import admin
from .models import Company
# from api.coronavstech.companies.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
