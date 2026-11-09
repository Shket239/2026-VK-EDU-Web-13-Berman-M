from django.test import RequestFactory, SimpleTestCase

from .pagination import paginate


class PaginationTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_pages_do_not_overlap_and_keep_last_partial_page(self):
        objects = list(range(23))
        pages = [paginate(objects, self.factory.get('/', {'page': i})) for i in (1, 2, 3)]
        self.assertEqual([list(page) for page in pages], [objects[:10], objects[10:20], objects[20:]])
        self.assertEqual(pages[0].paginator.num_pages, 3)

    def test_invalid_page_values_fall_back_to_first_page(self):
        for value in ('', 'abc', '1.5', '0', '-1', '999', '9' * 5000):
            with self.subTest(value=value[:20]):
                page = paginate(list(range(23)), self.factory.get('/', {'page': value}))
                self.assertEqual(page.number, 1)
                self.assertEqual(list(page), list(range(10)))

    def test_missing_parameter_and_empty_collection(self):
        page = paginate([], self.factory.get('/'))
        self.assertEqual(page.number, 1)
        self.assertEqual(list(page), [])
        self.assertEqual(page.paginator.num_pages, 1)

    def test_custom_page_size(self):
        page = paginate(list(range(23)), self.factory.get('/', {'page': 2}), 20)
        self.assertEqual(list(page), [20, 21, 22])
