import json
from tornado.web import RequestHandler

from .. import index


class SearchHandler(RequestHandler):

    SUPPORTED_METHODS = ('OPTIONS', 'GET')

    async def get(self):
        query = self.get_argument('q', '')
        terms = query.split(',')

        result = set()
        for term in terms:
            result.update(index.document_index.get_document_ids_by_term(term.lower()))

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(list(result)))
