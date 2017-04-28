from tornado.web import url

from .handler import document, search


__all__ = ('url_list',)


url_list = (
    url(r'/document/(?P<document_id>.*)', document.DocumentHandler),
    url(r'/search', search.SearchHandler),
)
