# -*-coding: utf-8-*-

import web
import model
import utils
import json
import cStringIO
import datetime
import config

urls = (
    '/api/new', 'api.UrlNew',
    '/([0-9a-zA-Z]+)', 'api.UrlRedirect',
)

class UrlNew:
    def POST(self):
        url=web.data()
        if len(url) > config.MAX_LEN_URL:
            web.ctx.status="400 Bad request"
            return "url too long"
            
        url=utils.encode_string(url)
        urlkey=utils.urlhash(url)
        ret, n_affected = model.url_new(urlkey, url)
        if ret != 0:
            return web.internalerror("db error")

        if n_affected == 0:
            web.ctx.status="200 OK"

        if n_affected == 1:
            web.ctx.status="201 Created"
        return urlkey
    
class UrlRedirect:
    def GET(self, urlkey):
        if len(urlkey) > config.MAX_LEN_URLKEY:
            web.ctx.status="400 Bad request"
            return "key too long"

        ret, url=model.url_get(str(urlkey))
        if ret != 0:
            return web.internalerror("db error")

        if url is None:
            return web.notfound("")

        return web.redirect(url)

