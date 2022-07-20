import contextlib
import tkinter as tk
import tkinter.ttk as ttk
import platform

class AutoScroll(object):
    """Configure the scrollbars for a widget."""

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        with contextlib.suppress(BaseException):
            vsb = ttk.Scrollbar(master, orient="vertical", command=self.yview)
        hsb = ttk.Scrollbar(master, orient="horizontal", command=self.xview)

        # self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        with contextlib.suppress(BaseException):
            self.configure(yscrollcommand=self._autoscroll(vsb))
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky="nsew")
        with contextlib.suppress(BaseException):
            vsb.grid(column=1, row=0, sticky="ns")
        hsb.grid(column=0, row=1, sticky="ew")

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        methods = (
            tk.Pack.__dict__.keys()
            | tk.Grid.__dict__.keys()
            | tk.Place.__dict__.keys()
        )

        for meth in methods:
            if meth[0] != "_" and meth not in ("config", "configure"):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        """Hide and show scrollbar as needed."""

        def wrapped(first, last):
            """Wrap scrollbar hide/show"""
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)

        return wrapped

    def __str__(self):
        return str(self.first_tab)


def _create_container(func):
    """Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget."""

    def wrapped(cls, master, **kw):
        """Wrap container"""
        container = ttk.Frame(master)
        container.bind("<Enter>", lambda e: _bound_to_mousewheel(e, container))
        container.bind("<Leave>", lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)

    return wrapped


def _bound_to_mousewheel(event, widget):
    """Enable On mousewheel scroll move scrollbar"""
    child = widget.winfo_children()[0]
    if platform.system() in ["Windows", "Darwin"]:
        child.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, child))
        child.bind_all("<Shift-MouseWheel>", lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all("<Button-4>", lambda e: _on_mousewheel(e, child))
        child.bind_all("<Button-5>", lambda e: _on_mousewheel(e, child))
        child.bind_all("<Shift-Button-4>", lambda e: _on_shiftmouse(e, child))
        child.bind_all("<Shift-Button-5>", lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    """Disable On mousewheel scroll move scrollbar"""
    if platform.system() in ["Windows", "Darwin"]:
        widget.unbind_all("<MouseWheel>")
        widget.unbind_all("<Shift-MouseWheel>")
    else:
        widget.unbind_all("<Button-4>")
        widget.unbind_all("<Button-5>")
        widget.unbind_all("<Shift-Button-4>")
        widget.unbind_all("<Shift-Button-5>")




def _on_mousewheel(event, widget):
    """On mousewheel scroll move scrollbar"""
    if platform.system() == "Windows":
        widget.yview_scroll(-1 * int(event.delta / 120), "units")
    elif platform.system() == "Darwin":
        widget.yview_scroll(-1 * int(event.delta), "units")
    elif event.num == 4:
        widget.yview_scroll(-1, "units")
    elif event.num == 5:
        widget.yview_scroll(1, "units")

def _on_shiftmouse(event, widget):
    """On shift mousewheel scroll move scrollbar"""
    if platform.system() == "Windows":
        widget.xview_scroll(-1 * int(event.delta / 120), "units")
    elif platform.system() == "Darwin":
        widget.xview_scroll(-1 * int(event.delta), "units")
    elif event.num == 4:
        widget.xview_scroll(-1, "units")
    elif event.num == 5:
        widget.xview_scroll(1, "units")