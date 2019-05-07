#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
import Tkinter as tk
import ttk
import tkFileDialog as filedialog
import tkMessageBox as messagebox
import sys
import brew_data
import platform
import math
import codecs
import string
import os
import webbrowser
import ast
from io import open
try:
	import bs4
except ImportError:
	pass

__mode__ = u'local'
_bgcolor = u'SystemButtonFace' if platform.system() == u'Windows' else u'#d9d9d9'
class beer_engine_mainwin(object):
	def __init__(self, master=None):

		_fgcolor = u'#000000'  # X11 color: 'black'
		_compcolor = u'#d9d9d9' # X11 color: 'gray85'
		_ana1color = u'#d9d9d9' # X11 color: 'gray85'
		_ana2color = u'#ececec' # Closest X11 color: 'gray92'
		font9 = u"-family {DejaVu Sans} -size 7 -weight normal -slant "  \
			u"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()

		if not os.path.isfile(resource_path(u'defaults.txt')):
			with open(resource_path(u'defaults.txt'), u'w') as f:
				volume = brew_data.constants[u'Volume']
				efficiency = brew_data.constants[u'Efficiency']*100
				evaporation = round((brew_data.constants[u'Boil Volume Scale']-1)*100, 1)
				LGratio = brew_data.constants[u'Liquor To Grist Ratio']
				attenuation = brew_data.constants[u'Attenuation Default']
				save_close = brew_data.constants[u'Save On Close']
				boil_time = brew_data.constants[u'Default Boil Time']
				replace_defaults = brew_data.constants[u'Replace Defaults']
				f.write(u'efficiency={efficiency}\nvolume={volume}\nevaporation={evaporation}\nLGratio={LGratio}\nattenuation={attenuation}\nsave_close={save_close}\nboil_time={boil_time}\nreplace_defaults={replace_defaults}'.format(efficiency=efficiency, volume=volume, evaporation=evaporation, LGratio=LGratio,
																																																										attenuation=attenuation, save_close=save_close, boil_time=boil_time, replace_defaults=replace_defaults))
		else:
			with open(resource_path(u'defaults.txt'), u'r') as f:
				data = [line.strip().split(u'=') for line in f]
				for constants in data:
					if constants[0] == u'efficiency': brew_data.constants[u'Efficiency'] = float(constants[1])/100
					elif constants[0] == u'volume': brew_data.constants[u'Volume'] = float(constants[1])
					elif constants[0] == u'evaporation': brew_data.constants[u'Boil Volume Scale'] = (float(constants[1])/100)+1
					elif constants[0] == u'LGratio': brew_data.constants[u'Liquor To Grist Ratio'] = float(constants[1])
					elif constants[0] == u'attenuation': brew_data.constants[u'Attenuation Default'] = constants[1]
					elif constants[0] == u'save_close': brew_data.constants[u'Save On Close'] = True if constants[1] == u'True' else False
					elif constants[0] == u'boil_time': brew_data.constants[u'Default Boil Time'] = int(constants[1])
					elif constants[0] == u'replace_defaults': brew_data.constants[u'Replace Defaults'] = True if constants[1] == u'True' else False

		if not os.path.isfile(resource_path(u'hop_data.txt')):
			with open(resource_path(u'hop_data.txt'), u'w') as f:
				for hop, value in brew_data.hop_data.items():
					name = hop
					hop_type = value[u'Form']
					origin = value[u'Origin']
					alpha = value[u'Alpha']
					use = value[u'Use']
					description = value[u'Description']
					f.write(u'{name}\t{hop_type}\t{origin}\t{alpha}\t{use}\t{description}\n'.format(name=name, hop_type=hop_type, origin=origin, alpha=alpha, use=use, description=description))
		else:
			with open(resource_path(u'hop_data.txt'), u'r') as f:
				if brew_data.constants[u'Replace Defaults']: brew_data.hop_data = {}
				data = [line.strip().split(u'\t') for line in f]
				for hop in data:
					# 'Nelson Sauvin': {'Form': 'Whole', 'Origin': 'New Zeland', 'Description': '', 'Use': 'General Purpose', 'Alpha': 12.7}
					name = hop[0]
					hop_type = hop[1]
					origin = hop[2]
					alpha = float(hop[3])
					use = hop[4]
					description = hop[5] if len(hop) >= 6 else u'No Description'
					brew_data.hop_data[name] = {u'Form': hop_type, u'Origin': origin, u'Alpha': alpha, u'Use': use, u'Description': description}
				#print('hop_data =', brew_data.hop_data)
		if not os.path.isfile(resource_path(u'grain_data.txt')):
			with open(resource_path(u'grain_data.txt'), u'w') as f:
				for ingredient, value in brew_data.grist_data.items():
					name = ingredient
					ebc = value[u'EBC']
					grain_type = value[u'Type']
					extract = value[u'Extract']
					moisture = value[u'Moisture']
					fermentability = value[u'Fermentability']
					description = value[u'Description']
					f.write(u'{name}\t{ebc}\t{grain_type}\t{extract}\t{moisture}\t{fermentability}\t{description}\n'.format(name=name, ebc=ebc, grain_type=grain_type, extract=extract, moisture=moisture, fermentability=fermentability, description=description))
		else:
			with open(resource_path(u'grain_data.txt'), u'r') as f:
				if brew_data.constants[u'Replace Defaults']: brew_data.grain_data = {}
				data = [line.strip().split(u'\t') for line in f]
				for ingredient in data:
					# {'Wheat Flour': {'EBC': 0.0, 'Type': 3.0, 'Extract': 304.0, 'Description': 'No Description', 'Moisture': 11.0, 'Fermentability': 62.0}}
					name = ingredient[0]
					ebc = float(ingredient[1])
					grain_type = float(ingredient[2])
					extract = float(ingredient[3])
					moisture = float(ingredient[4])
					fermentability = float(ingredient[5])
					description = ingredient[6]
					brew_data.grist_data[name] = {u'EBC': ebc, u'Type': grain_type, u'Extract': extract, u'Description': description, u'Moisture': moisture, u'Fermentability': fermentability}
				#print('grist_data =', brew_data.grist_data)

		if not os.path.isfile(resource_path(u'yeast_data.txt')):
			with open(resource_path(u'yeast_data.txt'), u'w') as f:
				if brew_data.constants[u'Replace Defaults']: brew_data.yeast_data = {}
				for yeast, value in brew_data.yeast_data.items():
					name = yeast
					yeast_type = value[u'Type']
					lab = value[u'Lab']
					flocculation = value[u'Flocculation']
					attenuation = value[u'Attenuation']
					temperature = value[u'Temperature']
					origin = value[u'Origin']
					description = value[u'Description']
					f.write(u'{name}\t{yeast_type}\t{lab}\t{flocculation}\t{attenuation}\t{temperature}\t{origin}\t{description}\n'.format(name=name, yeast_type=yeast_type, lab=lab, flocculation=flocculation, attenuation=attenuation, temperature=temperature, origin=origin, description=description))
		else:
			with open(resource_path(u'yeast_data.txt'), u'r') as f:
				data = [line.strip().split(u'\t') for line in f]
				for yeast in data:
					name = yeast[0]
					yeast_type = yeast[1]
					lab = yeast[2]
					flocculation = yeast[3]
					attenuation = yeast[4]
					temperature = yeast[5]
					origin = yeast[6]
					description = yeast[7]
					brew_data.yeast_data[name] = {u'Type': yeast_type, u'Lab': lab, u'Flocculation': flocculation, u'Attenuation': attenuation, u'Temperature': temperature, u'Description': description, u'Origin': origin}

		if not os.path.isfile(resource_path(u'water_chem_data.txt')):
			with open(resource_path(u'water_chem_data.txt'), u'w') as f:
				for water_chem, values in brew_data.water_chemistry_additions.items():
					value = values[u'Values']
					name = water_chem
					time = value[u'Time'] if u'Time' in value else u'N/A'
					#print(value)
					water_chem_type = value[u'Type']
					f.write(u'{name}\t{time}\t{water_chem_type}\n'.format(name=name, time=time, water_chem_type=water_chem_type))
		else:
			with open(resource_path(u'water_chem_data.txt'), u'r') as f:
				if brew_data.constants[u'Replace Defaults']: brew_data.water_chemistry_additions = {}
				data = [line.strip().split(u'\t') for line in f]
				for water_chem in data:
					name = water_chem[0]
					time = float(water_chem[1]) if water_chem[1] != u'N/A' else water_chem[1]
					water_chem_type = water_chem[2]
					brew_data.water_chemistry_additions[name] = {u'Values': {u'Type': water_chem_type}}
					if time != u'N/A': brew_data.water_chemistry_additions[name][u'Values'][u'Time'] = time


		self.style.configure(u'.',background=_bgcolor)
		self.style.configure(u'.',foreground=_fgcolor)
		self.style.configure(u'.',font=u"TkDefaultFont")
		self.style.map(u'.',background=
			[(u'selected', _compcolor), (u'active',_ana2color)])

		self.current_file = u''
		self.master = master
		self.master.protocol(u"WM_DELETE_WINDOW", self.quit)
		self.master.tk.call(u'wm', u'iconphoto', self.master._w, tk.PhotoImage(file=resource_path(u'logo.png')))
		self.master.geometry(u"800x480+674+369")
		self.master.title(u"Wheeler's Wort Works")
		self.master.configure(highlightcolor=u"black")
		self.master.resizable(0, 0)
		self.tabbed_frame = ttk.Notebook(self.master)

		self.first_tab = tk.Frame(self.tabbed_frame)
		self.second_tab = hops_editor(self.tabbed_frame)
		self.third_tab = grist_editor(self.tabbed_frame)
		self.fourth_tab = yeast_editor(self.tabbed_frame)
		self.fifth_tab = defaults_editor(self.tabbed_frame)
		self.sixth_tab = special_editor(self.tabbed_frame)
		self.seventh_tab = notes_area(self.tabbed_frame)
		self.tabbed_frame.add(self.first_tab, text=u"Engine Room")
		self.tabbed_frame.add(self.second_tab, text=u"Hop Editor")
		self.tabbed_frame.add(self.third_tab, text=u"Grist Editor")
		self.tabbed_frame.add(self.fourth_tab, text=u"Yeast Editor")
		self.tabbed_frame.add(self.fifth_tab, text=u"Defaults Editor")
		self.tabbed_frame.add(self.sixth_tab, text=u"Experimental Attenuation")
		self.tabbed_frame.add(self.seventh_tab, text=u"Notes Area")
		self.tabbed_frame.grid(row=0, column=0, sticky=u'nsew')
		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)

		######################### Menu ############################
		self.menubar = tk.Menu(self.master,font=u"TkMenuFont",bg=_bgcolor,fg=_fgcolor)
		self.master.configure(menu = self.menubar)

		self.file_menu = tk.Menu(self.master,tearoff=0)
		self.menubar.add_cascade(menu=self.file_menu,
				activebackground=u"#ececec",
				activeforeground=u"#000000",
				 background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"File")
		self.sub_menu1 = tk.Menu(self.master,tearoff=0)
		self.file_menu.add_command(activebackground=u"#ececec",
				activeforeground=u"#000000",
				 background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"Open",
				command=lambda: self.open_file(filedialog.askopenfilename(initialdir = os.path.expanduser(u'~/.config/Wheelers-Wort-Works/recipes/' if __mode__ == u'deb' else u'.'), title = u"Select file", filetypes = ((u"BERF",u"*.berf *.berfx"), (u"all files",u"*.*")))),
				accelerator=u"Ctrl+O")

		self.master.bind(u"<Control-o>", lambda e: self.open_file(filedialog.askopenfilename(initialdir = os.path.expanduser(u'~/.config/Wheelers-Wort-Works/recipes/' if __mode__ == u'deb' else u'.'), title = u"Select file", filetypes = ((u"BERF",u"*.berf *.berfx"), (u"all files",u"*.*")))))

		self.file_menu.add_command(activebackground=u"#ececec",
				activeforeground=u"#000000",
				 background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"Save",
				command=self.save,
				accelerator=u"Ctrl+S")
		self.master.bind(u"<Control-s>", lambda e: self.save())
		self.file_menu.add_command(activebackground=u"#ececec",
				activeforeground=u"#000000",
				 background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"Save All",
				command=self.save_all,
				accelerator=u"Ctrl+A")
		self.master.bind(u"<Control-a>", lambda e: self.save_all())
		self.file_menu.add_command(activebackground=u"#ececec",
				activeforeground=u"#000000",
				 background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"Save As",
				command=lambda: self.save_file(filedialog.asksaveasfilename(initialdir = os.path.expanduser(u'~/.config/Wheelers-Wort-Works/recipes/' if __mode__ == u'deb' else u'.'),title = u"Select file", defaultextension=u".berfx", initialfile=u'{0}.berf'.format(self.recipe_name_ent.get()))),
				accelerator=u"Ctrl+Shift+S")
		self.master.bind(u"<Control-S>", lambda e: self.save_file(filedialog.asksaveasfilename(initialdir = os.path.expanduser(u'~/.config/Wheelers-Wort-Works/recipes/' if __mode__ == u'deb' else u'.'),title = u"Select file", defaultextension=u".berf", initialfile=u'{0}.berf'.format(self.recipe_name_ent.get()))))
		self.file_menu.add_cascade(menu=self.sub_menu1,
				activebackground=u"#ececec",
				activeforeground=u"#000000",
				 background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"Print")
		self.sub_menu1.add_command(
				activebackground=u"#ececec",
				activeforeground=u"#000000",
				 background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"Simple HTML",
				command=self.create_html,
				accelerator=u"Ctrl+P")
		self.master.bind(u"<Control-p>", lambda e: self.create_html())
		self.sub_menu1.add_command(
				activebackground=u"#ececec",
				activeforeground=u"#000000",
				 background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"Complex HTML",
				command=self.create_complex_html,
				accelerator=u"Ctrl+Shift+P")
		self.master.bind(u"<Control-P>", lambda e: self.create_complex_html())

		self.file_menu.add_command(
				activebackground=u"#ececec",
				activeforeground=u"#000000",
				 background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"Quit",
				command=self.quit,
				accelerator=u"Ctrl+Q")
		self.master.bind(u"<Control-q>", lambda e: self.quit())

		self.help_menu = tk.Menu(self.master,tearoff=0)
		self.menubar.add_cascade(menu=self.help_menu,
				activebackground=u"#ececec",
				activeforeground=u"#000000",
				 background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"Help")
		self.help_menu.add_command(
				activebackground=u"#ececec",
				activeforeground=u"#000000",
				background=_bgcolor,
				font=u"TkMenuFont",
				foreground=u"#000000",
				label=u"Wheeler's Wort Works Help",
				command=lambda: webbrowser.open_new(u'https://github.com/jimbob88/wheelers-wort-works/wiki'),
				accelerator=u"Ctrl+H")
		self.master.bind(u"<Control-h>", lambda e: webbrowser.open_new(u'https://github.com/jimbob88/wheelers-wort-works/wiki'))

		######################## First Tab ########################
		self.first_tab.configure(background=_bgcolor)
		self.recipe_name_ent = tk.Entry(self.first_tab)
		self.recipe_name_ent.place(relx=0.126, rely=0.021, height=23
				, relwidth=0.28)
		self.recipe_name_ent.configure(background=u"white")
		self.recipe_name_ent.configure(font=u"TkFixedFont")
		self.recipe_name_ent.configure(selectbackground=u"#c4c4c4")
		self.recipe_name_ent.configure(justify=u'center')
		self.recipe_name_ent.insert(0, u'No Name')

		self.recipe_name_lbl = tk.Label(self.first_tab)
		self.recipe_name_lbl.place(relx=0.013, rely=0.021, height=18, width=90)
		self.recipe_name_lbl.configure(activebackground=u"#f9f9f9")
		self.recipe_name_lbl.configure(background=_bgcolor)
		self.recipe_name_lbl.configure(text=u'''Recipe Name:''')

		self.volume_lbl = tk.Label(self.first_tab)
		self.volume_lbl.place(relx=0.417, rely=0.021, height=18, width=53)
		self.volume_lbl.configure(activebackground=u"#f9f9f9")
		self.volume_lbl.configure(background=_bgcolor)
		self.volume_lbl.configure(text=u'''Volume:''')

		self.volume = tk.StringVar()
		self.volume_ent = tk.Entry(self.first_tab)
		self.volume_ent.place(relx=0.492, rely=0.021, height=23, width=55) #relwidth=0.045
		self.volume_ent.configure(background=u"white")
		self.volume_ent.configure(font=u"TkFixedFont")
		self.volume_ent.configure(selectbackground=u"#c4c4c4")
		self.volume_ent.configure(justify=u'center')
		self.volume_ent.configure(validate=u"focusout")
		self.volume_ent.configure(textvariable=self.volume)
		self.volume_ent.configure(validatecommand=lambda: self.boil_vol.set(round(float(self.volume.get())*brew_data.constants[u'Boil Volume Scale'], 2)))
		self.volume_ent.bind(u'<Return>', lambda event: self.boil_vol.set(round(float(self.volume.get())*brew_data.constants[u'Boil Volume Scale'], 2)))
		self.volume_ent.insert(0, unicode(brew_data.constants[u'Volume']))

		self.boil_volume_lbl = tk.Label(self.first_tab)
		self.boil_volume_lbl.place(relx=0.571, rely=0.021, height=18, width=85)
		self.boil_volume_lbl.configure(text=u'''Boil Volume:''')
		self.boil_volume_lbl.configure(background=_bgcolor)

		self.boil_vol = tk.StringVar()
		self.boil_volume_ent = tk.Entry(self.first_tab)
		self.boil_volume_ent.place(relx=0.682, rely=0.021,height=23, relwidth=0.058)
		self.boil_volume_ent.configure(background=u"white")
		self.boil_volume_ent.configure(font=u"TkFixedFont")
		self.boil_volume_ent.configure(width=46)
		self.boil_volume_ent.configure(justify=u'center')
		self.boil_volume_ent.configure(textvariable=self.boil_vol)
		self.boil_vol.set(unicode(brew_data.constants[u'Volume']*brew_data.constants[u'Boil Volume Scale']))
		self.ingredient_rem_butt = tk.Button(self.first_tab)
		self.ingredient_rem_butt.place(relx=0.013, rely=0.402, height=29
				, width=76)
		self.ingredient_rem_butt.configure(activebackground=u"#f9f9f9")
		self.ingredient_rem_butt.configure(background=_bgcolor)
		self.ingredient_rem_butt.configure(cursor=u"X_cursor")
		self.ingredient_rem_butt.configure(text=u'''Remove''')
		self.ingredient_rem_butt.configure(command=self.delete_ingredient)

		self.ingredient_add_new_butt = tk.Button(self.first_tab)
		self.ingredient_add_new_butt.place(relx=0.606, rely=0.085, height=28
				, width=82)
		self.ingredient_add_new_butt.configure(activebackground=u"#f9f9f9")
		self.ingredient_add_new_butt.configure(background=_bgcolor)
		self.ingredient_add_new_butt.configure(text=u'''Add New''')
		self.ingredient_add_new_butt.configure(command=self.add_grist)

		self.adjust_weight_ing_lbl = tk.Label(self.first_tab)
		self.adjust_weight_ing_lbl.place(relx=0.606, rely=0.169, height=14
				, width=91)
		self.adjust_weight_ing_lbl.configure(activebackground=u"#f9f9f9")
		self.adjust_weight_ing_lbl.configure(background=_bgcolor)
		self.adjust_weight_ing_lbl.configure(font=font9)
		self.adjust_weight_ing_lbl.configure(text=u'''Adjust Weight''')

		self.add_1000g_ing_butt = tk.Button(self.first_tab)
		self.add_1000g_ing_butt.place(relx=0.606, rely=0.211, height=28
				, width=45)
		self.add_1000g_ing_butt.configure(activebackground=u"#f9f9f9")
		self.add_1000g_ing_butt.configure(background=_bgcolor)
		self.add_1000g_ing_butt.configure(text=u'''+1Kg''')
		self.add_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(1000))
		self.add_1000g_ing_butt.configure(font=u"TkFixedFont")

		self.add_100g_ing_butt = tk.Button(self.first_tab)
		self.add_100g_ing_butt.place(relx=0.606, rely=0.275, height=28, width=45)
		self.add_100g_ing_butt.configure(activebackground=u"#f9f9f9")
		self.add_100g_ing_butt.configure(background=_bgcolor)
		self.add_100g_ing_butt.configure(text=u'''+100g''')
		self.add_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(100))
		self.add_100g_ing_butt.configure(font=u"TkFixedFont")

		self.rem_1000g_ing_butt = tk.Button(self.first_tab)
		self.rem_1000g_ing_butt.place(relx=0.669, rely=0.211, height=28
				, width=45)
		self.rem_1000g_ing_butt.configure(activebackground=u"#f9f9f9")
		self.rem_1000g_ing_butt.configure(background=_bgcolor)
		self.rem_1000g_ing_butt.configure(text=u'''-1Kg''')
		self.rem_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-1000))
		self.rem_1000g_ing_butt.configure(font=u"TkFixedFont")

		self.rem_100g_ing_butt = tk.Button(self.first_tab)
		self.rem_100g_ing_butt.place(relx=0.669, rely=0.275, height=28, width=45)
		self.rem_100g_ing_butt.configure(activebackground=u"#f9f9f9")
		self.rem_100g_ing_butt.configure(background=_bgcolor)
		self.rem_100g_ing_butt.configure(text=u'''-100g''')
		self.rem_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-100))
		self.rem_100g_ing_butt.configure(font=u"TkFixedFont")

		self.add_10g_ing_butt = tk.Button(self.first_tab)
		self.add_10g_ing_butt.place(relx=0.606, rely=0.338, height=28, width=45)
		self.add_10g_ing_butt.configure(activebackground=u"#f9f9f9")
		self.add_10g_ing_butt.configure(background=_bgcolor)
		self.add_10g_ing_butt.configure(text=u'''+10g''')
		self.add_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(10))
		self.add_10g_ing_butt.configure(font=u"TkFixedFont")

		self.rem_10g_ing_butt = tk.Button(self.first_tab)
		self.rem_10g_ing_butt.place(relx=0.669, rely=0.338, height=28, width=45)
		self.rem_10g_ing_butt.configure(activebackground=u"#f9f9f9")
		self.rem_10g_ing_butt.configure(background=_bgcolor)
		self.rem_10g_ing_butt.configure(text=u'''-10g''')
		self.rem_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-10))
		self.rem_10g_ing_butt.configure(font=u"TkFixedFont")

		self.add_1g_ing_butt = tk.Button(self.first_tab)
		self.add_1g_ing_butt.place(relx=0.606, rely=0.402, height=28, width=45)
		self.add_1g_ing_butt.configure(activebackground=u"#f9f9f9")
		self.add_1g_ing_butt.configure(background=_bgcolor)
		self.add_1g_ing_butt.configure(text=u'''+1g''')
		self.add_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(1))
		self.add_1g_ing_butt.configure(font=u"TkFixedFont")

		self.rem_1g_ing_butt = tk.Button(self.first_tab)
		self.rem_1g_ing_butt.place(relx=0.669, rely=0.402, height=28, width=45)
		self.rem_1g_ing_butt.configure(activebackground=u"#f9f9f9")
		self.rem_1g_ing_butt.configure(background=_bgcolor)
		self.rem_1g_ing_butt.configure(text=u'''-1g''')
		self.rem_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-1))
		self.rem_1g_ing_butt.configure(font=u"TkFixedFont")

		self.original_gravity_lbl = tk.Label(self.first_tab)
		self.original_gravity_lbl.place(relx=0.72, rely=0.085, height=14
				, width=79)
		self.original_gravity_lbl.configure(activebackground=u"#f9f9f9")
		self.original_gravity_lbl.configure(background=_bgcolor)
		self.original_gravity_lbl.configure(font=font9)
		self.original_gravity_lbl.configure(text=u'''Original Gravity''')

		self.original_gravity_ent = tk.Entry(self.first_tab)
		self.original_gravity_ent.place(relx=0.745, rely=0.127, height=20, width=18
				, relwidth=0.058)
		self.original_gravity_ent.configure(background=u"white")
		self.original_gravity_ent.configure(font=u"TkFixedFont")
		self.original_gravity_ent.configure(selectbackground=u"#c4c4c4")
		self.original_gravity_ent.configure(justify=u'center')
		self.ingredient_zero_butt = tk.Button(self.first_tab)
		self.ingredient_zero_butt.place(relx=0.745, rely=0.211, height=29
				, width=55)
		self.ingredient_zero_butt.configure(activebackground=u"#f9f9f9")
		self.ingredient_zero_butt.configure(background=_bgcolor)
		self.ingredient_zero_butt.configure(text=u'''Zero''')
		self.ingredient_zero_butt.configure(command=self.zero_ingredients)

		self.recalc_butt = tk.Button(self.first_tab)
		self.recalc_butt.place(relx=0.859, rely=0.042, height=29, width=97)
		self.recalc_butt.configure(activebackground=u"#f9f9f9")
		self.recalc_butt.configure(background=_bgcolor)
		self.recalc_butt.configure(text=u'''Recalculate''')
		self.recalc_butt.configure(command=self.recalculate)

		self.calculation_frame = ttk.Labelframe(self.first_tab)
		self.calculation_frame.place(relx=0.833, rely=0.106, relheight=0.391
				, relwidth=0.152)
		self.calculation_frame.configure(relief=u'sunken')
		self.calculation_frame.configure(text=u'''Calculation''')
		self.calculation_frame.configure(underline=u"0")
		self.calculation_frame.configure(relief=u'sunken')
		self.calculation_frame.grid_rowconfigure(0, weight=1)
		self.calculation_frame.grid_columnconfigure(0, weight=1)

		# self.calc_lbl = tk.Message(self.calculation_frame)
		# self.calc_lbl.grid(row=0, column=0, pady=5,padx=5)
		# self.calc_lbl.configure(background=_bgcolor)
		# self.calc_lbl.configure(foreground="#000000")
		# self.calc_lbl.configure(font=(None, 7))
		# self.calc_lbl.configure(relief='flat')
		# #self.calc_lbl.configure(anchor='nw')
		# self.calc_lbl.configure(text='''Efficiency: {efficiency}%
		# Final Gravity: {final_gravity}
		# Alcohol (ABV): {abv}
		# Colour: {colour}EBC
		# Mash Liquor: {mash_liquor}L
		# IBU:GU: {ibu_gu}'''.format(efficiency=brew_data.constants['Efficiency']*100, final_gravity=1.000, abv=0, colour=0, mash_liquor=0, ibu_gu=0))
		# #self.calc_lbl.configure(width=97)

		self.calc_lbl = tk.Text(self.calculation_frame)
		self.calc_lbl.grid(row=0, column=0, pady=5,padx=5)
		self.calc_lbl.configure(background=_bgcolor)
		self.calc_lbl.configure(foreground=u"#000000")
		self.calc_lbl.configure(font=(None, 7))
		self.calc_lbl.configure(relief=u'flat', wrap=tk.WORD)
		#self.calc_lbl.configure(anchor='nw')
		default_text = u'''Efficiency: {efficiency}%{enter}Final Gravity: {final_gravity}{enter}Alcohol (ABV): {abv}{enter}Colour: {colour}EBC{enter}Mash Liquor: {mash_liquor}L{enter}IBU:GU: {ibu_gu}'''.format(efficiency=brew_data.constants[u'Efficiency']*100, final_gravity=1.000, abv=0, colour=0, mash_liquor=0, ibu_gu=0, enter=u'\n\n')

		self.calc_lbl.insert(u'end', default_text)
		self.calc_lbl.configure(state=u'disabled')
		#self.calc_lbl.configure(width=97)

		self.hop_add_new_butt = tk.Button(self.first_tab)
		self.hop_add_new_butt.place(relx=0.707, rely=0.507, height=29, width=80)
		self.hop_add_new_butt.configure(activebackground=u"#f9f9f9")
		self.hop_add_new_butt.configure(background=_bgcolor)
		self.hop_add_new_butt.configure(text=u'''Add Hop''')
		self.hop_add_new_butt.configure(command=self.add_hop)

		self.adjust_weight_hop_lbl = tk.Label(self.first_tab)
		self.adjust_weight_hop_lbl.place(relx=0.72, rely=0.592, height=14
				, width=91)
		self.adjust_weight_hop_lbl.configure(activebackground=u"#f9f9f9")
		self.adjust_weight_hop_lbl.configure(background=_bgcolor)
		self.adjust_weight_hop_lbl.configure(font=font9)
		self.adjust_weight_hop_lbl.configure(text=u'''Adjust Weight''')

		self.add_100g_hop_butt = tk.Button(self.first_tab)
		self.add_100g_hop_butt.place(relx=0.72, rely=0.634, height=28, width=45)
		self.add_100g_hop_butt.configure(activebackground=u"#f9f9f9")
		self.add_100g_hop_butt.configure(background=_bgcolor)
		self.add_100g_hop_butt.configure(text=u'''+100g''')
		self.add_100g_hop_butt.configure(command=lambda: self.add_weight_hops(100))
		self.add_100g_hop_butt.configure(font=u"TkFixedFont")

		self.rem_100g_hop_butt = tk.Button(self.first_tab)
		self.rem_100g_hop_butt.place(relx=0.783, rely=0.634, height=28, width=45)
		self.rem_100g_hop_butt.configure(activebackground=u"#f9f9f9")
		self.rem_100g_hop_butt.configure(background=_bgcolor)
		self.rem_100g_hop_butt.configure(text=u'''-100g''')
		self.rem_100g_hop_butt.configure(command=lambda: self.add_weight_hops(-100))
		self.rem_100g_hop_butt.configure(font=u"TkFixedFont")

		self.add_25g_hop_butt = tk.Button(self.first_tab)
		self.add_25g_hop_butt.place(relx=0.72, rely=0.698, height=28, width=45)
		self.add_25g_hop_butt.configure(activebackground=u"#f9f9f9")
		self.add_25g_hop_butt.configure(background=_bgcolor)
		self.add_25g_hop_butt.configure(text=u'''+25g''')
		self.add_25g_hop_butt.configure(command=lambda: self.add_weight_hops(25))
		self.add_25g_hop_butt.configure(font=u"TkFixedFont")

		self.rem_25g_hop_butt = tk.Button(self.first_tab)
		self.rem_25g_hop_butt.place(relx=0.783, rely=0.698, height=28, width=45)
		self.rem_25g_hop_butt.configure(activebackground=u"#f9f9f9")
		self.rem_25g_hop_butt.configure(background=_bgcolor)
		self.rem_25g_hop_butt.configure(text=u'''-25g''')
		self.rem_25g_hop_butt.configure(command=lambda: self.add_weight_hops(-25))
		self.rem_25g_hop_butt.configure(font=u"TkFixedFont")

		self.add_10g_hop_butt = tk.Button(self.first_tab)
		self.add_10g_hop_butt.place(relx=0.72, rely=0.761, height=28, width=45)
		self.add_10g_hop_butt.configure(activebackground=u"#f9f9f9")
		self.add_10g_hop_butt.configure(background=_bgcolor)
		self.add_10g_hop_butt.configure(text=u'''+10g''')
		self.add_10g_hop_butt.configure(command=lambda: self.add_weight_hops(10))
		self.add_10g_hop_butt.configure(font=u"TkFixedFont")

		self.rem_10g_hop_butt = tk.Button(self.first_tab)
		self.rem_10g_hop_butt.place(relx=0.783, rely=0.761, height=28, width=45)
		self.rem_10g_hop_butt.configure(activebackground=u"#f9f9f9")
		self.rem_10g_hop_butt.configure(background=_bgcolor)
		self.rem_10g_hop_butt.configure(text=u'''-10g''')
		self.rem_10g_hop_butt.configure(command=lambda: self.add_weight_hops(-10))
		self.rem_10g_hop_butt.configure(font=u"TkFixedFont")

		self.add_1g_hop_butt = tk.Button(self.first_tab)
		self.add_1g_hop_butt.place(relx=0.72, rely=0.825, height=28, width=45)
		self.add_1g_hop_butt.configure(activebackground=u"#f9f9f9")
		self.add_1g_hop_butt.configure(background=_bgcolor)
		self.add_1g_hop_butt.configure(text=u'''+1g''')
		self.add_1g_hop_butt.configure(command=lambda: self.add_weight_hops(1))
		self.add_1g_hop_butt.configure(font=u"TkFixedFont")

		self.rem_1g_hop_butt = tk.Button(self.first_tab)
		self.rem_1g_hop_butt.place(relx=0.783, rely=0.825, height=28, width=45)
		self.rem_1g_hop_butt.configure(activebackground=u"#f9f9f9")
		self.rem_1g_hop_butt.configure(background=_bgcolor)
		self.rem_1g_hop_butt.configure(text=u'''-1g''')
		self.rem_1g_hop_butt.configure(command=lambda: self.add_weight_hops(-1))
		self.rem_1g_hop_butt.configure(font=u"TkFixedFont")

		self.hop_zero_butt = tk.Button(self.first_tab)
		self.hop_zero_butt.place(relx=0.859, rely=0.634, height=28, width=55)
		self.hop_zero_butt.configure(activebackground=u"#f9f9f9")
		self.hop_zero_butt.configure(background=_bgcolor)
		self.hop_zero_butt.configure(text=u'''Zero''')
		self.hop_zero_butt.configure(command=self.zero_hops)

		self.bitterness_ibu_lbl = tk.Label(self.first_tab)
		self.bitterness_ibu_lbl.place(relx=0.846, rely=0.507, height=14
				, width=79)
		self.bitterness_ibu_lbl.configure(activebackground=u"#f9f9f9")
		self.bitterness_ibu_lbl.configure(background=_bgcolor)
		self.bitterness_ibu_lbl.configure(font=font9)
		self.bitterness_ibu_lbl.configure(text=u'''Bitterness IBU''')

		self.bitterness_ibu_ent = tk.Entry(self.first_tab)
		self.bitterness_ibu_ent.place(relx=0.859, rely=0.55, height=20, width=18
				, relwidth=0.058)
		self.bitterness_ibu_ent.configure(background=u"white")
		self.bitterness_ibu_ent.configure(font=u"TkFixedFont")
		self.bitterness_ibu_ent.configure(selectbackground=u"#c4c4c4")
		self.bitterness_ibu_ent.configure(justify=u'center')

		self.hop_rem_butt = tk.Button(self.first_tab)
		self.hop_rem_butt.place(relx=0.013, rely=0.825, height=28, width=76)
		self.hop_rem_butt.configure(activebackground=u"#f9f9f9")
		self.hop_rem_butt.configure(background=_bgcolor)
		self.hop_rem_butt.configure(cursor=u"X_cursor")
		self.hop_rem_butt.configure(text=u'''Remove''')
		self.hop_rem_butt.configure(command=self.delete_hop)

		self.quit_btt = tk.Button(self.first_tab)
		self.quit_btt.place(relx=0.922, rely=0.93, height=29, width=53)
		self.quit_btt.configure(activebackground=u"#f9f9f9")
		self.quit_btt.configure(background=_bgcolor)
		self.quit_btt.configure(text=u'''Quit''')
		self.quit_btt.configure(command=self.quit)

		self.add_time_butt_1 = tk.Button(self.first_tab)
		self.add_time_butt_1.place(relx=0.426, rely=0.825, height=28
				, width=78)
		self.add_time_butt_1.configure(activebackground=u"#f9f9f9")
		self.add_time_butt_1.configure(background=_bgcolor)
		self.add_time_butt_1.configure(text=u'''Time +1''')
		self.add_time_butt_1.configure(command=lambda: self.add_time(1))

		self.rem_time_butt_1 = tk.Button(self.first_tab)
		self.rem_time_butt_1.place(relx=0.426, rely=0.888, height=28
				, width=78)
		self.rem_time_butt_1.configure(activebackground=u"#f9f9f9")
		self.rem_time_butt_1.configure(background=_bgcolor)
		self.rem_time_butt_1.configure(text=u'''Time -1''')
		self.rem_time_butt_1.configure(command=lambda: self.add_time(-1))

		self.add_time_butt_10 = tk.Button(self.first_tab)
		self.add_time_butt_10.place(relx=0.328, rely=0.825, height=28
				, width=78)
		self.add_time_butt_10.configure(activebackground=u"#f9f9f9")
		self.add_time_butt_10.configure(background=_bgcolor)
		self.add_time_butt_10.configure(text=u'''Time +10''')
		self.add_time_butt_10.configure(command=lambda: self.add_time(10))

		self.rem_time_butt_10 = tk.Button(self.first_tab)
		self.rem_time_butt_10.place(relx=0.328, rely=0.888, height=28
				, width=78)
		self.rem_time_butt_10.configure(activebackground=u"#f9f9f9")
		self.rem_time_butt_10.configure(background=_bgcolor)
		self.rem_time_butt_10.configure(text=u'''Time -10''')
		self.rem_time_butt_10.configure(command=lambda: self.add_time(-10))

		self.add_alpha_butt_pt1 = tk.Button(self.first_tab)
		self.add_alpha_butt_pt1.place(relx=0.129, rely=0.825, height=29
				, width=78)
		self.add_alpha_butt_pt1.configure(activebackground=u"#f9f9f9")
		self.add_alpha_butt_pt1.configure(background=_bgcolor)
		self.add_alpha_butt_pt1.configure(text=u'''Alpha +0.1''')
		self.add_alpha_butt_pt1.configure(command=lambda: self.add_alpha(0.1))

		self.rem_alpha_butt_pt1 = tk.Button(self.first_tab)
		self.rem_alpha_butt_pt1.place(relx=0.129, rely=0.888, height=28
				, width=78)
		self.rem_alpha_butt_pt1.configure(activebackground=u"#f9f9f9")
		self.rem_alpha_butt_pt1.configure(background=_bgcolor)
		self.rem_alpha_butt_pt1.configure(text=u'''Alpha -0.1''')
		self.rem_alpha_butt_pt1.configure(command=lambda: self.add_alpha(-0.1))

		self.add_alpha_butt_1 = tk.Button(self.first_tab)
		self.add_alpha_butt_1.place(relx=0.227, rely=0.825, height=29
				, width=76)
		self.add_alpha_butt_1.configure(activebackground=u"#f9f9f9")
		self.add_alpha_butt_1.configure(background=_bgcolor)
		self.add_alpha_butt_1.configure(text=u'''Alpha +1''')
		self.add_alpha_butt_1.configure(width=76)
		self.add_alpha_butt_1.configure(command=lambda: self.add_alpha(1))

		self.rem_alpha_butt_1 = tk.Button(self.first_tab)
		self.rem_alpha_butt_1.place(relx=0.227, rely=0.888, height=28
				, width=76)
		self.rem_alpha_butt_1.configure(activebackground=u"#f9f9f9")
		self.rem_alpha_butt_1.configure(background=_bgcolor)
		self.rem_alpha_butt_1.configure(text=u'''Alpha -1''')
		self.rem_alpha_butt_1.configure(command=lambda: self.add_alpha(-1))

		self.style.configure(u'Treeview.Heading',  font=u"TkDefaultFont")
		self.style.configure(u"mystyle.Treeview", highlightthickness=0, bd=0, font=(u'Deja Vu Sans Mono', 9)) #Calibri
		self.frame_ingredients = tk.Frame(self.first_tab, width=600)
		self.frame_ingredients.grid_rowconfigure(0, weight=1)
		self.frame_ingredients.grid_columnconfigure(0, weight=1)
		self.frame_ingredients.place(relx=0.013, rely=0.085
				, relheight=0.315, relwidth=0.581)
		self.ingredients = [] # [{'Name:': 'Wheat Flour', 'Values': {'EBC:': 0.0, 'Grav': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}}]

		self.frame_hops = tk.Frame(self.first_tab)
		self.frame_hops.grid_rowconfigure(0, weight=1)
		self.frame_hops.grid_columnconfigure(0, weight=1)
		self.frame_hops.place(relx=0.013, rely=0.55, relheight=0.273
				, relwidth=0.657)

		self.hops = [] # [{'Name': 'Nelson Sauvin', 'Values': {'Type': 'Whole', 'Alpha': 12.7, 'Time': 0.0, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}}]

		self.ingredients_imperial_chk_butt = tk.Checkbutton(self.first_tab)
		self.ingredients_imperial_chk_butt.place(relx=0.442, rely=0.402
				, relheight=0.044, relwidth=0.149)
		self.is_imperial_ingredient = tk.IntVar()
		self.ingredients_imperial_chk_butt.configure(text=u'''Imperial Units''')
		self.ingredients_imperial_chk_butt.configure(background=_bgcolor)
		self.ingredients_imperial_chk_butt.configure(command=self.ingredient_to_imperial)
		self.ingredients_imperial_chk_butt.configure(variable=self.is_imperial_ingredient)

		self.hops_imperial_chk_butt = tk.Checkbutton(self.first_tab)
		self.hops_imperial_chk_butt.place(relx=0.53, rely=0.825, relheight=0.044
			, relwidth=0.149)
		self.is_imperial_hop = tk.IntVar()
		self.hops_imperial_chk_butt.configure(text=u'''Imperial Units''')
		self.hops_imperial_chk_butt.configure(background=_bgcolor)
		self.hops_imperial_chk_butt.configure(command=self.hop_to_imperial)
		self.hops_imperial_chk_butt.configure(variable=self.is_imperial_hop)

		self.ogfixed_chkbutton = tk.Checkbutton(self.first_tab)
		self.is_ogfixed = tk.IntVar()
		self.ogfixed_chkbutton.place(relx=0.71, rely=0.127, relheight=0.044
				, relwidth=0.033)
		self.ogfixed_chkbutton.configure(activebackground=u"#f9f9f9")
		self.ogfixed_chkbutton.configure(background=_bgcolor)
		self.ogfixed_chkbutton.configure(justify=u'left')
		self.ogfixed_chkbutton.configure(variable=self.is_ogfixed)
		self.ogfixed_chkbutton.configure(command=self.og_fixed)

		self.ebufixed_chkbutton = tk.Checkbutton(self.first_tab)
		self.is_ebufixed = tk.IntVar()
		self.ebufixed_chkbutton.place(relx=0.821, rely=0.55, relheight=0.044
				, relwidth=0.033)
		self.ebufixed_chkbutton.configure(activebackground=u"#f9f9f9")
		self.ebufixed_chkbutton.configure(background=_bgcolor)
		self.ebufixed_chkbutton.configure(justify=u'left')
		self.ebufixed_chkbutton.configure(variable=self.is_ebufixed)
		self.ebufixed_chkbutton.configure(command=self.ebu_fixed)

		self.refresh_grist()
		self.refresh_hop()
		#self.tabbed_frame.bind('<Button-1>', lambda event: self.refresh_all() if self.tabbed_frame.tk.call(self.tabbed_frame._w, "identify", "tab", event.x, event.y) == 1 else False) # print(self.tabbed_frame.tk.call(self.tabbed_frame._w, "identify", "tab", event.x, event.y))
		self.tabbed_frame.bind(u'<Button-1>', self.refresh_tab_onclick)

		######################## Second Tab ########################
		#for hop in sorted(brew_data.hop_data):
		#	self.second_tab.hop_lstbx.insert(tk.END, hop)
		self.second_tab.reinsert()

		######################### Third Tab #########################
		#for grist in sorted(brew_data.grist_data):
		#	self.third_tab.grist_lstbx.insert(tk.END, grist)
		self.third_tab.reinsert()

		######################### Fifth Tab ##########################
		#self.tabbed_frame.bind('<Button-1>', lambda event: self.fifth_tab.refresh_all() if self.tabbed_frame.tk.call(self.tabbed_frame._w, "identify", "tab", event.x, event.y) == 5 else False) # print(self.tabbed_frame.tk.call(self.tabbed_frame._w, "identify", "tab", event.x, event.y))

		######################### Fourth Tab ##########################
		#for yeast in sorted(brew_data.yeast_data):
		#	self.fourth_tab.yeast_lstbx.insert(tk.END, yeast)
		self.fourth_tab.reinsert()

	def refresh_tab_onclick(self, event):
		tab = self.tabbed_frame.tk.call(self.tabbed_frame._w, u"identify", u"tab", event.x, event.y)
		if tab == 0:
			self.refresh_all()
		elif tab == 1:
			self.second_tab.reinsert()
		elif tab == 2:
			self.third_tab.reinsert()
		elif tab == 3:
			self.fourth_tab.reinsert()
		elif tab == 5:
			self.sixth_tab.refresh_all()

	def refresh_grist(self):
		def make_treeview():
			if u'scrolled_tree_ingredient' in vars(self):
				self.scrolled_tree_ingredient.delete(*self.scrolled_tree_ingredient.get_children())
			else:
				self.scrolled_tree_ingredient = ScrolledTreeView(self.frame_ingredients, style=u"mystyle.Treeview")
				self.scrolled_tree_ingredient.grid(row=0,column=0, sticky=u'nsew')
				self.ingredient_columns = (u"Ebc", u"Grav", u"lb:oz", u"Grams", u"%")
				self.scrolled_tree_ingredient.configure(columns=self.ingredient_columns)
				self.scrolled_tree_ingredient.heading(u"#0",text=u"Fermentable Ingredient", command=lambda c=u"Fermentable Ingredient": self.sort_by_grist(c))
				self.scrolled_tree_ingredient.column(u"#0",width=u"170",minwidth=u"20",stretch=u"1")
				for column in self.ingredient_columns:
					self.scrolled_tree_ingredient.heading(column, text=column, command=lambda c=column: self.sort_by_grist(c))
					self.scrolled_tree_ingredient.column(column, anchor=u"center")
					if column != u'lb:oz' and column != u'%' and column != u'EBC':
						self.scrolled_tree_ingredient.column(column, width=40)
					elif column == u'lb:oz':
						if len(self.ingredients) > 0:
							self.scrolled_tree_ingredient.column(u'lb:oz', width=max([len(u'{lb}:{oz}'.format(lb=int(ingredient[u'Values'][u'lb:oz'][0]), oz=round(ingredient[u'Values'][u'lb:oz'][1], 1))) for ingredient in self.ingredients])*7)
						else:
							self.scrolled_tree_ingredient.column(column, width=40)
					elif column == u'EBC':
						self.scrolled_tree_ingredient.column(column, width=28)
					elif column == u'%':
						self.scrolled_tree_ingredient.column(column, width=35)

		def refresh_percentage():
			total_weight = sum([ingredient[u'Values'][u'Grams'] for ingredient in self.ingredients])
			if total_weight > 0:
				for ingredient in self.ingredients:
					weight = ingredient[u'Values'][u'Grams']
					percentage = round((weight/total_weight)*100, 1)
					ingredient[u'Values'][u'Percent'] = percentage

		def refresh_orig_grav():
			non_mashables = [6.0, 5.0]
			volume = float(self.volume.get())
			points = sum([(brew_data.grist_data[ingredient[u'Name']][u'Extract']*(ingredient[u'Values'][u'Grams'])/1000) * (1 if brew_data.grist_data[ingredient[u'Name']][u'Type'] in non_mashables else brew_data.constants[u'Efficiency']) for ingredient in self.ingredients])

			orig_grav = ((points)/volume)+1000
			self.og = orig_grav
			self.original_gravity_ent.delete(0, tk.END)
			self.original_gravity_ent.insert(0, round(orig_grav, 1))

		def refresh_indiv_grav():
			non_mashables = [6.0, 5.0]
			volume = float(self.volume.get())
			for ingredient in self.ingredients:
				points = brew_data.grist_data[ingredient[u'Name']][u'Extract']*(ingredient[u'Values'][u'Grams'])/1000
				eff = (1 if brew_data.grist_data[ingredient[u'Name']][u'Type'] in non_mashables else brew_data.constants[u'Efficiency'])
				grav = ((points * eff)/volume)
				ingredient[u'Values'][u'Grav'] = grav
				#print(grav)

		make_treeview()
		if not self.is_ogfixed.get():
			refresh_orig_grav()
			refresh_percentage()
		else:
			non_mashables = [6.0, 5.0]
			factor = sum([ingredient[u'Values'][u'Percent']*brew_data.grist_data[ingredient[u'Name']][u'Extract']*(1 if brew_data.grist_data[ingredient[u'Name']][u'Type'] in non_mashables else brew_data.constants[u'Efficiency']) for idx, ingredient in enumerate(self.ingredients)])

			for idx, ingredient in enumerate(self.ingredients):
				EBC = int(brew_data.grist_data[ingredient[u'Name']][u'EBC'])
				percent = ingredient[u'Values'][u'Percent']
				orig_grav = float(self.original_gravity_ent.get())-1000
				vol = float(self.volume.get())
				try:
					weight = percent*((orig_grav*vol)/factor)*1000
				except:
					weight = 0
				lb = weight/brew_data.constants[u'Conversion'][u'lb-g']
				oz = (lb-int(lb))*16
				self.ingredients[idx] = {u'Name': ingredient[u'Name'], u'Values': {u'EBC': EBC, u'Grav': 0.0, u'lb:oz': (lb,oz), u'Grams': weight, u'Percent': percent}}
			refresh_percentage()

		refresh_indiv_grav()
		for ingredient in self.ingredients:
			values = (ingredient[u'Values'][u'EBC'], round(ingredient[u'Values'][u'Grav'], 1), u'{lb}:{oz}'.format(lb=int(ingredient[u'Values'][u'lb:oz'][0]), oz=round(ingredient[u'Values'][u'lb:oz'][1], 1)), round(ingredient[u'Values'][u'Grams'], 1), ingredient[u'Values'][u'Percent'])
			self.scrolled_tree_ingredient.insert(u'', u'end', text=ingredient[u'Name'], values=values)

	def refresh_hop(self):
		def make_treeview():
			if u'scrolled_tree_hops' in vars(self):
				self.scrolled_tree_hops.delete(*self.scrolled_tree_hops.get_children())
			else:
				self.scrolled_tree_hops = ScrolledTreeView(self.frame_hops, style=u"mystyle.Treeview")
				self.scrolled_tree_hops.grid(row=0, column=0, sticky=u'nsew')
				self.hop_columns = (u"Type", u"Alpha", u"Time", u"% Util", u"IBU", u"lb:oz", u"Grams", u"%")
				self.scrolled_tree_hops.configure(columns=self.hop_columns)
				self.scrolled_tree_hops.heading(u"#0",text=u"Hop Variety", command=lambda: self.sort_by_hop(u"Hop Variety"))
				self.scrolled_tree_hops.column(u"#0",width=u"90", anchor=u"w",minwidth=u"20",stretch=u"1")

				for column in self.hop_columns:
					self.scrolled_tree_hops.heading(column, text=column, command=lambda column=column: self.sort_by_hop(column))
					if column != u'lb:oz' and column != u'%':
						self.scrolled_tree_hops.column(column, width=40, anchor=u"center")
					elif column == u'lb:oz':
						if len(self.hops) > 0:
							self.scrolled_tree_hops.column(column, width=max([len(u'{lb}:{oz}'.format(lb=int(hop[u'Values'][u'lb:oz'][0]), oz=round(hop[u'Values'][u'lb:oz'][1], 1))) for hop in self.hops])*7, anchor=u"center")
						else:
							self.scrolled_tree_hops.column(column, width=40, anchor=u"center")
					elif column == u'%' or column == u'% Util':
						self.scrolled_tree_hops.column(column, width=35, anchor=u"center")

		def refresh_percentage():
			total_weight = sum([hop[u'Values'][u'Grams'] for hop in self.hops])
			if total_weight > 0:
				for hop in self.hops:
					weight = hop[u'Values'][u'Grams']
					percentage = round((weight/total_weight)*100, 1)
					hop[u'Values'][u'Percent'] = percentage

		def refresh_util():
			def boil_grav():
				volume = float(self.boil_vol.get())
				points = sum([brew_data.grist_data[ingredient[u'Name']][u'Extract']*(ingredient[u'Values'][u'Grams'])/1000 for ingredient in self.ingredients])
				boil_grav = ((points * brew_data.constants[u'Efficiency'])/volume)+1000
				return boil_grav
			u'''
			Utilization = f(G) x f(T)
			f(G) = 1.65 x 0.000125^(Gb - 1)
			f(T) = [1 - e^(-0.04 x T)] / 4.15
			Where Gb is boil gravity and T is time
			'''
			for hop in self.hops:
				boil_gravity = boil_grav()/1000 # Temporary Solution
				time = hop[u'Values'][u'Time']
				fG = 1.65 * (0.000125**(boil_gravity - 1))
				fT = (1 - math.e**(-0.04 * time)) / 4.15
				hop[u'Values'][u'Util'] = (fG * fT)*100

		def refresh_ibu():
			u'''
			IBU    =    grams x alpha acid x utilisation rate
				   -------------------------------------------------
									 Volume x 10
			'''
			ibu = sum([(hop[u'Values'][u'Grams'] * hop[u'Values'][u'Alpha'] * hop[u'Values'][u'Util']) / (float(self.boil_vol.get())*10)  for hop in self.hops])
			ibu = (ibu*float(self.boil_vol.get()))/float(self.volume.get())
			self.ibu = ibu
			self.bitterness_ibu_ent.delete(0, tk.END)
			self.bitterness_ibu_ent.insert(0, round(ibu))

		def refresh_indiv_ibu():
			for hop in self.hops:
				ibu = (hop[u'Values'][u'Grams'] * hop[u'Values'][u'Alpha'] * hop[u'Values'][u'Util']) / (float(self.boil_vol.get())*10)
				hop[u'Values'][u'ibu'] = ibu



		make_treeview()
		if not self.is_ebufixed.get():
			refresh_percentage()
			refresh_ibu()
		else:
			factor = sum([hop[u'Values'][u'Percent']*hop[u'Values'][u'Alpha']*hop[u'Values'][u'Util'] for idx, hop in enumerate(self.hops)])

			for idx, hop in enumerate(self.hops):
				percent = hop[u'Values'][u'Percent']

				alpha =  hop[u'Values'][u'Alpha']
				type = brew_data.hop_data[hop[u'Name']][u'Form']
				util = hop[u'Values'][u'Util']
				time = hop[u'Values'][u'Time']
				if util > 0 and alpha > 0:
					total_ibus = float(self.bitterness_ibu_ent.get())
					vol = float(self.volume.get())
					try:
						weight = percent*((total_ibus*vol*10)/factor) #(((total_ibus*(percent/100))*(vol*10))/util)/alpha
					except:
						weight = 0
					lb = weight/brew_data.constants[u'Conversion'][u'lb-g']
					oz = (lb-int(lb))*16
					self.hops[idx] = {u'Name': hop[u'Name'], u'Values': {u'Type': type, u'Alpha': alpha, u'Time': time, u'Util': 0.0, u'ibu': 0.0, u'lb:oz': (lb, oz), u'Grams': weight, u'Percent': percent}}
			refresh_percentage()
		refresh_util()
		refresh_indiv_ibu()
		for hop in self.hops:
			values = (hop[u'Values'][u'Type'], hop[u'Values'][u'Alpha'], hop[u'Values'][u'Time'], round(hop[u'Values'][u'Util'], 1), round(hop[u'Values'][u'ibu']),u'{lb}:{oz}'.format(lb=int(hop[u'Values'][u'lb:oz'][0]), oz=round(hop[u'Values'][u'lb:oz'][1], 1)), round(hop[u'Values'][u'Grams'], 1), hop[u'Values'][u'Percent'])
			self.scrolled_tree_hops.insert(u'', u'end', text=hop[u'Name'], values=values)

	def refresh_all(self):
		self.refresh_hop()
		self.refresh_grist()
		self.recalculate()

	def add_grist(self):
		def insert():
			name = grist_options.item(grist_options.focus())[u'text']
			EBC = int(brew_data.grist_data[name][u'EBC'])
			self.ingredients.append({u'Name': name, u'Values': {u'EBC': EBC, u'Grav': 0.0, u'lb:oz': (0.0,0.0), u'Grams': 0, u'Percent': 0.0}})
			self.refresh_grist()

		def bound(event, treeview, list_data): #https://mail.python.org/pipermail/python-list/2002-May/170135.html ADDED TREEVIEW functionality
			key=event.keysym
			if key == u'Escape':
				add_grist_gui.destroy()
			if len(key)<=1:
				if key in string.ascii_lowercase:
					try:
						start_n= int(treeview.focus()[1:], 16)-1
					except IndexError:
						start_n=-1
					## clear the selection.
					treeview.selection_clear()
					## start from previous selection +1
					for n in xrange(start_n+1, len(list_data)):
						item=list_data[n]
						if item[0].lower()==key.lower():
							treeview.selection_set(u'I{iid}'.format(iid=format(n+1, u'03x')))
							treeview.focus(u'I{iid}'.format(iid=format(n+1, u'03x')))
							treeview.yview(n)
							return
						treeview.yview(n)
					else:
						# has not found it so loop from top
						for n in xrange(len(list_data)):
							item=list_data[n]
							if item[0].lower()==key.lower():
								treeview.yview(n)
								treeview.selection_set(u'I{iid}'.format(iid=format(n+1, u'03x')))
								treeview.focus(u'I{iid}'.format(iid=format(n+1, u'03x')))
								return
						treeview.yview(n)

		add_grist_gui = tk.Toplevel()
		add_grist_gui.resizable(0, 0)
		grist_options = ScrolledTreeView(add_grist_gui, show=u"tree", columns=(u"EBC"))
		grist_options.column(column=u"EBC",width=80)
		grist_options.grid(row=1,column=0)
		for grist in sorted(brew_data.grist_data):
			ebc = unicode(brew_data.grist_data[grist][u'EBC']) + u' EBC'
			grist_options.insert(u'', tk.END, text=(grist), values=(ebc,))
		grist_add_new = tk.Button(add_grist_gui, text=u'Add New', command = insert)
		grist_add_new.grid(row=1,column=1)
		add_grist_gui.bind(u'<Any-Key>', lambda evt: bound(evt, grist_options, sorted(brew_data.grist_data)))
		add_grist_gui.mainloop()

	def add_hop(self):
		def insert():
			name = hop_options.item(hop_options.focus())[u'text']
			alpha =  brew_data.hop_data[name][u'Alpha']
			type = brew_data.hop_data[name][u'Form']
			time = brew_data.constants[u'Hop Time']
			self.hops.append({u'Name': name, u'Values': {u'Type': type, u'Alpha': alpha, u'Time': time, u'Util': 0.0, u'ibu': 0.0, u'lb:oz': (0.0,0.0), u'Grams': 0, u'Percent': 0.0}})
			self.refresh_hop()
		def bound(event, treeview, list_data): #https://mail.python.org/pipermail/python-list/2002-May/170135.html
			key=event.keysym
			if key == u'Escape':
				add_hop_gui.destroy()
			if len(key)<=1:
				if key in string.ascii_lowercase:
					try:
						start_n= int(treeview.focus()[1:], 16)-1
					except IndexError:
						start_n=-1
					## clear the selection.
					treeview.selection_clear()
					## start from previous selection +1
					for n in xrange(start_n+1, len(list_data)):
						item=list_data[n]
						if item[0].lower()==key.lower():
							treeview.selection_set(u'I{iid}'.format(iid=format(n+1, u'03x')))
							treeview.focus(u'I{iid}'.format(iid=format(n+1, u'03x')))
							treeview.yview(n)
							return
						treeview.yview(n)
					else:
						# has not found it so loop from top
						for n in xrange(len(list_data)):
							item=list_data[n]
							if item[0].lower()==key.lower():
								treeview.yview(n)
								treeview.selection_set(u'I{iid}'.format(iid=format(n+1, u'03x')))
								treeview.focus(u'I{iid}'.format(iid=format(n+1, u'03x')))
								return
						treeview.yview(n)
		add_hop_gui = tk.Toplevel()
		add_hop_gui.resizable(0, 0)
		hop_options = ScrolledTreeView(add_hop_gui, show=u"tree", columns=(u"Form"))
		hop_options.column(column=u"Form",width=80)
		hop_options.grid(row=1, column=0)
		for hop in sorted(brew_data.hop_data):
			hop_options.insert(u'',tk.END, text=(hop), values=(brew_data.hop_data[hop][u'Form'],))
		hop_add_new = tk.Button(add_hop_gui, text=u'Add New', command = insert)
		hop_add_new.grid(row=1,column=1)
		add_hop_gui.bind(u'<Any-Key>', lambda evt: bound(evt, hop_options, sorted(brew_data.hop_data)))
		add_hop_gui.mainloop()

	def add_weight_ingredients(self, weight): # Selected Item
		try:
			selection = self.scrolled_tree_ingredient.selection()[0]
			id = int(unicode(selection)[1:], 16)
			#print(id, selection)
			grams = self.ingredients[id-1][u'Values'][u'Grams']+weight
			if grams < 0: grams=0
			lb = grams/brew_data.constants[u'Conversion'][u'lb-g']
			oz = (lb-int(lb))*16
			self.ingredients[id-1][u'Values'][u'Grams'] = grams
			self.ingredients[id-1][u'Values'][u'lb:oz'] = (lb, oz)
			self.refresh_grist()
			self.recalculate()
			self.scrolled_tree_ingredient.focus_set()
			self.scrolled_tree_ingredient.see(selection)
			self.scrolled_tree_ingredient.selection_set(selection)
		except IndexError:
			pass

	def add_weight_hops(self, weight): # Selected Item
		try:
			selection = self.scrolled_tree_hops.selection()[0]
			id = int(unicode(selection)[1:], 16)
			grams = self.hops[id-1][u'Values'][u'Grams']+weight
			if grams < 0: grams=0
			lb = grams/brew_data.constants[u'Conversion'][u'lb-g']
			oz = (lb-int(lb))*16
			self.hops[id-1][u'Values'][u'Grams'] = grams
			self.hops[id-1][u'Values'][u'lb:oz'] = (lb, oz)
			self.refresh_hop()
			self.recalculate()
			self.scrolled_tree_hops.focus_set()
			self.scrolled_tree_hops.see(selection)
			self.scrolled_tree_hops.selection_set(selection)
		except IndexError:
			pass

	def zero_ingredients(self, curr_selection=None):
		try:
			if curr_selection is None:
				selection = self.scrolled_tree_ingredient.selection()[0]
			else:
				selection = curr_selection
			id = int(unicode(selection)[1:], 16)
			EBC = int(brew_data.grist_data[self.ingredients[id-1][u'Name']][u'EBC'])
			self.ingredients[id-1] = {u'Name': self.ingredients[id-1][u'Name'], u'Values': {u'EBC': EBC, u'Grav': 0.0, u'lb:oz': (0.0,0.0), u'Grams': 0, u'Percent': 0.0}}
			self.refresh_grist()
			self.recalculate()
			self.scrolled_tree_ingredient.focus_set()
			self.scrolled_tree_ingredient.see(selection)
			self.scrolled_tree_ingredient.selection_set(selection)
		except IndexError:
			pass

	def zero_hops(self):
		try:
			selection = self.scrolled_tree_hops.selection()[0]
			id = int(unicode(selection)[1:], 16)
			alpha =  brew_data.hop_data[self.hops[id-1][u'Name']][u'Alpha']
			type = brew_data.hop_data[self.hops[id-1][u'Name']][u'Form']
			self.hops[id-1] = {u'Name': self.hops[id-1][u'Name'], u'Values': {u'Type': type, u'Alpha': alpha, u'Time': 0.0, u'Util': 0.0, u'ibu': 0.0, u'lb:oz': (0.0,0.0), u'Grams': 0, u'Percent': 0.0}}
			self.refresh_hop()
			self.recalculate()
			self.scrolled_tree_hops.focus_set()
			self.scrolled_tree_hops.see(selection)
			self.scrolled_tree_hops.selection_set(selection)
		except IndexError:
			pass

	def delete_ingredient(self):
		try:
			selection = self.scrolled_tree_ingredient.selection()[0]
			id = int(unicode(selection)[1:], 16)
			del self.ingredients[id-1]
			self.refresh_grist()
			self.recalculate()
		except IndexError:
			pass

	def delete_hop(self):
		try:
			selection = self.scrolled_tree_hops.selection()[0]
			id = int(unicode(selection)[1:], 16)
			del self.hops[id-1]
			self.refresh_hop()
			self.recalculate()
		except IndexError:
			pass
	def add_time(self, time):
		try:
			selection = self.scrolled_tree_hops.selection()[0]
			id = int(unicode(selection)[1:], 16)
			time = round(self.hops[id-1][u'Values'][u'Time']+time,1)
			if time < 0: time = 0
			self.hops[id-1][u'Values'][u'Time'] = time
			self.refresh_hop()
			self.recalculate()
			self.scrolled_tree_hops.focus_set()
			self.scrolled_tree_hops.see(selection)
			self.scrolled_tree_hops.selection_set(selection)
		except IndexError:
			pass
	def add_alpha(self, alpha):
		try:
			selection = self.scrolled_tree_hops.selection()[0]
			id = int(unicode(selection)[1:], 16)
			alpha = round(self.hops[id-1][u'Values'][u'Alpha']+alpha, 1)
			if alpha < 0: alpha = 0
			self.hops[id-1][u'Values'][u'Alpha'] = alpha
			self.refresh_hop()
			self.recalculate()
			self.scrolled_tree_hops.focus_set()
			self.scrolled_tree_hops.see(selection)
			self.scrolled_tree_hops.selection_set(selection)
		except IndexError:
			pass

	def recalculate(self):
		def final_gravity():
			non_mashables = [6.0, 5.0]
			a = sum([((self.attenuation_apply(ingredient)/100)*((ingredient[u'Values'][u'Grams']/1000) * brew_data.grist_data[ingredient[u'Name']][u'Extract'])) * (1 if brew_data.grist_data[ingredient[u'Name']][u'Type'] in non_mashables else brew_data.constants[u'Efficiency']) for ingredient in self.ingredients])
			b = sum([(((100 - self.attenuation_apply(ingredient))/100)*((ingredient[u'Values'][u'Grams']/1000) * brew_data.grist_data[ingredient[u'Name']][u'Extract'])) * (1 if brew_data.grist_data[ingredient[u'Name']][u'Type'] in non_mashables else brew_data.constants[u'Efficiency']) for ingredient in self.ingredients])
			return ((b-(a*0.225))/float(self.volume.get()))+1000
		def alcohol_by_volume(og, fg):
			#return (1.05/0.79) * ((og - fg) / fg) *100
			return (((1.05*(og-fg))/fg/0.79))*100
		def mash_liquor():
			non_mashables = [6.0, 5.0] # ["Copper Sugar", "Malt Extract"]
			grist_mass = sum([0 if brew_data.grist_data[ingredient[u'Name']][u'Type'] in non_mashables else ingredient[u'Values'][u'Grams'] for ingredient in self.ingredients])/1000
			return grist_mass*brew_data.constants[u'Liquor To Grist Ratio']
		def colour_ebc():
			# [{'Name:': 'Wheat Flour', 'Values': {'EBC:': 0.0, 'Grav': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}}]
			def formula(ingredient, efficiency):
				ebc = ingredient[u'Values'][u'EBC']
				mass = ingredient[u'Values'][u'Grams']/1000
				volume = float(self.volume.get())
				return (ebc*mass*efficiency*10)/volume

			non_mashables = [6.0, 5.0] # Not effected by efficiency  ["Copper Sugar", "Malt Extract"]
			return (sum([formula(ingredient, 1) if brew_data.grist_data[ingredient[u'Name']][u'Type'] in non_mashables else formula(ingredient, brew_data.constants[u'Efficiency']) for ingredient in self.ingredients]))

		u'''
		MCU = color rating of the malt °L × weight(lb)
			°SRM = MCU 					(Traditional)
			°SRM = 0.3 × MCU + 4.7		(Mosher)
			°SRM = 0.2 × MCU + 8.4		(Daniels)
			°SRM = 1.49 × MCU ^ 0.69	(Morey)
		'''
		#self.colour = 1.49 * (sum([((ingredient['Values']['EBC']*1.84)*(ingredient['Values']['lb:oz'][0] + (ingredient['Values']['lb:oz'][1]/16)))/(float(self.volume.get())/brew_data.constants['Conversion']['usg-l']) for ingredient in self.ingredients]) ** 0.69) # Morey's Formula
		self.refresh_hop()
		self.refresh_grist()

		self.colour = colour_ebc()
		self.fg = final_gravity()
		self.og = float(self.og)
		self.abv = alcohol_by_volume(self.og/1000, self.fg/1000)
		self.ibu_gu = float(self.ibu) / (self.og - 1000) if (self.og - 1000) != 0 else 0
		self.calc_lbl.configure(state=u'normal')
		self.calc_lbl.delete(u'1.0', u'end')
		self.calc_lbl.insert(u'end', u'''Efficiency: {efficiency}%{enter}Final Gravity: {final_gravity}{enter}Alcohol (ABV): {abv}{enter}Colour: {colour}EBC{enter}Mash Liquor: {mash_liquor}L{enter}IBU:GU: {ibu_gu}'''.format(
			efficiency=round(brew_data.constants[u'Efficiency']*100, 13), final_gravity=round(self.fg, 1),
			abv=round(self.abv, 1), colour=round(self.colour,1), mash_liquor=round(mash_liquor(),1),
			ibu_gu=round(self.ibu_gu, 2), enter=u'\n\n'))
		self.calc_lbl.configure(state=u'disabled')
		self.refresh_hop()
		self.refresh_grist()

	def ingredient_to_imperial(self):
		if self.is_imperial_ingredient.get() == 0:
			self.add_1000g_ing_butt.configure(text=u'''+1Kg''')
			self.add_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(1000))
			self.add_1000g_ing_butt.configure(font=u"TkFixedFont")

			self.add_100g_ing_butt.configure(text=u'''+100g''')
			self.add_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(100))
			self.add_100g_ing_butt.configure(font=u"TkFixedFont")

			self.rem_1000g_ing_butt.configure(text=u'''-1Kg''')
			self.rem_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-1000))
			self.rem_1000g_ing_butt.configure(font=u"TkFixedFont")

			self.rem_100g_ing_butt.configure(text=u'''-100g''')
			self.rem_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-100))
			self.rem_100g_ing_butt.configure(font=u"TkFixedFont")

			self.add_10g_ing_butt.configure(text=u'''+10g''')
			self.add_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(10))
			self.add_10g_ing_butt.configure(font=u"TkFixedFont")

			self.rem_10g_ing_butt.configure(text=u'''-10g''')
			self.rem_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-10))
			self.rem_10g_ing_butt.configure(font=u"TkFixedFont")

			self.add_1g_ing_butt.configure(text=u'''+1g''')
			self.add_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(1))
			self.add_1g_ing_butt.configure(font=u"TkFixedFont")

			self.rem_1g_ing_butt.configure(text=u'''-1g''')
			self.rem_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-1))
			self.rem_1g_ing_butt.configure(font=u"TkFixedFont")

		elif self.is_imperial_ingredient.get() == 1:
			self.add_1000g_ing_butt.configure(text=u'''+1lb''')
			self.add_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(brew_data.constants[u'Conversion'][u'lb-g']))
			self.add_1000g_ing_butt.configure(font=(None,7))

			self.add_100g_ing_butt.configure(text=u'''+1oz''')
			self.add_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(brew_data.constants[u'Conversion'][u'oz-g']))
			self.add_100g_ing_butt.configure(font=(None,7))

			self.rem_1000g_ing_butt.configure(text=u'''-1lb''')
			self.rem_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-brew_data.constants[u'Conversion'][u'lb-g']))
			self.rem_1000g_ing_butt.configure(font=(None,7))

			self.rem_100g_ing_butt.configure(text=u'''-1oz''')
			self.rem_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-brew_data.constants[u'Conversion'][u'oz-g']))
			self.rem_100g_ing_butt.configure(font=(None,7))

			self.add_10g_ing_butt.configure(text=u'''+1/4oz''')
			self.add_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(brew_data.constants[u'Conversion'][u'oz-g']/4))
			self.add_10g_ing_butt.configure(font=(None,7))

			self.rem_10g_ing_butt.configure(text=u'''-1/4oz''')
			self.rem_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-brew_data.constants[u'Conversion'][u'oz-g']/4))
			self.rem_10g_ing_butt.configure(font=(None,7))

			self.add_1g_ing_butt.configure(text=u'''+1/16oz''')
			self.add_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(brew_data.constants[u'Conversion'][u'oz-g']/16))
			self.add_1g_ing_butt.configure(font=(None,7))

			self.rem_1g_ing_butt.configure(text=u'''-1/16oz''')
			self.rem_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-brew_data.constants[u'Conversion'][u'oz-g']/16))
			self.rem_1g_ing_butt.configure(font=(None,7))

	def hop_to_imperial(self):
		if self.is_imperial_hop.get() == 0:
			self.add_100g_hop_butt.configure(text=u'''+100g''')
			self.add_100g_hop_butt.configure(command=lambda: self.add_weight_hops(100))
			self.add_100g_hop_butt.configure(font=u"TkFixedFont")

			self.rem_100g_hop_butt.configure(text=u'''-100g''')
			self.rem_100g_hop_butt.configure(command=lambda: self.add_weight_hops(-100))
			self.rem_100g_hop_butt.configure(font=u"TkFixedFont")

			self.add_25g_hop_butt.configure(text=u'''+25g''')
			self.add_25g_hop_butt.configure(command=lambda: self.add_weight_hops(25))
			self.add_25g_hop_butt.configure(font=u"TkFixedFont")
			self.rem_25g_hop_butt.configure(text=u'''-25g''')
			self.rem_25g_hop_butt.configure(command=lambda: self.add_weight_hops(-25))
			self.rem_25g_hop_butt.configure(font=u"TkFixedFont")

			self.add_10g_hop_butt.configure(text=u'''+10g''')
			self.add_10g_hop_butt.configure(command=lambda: self.add_weight_hops(10))
			self.add_10g_hop_butt.configure(font=u"TkFixedFont")

			self.rem_10g_hop_butt.configure(text=u'''-10g''')
			self.rem_10g_hop_butt.configure(command=lambda: self.add_weight_hops(-10))
			self.rem_10g_hop_butt.configure(font=u"TkFixedFont")

			self.add_1g_hop_butt.configure(text=u'''+1g''')
			self.add_1g_hop_butt.configure(command=lambda: self.add_weight_hops(1))
			self.add_1g_hop_butt.configure(font=u"TkFixedFont")

			self.rem_1g_hop_butt.configure(text=u'''-1g''')
			self.rem_1g_hop_butt.configure(command=lambda: self.add_weight_hops(-1))
			self.rem_1g_hop_butt.configure(font=u"TkFixedFont")

		elif self.is_imperial_hop.get() == 1:
			self.add_100g_hop_butt.configure(text=u'''+4oz''')
			self.add_100g_hop_butt.configure(command=lambda: self.add_weight_hops(brew_data.constants[u'Conversion'][u'oz-g']*4))
			self.add_100g_hop_butt.configure(font=(None,7))

			self.rem_100g_hop_butt.configure(text=u'''-4oz''')
			self.rem_100g_hop_butt.configure(command=lambda: self.add_weight_hops(-brew_data.constants[u'Conversion'][u'oz-g']*4))
			self.rem_100g_hop_butt.configure(font=(None,7))

			self.add_25g_hop_butt.configure(text=u'''+1oz''')
			self.add_25g_hop_butt.configure(command=lambda: self.add_weight_hops(brew_data.constants[u'Conversion'][u'oz-g']))
			self.add_25g_hop_butt.configure(font=(None,7))
			self.rem_25g_hop_butt.configure(text=u'''-1oz''')
			self.rem_25g_hop_butt.configure(command=lambda: self.add_weight_hops(-brew_data.constants[u'Conversion'][u'oz-g']))
			self.rem_25g_hop_butt.configure(font=(None,7))

			self.add_10g_hop_butt.configure(text=u'''+1/4oz''')
			self.add_10g_hop_butt.configure(command=lambda: self.add_weight_hops(brew_data.constants[u'Conversion'][u'oz-g']/4))
			self.add_10g_hop_butt.configure(font=(None,7))

			self.rem_10g_hop_butt.configure(text=u'''-1/4oz''')
			self.rem_10g_hop_butt.configure(command=lambda: self.add_weight_hops(-brew_data.constants[u'Conversion'][u'oz-g']/4))
			self.rem_10g_hop_butt.configure(font=(None,7))

			self.add_1g_hop_butt.configure(text=u'''+1/16oz''')
			self.add_1g_hop_butt.configure(command=lambda: self.add_weight_hops(brew_data.constants[u'Conversion'][u'oz-g']/16))
			self.add_1g_hop_butt.configure(font=(None,7))

			self.rem_1g_hop_butt.configure(text=u'''-1/16oz''')
			self.rem_1g_hop_butt.configure(command=lambda: self.add_weight_hops(-brew_data.constants[u'Conversion'][u'oz-g']/16))
			self.rem_1g_hop_butt.configure(font=(None,7))

	def attenuation_apply(self, ingredient):
		#print(brew_data.grist_data[ingredient['Name']]['Fermentability'])
		if int(brew_data.grist_data[ingredient[u'Name']][u'Fermentability']) == 200:
			table_dict = {
				u'low-62': 51, u'med-62': 59, u'high-62': 66,
				u'low-63': 52, u'med-63': 60, u'high-63': 68,
				u'low-64': 53, u'med-64': 61, u'high-64': 69,
				u'low-65': 53, u'med-65': 62, u'high-65': 69,
				u'low-66': 53, u'med-66': 62, u'high-66': 69,
				u'low-67': 53, u'med-67': 62, u'high-67': 69,
				u'low-68': 52, u'med-68': 60, u'high-68': 67,
				u'low-69': 51, u'med-69': 58, u'high-69': 66,
				u'low-70': 49, u'med-70': 56, u'high-70': 63,
				u'low-71': 47, u'med-71': 54, u'high-71': 61,
				u'low-72': 44, u'med-72': 51, u'high-72': 57
			}
			#print(table_dict[self.fifth_tab.current_attenuation.get()])
			return table_dict[self.sixth_tab.current_attenuation.get()]
		else:
			#print('else')
			return brew_data.grist_data[ingredient[u'Name']][u'Fermentability']

	def sort_by_grist(self, column):
		# [{'Name:': 'Wheat Flour', 'Values': {'EBC:': 0.0, 'Grav': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}}]
		################################### Grist ###################################
		old_ingred = self.ingredients

		if column == u'Fermentable Ingredient':
			self.ingredients = sorted(self.ingredients, key=lambda k: k[u'Name'])
		elif column == u'Ebc':
			self.ingredients = sorted(self.ingredients, key=lambda k: k[u'Values'][u'EBC'])
		elif column == u'Grav':
			self.ingredients = sorted(self.ingredients, key=lambda k: k[u'Values'][u'Grav'])
		elif column == u'lb:oz':
			self.ingredients = sorted(self.ingredients, key=lambda k: (k[u'Values'][u'lb:oz'][0] + (k[u'Values'][u'lb:oz'][1]/16)))
		elif column == u'Grams':
			self.ingredients = sorted(self.ingredients, key=lambda k: k[u'Values'][u'Grams'])
		elif column == u'%':
			self.ingredients = sorted(self.ingredients, key=lambda k: k[u'Values'][u'Percent'])

		if old_ingred == self.ingredients:
			self.ingredients.reverse()

		self.refresh_grist()

	def sort_by_hop(self, column):
		# [{'Name': 'Nelson Sauvin', 'Values': {'Type': 'Whole', 'Alpha': 12.7, 'Time': 0.0, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}}]
		old_hops = self.hops
		if column == u'Hop Variety':
			self.hops = sorted(self.hops, key=lambda k: k[u'Name'])
		elif column == u'Type':
			self.hops = sorted(self.hops, key=lambda k: k[u'Values'][u'Type'])
		elif column == u'Alpha':
			self.hops = sorted(self.hops, key=lambda k: k[u'Values'][u'Alpha'])
		elif column == u'Time':
			self.hops = sorted(self.hops, key=lambda k: k[u'Values'][u'Time'])
		elif column == u'% Util':
			self.hops = sorted(self.hops, key=lambda k: k[u'Values'][u'Util'])
		elif column == u'IBU':
			self.hops = sorted(self.hops, key=lambda k: k[u'Values'][u'ibu'])
		elif column == u'lb:oz':
			self.hops = sorted(self.hops, key=lambda k: (k[u'Values'][u'lb:oz'][0] + (k[u'Values'][u'lb:oz'][1]/16)))
		elif column == u'Grams':
			self.hops = sorted(self.hops, key=lambda k: k[u'Values'][u'Grams'])
		elif column == u'%':
			self.hops = sorted(self.hops, key=lambda k: k[u'Values'][u'Percent'])
		if old_hops == self.hops:
			self.hops.reverse()
		self.refresh_hop()

	def create_html(self, start=u'', open_browser=True, use_sorttable=False):
		self.recalculate()
		if use_sorttable: start += u'<script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>'
		start += u'<html><head><title>{name}</title><link rel="shortcut icon" href="{logo}" />'.format(name=self.recipe_name_ent.get().replace(u'&', u'&amp;'), logo=resource_path(u'logo.png'))
		start += ur'''
		<!--Extracted From Graham Wheeler's Beer Engine recipe.html-->
		<!--Yeast Section added by jimbob88-->
		<style>
		body {text-align: left; margin-left: 30; margin-top: 15px; background: #FFFFFF; font-family: Helvetica,Verdana,Tahoma,Sans-serif; font-size: 10pt; color: #000000}
		table {border-spacing:0}
		td {text-align:left;font-family: Helvetica,Verdana,Tahoma,Sans-serif; font-size: 10pt; color: #000000;padding:0px;border-bottom: 1px solid  #000000;border-left: 1px solid  #000000;}
		td.ing1 {width:200; text-align:left;background-color: #FFFFFF;padding:4px}
		td.ing2 {width:70; text-align:right; background-color: #FFFFFF;padding:4px}
		td.ing3 {width:90; text-align:right; background-color: #FFFFFF;padding:4px}
		td.ing4 {width:40; text-align:right; background-color: #FFFFFF;padding:4px;border-right: 1px solid #000000;}
		td.hop1 {width:152; text-align:left; background-color: #FFFFFF;padding:4px}
		td.hop2 {width:60; text-align:center; background-color: #FFFFFF;padding:4px}
		td.hop3 {width:50; text-align:right; background-color: #FFFFFF;padding:4px}
		td.hop4 {width:60; text-align:right; background-color: #FFFFFF;padding:4px}
		td.hop5 {width:80; text-align:right; background-color: #FFFFFF;padding:4px}
		td.hop6 {width:40; text-align:right; background-color: #FFFFFF;padding:4px;border-right: 1px solid #000000;}
		td.yst1 {width:300; text-align:left;background-color: #FFFFFF;padding:4px}
		td.yst2 {width:100; text-align:center; background-color: #FFFFFF;padding:4px}
		td.yst3 {width:100; text-align:center; background-color: #FFFFFF;padding:4px}
		td.yst4 {width:40; text-align:center; background-color: #FFFFFF;padding:4px}
		td.yst5 {width:40; text-align:center; background-color: #FFFFFF;padding:4px}
		td.yst6 {width:20; text-align:center; background-color: #FFFFFF;padding:4px}
		td.yst7 {width:10; text-align:center; background-color: #FFFFFF;padding:4px;border-right: 1px solid #000000;}
		span.bold {font-weight: bold}
		th.subhead {font-weight:bold; text-align:center;background-color:#E8E8E8;padding:4px;border-top: 1px solid #000000;border-left: 1px solid #000000;border-bottom: 1px solid #000000;}
		th.subhead2 {font-weight:bold; text-align:center;background-color:#E8E8E8;padding:4px;border-top: 1px solid #000000;border-left: 1px solid #000000;border-right: 1px solid #000000;border-bottom: 1px solid #000000;}
		table.sortable th:not(.sorttable_sorted):not(.sorttable_sorted_reverse):not(.sorttable_nosort):after {
    		content: " \25B4\25BE"
		}
		</style>'''
		start += u'</head><body>'
		start += u'<h2>{name}</h2>'.format(name=self.recipe_name_ent.get().replace(u'&', u'&amp;'))
		if use_sorttable:
			start += u'<table style="width:800px" class="sortable" id="sortable">'
		else:
			start += u'<table style="width:800px">'
		start += u'<tr><th class="subhead">Fermentable</th><th class="subhead">Colour</th><th class="subhead">lb:oz</th><th class="subhead">Grams</th><th class="subhead2">Ratio</th></tr>'

		for addition in self.sixth_tab.added_additions:
			try:
				if brew_data.water_chemistry_additions[addition][u'Values'][u'Type'] == u'Malt':
					start += u'<tr>'
					start += u'<td class="ing1">{name}</td>'.format(name=addition)
					start += u'<td class="ing2">N/A</td>'
					start += u'<td class="ing3">N/A</td>'
					start += u'<td class="ing3">N/A</td>'
					start += u'<td class="ing4">N/A</td>'
					start += u'</tr>'
			except KeyError:
				pass

		for ingredient in self.ingredients:
			start += u'<tr>'
			start += u'<td class="ing1">{name}</td>'.format(name=ingredient[u'Name'])
			start += u'<td class="ing2">{colour}</td>'.format(colour=ingredient[u'Values'][u'EBC'])
			start += u'<td class="ing3">{lb}:{oz}</td>'.format(lb=int(ingredient[u'Values'][u'lb:oz'][0]), oz=round(ingredient[u'Values'][u'lb:oz'][1], 1))
			start += u'<td class="ing3">{grams}</td>'.format(grams=(round(ingredient[u'Values'][u'Grams'], 1)) if (ingredient[u'Values'][u'Grams']-int(ingredient[u'Values'][u'Grams'])) >= 2 else round(ingredient[u'Values'][u'Grams']))
			start += u'<td class="ing4">{percentage}%</td>'.format(percentage=ingredient[u'Values'][u'Percent'])
			start += u'</tr>'
		start += u'</table><br>'
		if start[-179:] == u'<tr><th class="subhead">Fermentable</th><th class="subhead">Colour</th><th class="subhead">lb:oz</th><th class="subhead">Grams</th><th class="subhead2">Ratio</th></tr></table><br>': start = start[:-179]

		if self.sixth_tab.water_boil_is_disabled.get() == 1:
			start += u'<p><b>Boil Time: </b>{boil_time}</p>'.format(boil_time=self.sixth_tab.water_boil_time_spinbx.get())

		if use_sorttable:
			start += u'<table style="width:800px" class="sortable" id="sortable">'
		else:
			start += u'<table style="width:800px">'
		start += u'<tr><th class="subhead">Hop Variety</th><th class="subhead">Type</th><th class="subhead">Alpha</th><th class="subhead">Time</th><th class="subhead">lb:oz</th><th class="subhead">Grams</th><th class="subhead2">Ratio</th></tr>'
		#temp_hop = [*self.hops] + [{'Name': addition, 'Values': brew_data.water_chemistry_additions[addition]['Values']} if brew_data.water_chemistry_additions[addition]['Values']['Type'] == 'Hop' else None for addition in self.sixth_tab.added_additions]
		temp_hop = self.hops[:]
		for addition in self.sixth_tab.added_additions:
			try:
				if brew_data.water_chemistry_additions[addition][u'Values'][u'Type'] == u'Hop':
					temp_hop.append({u'Name': addition, u'Values': brew_data.water_chemistry_additions[addition][u'Values']})
				else:
					temp_hop.append(None)
			except KeyError:
				pass

		temp_hop = list(sorted([x for x in temp_hop if x is not None], key=lambda k: k[u'Values'][u'Time']))
		for hop in reversed(temp_hop):
			if hop[u'Values'][u'Type'] != u'Hop':
				start += u'<tr>'
				start += u'<td class="hop1">{name}</td>'.format(name=hop[u'Name'])
				start += u'<td class="hop2">{type}</td>'.format(type=hop[u'Values'][u'Type'])
				start += u'<td class="hop3">{alpha}</td>'.format(alpha=hop[u'Values'][u'Alpha'])
				start += u'<td class="hop4">{time}</td>'.format(time=round(hop[u'Values'][u'Time']))
				start += u'<td class="hop5">{lb}:{oz}</td>'.format(lb=int(hop[u'Values'][u'lb:oz'][0]), oz=round(hop[u'Values'][u'lb:oz'][1], 1))
				start += u'<td class="hop5">{grams}</td>'.format(grams=(round(hop[u'Values'][u'Grams'], 1)) if (hop[u'Values'][u'Grams']-int(hop[u'Values'][u'Grams'])) >= 2 else round(hop[u'Values'][u'Grams']))
				start += u'<td class="hop6">{percentage}%</td>'.format(percentage=hop[u'Values'][u'Percent'])
				start += u'</tr>'
			else:
				start += u'<tr>'
				start += u'<td class="hop1">{name}</td>'.format(name=hop[u'Name'])
				start += u'<td class="hop2">N/A</td>'
				start += u'<td class="hop3">N/A</td>'
				start += u'<td class="hop4">{time}</td>'.format(time=hop[u'Values'][u'Time'])
				start += u'<td class="hop5">N/A</td>'
				start += u'<td class="hop5">N/A</td>'
				start += u'<td class="hop6">N/A</td>'
				start += u'</tr>'
		start += u'</table><br>'
		if start[-236:] == u'<tr><th class="subhead">Hop Variety</th><th class="subhead">Type</th><th class="subhead">Alpha</th><th class="subhead">Time</th><th class="subhead">lb:oz</th><th class="subhead">Grams</th><th class="subhead2">Ratio</th></tr></table><br>': start = start[:-236]


		if use_sorttable:
			start += u'<table style="width:800px" class="sortable" id="sortable">'
		else:
			start += u'<table style="width:800px">'
		start += u'<tr><th class="subhead">Yeast</th><th class="subhead">Lab</th><th class="subhead">Origin</th><th class="subhead">Type</th><th class="subhead">Flocculation</th><th class="subhead">Attenuation</th><th class="subhead2">Temperature</th></tr>'
		for addition in self.sixth_tab.added_additions:
			try:
				if brew_data.yeast_data[addition][u'Type'] == u'D':
					yeast_type = u'Dry'
				elif brew_data.yeast_data[addition][u'Type'] == u'L':
					yeast_type = u'Liquid'
				else:
					yeast_type = brew_data.yeast_data[addition][u'Type']

				lab = brew_data.yeast_data[addition][u'Lab']
				origin = brew_data.yeast_data[addition][u'Origin']
				flocculation = brew_data.yeast_data[addition][u'Flocculation']
				attenuation = brew_data.yeast_data[addition][u'Attenuation']
				if len(brew_data.yeast_data[addition][u'Temperature'].replace(u'°', u'').split(u'-')) >= 2:
					temperature = brew_data.yeast_data[addition][u'Temperature'].replace(u'°', u'').split(u'-')[0]
					temperature += u'-' + brew_data.yeast_data[addition][u'Temperature'].replace(u'°', u'').split(u'-')[1]
				else:
					temperature = temperature

				start += u'<tr>'
				start += u'<td class="yst1">{name}</td>'.format(name=addition)
				start += u'<td class="yst2">{lab}</td>'.format(lab=lab)
				start += u'<td class="yst3">{origin}</td>'.format(origin=origin)
				start += u'<td class="yst4">{yeast_type}</td>'.format(yeast_type=yeast_type)
				start += u'<td class="yst5">{flocculation}</td>'.format(flocculation=flocculation)
				start += u'<td class="yst6">{attenuation}</td>'.format(attenuation=attenuation)
				start += u'<td class="yst7">{temperature}</td>'.format(temperature=temperature)
				start += u'</tr>'
			except KeyError:
				try:
					if brew_data.water_chemistry_additions[addition][u'Values'][u'Type'] == u'Yeast':
						start += u'<tr>'
						start += u'<td class="yst1">{name}</td>'.format(name=addition)
						start += u'<td class="yst2">N/A</td>'
						start += u'<td class="yst3">N/A</td>'
						start += u'<td class="yst4">N/A</td>'
						start += u'<td class="yst5">N/A</td>'
						start += u'<td class="yst6">N/A</td>'
						start += u'<td class="yst7">N/A</td>'
						start += u'</tr>'
				except KeyError:
					pass
		start += u'</table>'
		if start[-245:] == u'<tr><th class="subhead">Yeast</th><th class="subhead">Lab</th><th class="subhead">Origin</th><th class="subhead">Type</th><th class="subhead">Flocculation</th><th class="subhead">Attenuation</th><th class="subhead2">Temperature</th></tr></table>': start = start[:-245]

		start += u'<p><b>Final Volume: </b>{volume} Litres</p>'.format(volume=self.volume.get())
		start += u'<p><b>Original Gravity: </b>{og}</p>'.format(og=round(self.og, 1))
		start += u'<p><b>Final Gravity: </b>{fg}</p>'.format(fg=round(self.fg, 1))
		start += u'<p><b>Alcohol Content: </b>{abv}% ABV</p>'.format(abv=round(self.abv, 1))
		start += u'<p><b>Mash Efficiency: </b>{efficiency}</p>'.format(efficiency=brew_data.constants[u'Efficiency']*100)
		start += u'<p><b>Bitterness: </b>{bitterness} IBU</p>'.format(bitterness=round(self.ibu))
		start += u'<p><b>Colour: </b>{colour} EBC</p>'.format(colour=round(self.colour, 1))
		notes = self.seventh_tab.texpert.get(u'1.0', u'end')
		if self.seventh_tab.html_formatting.get():
			start += u'''<hr><h2>Notes</h2>\n{notes}'''.format(notes=notes) if len(notes) >= 1 else u''
		else:
			start += u'''<hr><h2>Notes</h2>\n<p>{notes}</p>'''.format(notes=notes.replace(u'\n', u'<br>')) if len(notes) >= 1 else u''
		start += u'</body>'
		start += u'</html>'

		start = bs4.BeautifulSoup(start, features=u"html.parser").prettify() if u'bs4' in sys.modules else start
		text_file_name = resource_path(u'{recipe_name}.html'.format(recipe_name=self.recipe_name_ent.get().replace(u'/', u'⁄')))
		with open(text_file_name, u'w') as hs:
			hs.write(start)
		if open_browser: webbrowser.open(u'file://' + os.path.realpath(text_file_name), new=1)

	def create_complex_html(self):
		self.create_html(use_sorttable=True)

	def open_file(self, file):
		if file != u'' and file != None and type(file) != tuple:
			self.sixth_tab.original_additions = list(sorted(brew_data.water_chemistry_additions)) + list(sorted(brew_data.yeast_data))
			self.sixth_tab.added_additions = []
			self.sixth_tab.refresh_all()
			examples = [u'1920s Bitter', u'Bog-Standard Bitter', u'Black-Country Mild', u'Irish Stout', u'1920s Mild', u'1920s Porter', u'1920s Stock Ale', u'1920s Stout']
			is_ogfixed = 0
			is_ebufixed = 0
			self.ingredients = []
			self.hops = []
			self.seventh_tab.texpert.delete(u'1.0', u'end')
			notes = ''
			if file.lower()[-5:] == u'.berf' or file.split(u'/')[-1] in examples:
				self.current_file = file
				with open(file, u'rb') as f:
					#data = [line for line in f]
					data = [line.replace('\xa7', '\t').strip().decode(u'ISO-8859-1').split(u'\t') for line in f]
					#print(data)
					for sublist in data:
						if sublist[0] == u'grain':
							grams = float(sublist[7])
							lb = grams/brew_data.constants[u'Conversion'][u'lb-g']
							oz = (lb-int(lb))*16
							percent = float(sublist[8])
							EBC = float(sublist[2])
							self.ingredients.append({u'Name': sublist[1], u'Values': {u'EBC': EBC, u'Grav': 0, u'lb:oz': (lb,oz), u'Grams': grams, u'Percent': percent}})
						elif sublist[0] == u'hop':
							alpha = float(sublist[3])
							grams = float(sublist[5])
							lb = grams/brew_data.constants[u'Conversion'][u'lb-g']
							oz = (lb-int(lb))*16
							time = float(sublist[6])
							percent = float(sublist[7])
							self.hops.append({u'Name': sublist[1], u'Values': {u'Type': sublist[2], u'Alpha': alpha, u'Time': time, u'Util': 0.0, u'ibu': 0.0, u'lb:oz': (lb,oz), u'Grams': grams, u'Percent': percent}})
						elif sublist[0] == u'add':
							name = sublist[1]
							dictionary = ast.literal_eval(sublist[2])
							if u'Lab' in dictionary:
								brew_data.yeast_data[name] = dictionary
							else:
								brew_data.water_chemistry_additions[name] = dictionary

							self.sixth_tab.added_additions.append(name)

						elif sublist[1] == u'recipename':
							self.recipe_name_ent.delete(0, tk.END)
							self.recipe_name_ent.insert(0, sublist[2])
						elif sublist[1] == u'volume':
							self.volume_ent.delete(0, tk.END)
							self.volume_ent.insert(0, sublist[2])
							if not any(e[1] == u'boilvol' for e in data):
								self.boil_volume_ent.delete(0, tk.END)
								self.boil_volume_ent.insert(0, float(sublist[2])*brew_data.constants[u'Boil Volume Scale'])
						elif sublist[1] == u'boilvol':
							self.boil_volume_ent.delete(0, tk.END)
							self.boil_volume_ent.insert(0, sublist[2])
						elif sublist[1] == u'efficiency':
							brew_data.constants[u'Efficiency'] = float(sublist[2])/100
						elif sublist[0] == u'miscel':
							if sublist[1] == u'ogfixed':
								is_ogfixed = sublist[2]
							elif sublist[1] == u'ebufixed':
								is_ebufixed = sublist[2]
							elif sublist[1] == u'notes':
								# notes += bytes(sublist[2],encoding='utf8')
								# print(notes, str(sublist[2]))
								notes = sublist[2]
								# print(notes, ast.literal_eval("'"+notes+"'"))

			elif file.lower()[-6:] == u'.berfx':
				self.current_file = file
				with open(file, u'r') as f:
					#data = [line.replace(b'\xa7', b'\t').strip().decode().split('\t') for line in f]
					data = [line.replace(u'\xa7', u'\t').strip().split(u'\t') for line in f]
					for sublist in data:
						if sublist[0] == u'grain':
							self.ingredients.append({u'Name': sublist[1] , u'Values': ast.literal_eval(sublist[2])})
						elif sublist[0] == u'hop':
							self.hops.append({u'Name': sublist[1] , u'Values': ast.literal_eval(sublist[2])})
						elif sublist[0] == u'add':
							name = sublist[1]
							dictionary = ast.literal_eval(sublist[2])

							if u'Lab' in dictionary:
								brew_data.yeast_data[name] = dictionary
							else:
								brew_data.water_chemistry_additions[name] = dictionary

							self.sixth_tab.added_additions.append(name)
						elif sublist[0] == u'database':
							if sublist[1] == u'grist':
								brew_data.grist_data[sublist[2]] = ast.literal_eval(sublist[3])
							elif sublist[1] == u'hop':
								brew_data.hop_data[sublist[2]] = ast.literal_eval(sublist[3])
							elif sublist[1] == u'yeast':
								brew_data.yeast_data[sublist[2]] = ast.literal_eval(sublist[3])
							elif sublist[1] == u'water_chem':
								brew_data.water_chemistry_additions[sublist[2]] = ast.literal_eval(sublist[3])
							elif sublist[1] == u'constant':
								for constant, value in ast.literal_eval(sublist[2]).items():
									brew_data.constants[constant] = value
						elif sublist[0] == u'miscel':
							if sublist[1] == u'ogfixed':
								is_ogfixed = sublist[2]
							elif sublist[1] == u'ebufixed':
								is_ebufixed = sublist[2]
							elif sublist[1] == u'recipename':
								self.recipe_name_ent.delete(0, tk.END)
								self.recipe_name_ent.insert(0, sublist[2])
							elif sublist[1] == u'notes':
								#notes += bytes(sublist[2],encoding='utf8')
								notes = sublist[2]

			self.seventh_tab.texpert.insert(u'1.0', ast.literal_eval(u"'"+notes+u"'"))
			self.refresh_hop()
			self.refresh_grist()
			self.sixth_tab.original_additions = sorted(set(self.sixth_tab.original_additions) - set(self.sixth_tab.added_additions), key=self.sixth_tab.original_additions.index)
			#print(set(self.sixth_tab.original_additions) - set(self.sixth_tab.added_additions))
			self.fifth_tab.open_locals()
			self.sixth_tab.refresh_all()
			self.recalculate()
			self.is_ogfixed.set(is_ogfixed)
			self.is_ebufixed.set(is_ebufixed)
			self.recalculate()


	def save_file(self, file):
		if file != u'' and type(file) == unicode:
			if file.lower()[-5:] == u'.berf':
				self.current_file = file
				with codecs.open(file, u'w', u'ISO-8859-1', errors=u'ignore') as f:
					for ingredient in self.ingredients:
						ebc = ingredient[u'Values'][u'EBC']
						ingred_type = brew_data.grist_data[ingredient[u'Name']][u'Type']
						units = (ingredient[u'Values'][u'Grams']/1000)*brew_data.constants[u'Efficiency']
						moisture = brew_data.grist_data[ingredient[u'Name']][u'Moisture']
						fermentability = brew_data.grist_data[ingredient[u'Name']][u'Fermentability']
						grams = ingredient[u'Values'][u'Grams']
						percentage = ingredient[u'Values'][u'Percent']
						f.write(u'grain\xa7{name}\t{ebc}\t{type}\t{units}\t{moisture}\t{fermentability}\t{grams}\t{percentage}\n'.format(name=ingredient[u'Name'], ebc=ebc, type=ingred_type, units=units, moisture=moisture, fermentability=fermentability, grams=grams, percentage=percentage))
					for hop in self.hops:
						# 'Values': {'Type': 'Whole', 'Alpha': 12.7, 'Time': 0.0, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}
						hop_type = hop[u'Values'][u'Type']
						alpha = hop[u'Values'][u'Alpha']
						ibu =  hop[u'Values'][u'ibu']
						grams = hop[u'Values'][u'Grams']
						time = hop[u'Values'][u'Time']
						percentage = hop[u'Values'][u'Percent']
						f.write(u'hop\xa7{name}\t{type}\t{alpha}\t{ibu}\t{grams}\t{time}\t{percentage}\n'.format(name=hop[u'Name'], type=hop_type, alpha=alpha, ibu=ibu, grams=grams, time=time, percentage=percentage))
					for addition in self.sixth_tab.added_additions:
						all_chem = dict(brew_data.water_chemistry_additions)
						all_chem.update(brew_data.yeast_data)
						name = addition
						addition_type = all_chem[name]
						f.write(u'add\xa7{name}\t{type}\n'.format(name=name, type=addition_type))
					f.write(u'default\xa7efficiency\t{efficiency}\n'.format(efficiency=brew_data.constants[u'Efficiency']*100))
					f.write(u'default\xa7volume\t{volume}\n'.format(volume=self.volume.get()))
					f.write(u'default\xa7boilvol\t{boilvol}\n'.format(boilvol=self.boil_vol.get()))
					f.write(u'miscel\xa7recipename\t{recipename}\n'.format(recipename=self.recipe_name_ent.get()))
					f.write(u'miscel\xa7ogfixed\t{ogfixed}\n'.format(ogfixed=self.is_ogfixed.get()))
					f.write(u'miscel\xa7ebufixed\t{ebufixed}\n'.format(ebufixed=self.is_ebufixed.get()))
					f.write(u'miscel\xa7origgrav\t{origgrav}\n'.format(origgrav=self.og))

					notes = repr(self.seventh_tab.texpert.get(u'1.0', u'end'))#, encoding='utf8')
					# print(notes)
					f.write(u'miscel\xa7notes\t{notes}\n'.format(notes=notes[1:-1]))

			elif file.lower()[-6:] == u'.berfx':
				self.current_file = file
				with open(file, u'w') as f:
					for ingredient in self.ingredients:
						f.write(u'grain\xa7{name}\t{data}\n'.format(name=ingredient[u'Name'], data=ingredient[u'Values']))
					for hop in self.hops:
						# 'Values': {'Type': 'Whole', 'Alpha': 12.7, 'Time': 0.0, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}
						f.write(u'hop\xa7{name}\t{data}\n'.format(name=hop[u'Name'], data=hop[u'Values']))
					for addition in self.sixth_tab.added_additions:
						all_chem = dict(brew_data.water_chemistry_additions)
						all_chem.update(brew_data.yeast_data)
						name = addition
						addition_type = all_chem[name]
						f.write(u'add\xa7{name}\t{type}\n'.format(name=name, type=addition_type))

					f.write(u'miscel\xa7ogfixed\t{ogfixed}\n'.format(ogfixed=self.is_ogfixed.get()))
					f.write(u'miscel\xa7ebufixed\t{ebufixed}\n'.format(ebufixed=self.is_ebufixed.get()))
					f.write(u'miscel\xa7recipename\t{recipename}\n'.format(recipename=self.recipe_name_ent.get()))
					f.write(u'default\xa7boilvol\t{boilvol}\n'.format(boilvol=self.boil_vol.get()))

					notes = repr(self.seventh_tab.texpert.get(u'1.0', u'end'))
					f.write(u'miscel\xa7notes\t{notes}\n'.format(notes=notes[1:-1]))

					for key, grist in brew_data.grist_data.items(): f.write(u'database\xa7grist\xa7{name}\t{data}\n'.format(name=key, data=grist))
					for key, hop in brew_data.hop_data.items(): f.write(u'database\xa7hop\xa7{name}\t{data}\n'.format(name=key, data=hop))
					for key, yeast in brew_data.yeast_data.items(): f.write(u'database\xa7yeast\xa7{name}\t{data}\n'.format(name=key, data=yeast))
					for key, water_chem in brew_data.water_chemistry_additions.items(): f.write(u'database\xa7water_chem\xa7{name}\t{data}\n'.format(name=key, data=water_chem))
					#for key, constant in brew_data.constants.items(): f.write('database\xa7constant\xa7{name}\t{data}\n'.format(name=key, data=constant))
					f.write(u'database\xa7constant\xa7{constants}'.format(constants=brew_data.constants))

	def save(self):
		if self.current_file != u'':
			self.save_file(self.current_file)
		else:
		 	self.save_file(filedialog.asksaveasfilename(initialdir = os.path.expanduser(u'~/.config/Wheelers-Wort-Works/recipes/' if __mode__ == u'deb' else u'.'),title = u"Select file", defaultextension=u".berf", initialfile=u'{0}.berf'.format(self.recipe_name_ent.get())))

	def save_all(self):
		self.save()
		self.create_html()

	def quit(self):
		if messagebox.askokcancel(u"Quit", u"Do you want to quit?"):
			if brew_data.constants[u'Save On Close']:
				self.save()
			self.master.destroy()

	def add_percent_ingredients(self, amount, curr_selection=None):
		try:
			if curr_selection is None:
				selection = self.scrolled_tree_ingredient.selection()[0]
			else:
				selection = curr_selection
			id = int(unicode(selection)[1:], 16)
			percent = self.ingredients[id-1][u'Values'][u'Percent'] + amount
			if percent < 0: percent = 0
			self.ingredients[id-1][u'Values'][u'Percent'] = percent
			self.refresh_grist()
			self.scrolled_tree_ingredient.focus_set()
			self.scrolled_tree_ingredient.see(selection)
			self.scrolled_tree_ingredient.selection_set(selection)
		except IndexError:
			pass

	def add_percent_hops(self, amount, curr_selection=None):
		try:
			if curr_selection is None:
				selection = self.scrolled_tree_hops.selection()[0]
			else:
				selection = curr_selection
			id = int(unicode(selection)[1:], 16)
			percent = self.hops[id-1][u'Values'][u'Percent'] + amount
			if percent < 0: percent = 0
			self.hops[id-1][u'Values'][u'Percent'] = percent
			self.refresh_hop()
			self.scrolled_tree_hops.focus_set()
			self.scrolled_tree_hops.see(selection)
			self.scrolled_tree_hops.selection_set(selection)
		except IndexError:
			pass

	def ebu_fixed(self):
		if self.is_ebufixed.get() == 1:
			self.add_100g_hop_butt.configure(text=u'''+10%''')
			self.add_100g_hop_butt.configure(command=lambda: self.add_percent_hops(10))
			self.add_100g_hop_butt.configure(font=u"TkFixedFont")

			self.rem_100g_hop_butt.configure(text=u'''-10%''')
			self.rem_100g_hop_butt.configure(command=lambda: self.add_percent_hops(-10))
			self.rem_100g_hop_butt.configure(font=u"TkFixedFont")

			self.add_25g_hop_butt.configure(text=u'''+5%''')
			self.add_25g_hop_butt.configure(command=lambda: self.add_percent_hops(5))
			self.add_25g_hop_butt.configure(font=u"TkFixedFont")

			self.rem_25g_hop_butt.configure(text=u'''-5%''')
			self.rem_25g_hop_butt.configure(command=lambda: self.add_percent_hops(-5))
			self.rem_25g_hop_butt.configure(font=u"TkFixedFont")

			self.add_10g_hop_butt.configure(text=u'''+1%''')
			self.add_10g_hop_butt.configure(command=lambda: self.add_percent_hops(1))
			self.add_10g_hop_butt.configure(font=u"TkFixedFont")

			self.rem_10g_hop_butt.configure(text=u'''-1%''')
			self.rem_10g_hop_butt.configure(command=lambda: self.add_percent_hops(-1))
			self.rem_10g_hop_butt.configure(font=u"TkFixedFont")

			self.add_1g_hop_butt.configure(text=u'''+0.1%''')
			self.add_1g_hop_butt.configure(command=lambda: self.add_percent_hops(0.1))
			self.add_1g_hop_butt.configure(font=u"TkFixedFont")

			self.rem_1g_hop_butt.configure(text=u'''-0.1%''')
			self.rem_1g_hop_butt.configure(command=lambda: self.add_percent_hops(-0.1))
			self.rem_1g_hop_butt.configure(font=u"TkFixedFont")
		else:
			self.hop_to_imperial()

	def og_fixed(self):
		if self.is_ogfixed.get() == 1:
			self.add_1000g_ing_butt.configure(text=u'''+10%''')
			self.add_1000g_ing_butt.configure(command=lambda: self.add_percent_ingredients(10))
			self.add_1000g_ing_butt.configure(font=u"TkFixedFont")

			self.add_100g_ing_butt.configure(text=u'''+5%''')
			self.add_100g_ing_butt.configure(command=lambda: self.add_percent_ingredients(5))
			self.add_100g_ing_butt.configure(font=u"TkFixedFont")

			self.rem_1000g_ing_butt.configure(text=u'''-10%''')
			self.rem_1000g_ing_butt.configure(command=lambda: self.add_percent_ingredients(-10))
			self.rem_1000g_ing_butt.configure(font=u"TkFixedFont")

			self.rem_100g_ing_butt.configure(text=u'''-5%''')
			self.rem_100g_ing_butt.configure(command=lambda: self.add_percent_ingredients(-5))
			self.rem_100g_ing_butt.configure(font=u"TkFixedFont")

			self.add_10g_ing_butt.configure(text=u'''+1%''')
			self.add_10g_ing_butt.configure(command=lambda: self.add_percent_ingredients(1))
			self.add_10g_ing_butt.configure(font=u"TkFixedFont")

			self.rem_10g_ing_butt.configure(text=u'''-1%''')
			self.rem_10g_ing_butt.configure(command=lambda: self.add_percent_ingredients(-1))
			self.rem_10g_ing_butt.configure(font=u"TkFixedFont")

			self.add_1g_ing_butt.configure(text=u'''+0.1%''')
			self.add_1g_ing_butt.configure(command=lambda: self.add_percent_ingredients(0.1))
			self.add_1g_ing_butt.configure(font=u"TkFixedFont")

			self.rem_1g_ing_butt.configure(text=u'''-0.1%''')
			self.rem_1g_ing_butt.configure(command=lambda: self.add_percent_ingredients(-0.1))
			self.rem_1g_ing_butt.configure(font=u"TkFixedFont")
		else:
			self.ingredient_to_imperial()

class hops_editor(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.widgets()

	def widgets(self):
		u'''This class configures and populates the toplevel window.
		   top is the toplevel containing window.'''
		_fgcolor = u'#000000'  # X11 color: 'black'
		_compcolor = u'#d9d9d9' # X11 color: 'gray85'
		_ana1color = u'#d9d9d9' # X11 color: 'gray85'
		_ana2color = u'#ececec' # Closest X11 color: 'gray92'
		font9 = u"-family {DejaVu Sans} -size 10 -weight bold -slant "  \
			u"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()
		self.style.configure(u'.',background=_bgcolor)
		self.style.configure(u'.',foreground=_fgcolor)
		self.style.configure(u'.',font=u"TkDefaultFont")
		self.style.map(u'.',background=
			[(u'selected', _compcolor), (u'active',_ana2color)])

		self.TPanedwindow1 = tk.PanedWindow(self, orient=u"horizontal")
		self.TPanedwindow1.place(relx=0.013, rely=0.0, relheight=0.973
				, relwidth=0.966)
		self.TPanedwindow1.configure(width=800)
		self.hop_panedwindow1 = tk.LabelFrame(width=400, text=u'Hops:', background=_bgcolor)
		self.TPanedwindow1.add(self.hop_panedwindow1)
		self.hop_panedwindow2 = tk.LabelFrame(text=u'Modifications:', background=_bgcolor)
		self.TPanedwindow1.add(self.hop_panedwindow2)

		self.hop_lstbx = ScrolledListBox(self.hop_panedwindow1)
		self.hop_lstbx.place(relx=0.025, rely=0.043, relheight=0.887
				, relwidth=0.94, bordermode=u'ignore')
		self.hop_lstbx.configure(background=u"white")
		self.hop_lstbx.configure(font=u"TkFixedFont")
		self.hop_lstbx.configure(highlightcolor=u"#d9d9d9")
		self.hop_lstbx.configure(selectbackground=u"#c4c4c4")
		self.hop_lstbx.configure(width=10)

		self.hop_delete_butt = tk.Button(self.hop_panedwindow1)
		self.hop_delete_butt.place(relx=0.025, rely=0.929, height=28, width=83
				, bordermode=u'ignore')
		self.hop_delete_butt.configure(takefocus=u"")
		self.hop_delete_butt.configure(text=u'''Delete''')
		self.hop_delete_butt.configure(command=self.delete)

		self.hop_modify_butt = tk.Button(self.hop_panedwindow1)
		self.hop_modify_butt.place(relx=0.35, rely=0.929, height=28, width=83
				, bordermode=u'ignore')
		self.hop_modify_butt.configure(takefocus=u"")
		self.hop_modify_butt.configure(text=u'''Modify''')
		self.hop_modify_butt.configure(command=lambda: self.input_state(1))

		self.hop_new_butt = tk.Button(self.hop_panedwindow1)
		self.hop_new_butt.place(relx=0.725, rely=0.929, height=28, width=83
				, bordermode=u'ignore')
		self.hop_new_butt.configure(takefocus=u"")
		self.hop_new_butt.configure(text=u'''New''')
		self.hop_new_butt.configure(command=self.new)

		############################ Config Section ############################

		self.hop_name_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_name_lbl.place(relx=0.056, rely=0.087, bordermode=u'ignore')
		self.hop_name_lbl.configure(background=_bgcolor)
		self.hop_name_lbl.configure(foreground=u"#000000")
		self.hop_name_lbl.configure(font=font9)
		self.hop_name_lbl.configure(relief=u'flat')
		self.hop_name_lbl.configure(text=u'''Name:''')

		self.hop_name_ent = tk.Entry(self.hop_panedwindow2)
		self.hop_name_ent.place(relx=0.222, rely=0.087, relheight=0.046
				, relwidth=0.511, bordermode=u'ignore')
		self.hop_name_ent.configure(justify=u'center')
		self.hop_name_ent.configure(width=184)
		self.hop_name_ent.configure(foreground=u"#000000")
		self.hop_name_ent.configure(takefocus=u"")
		self.hop_name_ent.configure(cursor=u"xterm")

		self.hop_form_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_form_lbl.place(relx=0.056, rely=0.152, bordermode=u'ignore')
		self.hop_form_lbl.configure(background=_bgcolor)
		self.hop_form_lbl.configure(foreground=u"#000000")
		self.hop_form_lbl.configure(font=font9)
		self.hop_form_lbl.configure(relief=u'flat')
		self.hop_form_lbl.configure(text=u'''Form:''')

		self.hop_form_combo = ttk.Combobox(self.hop_panedwindow2)
		self.hop_form_combo.place(relx=0.222, rely=0.152, relheight=0.046
				, relwidth=0.511, bordermode=u'ignore')
		self.hop_form_combo.configure(justify=u'center')
		self.hop_form_combo.configure(width=187)
		self.hop_form_combo.configure(takefocus=u"")
		self.hop_form_combo_values = [u"Whole", u"Pellet"]
		self.hop_form_combo.configure(values=self.hop_form_combo_values)

		self.hop_origin_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_origin_lbl.place(relx=0.056, rely=0.217, bordermode=u'ignore')
		self.hop_origin_lbl.configure(background=_bgcolor)
		self.hop_origin_lbl.configure(foreground=u"#000000")
		self.hop_origin_lbl.configure(font=font9)
		self.hop_origin_lbl.configure(relief=u'flat')
		self.hop_origin_lbl.configure(text=u'''Origin:''')

		self.hop_origin_ent = tk.Entry(self.hop_panedwindow2)
		self.hop_origin_ent.place(relx=0.222, rely=0.217, relheight=0.046
				, relwidth=0.511, bordermode=u'ignore')
		self.hop_origin_ent.configure(justify=u'center')
		self.hop_origin_ent.configure(width=184)
		self.hop_origin_ent.configure(takefocus=u"")
		self.hop_origin_ent.configure(cursor=u"xterm")

		self.hop_alpha_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_alpha_lbl.place(relx=0.056, rely=0.283, bordermode=u'ignore')
		self.hop_alpha_lbl.configure(background=_bgcolor)
		self.hop_alpha_lbl.configure(foreground=u"#000000")
		self.hop_alpha_lbl.configure(font=font9)
		self.hop_alpha_lbl.configure(relief=u'flat')
		self.hop_alpha_lbl.configure(text=u'''Alpha:''')

		self.hop_alpha_ent = tk.Entry(self.hop_panedwindow2)
		self.hop_alpha_ent.place(relx=0.222, rely=0.283, relheight=0.046
				, relwidth=0.456, bordermode=u'ignore')
		self.hop_alpha_ent.configure(justify=u'center')
		self.hop_alpha_ent.configure(takefocus=u"")
		self.hop_alpha_ent.configure(cursor=u"xterm")

		self.hop_alpha_percent = tk.Label(self.hop_panedwindow2)
		self.hop_alpha_percent.place(relx=0.694, rely=0.283, bordermode=u'ignore')
		self.hop_alpha_percent.configure(background=_bgcolor)
		self.hop_alpha_percent.configure(foreground=u"#000000")
		self.hop_alpha_percent.configure(font=font9)
		self.hop_alpha_percent.configure(relief=u'flat')
		self.hop_alpha_percent.configure(text=u'''%''')

		self.hop_use_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_use_lbl.place(relx=0.056, rely=0.348, bordermode=u'ignore')
		self.hop_use_lbl.configure(background=_bgcolor)
		self.hop_use_lbl.configure(foreground=u"#000000")
		self.hop_use_lbl.configure(font=font9)
		self.hop_use_lbl.configure(relief=u'flat')
		self.hop_use_lbl.configure(text=u'''Use:''')

		self.hop_use_combo = ttk.Combobox(self.hop_panedwindow2)
		self.hop_use_combo.place(relx=0.222, rely=0.348, relheight=0.046
				, relwidth=0.511, bordermode=u'ignore')
		self.hop_use_combo.configure(justify=u'center')
		self.hop_use_combo_values = [u"Bittering", u"Aroma", u"General Purpose"]
		self.hop_use_combo.configure(values=self.hop_use_combo_values)
		self.hop_use_combo.configure(takefocus=u"")
		self.hop_comm_ent = tk.Entry(self.hop_panedwindow2)
		self.hop_comm_ent.place(relx=0.028, rely=0.5, relheight=0.046
				, relwidth=0.956, bordermode=u'ignore')
		self.hop_comm_ent.configure(width=344)
		self.hop_comm_ent.configure(takefocus=u"")
		self.hop_comm_ent.configure(cursor=u"xterm")

		self.hop_comm_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_comm_lbl.place(relx=0.056, rely=0.453, bordermode=u'ignore')
		self.hop_comm_lbl.configure(background=_bgcolor)
		self.hop_comm_lbl.configure(foreground=u"#000000")
		self.hop_comm_lbl.configure(font=font9)
		self.hop_comm_lbl.configure(relief=u'flat')
		self.hop_comm_lbl.configure(text=u'''Comments:''')

		self.hop_cancel_butt = tk.Button(self.hop_panedwindow2)
		self.hop_cancel_butt.place(relx=0.028, rely=0.565, height=28, width=83
				, bordermode=u'ignore')
		self.hop_cancel_butt.configure(takefocus=u"")
		self.hop_cancel_butt.configure(text=u'''Cancel''')
		self.hop_cancel_butt.configure(command=lambda: self.show_data(self.hop_lstbx.get(tk.ACTIVE)))

		self.hop_clear_butt = tk.Button(self.hop_panedwindow2)
		self.hop_clear_butt.place(relx=0.389, rely=0.565, height=28, width=83
				, bordermode=u'ignore')
		self.hop_clear_butt.configure(takefocus=u"")
		self.hop_clear_butt.configure(text=u'''Clear Form''')
		self.hop_clear_butt.configure(command=self.clear_form)

		self.hop_done_butt = tk.Button(self.hop_panedwindow2)
		self.hop_done_butt.place(relx=0.75, rely=0.565, height=28, width=83
				, bordermode=u'ignore')
		self.hop_done_butt.configure(takefocus=u"")
		self.hop_done_butt.configure(text=u'''Done''')
		self.hop_done_butt.configure(command=self.done)

		self.hop_save_data_butt = tk.Button(self.hop_panedwindow2)
		self.hop_save_data_butt.place(relx=0.222, rely=0.696, height=108
				, width=213, bordermode=u'ignore')
		self.hop_save_data_butt.configure(takefocus=u"")
		self.hop_save_data_butt.configure(text=u'''Save to Database''')
		self.hop_save_data_butt.configure(width=213)
		self.hop_save_data_butt.configure(command=self.save)

		self.hop_lstbx.bind(u'<<ListboxSelect>>', self.select_listbox)
		self.show_data(list(sorted(brew_data.hop_data.keys()))[0])

	def __adjust_sash0(self, event):
		paned = event.widget
		pos = [400, ]
		i = 0
		for sash in pos:
			paned.sashpos(i, sash)
			i += 1
		paned.unbind(u'<map>', self.__funcid0)
		del self.__funcid0

	def select_listbox(self, event):
		try:
			self.show_data(self.hop_lstbx.get(self.hop_lstbx.curselection()))
		except:
			pass

	def show_data(self, hop):
		self.input_state(1)
		self.name = hop
		name = hop
		form = brew_data.hop_data[name][u'Form']
		origin = brew_data.hop_data[name][u'Origin']
		description = brew_data.hop_data[name][u'Description']
		use = brew_data.hop_data[name][u'Use']
		alpha = brew_data.hop_data[name][u'Alpha']

		self.hop_name_ent.delete(0, tk.END)
		self.hop_origin_ent.delete(0, tk.END)
		self.hop_alpha_ent.delete(0, tk.END)
		self.hop_comm_ent.delete(0, tk.END)

		if form not in self.hop_form_combo_values:
			self.hop_form_combo_values.append(form)
			self.hop_form_combo.configure(values=self.hop_form_combo_values)

		if use not in self.hop_use_combo_values:
			self.hop_use_combo_values.append(use)
			self.hop_use_combo.configure(values=self.hop_use_combo_values)

		self.hop_name_ent.insert(0, name)
		self.hop_origin_ent.insert(0, origin)
		self.hop_alpha_ent.insert(0, alpha)
		self.hop_comm_ent.insert(0, description)

		self.hop_form_combo.set(form)
		self.hop_use_combo.set(use)

		self.input_state(0)

	def input_state(self, state):
		state = u"disabled" if state == 0 else u"normal"

		self.hop_name_ent.configure(state=state)
		self.hop_origin_ent.configure(state=state)
		self.hop_alpha_ent.configure(state=state)
		self.hop_comm_ent.configure(state=state)

		self.hop_form_combo.configure(state=state)
		self.hop_use_combo.configure(state=state)

		self.hop_done_butt.configure(state=state)
		self.hop_clear_butt.configure(state=state)
		self.hop_cancel_butt.configure(state=state)

	def done(self):
		name = self.hop_name_ent.get()
		form = self.hop_form_combo.get()
		origin = self.hop_origin_ent.get()
		alpha = float(self.hop_alpha_ent.get())
		use = self.hop_use_combo.get()
		description = self.hop_comm_ent.get()
		brew_data.hop_data[name] = {u'Form': form, u'Origin': origin, u'Description': description, u'Use': use, u'Alpha': alpha}
		del brew_data.hop_data[self.name]
		idx = list(sorted(brew_data.hop_data.keys())).index(name)
		self.reinsert()
		self.show_data(name)

	def clear_form(self):
		self.hop_name_ent.delete(0, tk.END)
		self.hop_origin_ent.delete(0, tk.END)
		self.hop_alpha_ent.delete(0, tk.END)
		self.hop_comm_ent.delete(0, tk.END)

	def delete(self):
		del brew_data.hop_data[self.hop_lstbx.get(self.hop_lstbx.curselection())]
		self.hop_lstbx.delete(self.hop_lstbx.curselection())

	def new(self):
		name = u'New Hop {num}'.format(num=sum(u'New Hop' in s for s in brew_data.hop_data))
		self.hop_lstbx.insert(tk.END, name)
		try:
			brew_data.hop_data[name] = brew_data.hop_data[self.hop_lstbx.get(self.hop_lstbx.curselection())]
		except:
			try:
				brew_data.hop_data[name] = brew_data.hop_data[tk.ACTIVE]
			except:
				brew_data.hop_data[name] = {u'Form': u'Whole', u'Origin': u'Unkown', u'Description': u'', u'Use': u'General Purpose', u'Alpha': 12.7}
		self.show_data(name)
		self.hop_lstbx.select_set(tk.END)
		self.hop_lstbx.activate(tk.END)
		self.hop_lstbx.yview(tk.END)

	def save(self):
		with open(resource_path(u'hop_data.txt'), u'w') as f:
			for hop, value in brew_data.hop_data.items():
				name = hop
				type = value[u'Form']
				origin = value[u'Origin']
				alpha = value[u'Alpha']
				use = value[u'Use']
				description = value[u'Description']
				f.write(u'{name}\t{type}\t{origin}\t{alpha}\t{use}\t{description}\n'.format(name=name, type=type, origin=origin, alpha=alpha, use=use, description=description))

	def reinsert(self):
		self.hop_lstbx.delete(0, tk.END)
		for hop in sorted(brew_data.hop_data):
			self.hop_lstbx.insert(tk.END, hop)

class grist_editor(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.widgets()

	def widgets(self):
		u'''This class configures and populates the selflevel window.
		   self is the selflevel containing window.'''
		_fgcolor = u'#000000'  # X11 color: 'black'
		_compcolor = u'#d9d9d9' # X11 color: 'gray85'
		_ana1color = u'#d9d9d9' # X11 color: 'gray85'
		_ana2color = u'#ececec' # Closest X11 color: 'gray92'
		font10 = u"-family {DejaVu Sans} -size 10 -weight bold -slant "  \
			u"roman -underline 0 -overstrike 0"
		font9 = u"-family {DejaVu Sans} -size 9 -weight bold -slant "  \
			u"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()
		self.style.configure(u'.',background=_bgcolor)
		self.style.configure(u'.',foreground=_fgcolor)
		self.style.configure(u'.',font=u"TkDefaultFont")
		self.style.map(u'.',background=
			[(u'selected', _compcolor), (u'active',_ana2color)])

		self.TPanedwindow1 = tk.PanedWindow(self, orient=u"horizontal",  background=_bgcolor)
		self.TPanedwindow1.place(relx=0.013, rely=0.0, relheight=0.973
				, relwidth=0.966)
		self.grist_panedwindow1 = tk.LabelFrame(width=400
				, text=u'Fermentable Ingredients:',  background=_bgcolor)
		self.TPanedwindow1.add(self.grist_panedwindow1)
		self.grist_panedwindow2 = tk.LabelFrame(text=u'Modifications:',  background=_bgcolor)
		self.TPanedwindow1.add(self.grist_panedwindow2)

		self.grist_lstbx = ScrolledListBox(self.grist_panedwindow1)
		self.grist_lstbx.place(relx=0.025, rely=0.043, relheight=0.887
				, relwidth=0.94, bordermode=u'ignore')
		self.grist_lstbx.configure(background=u"white")
		self.grist_lstbx.configure(font=u"TkFixedFont")
		self.grist_lstbx.configure(highlightcolor=u"#d9d9d9")
		self.grist_lstbx.configure(selectbackground=u"#c4c4c4")
		self.grist_lstbx.configure(width=10)

		self.grist_delete_butt = tk.Button(self.grist_panedwindow1)
		self.grist_delete_butt.place(relx=0.025, rely=0.924, height=28, width=83
				, bordermode=u'ignore')
		self.grist_delete_butt.configure(takefocus=u"")
		self.grist_delete_butt.configure(text=u'''Delete''')
		self.grist_delete_butt.configure(command=self.delete)

		self.grist_modify_butt = tk.Button(self.grist_panedwindow1)
		self.grist_modify_butt.place(relx=0.35, rely=0.924, height=28, width=83
				, bordermode=u'ignore')
		self.grist_modify_butt.configure(takefocus=u"")
		self.grist_modify_butt.configure(text=u'''Modify''')
		self.grist_modify_butt.configure(command=lambda: self.input_state(1))

		self.grist_new_butt = tk.Button(self.grist_panedwindow1)
		self.grist_new_butt.place(relx=0.725, rely=0.924, height=28, width=83
				, bordermode=u'ignore')
		self.grist_new_butt.configure(takefocus=u"")
		self.grist_new_butt.configure(text=u'''New''')
		self.grist_new_butt.configure(command=self.new)

		############################ Config Section ############################

		self.grist_name_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_name_lbl.place(relx=0.056, rely=0.087, bordermode=u'ignore')
		self.grist_name_lbl.configure(background=_bgcolor)
		self.grist_name_lbl.configure(foreground=u"#000000")
		self.grist_name_lbl.configure(font=font10)
		self.grist_name_lbl.configure(relief=u'flat')
		self.grist_name_lbl.configure(text=u'''Name:''')

		self.grist_name_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_name_ent.place(relx=0.222, rely=0.087, relheight=0.046
				, relwidth=0.511, bordermode=u'ignore')
		self.grist_name_ent.configure(justify=u'center')
		self.grist_name_ent.configure(foreground=u"#000000")
		self.grist_name_ent.configure(takefocus=u"")
		self.grist_name_ent.configure(cursor=u"xterm")

		self.grist_colour_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_colour_lbl.place(relx=0.056, rely=0.152, bordermode=u'ignore')
		self.grist_colour_lbl.configure(background=_bgcolor)
		self.grist_colour_lbl.configure(foreground=u"#000000")
		self.grist_colour_lbl.configure(font=font10)
		self.grist_colour_lbl.configure(relief=u'flat')
		self.grist_colour_lbl.configure(text=u'''Colour:''')

		self.grist_colour_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_colour_ent.place(relx=0.222, rely=0.152, relheight=0.046
				, relwidth=0.511, bordermode=u'ignore')
		self.grist_colour_ent.configure(justify=u'center')
		self.grist_colour_ent.configure(foreground=u"#000000")
		self.grist_colour_ent.configure(takefocus=u"")
		self.grist_colour_ent.configure(cursor=u"xterm")

		self.grist_colour_ebc = tk.Label(self.grist_panedwindow2)
		self.grist_colour_ebc.place(relx=0.75, rely=0.152, bordermode=u'ignore')
		self.grist_colour_ebc.configure(background=_bgcolor)
		self.grist_colour_ebc.configure(foreground=u"#000000")
		self.grist_colour_ebc.configure(font=font10)
		self.grist_colour_ebc.configure(relief=u'flat')
		self.grist_colour_ebc.configure(text=u'''EBC''')

		self.grist_extract_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_extract_lbl.place(relx=0.056, rely=0.217, bordermode=u'ignore')
		self.grist_extract_lbl.configure(background=_bgcolor)
		self.grist_extract_lbl.configure(foreground=u"#000000")
		self.grist_extract_lbl.configure(font=font10)
		self.grist_extract_lbl.configure(relief=u'flat')
		self.grist_extract_lbl.configure(text=u'''Extract:''')

		self.grist_extract_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_extract_ent.place(relx=0.222, rely=0.217, relheight=0.046
				, relwidth=0.511, bordermode=u'ignore')
		self.grist_extract_ent.configure(justify=u'center')
		self.grist_extract_ent.configure(foreground=u"#000000")
		self.grist_extract_ent.configure(takefocus=u"")
		self.grist_extract_ent.configure(cursor=u"xterm")

		self.grist_extract_ldk = tk.Label(self.grist_panedwindow2)
		self.grist_extract_ldk.place(relx=0.75, rely=0.217, bordermode=u'ignore')
		self.grist_extract_ldk.configure(background=_bgcolor)
		self.grist_extract_ldk.configure(foreground=u"#000000")
		self.grist_extract_ldk.configure(font=font10)
		self.grist_extract_ldk.configure(relief=u'flat')
		self.grist_extract_ldk.configure(text=u'''LDK''')

		self.grist_moisture_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_moisture_lbl.place(relx=0.056, rely=0.283, bordermode=u'ignore')
		self.grist_moisture_lbl.configure(background=_bgcolor)
		self.grist_moisture_lbl.configure(foreground=u"#000000")
		self.grist_moisture_lbl.configure(font=font10)
		self.grist_moisture_lbl.configure(relief=u'flat')
		self.grist_moisture_lbl.configure(text=u'''Moisture:''')

		self.grist_moisture_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_moisture_ent.place(relx=0.278, rely=0.283, relheight=0.046
				, relwidth=0.456, bordermode=u'ignore')
		self.grist_moisture_ent.configure(justify=u'center')
		self.grist_moisture_ent.configure(foreground=u"#000000")
		self.grist_moisture_ent.configure(takefocus=u"")
		self.grist_moisture_ent.configure(cursor=u"xterm")

		self.grist_moisture_percent = tk.Label(self.grist_panedwindow2)
		self.grist_moisture_percent.place(relx=0.75, rely=0.283, bordermode=u'ignore')
		self.grist_moisture_percent.configure(background=_bgcolor)
		self.grist_moisture_percent.configure(foreground=u"#000000")
		self.grist_moisture_percent.configure(font=font10)
		self.grist_moisture_percent.configure(relief=u'flat')
		self.grist_moisture_percent.configure(text=u'''%''')


		self.grist_ferment_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_ferment_lbl.place(relx=0.056, rely=0.348, bordermode=u'ignore')
		self.grist_ferment_lbl.configure(background=_bgcolor)
		self.grist_ferment_lbl.configure(foreground=u"#000000")
		self.grist_ferment_lbl.configure(font=font9)
		self.grist_ferment_lbl.configure(relief=u'flat')
		self.grist_ferment_lbl.configure(text=u'''Fermentability:''')

		self.grist_ferment_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_ferment_ent.place(relx=0.361, rely=0.348, relheight=0.046
				, relwidth=0.372, bordermode=u'ignore')
		self.grist_ferment_ent.configure(takefocus=u"")
		self.grist_ferment_ent.configure(cursor=u"xterm")
		self.grist_ferment_ent.configure(justify=u'center')

		self.grist_ferment_percent = tk.Label(self.grist_panedwindow2)
		self.grist_ferment_percent.place(relx=0.75, rely=0.348, bordermode=u'ignore')
		self.grist_ferment_percent.configure(background=_bgcolor)
		self.grist_ferment_percent.configure(foreground=u"#000000")
		self.grist_ferment_percent.configure(font=font10)
		self.grist_ferment_percent.configure(relief=u'flat')
		self.grist_ferment_percent.configure(text=u'''%''')

		self.grist_type_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_type_lbl.place(relx=0.056, rely=0.413, bordermode=u'ignore')
		self.grist_type_lbl.configure(background=_bgcolor)
		self.grist_type_lbl.configure(foreground=u"#000000")
		self.grist_type_lbl.configure(font=font10)
		self.grist_type_lbl.configure(relief=u'flat')
		self.grist_type_lbl.configure(text=u'''Type:''')

		self.grist_type_combo = ttk.Combobox(self.grist_panedwindow2)
		self.grist_type_combo.place(relx=0.194, rely=0.413, relheight=0.046
				, relwidth=0.547, bordermode=u'ignore')
		self.grist_type_combo.configure(width=197)
		self.grist_type_combo.configure(takefocus=u"")
		self.grist_type_combo_values = [u'Primary Malt', u'Secondary Malt', u'Mash Tun Adjunct', u'Can Be Steeped', u'Malt Extract', u'Copper Sugar']
		#print([vals['Type'] for (grist, vals) in brew_data.grist_data.items()])
		#print([grist['Type'] for key, grist in brew_data.grist_data.items() if grist['Type'] not in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]])
		self.grist_type_combo_values.append([grist[u'Type'] for key, grist in brew_data.grist_data.items() if grist[u'Type'] not in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]])
		self.grist_type_combo.configure(values=self.grist_type_combo_values)

		self.grist_comm_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_comm_lbl.place(relx=0.056, rely=0.543, bordermode=u'ignore')
		self.grist_comm_lbl.configure(background=_bgcolor)
		self.grist_comm_lbl.configure(foreground=u"#000000")
		self.grist_comm_lbl.configure(font=font10)
		self.grist_comm_lbl.configure(relief=u'flat')
		self.grist_comm_lbl.configure(text=u'''Comments:''')

		self.grist_comm_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_comm_ent.place(relx=0.028, rely=0.587, relheight=0.046
				, relwidth=0.956, bordermode=u'ignore')
		self.grist_comm_ent.configure(foreground=u"#000000")
		self.grist_comm_ent.configure(takefocus=u"")
		self.grist_comm_ent.configure(cursor=u"xterm")

		self.grist_cancel_butt = tk.Button(self.grist_panedwindow2)
		self.grist_cancel_butt.place(relx=0.028, rely=0.652, height=28, width=83
				, bordermode=u'ignore')
		self.grist_cancel_butt.configure(takefocus=u"")
		self.grist_cancel_butt.configure(text=u'''Cancel''')
		self.grist_cancel_butt.configure(command=lambda: self.show_data(self.grist_lstbx.get(tk.ACTIVE)))

		self.grist_clear_butt = tk.Button(self.grist_panedwindow2)
		self.grist_clear_butt.place(relx=0.389, rely=0.652, height=28, width=83
				, bordermode=u'ignore')
		self.grist_clear_butt.configure(takefocus=u"")
		self.grist_clear_butt.configure(text=u'''Clear Form''')
		self.grist_clear_butt.configure(command=self.clear_form)

		self.grist_done_butt = tk.Button(self.grist_panedwindow2)
		self.grist_done_butt.place(relx=0.75, rely=0.652, height=28, width=83
				, bordermode=u'ignore')
		self.grist_done_butt.configure(takefocus=u"")
		self.grist_done_butt.configure(text=u'''Done''')
		self.grist_done_butt.configure(command=self.done)

		self.grist_save_data_butt = tk.Button(self.grist_panedwindow2)
		self.grist_save_data_butt.place(relx=0.222, rely=0.739, height=108
				, width=213, bordermode=u'ignore')
		self.grist_save_data_butt.configure(takefocus=u"")
		self.grist_save_data_butt.configure(text=u'''Save to Database''')
		self.grist_save_data_butt.configure(command=self.save)


		self.input_state(0)

		self.grist_lstbx.bind(u'<<ListboxSelect>>', self.select_listbox)

		self.show_data(list(sorted(brew_data.grist_data.keys()))[0])
	def __adjust_sash0(self, event):
		paned = event.widget
		pos = [400, ]
		i = 0
		for sash in pos:
			paned.sashpos(i, sash)
			i += 1
		paned.unbind(u'<map>', self.__funcid0)
		del self.__funcid0

	def select_listbox(self, event):
		try:
			self.show_data(self.grist_lstbx.get(self.grist_lstbx.curselection()))
		except:
			pass

	def show_data(self, grist):
		self.name = grist
		name = grist
		colour = brew_data.grist_data[name][u'EBC']
		extract = brew_data.grist_data[name][u'Extract']
		moisture = brew_data.grist_data[name][u'Moisture']
		fermentability = brew_data.grist_data[name][u'Fermentability']
		description = brew_data.grist_data[name][u'Description']
		type = int(float(brew_data.grist_data[name][u'Type']))

		self.input_state(1)
		self.grist_name_ent.delete(0, tk.END)
		self.grist_comm_ent.delete(0, tk.END)
		self.grist_extract_ent.delete(0, tk.END)
		self.grist_moisture_ent.delete(0, tk.END)
		self.grist_colour_ent.delete(0, tk.END)
		self.grist_ferment_ent.delete(0, tk.END)

		self.grist_name_ent.insert(0, name)
		self.grist_comm_ent.insert(0, description)
		self.grist_extract_ent.insert(0, extract)
		self.grist_colour_ent.insert(0, colour)
		self.grist_moisture_ent.insert(0, moisture)
		self.grist_ferment_ent.insert(0, fermentability)
		self.grist_type_combo.set(self.grist_type_combo_values[type-1])

		self.input_state(0)

	def input_state(self, state):

		state = u"disabled" if state == 0 else u"normal"

		self.grist_comm_ent.configure(state=state)
		self.grist_name_ent.configure(state=state)
		self.grist_extract_ent.configure(state=state)
		self.grist_moisture_ent.configure(state=state)
		self.grist_colour_ent.configure(state=state)
		self.grist_ferment_ent.configure(state=state)

		self.grist_done_butt.configure(state=state)
		self.grist_clear_butt.configure(state=state)
		self.grist_cancel_butt.configure(state=state)

		self.grist_type_combo.configure(state=state)

	def clear_form(self):
		self.grist_comm_ent.delete(0, tk.END)
		self.grist_name_ent.delete(0, tk.END)
		self.grist_extract_ent.delete(0, tk.END)
		self.grist_moisture_ent.delete(0, tk.END)
		self.grist_colour_ent.delete(0, tk.END)
		self.grist_ferment_ent.delete(0, tk.END)

	def delete(self):
		del brew_data.grist_data[self.grist_lstbx.get(self.grist_lstbx.curselection())]
		self.grist_lstbx.delete(self.grist_lstbx.curselection())

	def new(self):
		name = u'New Grist {num}'.format(num=sum(u'New Grist' in s for s in brew_data.grist_data))
		self.grist_lstbx.insert(tk.END, name)
		try:
			brew_data.grist_data[name] = brew_data.grist_data[self.grist_lstbx.get(self.grist_lstbx.curselection())]
		except:
			try:
				brew_data.grist_data[name] = brew_data.grist_data[tk.ACTIVE]
			except:
				brew_data.grist_data[name] = {u'EBC': 0.0, u'Type': 3.0, u'Extract': 0.0, u'Description': u'No Description', u'Moisture': 0.0, u'Fermentability': 62.0}

		self.show_data(name)
		self.grist_lstbx.select_set(tk.END)
		self.grist_lstbx.activate(tk.END)
		self.grist_lstbx.yview(tk.END)

	def save(self):
		with open(resource_path(u'grain_data.txt'), u'w') as f:
			for ingredient, value in brew_data.grist_data.items():
				name = ingredient
				ebc = value[u'EBC']
				type = value[u'Type']
				extract = value[u'Extract']
				moisture = value[u'Moisture']
				fermentability = value[u'Fermentability']
				description = value[u'Description']
				f.write(u'{name}\t{ebc}\t{type}\t{extract}\t{moisture}\t{fermentability}\t{description}\n'.format(name=name, ebc=ebc, type=type, extract=extract, moisture=moisture, fermentability=fermentability, description=description))

	def done(self):
		name = self.grist_name_ent.get()
		colour = float(self.grist_colour_ent.get())
		extract = float( self.grist_extract_ent.get())
		moisture = float(self.grist_moisture_ent.get())
		fermentability = float(self.grist_ferment_ent.get())
		description = self.grist_comm_ent.get()
		type = self.grist_type_combo_values.index(self.grist_type_combo.get()) + 1
		brew_data.grist_data[name] = {u'EBC': colour, u'Type': type, u'Extract': extract, u'Description': description, u'Moisture': moisture, u'Fermentability': fermentability}
		del brew_data.grist_data[self.name]
		#print(brew_data.grist_data[name])
		idx = list(sorted(brew_data.grist_data.keys())).index(name)
		self.reinsert()
		self.show_data(name)

	def reinsert(self):
		self.grist_lstbx.delete(0, tk.END)
		for hop in sorted(brew_data.grist_data):
			self.grist_lstbx.insert(tk.END, hop)

class defaults_editor(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, background=_bgcolor)

		self.widgets()
		self.reset_to_defaults()

	def widgets(self):
		_fgcolor = u'#000000'  # X11 color: 'black'
		_compcolor = u'#d9d9d9' # X11 color: 'gray85'
		_ana1color = u'#d9d9d9' # X11 color: 'gray85'
		_ana2color = u'#ececec' # Closest X11 color: 'gray92'
		font9 = u"-family {DejaVu Sans} -size 10 -weight bold -slant "  \
			u"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()
		self.style.configure(u'.',background=_bgcolor)
		self.style.configure(u'.',foreground=_fgcolor)
		self.style.configure(u'.',font=u"TkDefaultFont")
		self.style.map(u'.',background=
			[(u'selected', _compcolor), (u'active',_ana2color)])

		self.target_vol_lbl = tk.Label(self)
		self.target_vol_lbl.place(relx=0.038, rely=0.063, height=19, width=118)
		self.target_vol_lbl.configure(background=_bgcolor)
		self.target_vol_lbl.configure(foreground=u"#000000")
		self.target_vol_lbl.configure(font=font9)
		self.target_vol_lbl.configure(relief=u'flat')
		self.target_vol_lbl.configure(text=u'''Target Volume:''')

		self.boil_vol_lbl = tk.Label(self)
		self.boil_vol_lbl.place(relx=0.038, rely=0.148, height=19, width=143)
		self.boil_vol_lbl.configure(background=_bgcolor)
		self.boil_vol_lbl.configure(foreground=u"#000000")
		self.boil_vol_lbl.configure(font=font9)
		self.boil_vol_lbl.configure(relief=u'flat')
		self.boil_vol_lbl.configure(text=u'''Boil Volume Scale:''')

		self.liquor_to_grist_lbl = tk.Label(self)
		self.liquor_to_grist_lbl.place(relx=0.038, rely=0.317, height=19
				, width=165)
		self.liquor_to_grist_lbl.configure(background=_bgcolor)
		self.liquor_to_grist_lbl.configure(foreground=u"#000000")
		self.liquor_to_grist_lbl.configure(font=font9)
		self.liquor_to_grist_lbl.configure(relief=u'flat')
		self.liquor_to_grist_lbl.configure(text=u'''Liquor To Grist Ratio:''')

		self.target_vol_ent = tk.Entry(self)
		self.target_vol_ent.place(relx=0.202, rely=0.063, relheight=0.044
				, relwidth=0.106)
		self.target_vol_ent.configure(justify=u'center')
		self.target_vol_ent.configure(width=84)
		self.target_vol_ent.configure(takefocus=u"")
		self.target_vol_ent.configure(cursor=u"xterm")

		self.boil_vol_ent = tk.Entry(self)
		self.boil_vol_ent.place(relx=0.227, rely=0.148, relheight=0.044
				, relwidth=0.106)
		self.boil_vol_ent.configure(justify=u'center')
		self.boil_vol_ent.configure(takefocus=u"")
		self.boil_vol_ent.configure(cursor=u"xterm")

		self.liquor_to_grist_ent = tk.Entry(self)
		self.liquor_to_grist_ent.place(relx=0.253, rely=0.317, relheight=0.044
				, relwidth=0.106)
		self.liquor_to_grist_ent.configure(justify=u'center')
		self.liquor_to_grist_ent.configure(takefocus=u"")
		self.liquor_to_grist_ent.configure(cursor=u"xterm")

		self.target_vol_litres_lbl = tk.Label(self)
		self.target_vol_litres_lbl.place(relx=0.316, rely=0.063, height=19
				, width=46)
		self.target_vol_litres_lbl.configure(background=_bgcolor)
		self.target_vol_litres_lbl.configure(foreground=u"#000000")
		self.target_vol_litres_lbl.configure(font=font9)
		self.target_vol_litres_lbl.configure(relief=u'flat')
		self.target_vol_litres_lbl.configure(text=u'''Litres''')

		self.mash_efficiency_lbl = tk.Label(self)
		self.mash_efficiency_lbl.place(relx=0.038, rely=0.233, height=19
				, width=125)
		self.mash_efficiency_lbl.configure(background=_bgcolor)
		self.mash_efficiency_lbl.configure(foreground=u"#000000")
		self.mash_efficiency_lbl.configure(font=font9)
		self.mash_efficiency_lbl.configure(relief=u'flat')
		self.mash_efficiency_lbl.configure(text=u'''Mash Efficiency:''')

		self.mash_efficiency_ent = tk.Entry(self)
		self.mash_efficiency_ent.place(relx=0.215, rely=0.233, relheight=0.044
				, relwidth=0.106)
		self.mash_efficiency_ent.configure(justify=u'center')
		self.mash_efficiency_ent.configure(takefocus=u"")
		self.mash_efficiency_ent.configure(cursor=u"xterm")

		self.boil_vol_percent_lbl = tk.Label(self)
		self.boil_vol_percent_lbl.place(relx=0.341, rely=0.148, height=19
				, width=15)
		self.boil_vol_percent_lbl.configure(background=_bgcolor)
		self.boil_vol_percent_lbl.configure(foreground=u"#000000")
		self.boil_vol_percent_lbl.configure(font=font9)
		self.boil_vol_percent_lbl.configure(relief=u'flat')
		self.boil_vol_percent_lbl.configure(text=u'''%''')

		self.mash_efficiency_percent_lbl = tk.Label(self)
		self.mash_efficiency_percent_lbl.place(relx=0.328, rely=0.233, height=19
				, width=15)
		self.mash_efficiency_percent_lbl.configure(background=_bgcolor)
		self.mash_efficiency_percent_lbl.configure(foreground=u"#000000")
		self.mash_efficiency_percent_lbl.configure(font=font9)
		self.mash_efficiency_percent_lbl.configure(relief=u'flat')
		self.mash_efficiency_percent_lbl.configure(text=u'''%''')

		self.liquor_to_grist_lperkg_lbl = tk.Label(self)
		self.liquor_to_grist_lperkg_lbl.place(relx=0.366, rely=0.317, height=19
				, width=35)
		self.liquor_to_grist_lperkg_lbl.configure(background=_bgcolor)
		self.liquor_to_grist_lperkg_lbl.configure(foreground=u"#000000")
		self.liquor_to_grist_lperkg_lbl.configure(font=font9)
		self.liquor_to_grist_lperkg_lbl.configure(relief=u'flat')
		self.liquor_to_grist_lperkg_lbl.configure(text=u'''L/kg''')

		self.save_all_butt = tk.Button(self)
		self.save_all_butt.place(relx=0.808, rely=0.93, height=28, width=143)
		self.save_all_butt.configure(takefocus=u"")
		self.save_all_butt.configure(text=u'''Save All As Defaults''')
		self.save_all_butt.configure(command=self.save_all)

		self.done_button = tk.Button(self)
		self.done_button.place(relx=0.694, rely=0.93, height=28, width=83)
		self.done_button.configure(takefocus=u"")
		self.done_button.configure(text=u'''Done''')
		self.done_button.configure(command=self.temp_save)

		self.reset_to_defaults_butt = tk.Button(self)
		self.reset_to_defaults_butt.place(relx=0.013, rely=0.93, height=28, width=127)
		self.reset_to_defaults_butt.configure(takefocus=u"")
		self.reset_to_defaults_butt.configure(text=u'''Reset To Defaults''')
		self.reset_to_defaults_butt.configure(command=self.reset_to_defaults)

		self.attenuation_defaults_lbl= tk.Label(self)
		self.attenuation_defaults_lbl.place(relx=0.038, rely=0.402, height=19
				, width=155)
		self.attenuation_defaults_lbl.configure(background=_bgcolor)
		self.attenuation_defaults_lbl.configure(foreground=u"#000000")
		self.attenuation_defaults_lbl.configure(font=font9)
		self.attenuation_defaults_lbl.configure(relief=u'flat')
		self.attenuation_defaults_lbl.configure(text=u'''Attenuation Default:''')
		self.attenuation_defaults_lbl.configure(width=155)

		self.attenuation_types = [u'Low', u'Medium', u'High']
		self.attenuation_type_var = tk.StringVar()
		self.attenuation_type_combo = tk.OptionMenu(self, self.attenuation_type_var, *self.attenuation_types)
		self.attenuation_type_combo.place(relx=0.253, rely=0.402, relheight=0.064
				, relwidth=0.16)
		self.attenuation_type_combo.configure(width=127)
		self.attenuation_type_combo.configure(takefocus=u"")

		self.attenuation_temps = [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]
		self.attenuation_temp_var = tk.StringVar()
		self.attenuation_temp_combo = tk.OptionMenu(self, self.attenuation_temp_var, *self.attenuation_temps)
		self.attenuation_temp_combo.place(relx=0.429, rely=0.402, relheight=0.064
				, relwidth=0.072)
		self.attenuation_temp_combo.configure(width=57)
		self.attenuation_temp_combo.configure(takefocus=u"")

		self.save_on_close_lbl = tk.Label(self)
		self.save_on_close_lbl.place(relx=0.038, rely=0.486)
		self.save_on_close_lbl.configure(background=_bgcolor)
		self.save_on_close_lbl.configure(foreground=u"#000000")
		self.save_on_close_lbl.configure(font=font9)
		self.save_on_close_lbl.configure(relief=u'flat')
		self.save_on_close_lbl.configure(text=u'''Save on Close:''')

		self.save_on_close_var = tk.StringVar()
		self.save_on_close_combo = tk.OptionMenu(self, self.save_on_close_var, u'True', u'False')
		self.save_on_close_combo.place(relx=0.202, rely=0.486, relheight=0.064
				, relwidth=0.122)
		self.save_on_close_combo.configure(width=97)
		self.save_on_close_combo.configure(takefocus=u"")

		self.default_boil_time_lbl = tk.Label(self)
		self.default_boil_time_lbl.place(relx=0.038, rely=0.571)
		self.default_boil_time_lbl.configure(background=_bgcolor)
		self.default_boil_time_lbl.configure(foreground=u"#000000")
		self.default_boil_time_lbl.configure(font=font9)
		self.default_boil_time_lbl.configure(relief=u'flat')
		self.default_boil_time_lbl.configure(text=u'''Default Boil Time:''')

		self.default_boil_time_spinbox = tk.Spinbox(self, from_=1.0, to=100.0)
		self.default_boil_time_spinbox.place(relx=0.227, rely=0.571, relheight=0.049
				, relwidth=0.086)
		self.default_boil_time_spinbox.configure(activebackground=u"#f9f9f9")
		self.default_boil_time_spinbox.configure(background=u"white")
		self.default_boil_time_spinbox.configure(highlightbackground=u"black")
		self.default_boil_time_spinbox.configure(selectbackground=u"#c4c4c4")
		self.default_boil_time_spinbox.configure(width=68)

		self.default_boil_time_min_lbl = tk.Label(self)
		self.default_boil_time_min_lbl.place(relx=0.328, rely=0.571, height=19
				, width=65)
		self.default_boil_time_min_lbl.configure(background=_bgcolor)
		self.default_boil_time_min_lbl.configure(foreground=u"#000000")
		self.default_boil_time_min_lbl.configure(font=font9)
		self.default_boil_time_min_lbl.configure(relief=u'flat')
		self.default_boil_time_min_lbl.configure(text=u'''Minutes''')

		self.replace_default_vars = tk.Label(self)
		self.replace_default_vars.place(relx=0.038, rely=0.655)
		self.replace_default_vars.configure(background=_bgcolor)
		self.replace_default_vars.configure(foreground=u"#000000")
		self.replace_default_vars.configure(font=font9)
		self.replace_default_vars.configure(relief=u'flat')
		self.replace_default_vars.configure(text=u'''Update Default Configuration:''')

		self.replace_default_vars_chckbutt = tk.Checkbutton(self)
		self.replace_default_vars_chckbutt.place(relx=0.328, rely=0.655
				, relheight=0.049, relwidth=0.034)
		self.replace_default_vars_chckbutt.configure(background=_bgcolor)
		self.replace_default_vars_chckbutt.configure(justify=u'left')
		self.replace_default_vars_variable = tk.BooleanVar()
		self.replace_default_vars_chckbutt.configure(variable=self.replace_default_vars_variable)


	def reset_to_defaults(self):
		self.target_vol_ent.delete(0, tk.END)
		self.boil_vol_ent.delete(0, tk.END)
		self.mash_efficiency_ent.delete(0, tk.END)
		self.liquor_to_grist_ent.delete(0, tk.END)

		with open(resource_path(u'defaults.txt'), u'r') as f:
			data = [line.strip().split(u'=') for line in f]
			for constants in data:
				if constants[0] == u'efficiency': self.mash_efficiency_ent.insert(0, float(constants[1])) #float(constants[1])/100
				elif constants[0] == u'volume': self.target_vol_ent.insert(0, float(constants[1]))
				elif constants[0] == u'evaporation': self.boil_vol_ent.insert(0, float(constants[1])+100) #(float(constants[1])/100)+1
				elif constants[0] == u'LGratio': self.liquor_to_grist_ent.insert(0, float(constants[1]))
				elif constants[0] == u'attenuation':
					type = constants[1].split(u'-')[0]
					self.attenuation_type_var.set(type if type != u'med' else u'Medium')
					temp = constants[1].split(u'-')[1]
					self.attenuation_temp_var.set(temp)
				elif constants[0] == u'save_close':
					self.save_on_close_var.set(constants[1])
				elif constants[0] == u'boil_time':
					self.default_boil_time_spinbox.delete(0, tk.END)
					self.default_boil_time_spinbox.insert(0, constants[1])
				elif constants[0] == u'replace_defaults':
					self.replace_default_vars_variable.set(False if constants[1] == u'True' else True)

	def save_all(self):
		with open(resource_path(u'defaults.txt'), u'w') as f:
			volume = float(self.target_vol_ent.get())
			efficiency = float(self.mash_efficiency_ent.get())
			evaporation = (float(self.boil_vol_ent.get())-100) #round((brew_data.constants['Boil Volume Scale']-1)*100, 1)
			LGratio = float(self.liquor_to_grist_ent.get())
			attenuation_type = self.attenuation_type_var.get().lower()
			attenuation_temp = self.attenuation_temp_var.get()
			attenuation = (attenuation_type if attenuation_type != u'medium' else u'med') + u'-' + (attenuation_temp)
			save_close = self.save_on_close_var.get()
			boil_time = self.default_boil_time_spinbox.get()
			replace_defaults = not self.replace_default_vars_variable.get()
			f.write(u'efficiency={efficiency}\nvolume={volume}\nevaporation={evaporation}\nLGratio={LGratio}\nattenuation={attenuation}\nsave_close={save_close}\nboil_time={boil_time}\nreplace_defaults={replace_defaults}'.format(efficiency=efficiency, volume=volume, evaporation=evaporation, LGratio=LGratio,
																																																									attenuation=attenuation, save_close=save_close, boil_time=boil_time, replace_defaults=replace_defaults))
		self.temp_save()

	def temp_save(self):
		brew_data.constants[u'Volume'] = float(self.target_vol_ent.get())
		brew_data.constants[u'Efficiency'] = float(self.mash_efficiency_ent.get())/100
		brew_data.constants[u'Boil Volume Scale'] = (float(self.boil_vol_ent.get())/100)
		brew_data.constants[u'Liquor To Grist Ratio'] = float(self.liquor_to_grist_ent.get())
		brew_data.constants[u'Save On Close'] = True if self.save_on_close_var.get() == u'True' else False
		brew_data.constants[u'Default Boil Time'] = int(self.default_boil_time_spinbox.get())
		brew_data.constants[u'Replace Defaults'] = True if self.save_on_close_var.get() == u'True' else False

	def open_locals(self):
		self.target_vol_ent.delete(0, tk.END)
		self.boil_vol_ent.delete(0, tk.END)
		self.mash_efficiency_ent.delete(0, tk.END)
		self.liquor_to_grist_ent.delete(0, tk.END)
		self.default_boil_time_spinbox.delete(0, tk.END)

		self.mash_efficiency_ent.insert(0, brew_data.constants[u'Efficiency']*100)
		self.target_vol_ent.insert(0, brew_data.constants[u'Volume'])
		self.boil_vol_ent.insert(0, round(brew_data.constants[u'Boil Volume Scale']*100, 1))
		self.liquor_to_grist_ent.insert(0,  brew_data.constants[u'Liquor To Grist Ratio'])
		self.default_boil_time_spinbox.insert(0, brew_data.constants[u'Default Boil Time'])
		self.replace_default_vars_variable.set(not brew_data.constants[u'Replace Defaults'])
class special_editor(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, background=_bgcolor)
		self.current_attenuation = tk.StringVar()
		self.widgets()
		#self.attenuation_frame.bind('<Button-1>', lambda evt: print(self.current_attenuation.get()))
		self.current_attenuation.set(brew_data.constants[u'Attenuation Default'])
		self.original_additions = list(sorted(brew_data.water_chemistry_additions)) + list(sorted(brew_data.yeast_data))
		self.added_additions = []
		self.refresh_orig()
		self.refresh_add()

	def widgets(self):
		_fgcolor = u'#000000'  # X11 color: 'black'
		_compcolor = u'#d9d9d9' # X11 color: 'gray85'
		_ana1color = u'#d9d9d9' # X11 color: 'gray85'
		_ana2color = u'#ececec' # Closest X11 color: 'gray92'
		font9 = u"-family {DejaVu Sans} -size 9 -weight normal -slant "  \
			u"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()
		self.style.configure(u'.',background=_bgcolor)
		self.style.configure(u'.',foreground=_fgcolor)
		self.style.configure(u'.',font=u"TkDefaultFont")
		self.style.map(u'.',background=
			[(u'selected', _compcolor), (u'active',_ana2color)])
		u'''
		 	Low	Med	High
		C	54	62	70
		62	51	59	66
		63	52	60	68
		64	53	61	69
		65	53	61	69
		66	53	61	69
		67	53	61	69
		68	52	60	67
		69	51	58	66
		70	49	56	63
		71	47	54	61
		72	44	51	57
		'''
		self.table_dict = {
		  u'low-62': 51, u'med-62': 59, u'high-62': 66,
		  u'low-63': 52, u'med-63': 60, u'high-63': 68,
		  u'low-64': 53, u'med-64': 61, u'high-64': 69,
		  u'low-65': 53, u'med-65': 61, u'high-65': 69,
		  u'low-66': 53, u'med-66': 61, u'high-66': 69,
		  u'low-67': 53, u'med-67': 61, u'high-67': 69,
		  u'low-68': 52, u'med-68': 60, u'high-68': 67,
		  u'low-69': 51, u'med-69': 58, u'high-69': 66,
		  u'low-70': 49, u'med-70': 56, u'high-70': 63,
		  u'low-71': 47, u'med-71': 54, u'high-71': 61,
		  u'low-72': 44, u'med-72': 51, u'high-72': 57
		}

		self.attenuation_frame = tk.LabelFrame(self)
		self.attenuation_frame.place(relx=0.013, rely=0.021, relheight=0.591
			, relwidth=0.227)
		#self.attenuation_frame.configure(relief='')
		self.attenuation_frame.configure(text=u'''Yeast Attenuation''')
		self.attenuation_frame.configure(width=180)
		self.attenuation_frame.configure(background=_bgcolor)

		self.attenuation_low_lbl = tk.Label(self.attenuation_frame)
		self.attenuation_low_lbl.place(relx=0.278, rely=0.109, height=19
			, width=28, bordermode=u'ignore')
		self.attenuation_low_lbl.configure(background=_bgcolor)
		self.attenuation_low_lbl.configure(foreground=u"#000000")
		self.attenuation_low_lbl.configure(font=u"TkDefaultFont")
		self.attenuation_low_lbl.configure(relief=u'flat')
		self.attenuation_low_lbl.configure(text=u'''Low''')

		self.attenuation_med_lbl = tk.Label(self.attenuation_frame)
		self.attenuation_med_lbl.place(relx=0.5, rely=0.109, height=19, width=30
			, bordermode=u'ignore')
		self.attenuation_med_lbl.configure(background=_bgcolor)
		self.attenuation_med_lbl.configure(foreground=u"#000000")
		self.attenuation_med_lbl.configure(font=u"TkDefaultFont")
		self.attenuation_med_lbl.configure(relief=u'flat')
		self.attenuation_med_lbl.configure(text=u'''Med''')

		self.attenuation_high_lbl = tk.Label(self.attenuation_frame)
		self.attenuation_high_lbl.place(relx=0.722, rely=0.109, height=19
			, width=42, bordermode=u'ignore')
		self.attenuation_high_lbl.configure(background=_bgcolor)
		self.attenuation_high_lbl.configure(foreground=u"#000000")
		self.attenuation_high_lbl.configure(font=u"TkDefaultFont")
		self.attenuation_high_lbl.configure(relief=u'flat')
		self.attenuation_high_lbl.configure(text=u'''High''')
		self.attenuation_high_lbl.configure(width=42)


		self.attenuation_62_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_62_degrees.place(relx=0.056, rely=0.182, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_62_degrees.configure(background=_bgcolor)
		self.attenuation_62_degrees.configure(foreground=u"#000000")
		self.attenuation_62_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_62_degrees.configure(relief=u'flat')
		self.attenuation_62_degrees.configure(text=u'''62°C''')

		self.attenuation_63_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_63_degrees.place(relx=0.056, rely=0.255, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_63_degrees.configure(background=_bgcolor)
		self.attenuation_63_degrees.configure(foreground=u"#000000")
		self.attenuation_63_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_63_degrees.configure(relief=u'flat')
		self.attenuation_63_degrees.configure(text=u'''63°C''')

		self.attenuation_64_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_64_degrees.place(relx=0.056, rely=0.327, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_64_degrees.configure(background=_bgcolor)
		self.attenuation_64_degrees.configure(foreground=u"#000000")
		self.attenuation_64_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_64_degrees.configure(relief=u'flat')
		self.attenuation_64_degrees.configure(text=u'''64°C''')

		self.attenuation_65_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_65_degrees.place(relx=0.056, rely=0.4, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_65_degrees.configure(background=_bgcolor)
		self.attenuation_65_degrees.configure(foreground=u"#000000")
		self.attenuation_65_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_65_degrees.configure(relief=u'flat')
		self.attenuation_65_degrees.configure(text=u'''65°C''')

		self.attenuation_66_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_66_degrees.place(relx=0.056, rely=0.473, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_66_degrees.configure(background=_bgcolor)
		self.attenuation_66_degrees.configure(foreground=u"#000000")
		self.attenuation_66_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_66_degrees.configure(relief=u'flat')
		self.attenuation_66_degrees.configure(text=u'''66°C''')

		self.attenuation_67_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_67_degrees.place(relx=0.056, rely=0.545, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_67_degrees.configure(background=_bgcolor)
		self.attenuation_67_degrees.configure(foreground=u"#000000")
		self.attenuation_67_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_67_degrees.configure(relief=u'flat')
		self.attenuation_67_degrees.configure(text=u'''67°C''')


		self.attenuation_68_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_68_degrees.place(relx=0.056, rely=0.618, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_68_degrees.configure(background=_bgcolor)
		self.attenuation_68_degrees.configure(foreground=u"#000000")
		self.attenuation_68_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_68_degrees.configure(relief=u'flat')
		self.attenuation_68_degrees.configure(text=u'''68°C''')

		self.attenuation_69_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_69_degrees.place(relx=0.056, rely=0.691, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_69_degrees.configure(background=_bgcolor)
		self.attenuation_69_degrees.configure(foreground=u"#000000")
		self.attenuation_69_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_69_degrees.configure(relief=u'flat')
		self.attenuation_69_degrees.configure(text=u'''69°C''')

		self.attenuation_70_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_70_degrees.place(relx=0.056, rely=0.764, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_70_degrees.configure(background=_bgcolor)
		self.attenuation_70_degrees.configure(foreground=u"#000000")
		self.attenuation_70_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_70_degrees.configure(relief=u'flat')
		self.attenuation_70_degrees.configure(text=u'''70°C''')

		self.attenuation_71_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_71_degrees.place(relx=0.056, rely=0.836, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_71_degrees.configure(background=_bgcolor)
		self.attenuation_71_degrees.configure(foreground=u"#000000")
		self.attenuation_71_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_71_degrees.configure(relief=u'flat')
		self.attenuation_71_degrees.configure(text=u'''71°C''')

		self.attenuation_72_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_72_degrees.place(relx=0.056, rely=0.909, height=19
			, width=34, bordermode=u'ignore')
		self.attenuation_72_degrees.configure(background=_bgcolor)
		self.attenuation_72_degrees.configure(foreground=u"#000000")
		self.attenuation_72_degrees.configure(font=u"TkDefaultFont")
		self.attenuation_72_degrees.configure(relief=u'flat')
		self.attenuation_72_degrees.configure(text=u'''72°C''')

		####################################### Low #######################################
		self.attenuation_low_62 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_62.place(relx=0.278, rely=0.182, relheight=0.084
			, relwidth=0.172, bordermode=u'ignore')
		self.attenuation_low_62.configure(justify=u'left')
		self.attenuation_low_62.configure(value=u'low-62')
		self.attenuation_low_62.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_62.configure(background=_bgcolor)
		self.attenuation_low_62.configure(variable=self.current_attenuation)

		self.attenuation_low_63 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_63.place(relx=0.278, rely=0.255, relheight=0.084
			, relwidth=0.172, bordermode=u'ignore')
		self.attenuation_low_63.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_63.configure(background=_bgcolor)
		self.attenuation_low_63.configure(justify=u'left')
		self.attenuation_low_63.configure(value=u'low-63')
		self.attenuation_low_63.configure(variable=self.current_attenuation)

		self.attenuation_low_64 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_64.place(relx=0.278, rely=0.327, relheight=0.084
			, relwidth=0.172, bordermode=u'ignore')
		self.attenuation_low_64.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_64.configure(background=_bgcolor)
		self.attenuation_low_64.configure(justify=u'left')
		self.attenuation_low_64.configure(value=u'low-64')
		self.attenuation_low_64.configure(variable=self.current_attenuation)

		self.attenuation_low_65 = tk.Radiobutton(self)
		self.attenuation_low_65.place(relx=0.076, rely=0.254, relheight=0.049
			, relwidth=0.039)
		self.attenuation_low_65.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_65.configure(background=_bgcolor)
		self.attenuation_low_65.configure(justify=u'left')
		self.attenuation_low_65.configure(value=u'low-65')
		self.attenuation_low_65.configure(variable=self.current_attenuation)
		self.attenuation_low_66 = tk.Radiobutton(self)
		self.attenuation_low_66.place(relx=0.076, rely=0.296
			, relheight=0.049, relwidth=0.039)
		self.attenuation_low_66.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_66.configure(background=_bgcolor)
		self.attenuation_low_66.configure(justify=u'left')
		self.attenuation_low_66.configure(value=u'low-66')
		self.attenuation_low_66.configure(variable=self.current_attenuation)

		self.attenuation_low_67 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_67.place(relx=0.278, rely=0.545, relheight=0.084
			, relwidth=0.172, bordermode=u'ignore')
		self.attenuation_low_67.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_67.configure(background=_bgcolor)
		self.attenuation_low_67.configure(justify=u'left')
		self.attenuation_low_67.configure(value=u'low-67')
		self.attenuation_low_67.configure(variable=self.current_attenuation)

		self.attenuation_low_68 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_68.place(relx=0.278, rely=0.618, relheight=0.084
			, relwidth=0.172, bordermode=u'ignore')
		self.attenuation_low_68.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_68.configure(background=_bgcolor)
		self.attenuation_low_68.configure(justify=u'left')
		self.attenuation_low_68.configure(value=u'low-68')
		self.attenuation_low_68.configure(variable=self.current_attenuation)

		self.attenuation_low_69 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_69.place(relx=0.278, rely=0.691, relheight=0.084
			, relwidth=0.172, bordermode=u'ignore')
		self.attenuation_low_69.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_69.configure(background=_bgcolor)
		self.attenuation_low_69.configure(justify=u'left')
		self.attenuation_low_69.configure(value=u'low-69')
		self.attenuation_low_69.configure(variable=self.current_attenuation)

		self.attenuation_low_70 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_70.place(relx=0.278, rely=0.764, relheight=0.084
			, relwidth=0.172, bordermode=u'ignore')
		self.attenuation_low_70.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_70.configure(background=_bgcolor)
		self.attenuation_low_70.configure(justify=u'left')
		self.attenuation_low_70.configure(value=u'low-70')
		self.attenuation_low_70.configure(variable=self.current_attenuation)

		self.attenuation_low_71 = tk.Radiobutton(self)
		self.attenuation_low_71.place(relx=0.076, rely=0.507, relheight=0.049
			, relwidth=0.039)
		self.attenuation_low_71.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_71.configure(background=_bgcolor)
		self.attenuation_low_71.configure(justify=u'left')
		self.attenuation_low_71.configure(variable=self.current_attenuation)
		self.attenuation_low_71.configure(value=u'low-71')

		self.attenuation_low_72 = tk.Radiobutton(self)
		self.attenuation_low_72.place(relx=0.076, rely=0.55, relheight=0.049
			, relwidth=0.039)
		self.attenuation_low_72.configure(activebackground=u"#f9f9f9")
		self.attenuation_low_72.configure(background=_bgcolor)
		self.attenuation_low_72.configure(justify=u'left')
		self.attenuation_low_72.configure(value=u'low-72')
		self.attenuation_low_72.configure(variable=self.current_attenuation)

		####################################### MEDIUM #######################################
		self.attenuation_med_62 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_med_62.place(relx=0.5, rely=0.182, relheight=0.084
			, relwidth=0.172, bordermode=u'ignore')
		self.attenuation_med_62.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_62.configure(background=_bgcolor)
		self.attenuation_med_62.configure(justify=u'left')
		self.attenuation_med_62.configure(value=u'med-62')
		self.attenuation_med_62.configure(variable=self.current_attenuation)

		self.attenuation_med_63 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_med_63.place(relx=0.5, rely=0.255, relheight=0.084
			, relwidth=0.172, bordermode=u'ignore')
		self.attenuation_med_63.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_63.configure(background=_bgcolor)
		self.attenuation_med_63.configure(justify=u'left')
		self.attenuation_med_63.configure(value=u'med-63')
		self.attenuation_med_63.configure(variable=self.current_attenuation)

		self.attenuation_med_64 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_med_64.place(relx=0.5, rely=0.327, relheight=0.084
			, relwidth=0.172, bordermode=u'ignore')
		self.attenuation_med_64.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_64.configure(background=_bgcolor)
		self.attenuation_med_64.configure(justify=u'left')
		self.attenuation_med_64.configure(value=u'med-64')
		self.attenuation_med_64.configure(variable=self.current_attenuation)

		self.attenuation_med_65 = tk.Radiobutton(self)
		self.attenuation_med_65.place(relx=0.126, rely=0.254, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_65.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_65.configure(background=_bgcolor)
		self.attenuation_med_65.configure(justify=u'left')
		self.attenuation_med_65.configure(value=u'med-65')
		self.attenuation_med_65.configure(variable=self.current_attenuation)

		self.attenuation_med_66 = tk.Radiobutton(self)
		self.attenuation_med_66.place(relx=0.126, rely=0.296, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_66.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_66.configure(background=_bgcolor)
		self.attenuation_med_66.configure(justify=u'left')
		self.attenuation_med_66.configure(value=u'med-66')
		self.attenuation_med_66.configure(variable=self.current_attenuation)

		self.attenuation_med_67 = tk.Radiobutton(self)
		self.attenuation_med_67.place(relx=0.126, rely=0.338, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_67.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_67.configure(background=_bgcolor)
		self.attenuation_med_67.configure(justify=u'left')
		self.attenuation_med_67.configure(value=u'med-67')
		self.attenuation_med_67.configure(variable=self.current_attenuation)

		self.attenuation_med_68 = tk.Radiobutton(self)
		self.attenuation_med_68.place(relx=0.126, rely=0.381, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_68.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_68.configure(background=_bgcolor)
		self.attenuation_med_68.configure(justify=u'left')
		self.attenuation_med_68.configure(value=u'med-68')
		self.attenuation_med_68.configure(variable=self.current_attenuation)

		self.attenuation_med_69 = tk.Radiobutton(self)
		self.attenuation_med_69.place(relx=0.126, rely=0.423, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_69.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_69.configure(background=_bgcolor)
		self.attenuation_med_69.configure(justify=u'left')
		self.attenuation_med_69.configure(value=u'med-69')
		self.attenuation_med_69.configure(variable=self.current_attenuation)

		self.attenuation_med_70 = tk.Radiobutton(self)
		self.attenuation_med_70.place(relx=0.126, rely=0.465, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_70.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_70.configure(background=_bgcolor)
		self.attenuation_med_70.configure(justify=u'left')
		self.attenuation_med_70.configure(value=u'med-70')
		self.attenuation_med_70.configure(variable=self.current_attenuation)

		self.attenuation_med_71 = tk.Radiobutton(self)
		self.attenuation_med_71.place(relx=0.126, rely=0.507, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_71.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_71.configure(background=_bgcolor)
		self.attenuation_med_71.configure(justify=u'left')
		self.attenuation_med_71.configure(value=u'med-71')
		self.attenuation_med_71.configure(variable=self.current_attenuation)

		self.attenuation_med_72 = tk.Radiobutton(self)
		self.attenuation_med_72.place(relx=0.126, rely=0.55, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_72.configure(activebackground=u"#f9f9f9")
		self.attenuation_med_72.configure(background=_bgcolor)
		self.attenuation_med_72.configure(justify=u'left')
		self.attenuation_med_72.configure(value=u'med-72')
		self.attenuation_med_72.configure(variable=self.current_attenuation)

		####################################### HIGH #######################################
		self.attenuation_high_62 = tk.Radiobutton(self)
		self.attenuation_high_62.place(relx=0.177, rely=0.127, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_62.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_62.configure(background=_bgcolor)
		self.attenuation_high_62.configure(justify=u'left')
		self.attenuation_high_62.configure(value=u'high-62')
		self.attenuation_high_62.configure(variable=self.current_attenuation)

		self.attenuation_high_63 = tk.Radiobutton(self)
		self.attenuation_high_63.place(relx=0.177, rely=0.169, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_63.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_63.configure(background=_bgcolor)
		self.attenuation_high_63.configure(justify=u'left')
		self.attenuation_high_63.configure(value=u'high-63')
		self.attenuation_high_63.configure(variable=self.current_attenuation)

		self.attenuation_high_64 = tk.Radiobutton(self)
		self.attenuation_high_64.place(relx=0.177, rely=0.211, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_64.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_64.configure(background=_bgcolor)
		self.attenuation_high_64.configure(justify=u'left')
		self.attenuation_high_64.configure(value=u'high-64')
		self.attenuation_high_64.configure(variable=self.current_attenuation)

		self.attenuation_high_65 = tk.Radiobutton(self)
		self.attenuation_high_65.place(relx=0.177, rely=0.254, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_65.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_65.configure(background=_bgcolor)
		self.attenuation_high_65.configure(justify=u'left')
		self.attenuation_high_65.configure(value=u'high-65')
		self.attenuation_high_65.configure(variable=self.current_attenuation)

		self.attenuation_high_66 = tk.Radiobutton(self)
		self.attenuation_high_66.place(relx=0.177, rely=0.296, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_66.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_66.configure(background=_bgcolor)
		self.attenuation_high_66.configure(justify=u'left')
		self.attenuation_high_66.configure(value=u'high-66')
		self.attenuation_high_66.configure(variable=self.current_attenuation)

		self.attenuation_high_67 = tk.Radiobutton(self)
		self.attenuation_high_67.place(relx=0.177, rely=0.338, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_67.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_67.configure(background=_bgcolor)
		self.attenuation_high_67.configure(justify=u'left')
		self.attenuation_high_67.configure(value=u'high-67')
		self.attenuation_high_67.configure(variable=self.current_attenuation)

		self.attenuation_high_68 = tk.Radiobutton(self)
		self.attenuation_high_68.place(relx=0.177, rely=0.381, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_68.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_68.configure(background=_bgcolor)
		self.attenuation_high_68.configure(justify=u'left')
		self.attenuation_high_68.configure(value=u'high-68')
		self.attenuation_high_68.configure(variable=self.current_attenuation)

		self.attenuation_high_69 = tk.Radiobutton(self)
		self.attenuation_high_69.place(relx=0.177, rely=0.423, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_69.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_69.configure(background=_bgcolor)
		self.attenuation_high_69.configure(justify=u'left')
		self.attenuation_high_69.configure(value=u'high-69')
		self.attenuation_high_69.configure(variable=self.current_attenuation)

		self.attenuation_high_70 = tk.Radiobutton(self)
		self.attenuation_high_70.place(relx=0.177, rely=0.465, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_70.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_70.configure(background=_bgcolor)
		self.attenuation_high_70.configure(justify=u'left')
		self.attenuation_high_70.configure(value=u'high-70')
		self.attenuation_high_70.configure(variable=self.current_attenuation)

		self.attenuation_high_71 = tk.Radiobutton(self)
		self.attenuation_high_71.place(relx=0.177, rely=0.507, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_71.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_71.configure(background=_bgcolor)
		self.attenuation_high_71.configure(justify=u'left')
		self.attenuation_high_71.configure(value=u'high-71')
		self.attenuation_high_71.configure(variable=self.current_attenuation)

		self.attenuation_high_72 = tk.Radiobutton(self)
		self.attenuation_high_72.place(relx=0.177, rely=0.55, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_72.configure(activebackground=u"#f9f9f9")
		self.attenuation_high_72.configure(background=_bgcolor)
		self.attenuation_high_72.configure(justify=u'left')
		self.attenuation_high_72.configure(value=u'high-72')
		self.attenuation_high_72.configure(variable=self.current_attenuation)


		########################################### Water Chemistry ###########################################

		self.water_chem_add_frame = ttk.Labelframe(self)
		self.water_chem_add_frame.place(relx=0.253, rely=0.021, relheight=0.591 #relheight=0.591
				, relwidth=0.568)
		self.water_chem_add_frame.configure(relief=u'')
		self.water_chem_add_frame.configure(text=u'''Water Chemistry Additions''')
		self.water_chem_add_frame.configure(width=450)

		self.water_chem_orig_lstbx = ScrolledListBox(self.water_chem_add_frame)
		self.water_chem_orig_lstbx.place(relx=0.022, rely=0.073, relheight=0.865
				, relwidth=0.391, bordermode=u'ignore')
		self.water_chem_orig_lstbx.configure(background=u"white")
		self.water_chem_orig_lstbx.configure(font=u"TkFixedFont")
		self.water_chem_orig_lstbx.configure(highlightcolor=u"#d9d9d9")
		self.water_chem_orig_lstbx.configure(selectbackground=u"#c4c4c4")
		self.water_chem_orig_lstbx.configure(width=10)

		self.water_chem_new = tk.Button(self.water_chem_add_frame)
		self.water_chem_new.place(relx=0.444, rely=0.073, height=28, width=53
				, bordermode=u'ignore')
		self.water_chem_new.configure(takefocus=u"")
		self.water_chem_new.configure(text=u'''+''')
		self.water_chem_new.configure(command=self.new_water_chem)

		self.move_all_right = tk.Button(self.water_chem_add_frame)
		self.move_all_right.place(relx=0.444, rely=0.218, height=28, width=53
				, bordermode=u'ignore')
		self.move_all_right.configure(takefocus=u"")
		self.move_all_right.configure(text=u'''>>''')
		self.move_all_right.configure(width=53)
		self.move_all_right.configure(command=self.move_all_left_right)

		self.move_one_right = tk.Button(self.water_chem_add_frame)
		self.move_one_right.place(relx=0.444, rely=0.364, height=28, width=53
				, bordermode=u'ignore')
		self.move_one_right.configure(takefocus=u"")
		self.move_one_right.configure(text=u'''>''')
		self.move_one_right.configure(command=self.move_one_left_right)

		self.move_one_left = tk.Button(self.water_chem_add_frame)
		self.move_one_left.place(relx=0.444, rely=0.509, height=28, width=53 #  relx=0.444, rely=0.655
				, bordermode=u'ignore')
		self.move_one_left.configure(takefocus=u"")
		self.move_one_left.configure(text=u'''<''')
		self.move_one_left.configure(command=self.move_one_right_left)

		self.move_all_left = tk.Button(self)
		self.move_all_left.place(relx=0.505, rely=0.402, height=28, width=53)  # , height=28, width=53  relx=0.505, rely=0.317
		self.move_all_left.configure(takefocus=u"")
		self.move_all_left.configure(text=u'''<<''')
		self.move_all_left.configure(command=self.move_all_right_left)

		self.water_chem_added_lstbx = ScrolledListBox(self.water_chem_add_frame)
		self.water_chem_added_lstbx.place(relx=0.578, rely=0.073, relheight=0.865
				, relwidth=0.391, bordermode=u'ignore')
		self.water_chem_added_lstbx.configure(background=u"white")
		self.water_chem_added_lstbx.configure(font=u"TkFixedFont")
		self.water_chem_added_lstbx.configure(highlightcolor=u"#d9d9d9")
		self.water_chem_added_lstbx.configure(selectbackground=u"#c4c4c4")
		self.water_chem_added_lstbx.configure(width=10)

		#########################################################################################
		self.water_boil_frame = ttk.Labelframe(self)
		self.water_boil_frame.place(relx=0.013, rely=0.613, relheight=0.159
				, relwidth=0.227)
		self.water_boil_frame.configure(relief=u'')
		self.water_boil_frame.configure(text=u'''Water Boil:''')
		self.water_boil_frame.configure(width=180)

		self.water_boil_disable = tk.Checkbutton(self.water_boil_frame)
		self.water_boil_is_disabled = tk.IntVar()
		self.water_boil_disable.place(relx=0.778, rely=0.4, relheight=0.307
				, relwidth=0.15, bordermode=u'ignore')
		self.water_boil_disable.configure(justify=u'left')
		self.water_boil_disable.configure(variable=self.water_boil_is_disabled)
		self.water_boil_disable.configure(command=self.water_boil_check)

		self.water_boil_time_spinbx = tk.Spinbox(self.water_boil_frame, from_=1.0, to=9999.0)
		self.water_boil_time_spinbx.place(relx=0.444, rely=0.4, relheight=0.307, relwidth=0.322
				, bordermode=u'ignore')
		self.water_boil_time_spinbx.configure(activebackground=u"#f9f9f9")
		self.water_boil_time_spinbx.configure(background=u"white")
		self.water_boil_time_spinbx.configure(highlightbackground=u"black")
		self.water_boil_time_spinbx.configure(selectbackground=u"#c4c4c4")
		self.water_boil_time_spinbx.configure(width=58)
		#self.water_boil_time_spinbx.set(brew_data.constants['Default Boil Time'])
		self.water_boil_time_spinbx.delete(0, tk.END)
		self.water_boil_time_spinbx.insert(0,brew_data.constants[u'Default Boil Time'])

		self.water_boil_time_lbl = tk.Label(self.water_boil_frame)
		self.water_boil_time_lbl.place(relx=0.056, rely=0.4, height=17, width=65
				, bordermode=u'ignore')
		self.water_boil_time_lbl.configure(background=_bgcolor)
		self.water_boil_time_lbl.configure(foreground=u"#000000")
		self.water_boil_time_lbl.configure(font=font9)
		self.water_boil_time_lbl.configure(relief=u'flat')
		self.water_boil_time_lbl.configure(text=u'''Boil Time:''')
		self.water_boil_check()

	@staticmethod
	def popup1(event, *args, **kwargs):
		Popupmenu1 = tk.Menu(root, tearoff=0)
		Popupmenu1.configure(activebackground=u"#f9f9f9")
		Popupmenu1.post(event.x_root, event.y_root)

	def refresh_orig(self):
		self.water_chem_orig_lstbx.delete(0, tk.END)
		for idx, addition in enumerate(self.original_additions):
			self.water_chem_orig_lstbx.insert(tk.END, addition)
			if addition in brew_data.yeast_data:
				self.water_chem_orig_lstbx.itemconfig(idx, {u'bg':u'lightblue'})

	def refresh_add(self):
		self.water_chem_added_lstbx.delete(0, tk.END)
		for idx, addition in enumerate(self.added_additions):
			self.water_chem_added_lstbx.insert(tk.END, addition)
			if addition in brew_data.yeast_data:
				self.water_chem_added_lstbx.itemconfig(idx, {u'bg':u'lightblue'})

	def refresh_all(self):
		self.refresh_orig()
		self.refresh_add()

	def move_one_left_right(self):
		try:
			selection = self.water_chem_orig_lstbx.curselection()[0]
			self.added_additions.append(self.original_additions.pop(selection))
			self.refresh_all()
		except IndexError:
			pass

	def move_all_left_right(self):
		for _ in xrange(len(self.original_additions)):
			self.added_additions.append(self.original_additions.pop(0))
		self.refresh_all()

	def move_one_right_left(self):
		try:
			selection = self.water_chem_added_lstbx.curselection()[0]
			self.original_additions.append(self.added_additions.pop(selection))
			self.refresh_all()
		except IndexError:
			pass

	def move_all_right_left(self):
		for _ in xrange(len(self.added_additions)):
			self.original_additions.append(self.added_additions.pop(0))
		self.refresh_all()

	def water_boil_check(self):
		if self.water_boil_is_disabled.get() == 0:
			self.water_boil_time_spinbx.configure(state=u"disabled")
		else:
			self.water_boil_time_spinbx.configure(state=u"normal")

	def new_water_chem(self):
		def on_type_change(*args):
			if type_var.get() != u'Hop':
				time_spnbx.configure(state=u'disabled')
			else:
				time_spnbx.configure(state=u'normal')
		def done():
			brew_data.water_chemistry_additions[name_var.get()] = {u'Values': {u'Type': type_var.get()}}
			if type_var.get() == u'Hop': brew_data.water_chemistry_additions[name_var.get()][u'Values'][u'Time'] = float(time_var.get())
			self.original_additions = list(set(sorted(brew_data.water_chemistry_additions))-set(self.added_additions)) + list((set(sorted(brew_data.yeast_data))-set(self.added_additions)))
			self.refresh_all()

		def cancel():
			new_water_chem_win.destroy()

		def save_to_database():
			done()
			with open(resource_path(u'water_chem_data.txt'), u'w') as f:
				for water_chem, values in brew_data.water_chemistry_additions.items():
					value = values[u'Values']
					name = water_chem
					time = value[u'Time'] if u'Time' in value else u'N/A'
					#print(value)
					water_chem_type = value[u'Type']
					f.write(u'{name}\t{time}\t{water_chem_type}\n'.format(name=name, time=time, water_chem_type=water_chem_type))
			new_water_chem_win.destroy()

		new_water_chem_win = tk.Toplevel()
		name_var = tk.StringVar(value=u'New Item {num}'.format(num=sum(u'New Item' in s for s in brew_data.water_chemistry_additions)))
		time_var = tk.IntVar()
		type_var = tk.StringVar(value=u'Hop')
		tk.Label(new_water_chem_win, text=u"Name: ").grid(row=0, column=0)
		name_entry = tk.Entry(new_water_chem_win, textvariable=name_var, justify=u'center')
		name_entry.grid(row=0, column=1, sticky=u'nsew')
		tk.Label(new_water_chem_win, text=u"Time: ").grid(row=1, column=0)
		time_spnbx = tk.Spinbox(new_water_chem_win, from_=0, to=1000000000, textvariable=time_var, justify=u'center')
		time_spnbx.grid(row=1, column=1, sticky=u'nsew')
		tk.Label(new_water_chem_win, text=u"Type: ").grid(row=2, column=0)
		type_opt = tk.OptionMenu(new_water_chem_win, type_var, u"Hop", u"Malt", u"Yeast")
		type_opt.grid(row=2, column=1, sticky=u'nsew')

		type_var.trace(u'w', on_type_change)

		tk.Button(new_water_chem_win, text=u"Cancel", command=cancel).grid(row=3, column=0)
		tk.Button(new_water_chem_win, text=u"Done", command=done).grid(row=3, column=1, sticky=u'nsew')
		tk.Button(new_water_chem_win, text=u"Save To Database", command=save_to_database).grid(row=4, column=0, columnspan=2, sticky=u'nsew')

class yeast_editor(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.widgets()

	def widgets(self):
		_fgcolor = u'#000000'  # X11 color: 'black'
		_compcolor = u'#d9d9d9' # X11 color: 'gray85'
		_ana1color = u'#d9d9d9' # X11 color: 'gray85'
		_ana2color = u'#ececec' # Closest X11 color: 'gray92'
		font9 = u"-family {DejaVu Sans} -size 10 -weight bold -slant "  \
			u"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()
		self.style.configure(u'.',background=_bgcolor)
		self.style.configure(u'.',foreground=_fgcolor)
		self.style.configure(u'.',font=u"TkDefaultFont")
		self.style.map(u'.',background=
			[(u'selected', _compcolor), (u'active',_ana2color)])

		self.TPanedwindow1 = tk.PanedWindow(self, orient=u"horizontal",  background=_bgcolor)
		self.TPanedwindow1.place(relx=0.013, rely=0.0, relheight=0.973
				, relwidth=0.966)
		self.yeast_panedwindow1 = tk.LabelFrame(width=400, text=u'Yeasts:',  background=_bgcolor)
		self.TPanedwindow1.add(self.yeast_panedwindow1)
		self.yeast_panedwindow2 = tk.LabelFrame(text=u'Modifications:', background=_bgcolor)
		self.TPanedwindow1.add(self.yeast_panedwindow2)


		self.yeast_lstbx = ScrolledListBox(self.yeast_panedwindow1)
		self.yeast_lstbx.place(relx=0.025, rely=0.043, relheight=0.887
				, relwidth=0.94, bordermode=u'ignore')
		self.yeast_lstbx.configure(background=u"white")
		self.yeast_lstbx.configure(font=u"TkFixedFont")
		self.yeast_lstbx.configure(highlightcolor=u"#d9d9d9")
		self.yeast_lstbx.configure(selectbackground=u"#c4c4c4")
		self.yeast_lstbx.configure(width=10)

		self.yeast_delete_butt = tk.Button(self.yeast_panedwindow1)
		self.yeast_delete_butt.place(relx=0.025, rely=0.924, height=28, width=83
				, bordermode=u'ignore')
		self.yeast_delete_butt.configure(takefocus=u"")
		self.yeast_delete_butt.configure(text=u'''Delete''')
		self.yeast_delete_butt.configure(command=self.delete)

		self.yeast_modify_butt = tk.Button(self.yeast_panedwindow1)
		self.yeast_modify_butt.place(relx=0.35, rely=0.924, height=28, width=83
				, bordermode=u'ignore')
		self.yeast_modify_butt.configure(takefocus=u"")
		self.yeast_modify_butt.configure(text=u'''Modify''')
		self.yeast_modify_butt.configure(command=lambda: self.input_state(1))

		self.yeast_new_butt = tk.Button(self.yeast_panedwindow1)
		self.yeast_new_butt.place(relx=0.725, rely=0.924, height=28, width=83
				, bordermode=u'ignore')
		self.yeast_new_butt.configure(takefocus=u"")
		self.yeast_new_butt.configure(text=u'''New''')
		self.yeast_new_butt.configure(command=self.new)

		############################ Config Section ############################

		self.yeast_name_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_name_lbl.place(relx=0.056, rely=0.087, bordermode=u'ignore')
		self.yeast_name_lbl.configure(background=_bgcolor)
		self.yeast_name_lbl.configure(foreground=u"#000000")
		self.yeast_name_lbl.configure(font=font9)
		self.yeast_name_lbl.configure(relief=u'flat')
		self.yeast_name_lbl.configure(text=u'''Name:''')

		self.yeast_name_ent = tk.Entry(self.yeast_panedwindow2)
		self.yeast_name_ent.place(relx=0.222, rely=0.087, relheight=0.046
				, relwidth=0.511, bordermode=u'ignore')
		self.yeast_name_ent.configure(justify=u'center')
		self.yeast_name_ent.configure(foreground=u"#000000")
		self.yeast_name_ent.configure(takefocus=u"")
		self.yeast_name_ent.configure(cursor=u"xterm")

		self.yeast_type_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_type_lbl.place(relx=0.056, rely=0.152, bordermode=u'ignore')
		self.yeast_type_lbl.configure(background=_bgcolor)
		self.yeast_type_lbl.configure(foreground=u"#000000")
		self.yeast_type_lbl.configure(font=font9)
		self.yeast_type_lbl.configure(relief=u'flat')
		self.yeast_type_lbl.configure(text=u'''Type:''')

		self.yeast_type_combo = ttk.Combobox(self.yeast_panedwindow2)
		self.yeast_type_combo.place(relx=0.222, rely=0.152, relheight=0.046
				, relwidth=0.519, bordermode=u'ignore')
		self.yeast_type_combo.configure(width=187)
		self.yeast_type_combo_values = [u'Dry', u'Liquid']
		self.yeast_type_combo.configure(values=self.yeast_type_combo_values)
		self.yeast_type_combo.configure(takefocus=u"")
		self.yeast_type_combo.configure(justify=u'center')

		self.yeast_lab_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_lab_lbl.place(relx=0.056, rely=0.217, bordermode=u'ignore')
		self.yeast_lab_lbl.configure(background=_bgcolor)
		self.yeast_lab_lbl.configure(foreground=u"#000000")
		self.yeast_lab_lbl.configure(font=font9)
		self.yeast_lab_lbl.configure(relief=u'flat')
		self.yeast_lab_lbl.configure(text=u'''Lab:''')

		self.yeast_lab_ent = tk.Entry(self.yeast_panedwindow2)
		self.yeast_lab_ent.place(relx=0.222, rely=0.217, relheight=0.046
				, relwidth=0.511, bordermode=u'ignore')
		self.yeast_lab_ent.configure(justify=u'center')
		self.yeast_lab_ent.configure(foreground=u"#000000")
		self.yeast_lab_ent.configure(takefocus=u"")
		self.yeast_lab_ent.configure(cursor=u"xterm")

		self.yeast_origin_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_origin_lbl.place(relx=0.056, rely=0.283, bordermode=u'ignore')
		self.yeast_origin_lbl.configure(background=_bgcolor)
		self.yeast_origin_lbl.configure(foreground=u"#000000")
		self.yeast_origin_lbl.configure(font=font9)
		self.yeast_origin_lbl.configure(relief=u'flat')
		self.yeast_origin_lbl.configure(text=u'''Origin:''')

		self.yeast_origin_ent = tk.Entry(self.yeast_panedwindow2)
		self.yeast_origin_ent.place(relx=0.222, rely=0.283, relheight=0.046
				, relwidth=0.511, bordermode=u'ignore')
		self.yeast_origin_ent.configure(justify=u'center')
		self.yeast_origin_ent.configure(foreground=u"#000000")
		self.yeast_origin_ent.configure(takefocus=u"")
		self.yeast_origin_ent.configure(cursor=u"xterm")

		self.yeast_flocc_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_flocc_lbl.place(relx=0.056, rely=0.348, height=19, width=100
				, bordermode=u'ignore')
		self.yeast_flocc_lbl.configure(background=_bgcolor)
		self.yeast_flocc_lbl.configure(foreground=u"#000000")
		self.yeast_flocc_lbl.configure(font=font9)
		self.yeast_flocc_lbl.configure(relief=u'flat')
		self.yeast_flocc_lbl.configure(text=u'''Flocculation:''')
		self.yeast_flocc_lbl.configure(width=100)

		self.yeast_flocc_combo = ttk.Combobox(self.yeast_panedwindow2)
		self.yeast_flocc_combo.place(relx=0.361, rely=0.348, relheight=0.046
				, relwidth=0.381, bordermode=u'ignore')
		self.yeast_flocc_combo.configure(width=137)
		self.yeast_flocc_combo_values = [u'Low', u'Low/Medium', u'Medium', u'Medium/High', u'High']
		self.yeast_flocc_combo.configure(values=self.yeast_flocc_combo_values)
		self.yeast_flocc_combo.configure(takefocus=u"")
		self.yeast_flocc_combo.configure(justify=u'center')

		self.yeast_attenuation_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_attenuation_lbl.place(relx=0.056, rely=0.413, bordermode=u'ignore')
		self.yeast_attenuation_lbl.configure(background=_bgcolor)
		self.yeast_attenuation_lbl.configure(foreground=u"#000000")
		self.yeast_attenuation_lbl.configure(font=font9)
		self.yeast_attenuation_lbl.configure(relief=u'flat')
		self.yeast_attenuation_lbl.configure(text=u'''Attenuation:''')

		self.yeast_temperature_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_temperature_lbl.place(relx=0.056, rely=0.478, height=19
				, width=110, bordermode=u'ignore')
		self.yeast_temperature_lbl.configure(background=_bgcolor)
		self.yeast_temperature_lbl.configure(foreground=u"#000000")
		self.yeast_temperature_lbl.configure(font=font9)
		self.yeast_temperature_lbl.configure(relief=u'flat')
		self.yeast_temperature_lbl.configure(text=u'''Temperature:''')
		self.yeast_temperature_lbl.configure(width=110)

		self.yeast_attenuation_ent = tk.Entry(self.yeast_panedwindow2)
		self.yeast_attenuation_ent.place(relx=0.333, rely=0.413, relheight=0.046
				, relwidth=0.4, bordermode=u'ignore')
		self.yeast_attenuation_ent.configure(justify=u'center')
		self.yeast_attenuation_ent.configure(width=144)
		self.yeast_attenuation_ent.configure(foreground=u"#000000")
		self.yeast_attenuation_ent.configure(takefocus=u"")
		self.yeast_attenuation_ent.configure(cursor=u"xterm")

		self.yeast_temperature_spinbox1 = tk.Spinbox(self.yeast_panedwindow2, from_=1.0, to=100.0)
		self.yeast_temperature_spinbox1_value = tk.DoubleVar()
		self.yeast_temperature_spinbox1.place(relx=0.389, rely=0.478
				, relheight=0.05, relwidth=0.133, bordermode=u'ignore')
		self.yeast_temperature_spinbox1.configure(activebackground=u"#f9f9f9")
		self.yeast_temperature_spinbox1.configure(background=u"white")
		self.yeast_temperature_spinbox1.configure(highlightbackground=u"black")
		self.yeast_temperature_spinbox1.configure(selectbackground=u"#c4c4c4")
		self.yeast_temperature_spinbox1.configure(width=48)
		self.yeast_temperature_spinbox1.configure(textvariable=self.yeast_temperature_spinbox1_value)

		self.yeast_temperature_spinbox2 = tk.Spinbox(self.yeast_panedwindow2, from_=1.0, to=100.0)
		self.yeast_temperature_spinbox2_value = tk.DoubleVar()
		self.yeast_temperature_spinbox2.place(relx=0.528, rely=0.478
				, relheight=0.05, relwidth=0.133, bordermode=u'ignore')
		self.yeast_temperature_spinbox2.configure(activebackground=u"#f9f9f9")
		self.yeast_temperature_spinbox2.configure(background=u"white")
		self.yeast_temperature_spinbox2.configure(highlightbackground=u"black")
		self.yeast_temperature_spinbox2.configure(selectbackground=u"#c4c4c4")
		self.yeast_temperature_spinbox2.configure(width=48)
		self.yeast_temperature_spinbox2.configure(textvariable=self.yeast_temperature_spinbox2_value)

		self.yeast_comm_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_comm_lbl.place(relx=0.056, rely=0.543, bordermode=u'ignore')
		self.yeast_comm_lbl.configure(background=_bgcolor)
		self.yeast_comm_lbl.configure(foreground=u"#000000")
		self.yeast_comm_lbl.configure(font=font9)
		self.yeast_comm_lbl.configure(relief=u'flat')
		self.yeast_comm_lbl.configure(text=u'''Comments:''')

		self.yeast_comm_ent = tk.Entry(self.yeast_panedwindow2)
		self.yeast_comm_ent.place(relx=0.028, rely=0.587, relheight=0.046
		, relwidth=0.956, bordermode=u'ignore')
		self.yeast_comm_ent.configure(takefocus=u"")
		self.yeast_comm_ent.configure(cursor=u"xterm")

		self.yeast_cancel_butt = tk.Button(self.yeast_panedwindow2)
		self.yeast_cancel_butt.place(relx=0.028, rely=0.652, height=28, width=83
				, bordermode=u'ignore')
		self.yeast_cancel_butt.configure(takefocus=u"")
		self.yeast_cancel_butt.configure(text=u'''Cancel''')
		self.yeast_cancel_butt.configure(command=lambda: self.show_data(self.yeast_lstbx.get(tk.ACTIVE)))

		self.yeast_clear_butt = tk.Button(self.yeast_panedwindow2)
		self.yeast_clear_butt.place(relx=0.389, rely=0.652, height=28, width=83
				, bordermode=u'ignore')
		self.yeast_clear_butt.configure(takefocus=u"")
		self.yeast_clear_butt.configure(text=u'''Clear Form''')
		self.yeast_clear_butt.configure(command=self.clear_form)

		self.yeast_done_butt = tk.Button(self.yeast_panedwindow2)
		self.yeast_done_butt.place(relx=0.75, rely=0.652, height=28, width=83
				, bordermode=u'ignore')
		self.yeast_done_butt.configure(takefocus=u"")
		self.yeast_done_butt.configure(text=u'''Done''')
		self.yeast_done_butt.configure(command=self.done)

		self.yeast_save_data_butt = tk.Button(self.yeast_panedwindow2)
		self.yeast_save_data_butt.place(relx=0.222, rely=0.739, height=108
				, width=213, bordermode=u'ignore')
		self.yeast_save_data_butt.configure(takefocus=u"")
		self.yeast_save_data_butt.configure(text=u'''Save to Database''')
		self.yeast_save_data_butt.configure(command=self.save)


		self.yeast_lstbx.bind(u'<<ListboxSelect>>', self.select_listbox)
		self.input_state(0)

	def __adjust_sash0(self, event):
		paned = event.widget
		pos = [400, ]
		i = 0
		for sash in pos:
			paned.sashpos(i, sash)
			i += 1
		paned.unbind(u'<map>', self.__funcid0)
		del self.__funcid0

	def show_data(self, yeast):
		self.name = yeast
		name = yeast
		yeast_type = brew_data.yeast_data[name][u'Type']
		yeast_type = u'Dry' if yeast_type == u'D' else yeast_type
		yeast_type = u'Liquid' if yeast_type == u'L' else yeast_type
		lab = brew_data.yeast_data[name][u'Lab']
		flocculation = brew_data.yeast_data[name][u'Flocculation']
		attenuation = brew_data.yeast_data[name][u'Attenuation']

		if brew_data.yeast_data[name][u'Temperature'] != u'Unknown':
			temperature1 = float(brew_data.yeast_data[name][u'Temperature'].replace(u'°', u'').split(u'-')[0])
			temperature2 = float(brew_data.yeast_data[name][u'Temperature'].replace(u'°', u'').split(u'-')[1])
		else:
			temperature1 = 20
			temperature2 = 20

		origin = brew_data.yeast_data[name][u'Origin']
		description = brew_data.yeast_data[name][u'Description']

		self.input_state(1)
		self.yeast_name_ent.delete(0, tk.END)
		self.yeast_comm_ent.delete(0, tk.END)
		self.yeast_lab_ent.delete(0, tk.END)
		self.yeast_origin_ent.delete(0, tk.END)
		self.yeast_attenuation_ent.delete(0, tk.END)

		if flocculation not in self.yeast_flocc_combo_values:
			self.yeast_flocc_combo_values.append(flocculation)
			self.yeast_flocc_combo.configure(values=self.yeast_flocc_combo_values)

		if yeast_type not in self.yeast_type_combo_values:
			self.yeast_type_combo_values.append(yeast_type)
			self.yeast_type_combo.configure(values=self.yeast_type_combo_values)
		self.yeast_flocc_combo.set(flocculation)
		self.yeast_type_combo.set(yeast_type)

		self.yeast_temperature_spinbox1_value.set(round(temperature1))
		self.yeast_temperature_spinbox2_value.set(round(temperature2))

		self.yeast_name_ent.insert(0, name)
		self.yeast_comm_ent.insert(0, description)
		self.yeast_lab_ent.insert(0, lab)
		self.yeast_origin_ent.insert(0, origin)
		self.yeast_attenuation_ent.insert(0, attenuation)
		#self.grist_type_combo.set(self.grist_type_combo_values[type-1])

		self.input_state(0)

	def input_state(self, state):

		state = u"disabled" if state == 0 else u"normal"

		self.yeast_comm_ent.configure(state=state)
		self.yeast_name_ent.configure(state=state)
		self.yeast_origin_ent.configure(state=state)
		self.yeast_lab_ent.configure(state=state)
		self.yeast_attenuation_ent.configure(state=state)
		self.yeast_temperature_spinbox1.configure(state=state)
		self.yeast_temperature_spinbox2.configure(state=state)

		self.yeast_flocc_combo.configure(state=state)
		self.yeast_type_combo.configure(state=state)

		self.yeast_done_butt.configure(state=state)
		self.yeast_clear_butt.configure(state=state)
		self.yeast_cancel_butt.configure(state=state)
	def clear_form(self):
		self.yeast_name_ent.delete(0, tk.END)
		self.yeast_comm_ent.delete(0, tk.END)
		self.yeast_lab_ent.delete(0, tk.END)
		self.yeast_origin_ent.delete(0, tk.END)
		self.yeast_attenuation_ent.delete(0, tk.END)

	def delete(self):
		del brew_data.yeast_data[self.yeast_lstbx.get(self.yeast_lstbx.curselection())]
		self.yeast_lstbx.delete(self.yeast_lstbx.curselection())

	def new(self):
		name = u'New Yeast {num}'.format(num=sum(u'New Yeast' in s for s in brew_data.yeast_data))
		self.yeast_lstbx.insert(tk.END, name)
		try:
			brew_data.yeast_data[name] = brew_data.yeast_data[self.yeast_lstbx.get(self.yeast_lstbx.curselection())]
		except:
			try:
				brew_data.yeast_data[name] = brew_data.yeast_data[tk.ACTIVE]
			except:
				brew_data.yeast_data[name] = {u'Type': u'D', u'Lab': u'Lallemand', u'Flocculation': u'Low', u'Attenuation': u'High', u'Temperature': u'66-72°', u'Description': u'Unkown', u'Origin': u'Unknown'}

		self.show_data(name)
		self.yeast_lstbx.select_set(tk.END)
		self.yeast_lstbx.activate(tk.END)
		self.yeast_lstbx.yview(tk.END)

	def select_listbox(self, event):
		try:
			self.show_data(self.yeast_lstbx.get(self.yeast_lstbx.curselection()))
		except:
			pass

	def done(self):
		name = self.yeast_name_ent.get()
		lab = self.yeast_lab_ent.get()
		origin = self.yeast_origin_ent.get()
		attenuation = self.yeast_attenuation_ent.get()
		temp1 = float(self.yeast_temperature_spinbox1.get())
		temp2 = float(self.yeast_temperature_spinbox2.get())
		temperature = u'{temp1}-{temp2}°'.format(temp1=temp1, temp2=temp2)
		description = self.yeast_comm_ent.get()
		flocculation = self.yeast_flocc_combo.get()
		yeast_type = u'D' if self.yeast_type_combo.get() == u'Dry' else self.yeast_type_combo.get()
		yeast_type = u'L' if yeast_type == u'Liquid' else yeast_type
		brew_data.yeast_data[name] = {u'Type': yeast_type, u'Lab': lab, u'Flocculation': flocculation, u'Attenuation': attenuation, u'Temperature': temperature, u'Description': description, u'Origin': origin}
		del brew_data.yeast_data[self.name]
		self.reinsert()
		self.show_data(name)

	def save(self):
		with open(resource_path(u'yeast_data.txt'), u'w') as f:
			for yeast, value in brew_data.yeast_data.items():
				name = yeast
				yeast_type = value[u'Type']
				lab = value[u'Lab']
				flocculation = value[u'Flocculation']
				attenuation = value[u'Attenuation']
				temperature = value[u'Temperature']
				origin = value[u'Origin']
				description = value[u'Description']
				f.write(u'{name}\t{yeast_type}\t{lab}\t{flocculation}\t{attenuation}\t{temperature}\t{origin}\t{description}\n'.format(name=name, yeast_type=yeast_type, lab=lab, flocculation=flocculation, attenuation=attenuation, temperature=temperature, origin=origin, description=description))
		self.done()

	def reinsert(self):
		self.yeast_lstbx.delete(0, tk.END)
		for yeast in sorted(brew_data.yeast_data):
			self.yeast_lstbx.insert(tk.END, yeast)

class notes_area(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.widgets()

	def widgets(self):
		########################################################################################
		#				Salvaged from https://github.com/jimbob88/texpert/					   #
		########################################################################################
		self.texpert = ScrolledText(self, bg=u"white", undo=True, maxundo=-1, font=(u"Arial", 11))
		self.texpert.grid(row=0, column=0, sticky=u'nsew', padx=2, pady=2)
		self.texpert.focus_set()
		#edit menu
		self.editmenu = tk.Menu(tearoff=0)
		self.editmenu.add_command(label=u"Undo", command=self.undo_com, accelerator=u"Ctrl+Z")
		self.editmenu.add_command(label=u"Redo", command=self.redo_com, accelerator=u"Shift+Ctrl+Z")
		self.editmenu.add_separator()
		self.editmenu.add_command(label=u"Cut", command=self.cut_com, accelerator=u"Ctrl+X")
		self.texpert.bind(u"<Control-Key-x>", lambda e: self.undo_com)
		self.editmenu.add_command(label=u"Copy", command=self.copy_com, accelerator=u"Ctrl+C")
		self.texpert.bind(u"<Control-Key-c>", lambda e: self.undo_com)
		self.editmenu.add_command(label=u"Paste", command=self.paste_com, accelerator=u"Ctrl+V")
		self.texpert.bind(u"<Control-Key-v>", lambda e: self.undo_com)
		self.editmenu.add_separator()
		self.editmenu.add_command(label=u"Select All", command=self.select_all, accelerator=u"Ctrl+A")
		self.editmenu.add_separator()
		self.html_formatting = tk.BooleanVar()
		self.editmenu.add_checkbutton(label=u"HTML Mode", variable=self.html_formatting)
		# self.editmenu.add_separator()
		# self.editmenu.add_command(label="Find", command=self.find_win, accelerator="Ctrl+F")



		self.texpert.bind(u"<Control-Key-a>", self.select_all)
		self.texpert.bind(u"<Control-Key-A>", self.select_all)
		self.texpert.bind(u"<Button-3>", self.r_click)

		self.current_file = None
		self.file_type = None

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

	def r_click(self, event):
		self.editmenu.tk_popup(event.x_root, event.y_root)

	def mode_popup(self, event):
		try:
			self.submenu.post(event.x_root, event.y_root)
		finally:
			self.submenu.grab_release()

	def undo_com(self):
		# print(self.texpert.event_generate("<<Undo>>"))
		try: self.texpert.event_generate(u"<<Undo>>")
		except tk.TclError: print u'Undo Failed'

	def redo_com(self):
		try: self.texpert.event_generate(u"<<Redo>>")
		except tk.TclError: print u'Redo Failed'

	def cut_com(self):
		try: self.texpert.event_generate(u"<<Cut>>")
		except tk.TclError: pass

	def copy_com(self):
		try: self.texpert.event_generate(u"<<Copy>>")
		except tk.TclError: pass

	def paste_com(self):
		try: self.texpert.event_generate(u"<<Paste>>")
		except tk.TclError: pass

	def select_all(self, event=None):
		self.texpert.tag_add(tk.SEL, u'1.0', u'end-1c')
		self.texpert.mark_set(tk.INSERT, u'1.0')
		self.texpert.see(tk.INSERT)
		return u'break'



class AutoScroll(object):
	u'''Configure the scrollbars for a widget.'''

	def __init__(self, master):
		#  Rozen. Added the try-except clauses so that this class
		#  could be used for scrolled entry widget for which vertical
		#  scrolling is not supported. 5/7/14.
		try:
			vsb = ttk.Scrollbar(master, orient=u'vertical', command=self.yview)
		except:
			pass
		hsb = ttk.Scrollbar(master, orient=u'horizontal', command=self.xview)

		#self.configure(yscrollcommand=_autoscroll(vsb),
		#    xscrollcommand=_autoscroll(hsb))
		try:
			self.configure(yscrollcommand=self._autoscroll(vsb))
		except:
			pass
		self.configure(xscrollcommand=self._autoscroll(hsb))

		self.grid(column=0, row=0, sticky=u'nsew')
		try:
			vsb.grid(column=1, row=0, sticky=u'ns')
		except:
			pass
		hsb.grid(column=0, row=1, sticky=u'ew')

		master.grid_columnconfigure(0, weight=1)
		master.grid_rowconfigure(0, weight=1)

		if sys.version_info >= (3, 0):
			methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
				  | tk.Place.__dict__.keys()
		else:
			methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
				+ tk.Place.__dict__.keys()

		for meth in methods:
			if meth[0] != u'_' and meth not in (u'config', u'configure'):
				setattr(self, meth, getattr(master, meth))

	@staticmethod
	def _autoscroll(sbar):
		u'''Hide and show scrollbar as needed.'''
		def wrapped(first, last):
			first, last = float(first), float(last)
			if first <= 0 and last >= 1:
				sbar.grid_remove()
			else:
				sbar.grid()
			sbar.set(first, last)
		return wrapped

	def __str__(self):
		return unicode(self.first_tab)

def _create_container(func):
	u'''Creates a ttk Frame with a given master, and use this new frame to
	place the scrollbars and the widget.'''
	def wrapped(cls, master, **kw):
		container = ttk.Frame(master)
		container.bind(u'<Enter>', lambda e: _bound_to_mousewheel(e, container))
		container.bind(u'<Leave>', lambda e: _unbound_to_mousewheel(e, container))
		return func(cls, container, **kw)
	return wrapped

class ScrolledTreeView(AutoScroll, ttk.Treeview):
	u'''A standard ttk Treeview widget with scrollbars that will
	automatically show/hide as needed.'''
	@_create_container
	def __init__(self, master, **kw):
		ttk.Treeview.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

	def insert(self, parent, index, iid=None, **kw):
		opts = ttk._format_optdict(kw)
		if iid is not None:
			res = self.tk.call(self._w, u"insert", parent, index,
				u"-id", iid, *opts)
		else:
			iid = u'I{iid}'.format(iid=format(len(self.get_children())+1, u'03x')) #hex(len(self.get_children())).split('x')[-1]
			res = self.tk.call(self._w, u"insert", parent, index,
				u"-id", iid, *opts)
		return res

class ScrolledListBox(AutoScroll, tk.Listbox):
	u'''A standard Tkinter Text widget with scrollbars that will
	automatically show/hide as needed.'''
	@_create_container
	def __init__(self, master, **kw):
		tk.Listbox.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

class ScrolledText(AutoScroll, tk.Text):
	u'''A standard Tkinter Text widget with scrollbars that will
	automatically show/hide as needed.'''
	@_create_container
	def __init__(self, master, **kw):
		tk.Text.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)


def _bound_to_mousewheel(event, widget):
	child = widget.winfo_children()[0]
	if platform.system() == u'Windows' or platform.system() == u'Darwin':
		child.bind_all(u'<MouseWheel>', lambda e: _on_mousewheel(e, child))
		child.bind_all(u'<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
	else:
		child.bind_all(u'<Button-4>', lambda e: _on_mousewheel(e, child))
		child.bind_all(u'<Button-5>', lambda e: _on_mousewheel(e, child))
		child.bind_all(u'<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
		child.bind_all(u'<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
	if platform.system() == u'Windows' or platform.system() == u'Darwin':
		widget.unbind_all(u'<MouseWheel>')
		widget.unbind_all(u'<Shift-MouseWheel>')
	else:
		widget.unbind_all(u'<Button-4>')
		widget.unbind_all(u'<Button-5>')
		widget.unbind_all(u'<Shift-Button-4>')
		widget.unbind_all(u'<Shift-Button-5>')

def _on_mousewheel(event, widget):
	if platform.system() == u'Windows':
		widget.yview_scroll(-1*int(event.delta/120),u'units')
	elif platform.system() == u'Darwin':
		widget.yview_scroll(-1*int(event.delta),u'units')
	else:
		if event.num == 4:
			widget.yview_scroll(-1, u'units')
		elif event.num == 5:
			widget.yview_scroll(1, u'units')

def _on_shiftmouse(event, widget):
	if platform.system() == u'Windows':
		widget.xview_scroll(-1*int(event.delta/120), u'units')
	elif platform.system() == u'Darwin':
		widget.xview_scroll(-1*int(event.delta), u'units')
	else:
		if event.num == 4:
			widget.xview_scroll(-1, u'units')
		elif event.num == 5:
			widget.xview_scroll(1, u'units')

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
		elif os.path.splitext(os.path.basename(relative_path))[1] == u'.html':
			return os.path.join(os.path.expanduser(u'~/.config/Wheelers-Wort-Works/recipes/html'), relative_path)
		else:
			return os.path.join(os.path.expanduser(u'~/.config/Wheelers-Wort-Works/'), relative_path)
def main(file=None, update_available=False):
	root = tk.Tk()
	gui = beer_engine_mainwin(root)
	root.config(cursor=u"arrow")
	if file != None:
		gui.open_file(file)
	if update_available:
		messagebox.showinfo(u"Update Available", u"An update has become available, it is recommended you run the command: {command}".format(command=(u'sudo wheelers-wort-works --coreupdate' if __mode__ == u'deb' else u'python3 main.py --coreupdate')))
	root.mainloop()


if __name__ == u'__main__':
	main()
