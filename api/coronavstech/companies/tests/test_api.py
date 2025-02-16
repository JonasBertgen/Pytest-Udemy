from companies.models import Company
import json
from django.urls import reverse
import logging

import pytest
logger = logging.getLogger("log")
companies_url = reverse("companies-list")


@pytest.mark.django_db
def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.mark.django_db
def test_one_companies_exist_sucess(client) -> None:
    testCompany = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == testCompany.name
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


@pytest.mark.django_db
def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["This field is required."]}


@pytest.mark.django_db
def test_create_existing_company_should_fail(client) -> None:
    Company.objects.create(name="apple")
    response = client.post(
        path=companies_url, data={"name": "apple"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]}


@pytest.mark.django_db
def test_create_company_should_pass(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "test company"})
    assert response.status_code == 201
    response_content = (json.loads(response.content))
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


@pytest.mark.django_db
def test_create_company_with_layoffstatus_should_pass(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "test company", "status":
                                  "Layoffs"})
    assert response.status_code == 201
    response_content = (json.loads(response.content))
    assert response_content.get("status") == "Layoffs"


@pytest.mark.django_db
def test_create_company_with_wrong_status_should_pass(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "test company", "status":
                                  "layoffs"})
    assert response.status_code == 400
    # self.assertIn("WrongStatus", str(response.content))
    # assert "is not a valid choice" == str(response.content)
    assert str(response.content).__contains__("is not a valid choice")


@pytest.mark.xfail
def test_should_be_ok_if_failed() -> None:
    assert 1 == 2


@pytest.mark.skip
def test_should_be_skipped() -> None:
    assert 1 == 2


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
