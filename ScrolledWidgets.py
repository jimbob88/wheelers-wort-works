import tkinter as tk
import tkinter.ttk as ttk
from AutoScroll import _create_container, AutoScroll
from typing import List

class ScrolledListBox(AutoScroll, tk.Listbox):
	"""A standard Tkinter Text widget with scrollbars that will
	automatically show/hide as needed."""

	@_create_container
	def __init__(self, master, **kw):
		tk.Listbox.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)


class ScrolledText(AutoScroll, tk.Text):
	"""A standard Tkinter Text widget with scrollbars that will
	automatically show/hide as needed."""

	@_create_container
	def __init__(self, master, **kw):
		tk.Text.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)


class ScrolledTreeView(AutoScroll, ttk.Treeview):
	"""A standard ttk Treeview widget with scrollbars that will
	automatically show/hide as needed."""

	@_create_container
	def __init__(self, master, **kw):
		ttk.Treeview.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

	def insert(self, parent, index, iid=None, **kw):
		opts = ttk._format_optdict(kw)
		if iid is None:
			iid = "I{iid}".format(iid=format(len(self.get_children()) + 1, "03x"))

		return self.tk.call(self._w, "insert", parent, index, "-id", iid, *opts)

def set_treeview_selection(treeview, key: str, list_data: List, n: int):
	item = list_data[n]
	if item[0].lower() == key.lower():
		treeview.selection_set(
			"I{iid}".format(iid=format(n + 1, "03x"))
		)
		treeview.focus("I{iid}".format(iid=format(n + 1, "03x")))
		treeview.yview(n)
		return True
	treeview.yview(n)
	return False

def bind_treeview(key: str, treeview, list_data):
	"""
	Adapted from:
	https://mail.python.org/pipermail/python-list/2002-May/170135.html
	"""
	try:
		start_n = int(treeview.focus()[1:], 16) - 1
	except IndexError:
		start_n = -1
	# clear the selection.
	treeview.selection_clear()
	# start from previous selection +1
	for n in range(start_n + 1, len(list_data)):
		if set_treeview_selection(treeview, key, list_data, n):
			break
	else:
		# has not found it so loop from top
		for n, _ in enumerate(list_data):
			if set_treeview_selection(treeview, key, list_data, n):
				break
