from fastapi.testclient import TestClient

from unittest import TestCase
from examples.oauth import app


class TestOAuthExample(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_oauth_example(self) -> None:
        test_client = TestClient(app)

        components = test_client.get('/openapi.json').json()['components']
        self.assertDictEqual({
            'securitySchemes': {
                'OAuth2': {
                    'flows': {
                        'implicit': {
                            'authorizationUrl': 'https://login.something.com/authorize',
                            'scopes': {}
                        }
                    },
                    'type': 'oauth2'
                }
            }
        }, components)
        self.assertIn(
            'ui.initOAuth({"clientId": "my-client-id", "scopes": "required_scopes"})',
            test_client.get('/docs').text
        )

        v1_components = test_client.get('/v1/openapi.json').json()['components']
        self.assertDictEqual({
            'securitySchemes': {
                'OAuth2': {
                    'flows': {
                        'implicit': {
                            'authorizationUrl': 'https://login.something.com/authorize',
                            'scopes': {}
                        }
                    },
                    'type': 'oauth2'
                }
            }
        }, v1_components)
        self.assertIn(
            'ui.initOAuth({"clientId": "my-client-id", "scopes": "required_scopes"})',
            test_client.get('/v1/docs').text
        )
