# -*- coding: utf-8 -*-
from __future__ import with_statement
from __future__ import absolute_import
import sys
import os
import argparse
from io import open
if sys.version_info >= (3, 0):
	import beer_engine
	from urllib.request import urlopen
else:
	from urllib2 import urlopen
	os.getcwd = os.getcwdu
import json
locale = 'en'
_ = json.load(open('lang.json', 'r'))[locale]

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
			return u'/usr/include/wheelers-wort-works-ce/logo.png'
		elif os.path.basename(relative_path) == u'commit.txt':
			return os.path.expanduser(u'~/.config/Wheelers-Wort-Works-ce/commit.txt')
		else:
			return os.path.join(os.path.expanduser(u'/usr/include/wheelers-wort-works-ce'), relative_path)

def get_args():
	parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument(u'-f', u'--file',
						required=False,
						action=u'store',
						default=None,
						help=_[u'The file to open `--file file_name.berf[x]`'])
	parser.add_argument(u'-L', u'--locale',
						required=False,
						action=u'store',
						default='en',
						help=_[u'Change the language [fr, en]'])
	parser.add_argument(u'-u', u'--update',
						required=False,
						action=u'store_true',
						help=_[u'Using the current `update.py`, download the latest GitHub files'])
	parser.add_argument(u'-U', u'--coreupdate',
						required=False,
						action=u'store_true',
						help=_[u'Pull `update.py` from GitHub, then download the latest GitHub files'])
	parser.add_argument(u'-l', u'--local',
						required=False,
						action=u'store_true',
						help=_['Use the local mode'])
	parser.add_argument(u'-d', u'--deb',
						required=False,
						action=u'store_true',
						help=_[u'Use the debian mode (only use on a Debian/Ubuntu system)'])

	args = parser.parse_args()
	return args

__mode__ = u'local'
if __name__ == u'__main__':
	args = get_args()
	if args.deb:
		__mode__ = u'deb'
	if args.local:
		__mode__ = u'local'
	update_available = False
	update = False
	try:
		with urlopen(u'https://github.com/jimbob88/wheelers-wort-works/tree/community_edition') as response:
			text =response.read().decode(u'utf-8')
			sec = (''.join(text[text.find(u'<a class="commit-tease-sha mr-1"'):].partition(u'</a>')[0:2]))
			commit = (sec.split(u'"')[3].split(u'/')[-1])
			if os.path.isfile(resource_path(u'commit.txt')):
				prev_commit = [line for line in open(resource_path(u'commit.txt'), 'r')][0]
			else:
				prev_commit = 0
			if prev_commit != commit:
				update = True
				update_available = True
			else:
				print('Already the Latest Edition')
	except:
		update = True


	if args.update or args.coreupdate:
		commit = commit if 'commit' in locals() or 'commit' in globals() else [line for line in open(resource_path(u'commit.txt'), 'r')][0]
		if args.update and update:
			with open(resource_path(u'update.py'), u'r') as f:
				exec(f.read())
			update()
			with open(resource_path(u'commit.txt'), 'w') as f:
				f.write(commit)
		if args.coreupdate and update:
			with urlopen(u'https://raw.githubusercontent.com/jimbob88/wheelers-wort-works/ce_lang_beta/update.py') as response:
				update_text = response.read().decode(u'utf-8')
				exec(update_text)
			update()
			print(u'Updating {file} from {url}'.format(file=u'update.py', url=u'https://raw.githubusercontent.com/jimbob88/wheelers-wort-works/ce_lang_beta/update.py'))
			with open(resource_path('update.py'), 'w') as f:
				f.write(update_text)
			with open(resource_path(u'commit.txt'), 'w') as f:
				f.write(commit)
		if __mode__ == 'deb': exit()
	if args.file != None:
		if os.path.splitext(args.file)[1] in [u'.berf', u'.berfx']:
			beer_engine.__mode__ = __mode__
			file = os.path.join(os.getcwd(), args.file) if not os.path.isfile(args.file) else os.path.expanduser(args.file)
			beer_engine.main(file=file, update_available=update_available, locale=args.locale)
	else:
		beer_engine.__mode__ = __mode__
		beer_engine.main(update_available=update_available, locale=args.locale)
