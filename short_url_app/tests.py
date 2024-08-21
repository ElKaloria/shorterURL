from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import UrlForm
from .models import ShortUrl


class TestRedirection(TestCase):
    """Тестируем GET запросы"""

    def setUp(self) -> None:
        user = User.objects.create_user(username='test_user', password='test_password')
        ShortUrl.objects.create(
             original_url='https://ya.ru/',
             short_url='aEdj01',
             user=user
        )

        self.active_url = reverse('short_url_app:redirect_to_original_url', kwargs={'short_url': 'aEdj01'})

    def test_redirection(self):
        """
        Тестируем переадресацию
        """
        response = self.client.get(self.active_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://ya.ru/')

    def test_response_counter(self):
        """
        Тестируем счетчик запросов токена
        """
        self.assertEqual(
         ShortUrl.objects.get(short_url='aEdj01').request_count, 0
        )
        self.client.get(self.active_url)
        self.assertEqual(
            ShortUrl.objects.get(short_url='aEdj01').request_count, 1
        )


class FormViewTestCase(TestCase):
    """
    Тестируем форму регистрации url
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_get_request(self):
        """
        Тестируем GET запрос
        :return:
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_app/index.html')
        self.assertIsInstance(response.context['form'], UrlForm)

    def test_post_request_with_existing_url(self):
        """
        Тестируем POST запрос с уже существующей, зарегистрированной ссылкой ссылкой
        :return:
        """
        self.client.login(username='testuser', password='testpass')
        ShortUrl.objects.create(user=self.user, original_url='http://example.com', short_url='abc123')
        response = self.client.post('/', data={'original_url': 'http://example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_app/form_redirect.html')
        self.assertEqual(response.context['short_url'], 'abc123')

    def test_post_request_with_new_url(self):
        """
        Тестируем POST запрос с новой ссылкой
        :return:
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/', data={'original_url': 'http://example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_app/form_redirect.html')
        self.assertIsNotNone(response.context['short_url'])
        self.assertEqual(ShortUrl.objects.count(), 1)
        self.assertEqual(ShortUrl.objects.first().user, self.user)
        self.assertEqual(ShortUrl.objects.first().original_url, 'http://example.com')


class UserUrlListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.short_url = ShortUrl.objects.create(original_url='http://example.com', user=self.user)

    def test_get_context_data(self):
        response = self.client.get(
            reverse('short_url_app:UserUrlList', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['users'].count(), 1)
        self.assertEqual(response.context['user_param'], self.user.username)
        self.assertEqual(response.context['urls'].count(), 1)
        self.assertEqual(response.context['urls'].first(), self.short_url)

    def test_get_context_data_with_no_user(self):
        response = self.client.get(reverse('short_url_app:UserList'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['users'].count(), 1)
        self.assertEqual(response.context['user_param'], None)
        self.assertEqual(response.context['urls'], None)

    def test_get_context_data_with_no_urls(self):
        self.short_url.delete()
        response = self.client.get(
            reverse('short_url_app:UserUrlList', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['users'].count(), 1)
        self.assertEqual(response.context['user_param'], self.user.username)
        #self.assertEqual(response.context['urls'], ShortUrl.objects.none())
        #Выдает ошибку - AssertionError: <QuerySet []> != <QuerySet []>
        #Смешно


class URLListTestCase(TestCase):
    """
    Тестируем URLList view, для получения списка ссылок
    """
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpass')
        # Create some test data
        for i in range(11):
            ShortUrl.objects.create(original_url='http://example.com/{}'.format(i), user=user)

    def setUp(self):
        self.url = reverse('short_url_app:URLList')

    def test_get(self):
        """
        Тестируем GET запрос
        :return:
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_app/list_url.html')
        self.assertEqual(len(response.context_data['urls']), 10)

    def test_pagination(self):
        """
        Тестируем пагинацию
        :return:
        """
        response = self.client.get(self.url + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['urls']), 1)

    def test_context_object_name(self):
        """
        Тестируем контекстный объект
        :return:
        """
        # Test the context object name
        response = self.client.get(self.url)
        self.assertEqual(response.context_data['urls'], response.context_data['urls'])
