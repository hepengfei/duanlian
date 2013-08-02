# -*-mode:python; coding:utf-8-*-

import web
import MySQLdb

import config


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


def url_new(urlkey, url):
    try:
        db.insert('url', urlkey=urlkey, url=url)
    except MySQLdb.IntegrityError as err:
        return 0, 0
    except MySQLdb.Error as err:
        return get_errno(err), 0
    return 0, 1


def url_get(urlkey):
    try:
        results = db.select('url', where='urlkey=$urlkey', vars=locals())
    except MySQLdb.Error as err:
        return get_errno(err), None
    if len(results) > 0:
        return 0, results[0].url
    else:
        return 0, None

