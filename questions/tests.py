from html.parser import HTMLParser
from urllib.parse import urlsplit

from django.contrib.staticfiles import finders
from django.test import Client, SimpleTestCase
from django.urls import resolve, reverse

from .data import QUESTIONS


class Resources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('href', 'src', 'action') and value:
                self.urls.append(value)


class PageTests(SimpleTestCase):
    def setUp(self):
        self.pages = [
            ('questions:index', [], 'questions/index.html'),
            ('questions:hot', [], 'questions/hot.html'),
            ('questions:tag', ['css'], 'questions/tag.html'),
            ('questions:question', [35], 'questions/question.html'),
            ('questions:ask', [], 'questions/ask.html'),
            ('core:login', [], 'core/login.html'),
            ('core:signup', [], 'core/signup.html'),
            ('core:profile', [], 'core/profile.html'),
        ]

    def test_all_pages_use_base_and_have_resolvable_links_and_assets(self):
        for name, args, template in self.pages:
            with self.subTest(name=name):
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)
                self.assertTemplateUsed(response, 'core/base.html')
                parser = Resources()
                parser.feed(response.content.decode())
                for url in parser.urls:
                    path = urlsplit(url).path
                    self.assertNotIn('.html', path)
                    if path.startswith('/static/'):
                        self.assertIsNotNone(finders.find(path.removeprefix('/static/')), url)
                    elif path:
                        self.assertIsNotNone(resolve(path).url_name, url)

    def test_new_and_hot_sorting(self):
        new = self.client.get('/').context['page_obj']
        hot = self.client.get('/hot/').context['page_obj']
        self.assertEqual([q['id'] for q in new], list(range(125, 105, -1)))
        ratings = [q['rating'] for q in hot]
        self.assertEqual(ratings, sorted(ratings, reverse=True))

    def test_tag_filter_and_empty_tag(self):
        page = self.client.get('/tag/css/').context['page_obj']
        self.assertTrue(page.object_list)
        self.assertTrue(all('css' in q['tags'] for q in page))
        expected = sum('css' in q['tags'] for q in QUESTIONS)
        self.assertEqual(page.paginator.count, expected)
        self.assertGreater(page.paginator.num_pages, 1)
        ratings = [q['rating'] for q in page]
        self.assertEqual(ratings, sorted(ratings, reverse=True))
        self.assertContains(self.client.get('/tag/unknown/'), 'По этому тегу пока нет вопросов.')

    def test_list_pagination_and_invalid_page_parameters(self):
        for path in ('/', '/hot/', '/tag/css/', '/question/35/'):
            with self.subTest(path=path):
                first = self.client.get(path).context['page_obj']
                second = self.client.get(path, {'page': 2}).context['page_obj']
                self.assertEqual(second.number, 2)
                self.assertTrue(set(q['id'] for q in first).isdisjoint(q['id'] for q in second))
                for value in ('abc', '0', '-3', '10000', ''):
                    response = self.client.get(path, {'page': value})
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.context['page_obj'].number, 1)

    def test_answer_pagination_and_missing_question(self):
        response = self.client.get('/question/35/')
        self.assertEqual(response.context['question']['id'], 35)
        self.assertEqual(len(response.context['page_obj']), 30)
        self.assertEqual(len(self.client.get('/question/35/?page=2').context['page_obj']), 5)
        self.assertEqual(self.client.get('/question/99999/').status_code, 404)
        self.assertEqual(self.client.get('/question/not-an-id/').status_code, 404)

    def test_paginator_preserves_query_parameters_and_answer_anchor(self):
        self.assertContains(self.client.get('/?filter=example'), '?filter=example&amp;page=2')
        self.assertContains(self.client.get('/question/35/'), '?page=2#answers')
        self.assertContains(self.client.get('/'), 'aria-current="page"')

    def test_forms_have_csrf_and_post_is_explicitly_a_demo(self):
        client = Client(enforce_csrf_checks=True)
        for path in ('/login/', '/signup/', '/profile/', '/ask/', '/question/35/'):
            with self.subTest(path=path):
                response = client.get(path)
                self.assertContains(response, 'csrfmiddlewaretoken')
                self.assertEqual(client.post(path).status_code, 403)
                token = client.cookies['csrftoken'].value
                response = client.post(path, {'csrfmiddlewaretoken': token})
                self.assertContains(response, 'Это макет формы')

    def test_guest_header_and_avatar_fallback(self):
        self.assertContains(self.client.get('/login/'), '>Войти</a>')
        self.assertContains(self.client.get('/'), 'avatar-placeholder')
        self.assertContains(self.client.get('/'), 'aria-label="Аватар Dr. House"')
