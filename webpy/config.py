
import web
web.DEBUG=True

MAX_LEN_URL=4096
MAX_LEN_URLKEY=64
MIN_LEN_USERURLKEY=5

USERURLKEY_MAP="[a-zA-Z0-9-]"

import baseany

BASE32_MAP="5f6stacpb4zjeh27kmux38wr9gydviqn"
BASE32=baseany.new(BASE32_MAP)


using_sae=True
using_sae=False

MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "duanlian"
MYSQL_USER = "root"
MYSQL_PASS = ""

if using_sae:
    import sae.const
    MYSQL_HOST = sae.const.MYSQL_HOST
    MYSQL_PORT = sae.const.MYSQL_PORT
    MYSQL_DB = sae.const.MYSQL_DB
    MYSQL_USER = sae.const.MYSQL_USER
    MYSQL_PASS = sae.const.MYSQL_PASS

