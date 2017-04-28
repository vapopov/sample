from tornado.web import RequestHandler, HTTPError

from .. import index


class DocumentHandler(RequestHandler):

    SUPPORTED_METHODS = ('OPTIONS', 'GET', 'POST', 'DELETE')

    async def get(self, document_id):
        try:
            self.set_header("Content-Type", "text/plain; charset=UTF-8")
            self.write(index.document_index.get(document_id))
        except index.DocumentNotFoundException:
            raise HTTPError(status_code=404)

    async def post(self, document_id):
        try:
            index.document_index.add(document_id, self.request.body.decode())
        except index.DocumentAlreadyExistsException:
            raise HTTPError(status_code=400)

    async def delete(self, document_id):
        try:
            index.document_index.remove(document_id)
        except index.DocumentNotFoundException:
            raise HTTPError(status_code=404)
