from fastapi.testclient import TestClient

from unittest import TestCase
from examples.advanced import app, versions


class TestAdvanced(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_advanced(self) -> None:
        test_client = TestClient(app)

        self.assertListEqual([(1, 0), (2, 0)], versions)
        self.assertEqual(404, test_client.get('/').status_code)
        self.assertEqual(404, test_client.get('/specs').status_code)
        self.assertEqual(200, test_client.get('/openapi.json').status_code)
        self.assertEqual(200, test_client.get('/versions').status_code)
        self.assertEqual(200, test_client.get('/api-versions').status_code)
        self.assertEqual(200, test_client.get('/v1/specs').status_code)
        self.assertEqual(404, test_client.get('/v1/redoc').status_code)
        self.assertEqual(200, test_client.get('/v1/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v1/do_something', json={'something': 'something'}).status_code)
        self.assertEqual(200, test_client.post('/v1/do_something_else').status_code)
        self.assertEqual(404, test_client.post('/v1/do_something_new').status_code)
        self.assertEqual(200, test_client.get('/v2/specs').status_code)
        self.assertEqual(404, test_client.get('/v2/redoc').status_code)
        self.assertEqual(200, test_client.get('/v2/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/v2/do_something').status_code)
        self.assertEqual(200, test_client.post('/v2/do_something_else').status_code)
        self.assertEqual(200, test_client.post('/v2/do_something_new').status_code)
        self.assertEqual(200, test_client.get('/latest/specs').status_code)
        self.assertEqual(404, test_client.get('/latest/redoc').status_code)
        self.assertEqual(200, test_client.get('/latest/openapi.json').status_code)
        self.assertEqual(200, test_client.post('/latest/do_something').status_code)
        self.assertEqual(200, test_client.post('/latest/do_something_else').status_code)
        self.assertEqual(200, test_client.post('/latest/do_something_new').status_code)

        self.assertDictEqual(
            {'versions': [{'version': '1'}, {'version': '2'}]},
            test_client.get('/versions').json()
        )
        self.assertDictEqual(
            {'something': 'something'},
            test_client.post('/v1/do_something', json={'something': 'something'}).json()
        )
        self.assertDictEqual(
            {'message': 'something else'},
            test_client.post('/v1/do_something_else').json()
        )
        self.assertDictEqual(
            {'message': 'something'},
            test_client.post('/v2/do_something').json()
        )
        self.assertDictEqual(
            {'message': 'something else'},
            test_client.post('/v2/do_something_else').json()
        )
        self.assertDictEqual(
            {'message': 'something new'},
            test_client.post('/v2/do_something_new').json()
        )
        self.assertDictEqual(
            {
                'title': 'My Versioned API',
                'description': 'Look, I can version my APIs!',
                'version': '2.0'
            },
            test_client.get('/openapi.json').json()['info']
        )
        self.assertDictEqual(
            {
                '/versions': {
                    'get': {
                        'tags': [
                            'Versions'
                        ],
                        'summary': 'Get Versions ',
                        'operationId': 'get_versions__versions_get',
                        'responses': {
                            '200': {
                                'description': 'Successful Response',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/VersionsModel'
                                        }
                                    }
                                }
                            },
                            '400': {
                                'description': 'Bad Request',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            },
                            '500': {
                                'description': 'Internal Server Error',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            test_client.get('/openapi.json').json()['paths']
        )
        self.assertDictEqual(
            {'title': 'My Versioned API', 'version': '1'},
            test_client.get('/v1/openapi.json').json()['info']
        )
        self.assertDictEqual(
            {
                '/do_something': {
                    'post': {
                        'tags': [
                            'Something'
                        ],
                        'summary': 'Do Something',
                        'operationId': 'do_something_do_something_post',
                        'requestBody': {
                            'content': {
                                'application/json': {
                                    'schema': {
                                        '$ref': '#/components/schemas/TestModel'
                                    }
                                }
                            },
                            'required': True
                        },
                        'responses': {
                            '200': {
                                'description': 'Successful Response',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/TestModel'
                                        }
                                    }
                                }
                            },
                            '400': {
                                'description': 'Bad Request',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            },
                            '500': {
                                'description': 'Internal Server Error',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '/do_something_else': {
                    'post': {
                        'tags': [
                            'Something Else'
                        ],
                        'summary': 'Do Something Else',
                        'operationId': 'do_something_else_do_something_else_post',
                        'responses': {
                            '200': {
                                'description': 'Successful Response',
                                'content': {
                                    'application/json': {
                                        'schema': {}
                                    }
                                }
                            },
                            '400': {
                                'description': 'Bad Request',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            },
                            '500': {
                                'description': 'Internal Server Error',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            test_client.get('/v1/openapi.json').json()['paths']
        )
        self.assertDictEqual(
            {'title': 'My Versioned API', 'version': '2'},
            test_client.get('/v2/openapi.json').json()['info']
        )
        self.assertDictEqual(
            {
                '/do_something': {
                    'post': {
                        'tags': [
                            'Something'
                        ],
                        'summary': 'Do Something V2',
                        'operationId': 'do_something_v2_do_something_post',
                        'responses': {
                            '200': {
                                'description': 'Successful Response',
                                'content': {
                                    'application/json': {
                                        'schema': {}
                                    }
                                }
                            },
                            '400': {
                                'description': 'Bad Request',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            },
                            '500': {
                                'description': 'Internal Server Error',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '/do_something_else': {
                    'post': {
                        'tags': [
                            'Something Else'
                        ],
                        'summary': 'Do Something Else',
                        'operationId': 'do_something_else_do_something_else_post',
                        'responses': {
                            '200': {
                                'description': 'Successful Response',
                                'content': {
                                    'application/json': {
                                        'schema': {}
                                    }
                                }
                            },
                            '400': {
                                'description': 'Bad Request',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            },
                            '500': {
                                'description': 'Internal Server Error',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '/do_something_new': {
                    'post': {
                        'tags': [
                            'Something New'
                        ],
                        'summary': 'Do Something New',
                        'operationId': 'do_something_new_do_something_new_post',
                        'responses': {
                            '200': {
                                'description': 'Successful Response',
                                'content': {
                                    'application/json': {
                                        'schema': {}
                                    }
                                }
                            },
                            '400': {
                                'description': 'Bad Request',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            },
                            '500': {
                                'description': 'Internal Server Error',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/ErrorResponsesModel'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            test_client.get('/latest/openapi.json').json()['paths']
        )
