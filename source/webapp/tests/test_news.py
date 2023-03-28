from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from accounts.models import User
from webapp.models import News


class NewsTestsForUnregisterUser(TestCase):  # Для анонимных пользователей
    @classmethod
    def setUpTestData(cls):  # Создаём тестировочные данные  - юзера и одну статью
        test_user = User.objects.create_user(username='test_user', password='test_password')
        cls.test_news = News.objects.create(author=test_user, title='Some title', text='Some text')

    def setUp(self):
        self.client = Client()

    def test_add_news(self):
        url = reverse('webapp:news_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Проверка на то, что нет доступа для анонимных пользователей
        image_file = SimpleUploadedFile('image.jpg', b'image_content', content_type='image/jpg')
        # Создаю файл типа картинки (замена реальной картинки)
        data = {'title': 'Some text',
                'text': 'This is a long interesting text with at least 3 sentences.',
                'news_image': image_file}
        response = self.client.post(url, data)  # Отправляю запрос на создание статьи
        self.assertEqual(response.status_code, 302)  # Все ещё нет доступа на страницу
        self.assertEqual(News.objects.count(), 1)  # Проверяю, что статья не была создана

    def test_update_news(self):
        url = reverse('webapp:news_update', args=[self.test_news.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login') + '?next=' + url)
        data = {'title': 'Updated title',
                'text': 'Updated text'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        # Проверяем правильность перенаправления
        self.assertRedirects(response, reverse('accounts:login') + '?next=' + url)
        self.test_news.refresh_from_db()
        self.assertEqual(self.test_news.title, 'Some title')
        self.assertEqual(self.test_news.text, 'Some text')


class NewsTestsForRegisterUser(TestCase):  # Для зарегистрированных пользователей

    def setUp(self):  # Создаём тестировочные данные  - юзера и одну статью
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')  # Логинимся
        self.news = News.objects.create(author=self.user, title='Some title', text='Some text')

    def test_add_news(self):
        url = reverse('webapp:news_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'title': 'New title',
                'text': 'This is a long interesting text with at least 3 sentences.'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(News.objects.filter(title='New title').exists())
        news = News.objects.get(title='New title')
        self.assertEqual(news.author, self.user)
        self.assertEqual(News.objects.count(), 2)

    def test_update_news(self):
        url = reverse('webapp:news_update', args=[self.news.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'title': 'Updated title',
                'text': 'Updated text'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('webapp:news_detail', args=[self.news.pk]))
        news = News.objects.get(title='Updated title')
        self.assertEqual(news.author, self.user)
        self.assertEqual(news.title, 'Updated title')
        self.assertEqual(news.text, 'Updated text')
        self.assertEqual(News.objects.count(), 1)
