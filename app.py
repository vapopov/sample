#!/usr/bin/env python

from tornado import httpserver
from tornado.ioloop import IOLoop
from tornado.web import Application

from apps.base.autodiscover import autodiscover
from apps.options import settings as app_settings


class TestApplication(Application):

    def __init__(self, **settings):
        # settings['debug'] = app_settings.DEBUG,
        settings['autoreload'] = app_settings.AUTORELOAD
        super().__init__(**settings)

    def init(self):
        url_list = tuple()
        for url_module in autodiscover('urls'):
            if 'url_list' in url_module.__dict__.keys():
                url_list += url_module.url_list
        self.add_handlers(".*$", url_list)


if __name__ == '__main__':
    app = TestApplication()
    http_server = httpserver.HTTPServer(app)
    http_server.bind(port=app_settings.PORT)
    http_server.start(1 if app_settings.DEBUG else 0)
    app.init()

    IOLoop.current().start()
