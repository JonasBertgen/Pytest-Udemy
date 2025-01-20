from companies.models import Company
import json
from unittest import TestCase
from django.urls import reverse
from django.test import Client
import logging

import pytest
logger = logging.getLogger("log")


@pytest.mark.django_db
class TestGetCompanies(TestCase):
    def test_simple_test(self) -> None:
        pass

    def stuff():
        print("stuff")

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


def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")


def function_that_logs() -> None:
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")


def function_that_logs_info() -> None:
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        logger.info(f"I am logging {str(e)}")


def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)


def test_logged_warning_level(caplog) -> None:
    function_that_logs()
    assert "I am logging CoronaVirus Exception" in caplog.text


def test_logged_warning_level_info(caplog) -> None:
    with caplog.at_level(logging.INFO):
        function_that_logs_info()
        assert "I am logging CoronaVirus Exception" in caplog.text
