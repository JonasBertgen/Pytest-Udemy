from companies.models import Company
import json
from unittest import TestCase
import django
from django.urls import reverse
from django.test import Client

import pytest


@pytest.mark.django_db
class TestGetCompanies(TestCase):
    def test_simple_test(self) -> None:
        pass

    def test_zero_companies_should_return_empty_list(self) -> None:
        client = Client()
        companies_url = reverse("companies-list")
        response = client.get(companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_companies_exist_sucess(self) -> None:
        client = Client()
        testCompany = Company.objects.create(name="Amazon")
        companies_url = reverse("companies-list")
        response = client.get(companies_url)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response_content.get("name"), testCompany.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")
        testCompany.delete()
