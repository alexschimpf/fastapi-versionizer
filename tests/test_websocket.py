from fastapi import WebSocketDisconnect
from fastapi.testclient import TestClient

from unittest import TestCase
from examples.websocket import app, versions


class TestWebsocketExample(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_simple_example(self) -> None:
        test_client = TestClient(app)

        self.assertListEqual([(1, 0), (2, 0)], versions)

        # Make sure some pages don't exist
        self.assertEqual(404, test_client.get('/redoc').status_code)
        self.assertEqual(404, test_client.get('/v1/redoc').status_code)
        self.assertEqual(404, test_client.get('/v2/redoc').status_code)
        self.assertEqual(404, test_client.get('/latest/redoc').status_code)
        self.assertEqual(404, test_client.get('/chatterbox').status_code)
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

        # v1
        assert test_client.get('/v1/chatterbox').json() == 'v1'
        try:
            msg = None
            with test_client.websocket_connect('/v1/chatterbox') as websocket:
                websocket.send_text('ping')
                msg = websocket.receive_text()
        except WebSocketDisconnect:
            if msg is None:
                raise
        assert msg == 'ping'

        # v2
        assert test_client.get('/v2/chatterbox').json() == 'v2'
        try:
            with test_client.websocket_connect('/v2/chatterbox') as websocket:
                websocket.send_text('ping')
                msg = websocket.receive_text()
        except WebSocketDisconnect:
            if msg is None:
                raise
        assert msg == 'pong'

        # latest
        assert test_client.get('/v2/chatterbox').json() == 'v2'
        try:
            with test_client.websocket_connect('/v2/chatterbox') as websocket:
                websocket.send_text('ping')
                msg = websocket.receive_text()
        except WebSocketDisconnect:
            if msg is None:
                raise
        assert msg == 'pong'

        # docs
        self.assertEqual(200, test_client.get('/swagger').status_code)
        self.assertEqual(200, test_client.get('/v1/swagger').status_code)
        self.assertEqual(200, test_client.get('/v2/swagger').status_code)
        self.assertEqual(200, test_client.get('/latest/swagger').status_code)

        # openapi
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test',
                    'description': 'Websocket example of FastAPI Versionizer.',
                    'termsOfService': 'https://github.com/alexschimpf/fastapi-versionizer',
                    'version': '0.1.0'
                },
                'paths': {
                    '/v1/chatterbox': {
                        'get': {
                            'tags': [
                                'Chatting'
                            ],
                            'summary': 'Get Explaination',
                            'operationId': 'get_explaination_v1_chatterbox_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Explaination V1 Chatterbox Get'
                                            }
                                        }
                                    }
                                }
                            },
                            'deprecated': True
                        }
                    },
                    '/v2/chatterbox': {
                        'get': {
                            'tags': [
                                'Chatting'
                            ],
                            'summary': 'Get Explaination V2',
                            'operationId': 'get_explaination_v2_v2_chatterbox_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Explaination V2 V2 Chatterbox Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/latest/chatterbox': {
                        'get': {
                            'tags': [
                                'Chatting'
                            ],
                            'summary': 'Get Explaination V2',
                            'operationId': 'get_explaination_v2_latest_chatterbox_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Explaination V2 Latest Chatterbox Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/versions': {
                        'get': {
                            'tags': [
                                'Versions'
                            ],
                            'summary': 'Get Versions',
                            'operationId': 'get_versions_versions_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'object',
                                                'title': 'Response Get Versions Versions Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            test_client.get('/api_schema.json').json()
        )
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test - v1',
                    'description': 'Websocket example of FastAPI Versionizer.',
                    'termsOfService': 'https://github.com/alexschimpf/fastapi-versionizer',
                    'version': 'v1'
                },
                'paths': {
                    '/v1/chatterbox': {
                        'get': {
                            'tags': [
                                'Chatting'
                            ],
                            'summary': 'Get Explaination',
                            'operationId': 'get_explaination_v1_chatterbox_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Explaination V1 Chatterbox Get'
                                            }
                                        }
                                    }
                                }
                            },
                            'deprecated': True
                        }
                    }
                }
            },
            test_client.get('/v1/api_schema.json').json()
        )
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test - v2',
                    'description': 'Websocket example of FastAPI Versionizer.',
                    'termsOfService': 'https://github.com/alexschimpf/fastapi-versionizer',
                    'version': 'v2'
                },
                'paths': {
                    '/v2/chatterbox': {
                        'get': {
                            'tags': [
                                'Chatting'
                            ],
                            'summary': 'Get Explaination V2',
                            'operationId': 'get_explaination_v2_v2_chatterbox_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Explaination V2 V2 Chatterbox Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            test_client.get('/v2/api_schema.json').json()
        )
        self.assertDictEqual(
            {
                'openapi': '3.1.0',
                'info': {
                    'title': 'test - v2',
                    'description': 'Websocket example of FastAPI Versionizer.',
                    'termsOfService': 'https://github.com/alexschimpf/fastapi-versionizer',
                    'version': 'v2'
                },
                'paths': {
                    '/latest/chatterbox': {
                        'get': {
                            'tags': [
                                'Chatting'
                            ],
                            'summary': 'Get Explaination V2',
                            'operationId': 'get_explaination_v2_latest_chatterbox_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Explaination V2 Latest Chatterbox Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            test_client.get('/latest/api_schema.json').json()
        )
