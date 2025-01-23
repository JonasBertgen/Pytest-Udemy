from companies.models import Company
import json
from unittest import TestCase
from django.urls import reverse
from django.test import Client
import logging

import pytest
logger = logging.getLogger("log")


@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self) -> None:
        pass


class TestGetCompanies(BasicCompanyAPITestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self) -> None:
        pass

    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_companies_exist_sucess(self) -> None:
        testCompany = Company.objects.create(name="Amazon")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), testCompany.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")
        testCompany.delete()


class TestPostCompanies(BasicCompanyAPITestCase):
    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    def test_create_existing_company_should_fail(self) -> None:
        Company.objects.create(name="apple")
        response = self.client.post(
            path=self.companies_url, data={"name": "apple"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {
                "name": ["company with this name already exists."]}
        )

    def test_create_company_should_pass(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "test company"})
        self.assertEqual(response.status_code, 201)
        response_content = (json.loads(response.content))
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffstatus_should_pass(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "test company", "status":
                                           "Layoffs"})
        self.assertEqual(response.status_code, 201)
        response_content = (json.loads(response.content))
        self.assertEqual(response_content.get("status"), "Layoffs")

    def test_create_company_with_wrong_status_should_pass(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "test company", "status":
                                           "layoffs"})
        self.assertEqual(response.status_code, 400)
        # self.assertIn("WrongStatus", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))

    @pytest.mark.xfail
    def test_should_be_ok_if_failed(self) -> None:
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_should_be_skipped(self) -> None:
        self.assertEqual(1, 2)


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
