from fastapi.testclient import TestClient

from unittest import TestCase
from examples.tags import app, versions, tags


class TestTagsExample(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_tags_example(self) -> None:
        test_client = TestClient(app)

        self.assertListEqual([(1, 0), (2, 0)], versions)

        # Make sure some pages don't exist
        self.assertEqual(404, test_client.get('/redoc').status_code)
        self.assertEqual(404, test_client.get('/v1/redoc').status_code)
        self.assertEqual(404, test_client.get('/v2/redoc').status_code)
        self.assertEqual(404, test_client.get('/latest/redoc').status_code)
        self.assertEqual(404, test_client.post('/users').status_code)
        self.assertEqual(404, test_client.post('/items').status_code)
        self.assertEqual(404, test_client.get('/users').status_code)
        self.assertEqual(404, test_client.get('/items').status_code)
        self.assertEqual(404, test_client.get('/users/1').status_code)
        self.assertEqual(404, test_client.get('/items/1').status_code)
        self.assertEqual(404, test_client.get('/v2/items/1').status_code)
        self.assertEqual(404, test_client.get('/v1/versions').status_code)
        self.assertEqual(404, test_client.get('/v2/versions').status_code)
        self.assertEqual(404, test_client.get('/latest/versions').status_code)

        # versions route
        self.assertDictEqual(
            {
                'versions': [
                    {
                        'version': '1',
                        'openapi_url': '/v1/api_schema.json',
                        'swagger_url': '/v1/swagger',
                    },
                    {
                        'version': '2',
                        'openapi_url': '/v2/api_schema.json',
                        'swagger_url': '/v2/swagger',
                    },
                ]
            },
            test_client.get('/versions').json(),
        )

        # docs
        self.assertEqual(200, test_client.get('/swagger').status_code)
        self.assertEqual(200, test_client.get('/v1/swagger').status_code)
        self.assertEqual(200, test_client.get('/v2/swagger').status_code)
        self.assertEqual(200, test_client.get('/latest/swagger').status_code)

        tags_main = test_client.get('/api_schema.json').json().get('tags', {})
        tags_v1 = test_client.get('/v1/api_schema.json').json().get('tags', {})
        tags_v2 = test_client.get('/v2/api_schema.json').json().get('tags', None)
        tags_latest = test_client.get('/latest/api_schema.json').json().get('tags', None)

        # openapi
        self.assertListEqual(tags, tags_main)
        self.assertListEqual(tags, tags_v1)
        self.assertIsNone(tags_v2)
        self.assertIsNone(tags_latest)
