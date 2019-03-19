# -*- coding: utf-8 -*-
from __future__ import with_statement
from __future__ import absolute_import
import sys
from io import open
import os
if sys.version_info >= (3, 0):
    import beer_engine
    from urllib.request import urlopen
else:
    import beer_engine2 as beer_engine
    from urllib2 import urlopen

def resource_path(relative_path):
	u""" Get absolute path to resource, works for dev and for PyInstaller """
	if __mode__ in [u'pyinstaller', u'local']:
		try:
			# PyInstaller creates a temp folder and stores path in _MEIPASS
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.abspath(u".")

		return os.path.join(base_path, relative_path)
	elif __mode__ == u'deb':
		if os.path.basename(relative_path) == u'logo.png':
			return u'/usr/include/wheelers-wort-works/logo.png'
		else:
			return os.path.join(os.path.expanduser(u'/usr/include/wheelers-wort-works'), relative_path)

__mode__ = u'local'
if __name__ == u'__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == u'--update':
            with open(resource_path(u'update.py'), u'r') as f:
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
