from http import HTTPStatus

import pytest
from pytest_django.asserts import assertTemplateUsed

from shortener.forms import UrlForm


INDEX_LAZY_URL = pytest.lazy_fixture('index_url')
CREATE_LAZY_URL = pytest.lazy_fixture('create_url')
DELETE_LAZY_URL = pytest.lazy_fixture('delete_url')
GOTO_LAZY_URL = pytest.lazy_fixture('goto_url')


ANONYMOUSE_CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')


@pytest.mark.parametrize(
    'url_path, route',
    (
        ('/', INDEX_LAZY_URL),
        ('/create/', CREATE_LAZY_URL),
        ('/delete/123/', DELETE_LAZY_URL),
        ('/go/123/', GOTO_LAZY_URL),
    )
)
def test_url_reverse_matching(url_path, route):
    assert url_path == route


@pytest.mark.parametrize(
    'route, request_client, expected_status',
    (
        (INDEX_LAZY_URL, ANONYMOUSE_CLIENT, HTTPStatus.OK),
        (CREATE_LAZY_URL, ANONYMOUSE_CLIENT, HTTPStatus.FOUND),
        (DELETE_LAZY_URL, ANONYMOUSE_CLIENT, HTTPStatus.FOUND),
        (GOTO_LAZY_URL, ANONYMOUSE_CLIENT, HTTPStatus.FOUND),
        (INDEX_LAZY_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (CREATE_LAZY_URL, AUTHOR_CLIENT, HTTPStatus.FOUND),
        (DELETE_LAZY_URL, AUTHOR_CLIENT, HTTPStatus.FOUND),
        (GOTO_LAZY_URL, AUTHOR_CLIENT, HTTPStatus.FOUND)
    )
)
def test_url_availability(route, request_client, expected_status):
    response = request_client.get(route)
    assert response.status_code == expected_status


def test_index_page_has_correct_template(index_url, client):
    response = client.get(index_url)
    assertTemplateUsed(response, 'index.html')


def test_index_page_has_form_in_context(index_url, client):
    response = client.get(index_url)
    assert 'form' in response.context
    form = response.context['form']
    assert isinstance(form, UrlForm)
