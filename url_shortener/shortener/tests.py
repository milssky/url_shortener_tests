from http import HTTPStatus

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


from .models import Url, User
from .forms import UrlForm


class TestUrls(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('user')
        cls.url = Url.objects.create(
            author=cls.user,
            full_url='https://ya.ru',
            shorted_url='123'
        )

        cls.INDEX_URL = reverse('index')
        cls.CREATE_URL = reverse('create_url')
        cls.DELETE_URL = reverse(
            'delete_url',
            args=(cls.url.shorted_url,)
        )
        cls.GOTO_URL = reverse(
            'goto',
            args=(cls.url.shorted_url,)
        )

        cls.routes_with_expected_reverses = (
            ('/', cls.INDEX_URL),
            ('/create/', cls.CREATE_URL),
            (f'/delete/{cls.url.shorted_url}/', cls.DELETE_URL),
            (f'/go/{cls.url.shorted_url}/', cls.GOTO_URL),
        )

    def setUp(self) -> None:
        self.unauth_client = Client()
        self.auth_client = Client()
        self.auth_client.force_login(self.user)

        self.urls = (
            (self.INDEX_URL, self.unauth_client, HTTPStatus.OK),
            (self.CREATE_URL, self.auth_client, HTTPStatus.FOUND),
            (self.DELETE_URL, self.auth_client, HTTPStatus.FOUND),
            (self.GOTO_URL, self.unauth_client, HTTPStatus.NOT_FOUND),
            (self.DELETE_URL, self.unauth_client, HTTPStatus.FOUND),
        )

    def test_routes(self):
        """Тестируем соответсвие реверса и заданного в ТЗ адреса."""
        for address, route in self.routes_with_expected_reverses:
            with self.subTest(address=address, route=route):
                self.assertEqual(address, route)

    def test_urls_availability(self):
        for address, client, code in self.urls:
            with self.subTest(address=address, client=client, http_code=code):
                response = client.get(address)
                self.assertEqual(response.status_code, code)

    def test_uses_templates(self):
        response = self.unauth_client.get(self.INDEX_URL)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_page_has_form_in_context_for_auth_user(self):
        response = self.auth_client.get(self.INDEX_URL)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], UrlForm)
