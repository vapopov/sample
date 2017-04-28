import json
import tornado
from uuid import uuid4

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.testing import AsyncTestCase
from tornado import gen
from apps.base.ioloop import IOLoop


class TestSearch(AsyncTestCase):

    _base_url = 'http://localhost:8080'

    def setUp(self):
        self.io_loop = IOLoop.current()

        self._sample_text = 'Test Document, With CAPITAL LETTERS.'
        self._sample_token = 'document'
        self._sample_document_id = str(uuid4())

    @tornado.testing.gen_test
    def test_add_document(self):
        client = AsyncHTTPClient(self.io_loop)
        url = '/'.join([self._base_url, 'document', self._sample_document_id])

        response = yield client.fetch(HTTPRequest(url, method='POST', body=self._sample_text))
        self.assertEqual(response.code, 200, 'Document wasn\'t added')

        response = yield client.fetch(HTTPRequest(url, method='GET'))
        self.assertEqual(response.code, 200, 'Document wasn\'t found')
        self.assertEqual(self._sample_text, response.body.decode(), 'Content is different')

    @tornado.testing.gen_test
    def test_delete_document(self):
        client = AsyncHTTPClient(self.io_loop)
        url = '/'.join([self._base_url, 'document', self._sample_document_id])

        response = yield client.fetch(HTTPRequest(url, method='POST', body=self._sample_text))
        self.assertEqual(response.code, 200, 'Document wasn\'t added')

        response = yield client.fetch(HTTPRequest(url, method='DELETE'))
        self.assertEqual(response.code, 200, 'Document wasn\'t deleted')

        response = yield client.fetch(HTTPRequest(url, method='GET'), raise_error=False)
        self.assertEqual(response.code, 404, 'Document wasn\'t deleted')

    def _terms_data_fixture(self):
        return {
            str(uuid4()): ('today', 'Sample text.Today, many words.'),
            str(uuid4()): ('lorem', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
                           'tempor incididunt ut labore et dolore magna aliqua.Many.'),
            str(uuid4()): ('many', 'Text that present in each document - many.')
        }

    @gen.coroutine
    def _create_documents_by_fixture(self, test_terms):
        client = AsyncHTTPClient(self.io_loop)
        for document_id, (term, text) in test_terms.items():
            document_url = '/'.join([self._base_url, 'document', document_id])
            response = yield client.fetch(HTTPRequest(document_url, method='POST', body=text))
            self.assertEqual(response.code, 200, 'Document wasn\'t added')

    @tornado.testing.gen_test
    def test_search(self):
        test_terms = self._terms_data_fixture()
        client = AsyncHTTPClient(self.io_loop)
        search_url = '/'.join([self._base_url, 'search'])

        yield self._create_documents_by_fixture(test_terms)

        for document_id, (term, text) in test_terms.items():
            response = yield client.fetch(HTTPRequest(search_url + '?q={}'.format(term), method='GET'))
            ids = json.loads(response.body.decode())
            self.assertIn(document_id, ids)

        response = yield client.fetch(HTTPRequest(search_url + '?q={}'.format('many'), method='GET'))
        ids = json.loads(response.body.decode())
        for document_id in test_terms.keys():
            self.assertIn(document_id, ids)

    @tornado.testing.gen_test
    def test_search_after_delete(self):
        test_terms = self._terms_data_fixture()
        client = AsyncHTTPClient(self.io_loop)
        search_url = '/'.join([self._base_url, 'search'])
        yield self._create_documents_by_fixture(test_terms)

        for document_id in test_terms.keys():
            document_url = '/'.join([self._base_url, 'document', document_id])
            response = yield client.fetch(HTTPRequest(document_url, method='DELETE'))
            self.assertEqual(response.code, 200, 'Document wasn\'t deleted')

        response = yield client.fetch(HTTPRequest(search_url + '?q={}'.format('many'), method='GET'))
        ids = json.loads(response.body.decode())
        for document_id in test_terms.keys():
            self.assertNotIn(document_id, ids)
