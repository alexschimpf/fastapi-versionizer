from fastapi.testclient import TestClient

from unittest import TestCase
from examples.with_lifespan import app, versions


class TestWithLifespanExample(TestCase):

    def test_with_lifespan_example(self) -> None:
        with TestClient(app) as test_client:

            self.assertListEqual([(1, 0), (2, 0)], versions)

            # versions route
            self.assertDictEqual(
                {
                    'versions': [
                        {
                            'version': '1',
                            'openapi_url': '/v1/api_schema.json',
                            'swagger_url': '/v1/swagger'
                        },
                        {
                            'version': '2',
                            'openapi_url': '/v2/api_schema.json',
                            'swagger_url': '/v2/swagger',
                        }
                    ]
                },
                test_client.get('/versions').json()
            )

            # status route
            self.assertEqual(200, test_client.get('/v1/status').status_code)
            self.assertEqual(200, test_client.get('/v2/status').status_code)

            # test middleware
            self.assertIsNotNone(
                test_client.get('/v1/status').headers.get('X-Process-Time'),
                'Middleware not working'
            )
