from fastapi.testclient import TestClient

from unittest import TestCase
from examples.sorted import app, versions


class TestSorted(TestCase):

    def test_sorted(self) -> None:
        test_client = TestClient(app)

        self.assertListEqual([(1, 0), (2, 0), (10, 0), (10, 1)], versions)
        self.assertEqual(404, test_client.get('/').status_code)

        self.assertEqual(200, test_client.get('/v1.0/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v1.0/1', json={'something': 'something'}).status_code)
        self.assertEqual(200, test_client.post('/v1.0/2').status_code)
        self.assertEqual(404, test_client.post('/v1.0/10').status_code)

        self.assertEqual(200, test_client.get('/v2.0/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v2.0/1').status_code)
        self.assertEqual(200, test_client.post('/v2.0/2').status_code)
        self.assertEqual(404, test_client.post('/v2.0/10').status_code)

        self.assertEqual(200, test_client.get('/v10.0/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v10.0/1').status_code)
        self.assertEqual(200, test_client.post('/v10.0/2').status_code)
        self.assertEqual(200, test_client.post('/v10.0/10').status_code)

        self.assertEqual(200, test_client.get('/v10.1/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v10.1/1').status_code)
        self.assertEqual(200, test_client.post('/v10.1/2').status_code)
        self.assertEqual(200, test_client.post('/v10.1/10').status_code)
        self.assertEqual(200, test_client.post('/v10.1/10/0').status_code)

        self.assertDictEqual(
            {
                'title': 'My Versioned API (route-path sorted)',
                'description': 'Look, I can version my APIs and sort the route-paths!',
                'version': '10.1'
            },
            test_client.get('/v10.1/openapi.json').json()['info']
        )

        self.assertListEqual(
            ['/1', '/2'],
            list(test_client.get('/v1.0/openapi.json').json()['paths'].keys())
        )

        self.assertListEqual(
            ['/1', '/2'],
            list(test_client.get('/v2.0/openapi.json').json()['paths'].keys())
        )

        self.assertListEqual(
            ['/1', '/2', '/10', '/10/0'],
            list(test_client.get('/latest/openapi.json').json()['paths'].keys())
        )

        self.assertListEqual(
            ['/1', '/2', '/10'],
            list(test_client.get('/v10.0/openapi.json').json()['paths'].keys())
        )

        self.assertListEqual(
            ['/1', '/2', '/10', '/10/0'],
            list(test_client.get('/v10.1/openapi.json').json()['paths'].keys())
        )

        self.assertEqual(
            'Do Something Newer',
            test_client.get('/v10.1/openapi.json').json()['paths']['/10']['post']['summary']
        )
