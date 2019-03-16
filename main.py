# -*- coding: utf-8 -*-
from __future__ import with_statement
from __future__ import absolute_import
import sys
from io import open
if sys.version_info >= (3, 0):
    import beer_engine
    from urllib.request import urlopen
else:
    import beer_engine2 as beer_engine
    from urllib2 import urlopen

__mode__ = u'local'
if __name__ == u'__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == u'--update':
            with open(u'update.py', u'r') as f:
                exec(f.read())
            update()
        elif sys.argv[1] == u'--coreupdate':
            with urlopen(u'https://raw.githubusercontent.com/jimbob88/wheelers-wort-works/master/update.py') as response:
                exec(response.read().decode(u'utf-8'))
            update()
        else:
            print(u'Run --update to update the current install, or run --coreupdate to update the updater script')
            exit()
    beer_engine.__mode__ = __mode__
    beer_engine.main()
