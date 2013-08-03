# -*-mode:python; coding:utf-8-*-

import web
import MySQLdb

import config
import utils


db = web.database(dbn='mysql',
                  host=config.MYSQL_HOST,
                  port=int(config.MYSQL_PORT),
                  db=config.MYSQL_DB,
                  user=config.MYSQL_USER, 
                  passwd=config.MYSQL_PASS)


def get_errno(err):
    print "mysql error: " + str(err)
    errno = -1
    try:
        errno = int(str(err)[1:10].split(',')[0])
    except:
        pass
    return errno

def urlid_new():
    try:
        db.query('delete from urlid')
        urlid = db.insert('urlid', seqname='urlid', urlid=0)
        return 0, urlid
    except MySQLdb.IntegrityError as err:
        return 0, 0
    except MySQLdb.Error as err:
        return get_errno(err), 0

# TODO: 没有处理key重复的情况，概率很小；重复时返回已存在，创建失败
def url_new(url, urlkey=None):
    try:
        if urlkey is None:
            ret, urlid = urlid_new()
            if ret != 0 or urlid == 0:
                return ret, 0, None
            urlkey=utils.idtostr(urlid)
        db.insert('url', seqname=False,
                  urlkey=urlkey, url=url,
                  dt_created=web.SQLLiteral("NOW()"))
        return 0, 1, urlkey
    except MySQLdb.IntegrityError as err:
        return 0, 0, None
    except MySQLdb.Error as err:
        return get_errno(err), 0, None

def url_modify(urlkey, url):
    try:
        affected = db.update('url', url=url,
                             dt_created=web.SQLLiteral("NOW()"),
                             where="urlkey=$urlkey",
                             vars=locals())
        return 0, affected
    except MySQLdb.Error as err:
        return get_errno(err), 0

def url_get(urlkey):
    try:
        results = db.select('url', where='urlkey=$urlkey', vars=locals())
        if len(results) > 0:
            return 0, results[0].url
        else:
            return 0, None
    except MySQLdb.Error as err:
        return get_errno(err), None


def url_list(offset, limit):
    try:
        results = db.select('url', offset=offset, limit=limit)
        return 0, results
    except MySQLdb.Error as err:
        return get_errno(err), None

def urlstat_total_incpv(urlkey):
    try:
        db.query("insert into urlstat_total set urlkey=$urlkey, numpv=1, dtlast=Now() on duplicate key update numpv=numpv+1, dtlast=Now()", vars=locals())
        return 0
    except MySQLdb.Error as err:
        return get_errno(err)

def urlstat_total_get(urlkey):
    try:
        results = db.select('urlstat_total', where='urlkey=$urlkey', vars=locals())
        if len(results) > 0:
            return 0, results[0]
        else:
            return 0, None
    except MySQLdb.Error as err:
        return get_errno(err), None
