from fastapi.testclient import TestClient

from unittest import TestCase
from examples.sorted import app, versions


class TestSorted(TestCase):

    def test_sorted(self) -> None:
        test_client = TestClient(app)

        self.assertListEqual([(1, 0), (2, 0), (2, 1)], versions)
        self.assertEqual(404, test_client.get('/').status_code)

        self.assertEqual(200, test_client.get('/v1.0/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v1.0/xxx_do_something', json={'something': 'something'}).status_code)
        self.assertEqual(200, test_client.post('/v1.0/bbb_do_something_else').status_code)
        self.assertEqual(404, test_client.post('/v1.0/aaa_do_something_new').status_code)

        self.assertEqual(200, test_client.get('/v2.0/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v2.0/xxx_do_something').status_code)
        self.assertEqual(200, test_client.post('/v2.0/bbb_do_something_else').status_code)
        self.assertEqual(200, test_client.post('/v2.0/aaa_do_something_new').status_code)

        self.assertEqual(200, test_client.post('/v2.1/aaa_do_something_new').status_code)

        self.assertDictEqual(
            {
                'title': 'My Versioned API (route-path sorted)',
                'description': 'Look, I can version my APIs and sort the route-paths!',
                'version': '2.1'
            },
            test_client.get('/v2.1/openapi.json').json()['info']
        )

        self.assertListEqual(
            ['/bbb_do_something_else', '/xxx_do_something'],
            list(test_client.get('/v1.0/openapi.json').json()['paths'].keys())
        )

        self.assertListEqual(
            ['/aaa_do_something_new', '/bbb_do_something_else', '/xxx_do_something'],
            list(test_client.get('/v2.0/openapi.json').json()['paths'].keys())
        )

        self.assertListEqual(
            ['/aaa_do_something_new', '/bbb_do_something_else', '/xxx_do_something'],
            list(test_client.get('/latest/openapi.json').json()['paths'].keys())
        )

        self.assertListEqual(
            ['/aaa_do_something_new', '/bbb_do_something_else', '/xxx_do_something'],
            list(test_client.get('/v2.1/openapi.json').json()['paths'].keys())
        )

        self.assertEqual(
            'Do Something Newer',
            test_client.get('/v2.1/openapi.json').json()['paths']['/aaa_do_something_new']['post']['summary']
        )
