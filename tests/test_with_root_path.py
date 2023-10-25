from fastapi.testclient import TestClient

from unittest import TestCase
from examples.with_root_path import app, versions


class TestWitRootPathExample(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_with_root_path_example(self) -> None:
        test_client = TestClient(app)

        self.assertListEqual([(1, 0), (2, 0)], versions)

        # versions route
        self.assertDictEqual(
            {
                'versions': [
                    {
                        'version': '1',
                        'openapi_url': '/api/v1/api_schema.json',
                        'swagger_url': '/api/v1/swagger'
                    },
                    {
                        'version': '2',
                        'openapi_url': '/api/v2/api_schema.json',
                        'swagger_url': '/api/v2/swagger',
                    }
                ]
            },
            test_client.get('/versions').json()
        )

        self.assertEqual('"Okv1"', test_client.get('/v1/status').text)
        self.assertEqual('"Okv2"', test_client.get('/v2/status').text)
        self.assertEqual('"Okv2"', test_client.get('/latest/status').text)

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
                    'version': '0.1.0'
                },
                'servers': [
                    {
                        'url': '/api'
                    }
                ],
                'paths': {
                    '/v1/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status V1',
                            'operationId': 'get_status_v1_v1_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V1 V1 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/v2/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status V2',
                            'operationId': 'get_status_v2_v2_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V2 V2 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    '/latest/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status V2',
                            'operationId': 'get_status_v2_latest_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V2 Latest Status Get'
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
                    'version': 'v1'
                },
                'servers': [
                    {
                        'url': '/api'
                    }
                ],
                'paths': {
                    '/v1/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status V1',
                            'operationId': 'get_status_v1_v1_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V1 V1 Status Get'
                                            }
                                        }
                                    }
                                }
                            }
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
                    'version': 'v2'
                },
                'servers': [
                    {
                        'url': '/api'
                    }
                ],
                'paths': {
                    '/v2/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status V2',
                            'operationId': 'get_status_v2_v2_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V2 V2 Status Get'
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
                    'version': 'v2'
                },
                'servers': [
                    {
                        'url': '/api'
                    }
                ],
                'paths': {
                    '/latest/status': {
                        'get': {
                            'tags': [
                                'Status'
                            ],
                            'summary': 'Get Status V2',
                            'operationId': 'get_status_v2_latest_status_get',
                            'responses': {
                                '200': {
                                    'description': 'Successful Response',
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'string',
                                                'title': 'Response Get Status V2 Latest Status Get'
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
