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
    '/api/new/([a-zA-Z0-9-]+)$', 'api.UrlNew',
    '/([0-9a-zA-Z]+)', 'api.UrlRedirect',
    '/api/stat/([0-9a-zA-Z]+)', 'api.UrlStat',
    '/api/modify/([a-zA-Z0-9-]+)$', 'api.UrlModify',
    '/api/list/([0-9]+)/([0-9]+)$', 'api.UrlList',
)

class UrlNew:
    def POST(self, userurlkey=None):
        url=web.data()
        if len(url) > config.MAX_LEN_URL:
            web.ctx.status="400 Bad request"
            return "url too long"
        if userurlkey is not None:
            print userurlkey
            if len(userurlkey) < config.MIN_LEN_USERURLKEY:
                web.ctx.status="400 Bad request"
                return "key too short"
            if len(userurlkey) > config.MAX_LEN_URLKEY:
                web.ctx.status="400 Bad request"
                return "key too long"
            userurlkey = str.lower(utils.encode_string(userurlkey))
            
        url=utils.encode_string(url)
        if False == utils.check_url(url):
            web.ctx.status="400 Bad request"
            return "bad url"
            
        ret, n_affected, urlkey = model.url_new(url, userurlkey)
        if ret != 0:
            return web.internalerror("db error")

        retval = {
            "is_created": (n_affected==1 or True and False),
            "key": urlkey
        }
        web.ctx.status="200 OK"
        return json.dumps(retval)
    
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

        # update stats
        model.urlstat_total_incpv(urlkey)

        return web.redirect(url)

class UrlStat:
    def GET(self, urlkey):
        if len(urlkey) > config.MAX_LEN_URLKEY:
            web.ctx.status="400 Bad request"
            return "key too long"

        ret, stat=model.urlstat_total_get(str(urlkey))
        if ret != 0:
            return web.internalerror("db error")

        if stat is None:
            return web.notfound("")

        stat_info={
            "key" : stat.urlkey,
            "numpv" : stat.numpv,
            "dtlast" : stat.dtlast.strftime("%Y-%m-%d %H:%M:%S")
        }
        return json.dumps(stat_info)


class UrlModify:
    def POST(self, urlkey):
        url=web.data()
        if len(url) > config.MAX_LEN_URL:
            web.ctx.status="400 Bad request"
            return "url too long"
        if urlkey is not None:
            if len(urlkey) > config.MAX_LEN_URLKEY:
                web.ctx.status="400 Bad request"
                return "key too long"
            urlkey = str.lower(utils.encode_string(urlkey))
            
        url=utils.encode_string(url)
        if False == utils.check_url(url):
            web.ctx.status="400 Bad request"
            return "bad url"
            
        ret, n_affected = model.url_modify(urlkey, url)
        if ret != 0:
            return web.internalerror("db error")

        ret_val={ 'n_affected': n_affected}
        return json.dumps(ret_val)

class UrlList:
    def GET(self, offset=0, limit=100):
        ret, urllist=model.url_list(offset, limit)
        if ret != 0:
            return web.internalerror("db error")

        io = cStringIO.StringIO()
        io.write("[\n")
        for url in urllist:
            url['dt_created']=url['dt_created'].strftime('%Y-%m-%d %H:%M:%S')
            json.dump(url, io)
            io.write(",\n")
        out = io.getvalue()
        outdata = out[:-2]+'\n]'
        return outdata

