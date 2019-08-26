#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
	import tkinter as tk
	import tkinter.ttk as ttk
	from tkinter import filedialog, messagebox
except:
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
import datetime
try:
	import bs4
except ImportError:
	pass

__mode__ = 'local'
_bgcolor = 'SystemButtonFace' if platform.system() == 'Windows' else '#d9d9d9'
class beer_engine_mainwin:
	def __init__(self, master=None):

		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85'
		_ana2color = '#ececec' # Closest X11 color: 'gray92'
		font9 = "-family {DejaVu Sans} -size 7 -weight normal -slant "  \
			"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()

		if not os.path.isfile(resource_path('defaults.txt')):
			with open(resource_path('defaults.txt'), 'w') as f:
				volume = brew_data.constants['Volume']
				efficiency = brew_data.constants['Efficiency']*100
				evaporation = round((brew_data.constants['Boil Volume Scale']-1)*100, 1)
				LGratio = brew_data.constants['Liquor To Grist Ratio']
				attenuation = brew_data.constants['Attenuation Default']
				save_close = brew_data.constants['Save On Close']
				boil_time = brew_data.constants['Default Boil Time']
				replace_defaults = brew_data.constants['Replace Defaults']
				f.write('efficiency={efficiency}\nvolume={volume}\nevaporation={evaporation}\nLGratio={LGratio}\nattenuation={attenuation}\nsave_close={save_close}\nboil_time={boil_time}\nreplace_defaults={replace_defaults}'.format(efficiency=efficiency, volume=volume, evaporation=evaporation, LGratio=LGratio,
																																																										attenuation=attenuation, save_close=save_close, boil_time=boil_time, replace_defaults=replace_defaults))
		else:
			with open(resource_path('defaults.txt'), 'r') as f:
				data = [line.strip().split('=') for line in f]
				for constants in data:
					if constants[0] == 'efficiency': brew_data.constants['Efficiency'] = float(constants[1])/100
					elif constants[0] == 'volume': brew_data.constants['Volume'] = float(constants[1])
					elif constants[0] == 'evaporation': brew_data.constants['Boil Volume Scale'] = (float(constants[1])/100)+1
					elif constants[0] == 'LGratio': brew_data.constants['Liquor To Grist Ratio'] = float(constants[1])
					elif constants[0] == 'attenuation': brew_data.constants['Attenuation Default'] = constants[1]
					elif constants[0] == 'save_close': brew_data.constants['Save On Close'] = True if constants[1] == 'True' else False
					elif constants[0] == 'boil_time': brew_data.constants['Default Boil Time'] = int(constants[1])
					elif constants[0] == 'replace_defaults': brew_data.constants['Replace Defaults'] = True if constants[1] == 'True' else False

		if not os.path.isfile(resource_path('hop_data.txt')):
			with open(resource_path('hop_data.txt'), 'w') as f:
				for hop, value in brew_data.hop_data.items():
					name = hop
					hop_type = value['Form']
					origin = value['Origin']
					alpha = value['Alpha']
					use = value['Use']
					description = value['Description']
					f.write('{name}\t{hop_type}\t{origin}\t{alpha}\t{use}\t{description}\n'.format(name=name, hop_type=hop_type, origin=origin, alpha=alpha, use=use, description=description))
		else:
			with open(resource_path('hop_data.txt'), 'r') as f:
				if brew_data.constants['Replace Defaults']: brew_data.hop_data = {}
				data = [line.strip().split('\t') for line in f]
				for hop in data:
					# 'Nelson Sauvin': {'Form': 'Whole', 'Origin': 'New Zeland', 'Description': '', 'Use': 'General Purpose', 'Alpha': 12.7}
					name = hop[0]
					hop_type = hop[1]
					origin = hop[2]
					alpha = float(hop[3])
					use = hop[4]
					description = hop[5] if len(hop) >= 6 else 'No Description'
					brew_data.hop_data[name] = {'Form': hop_type, 'Origin': origin, 'Alpha': alpha, 'Use': use, 'Description': description}
				#print('hop_data =', brew_data.hop_data)
		if not os.path.isfile(resource_path('grain_data.txt')):
			with open(resource_path('grain_data.txt'), 'w') as f:
				for ingredient, value in brew_data.grist_data.items():
					name = ingredient
					ebc = value['EBC']
					grain_type = value['Type']
					extract = value['Extract']
					moisture = value['Moisture']
					fermentability = value['Fermentability']
					description = value['Description']
					f.write('{name}\t{ebc}\t{grain_type}\t{extract}\t{moisture}\t{fermentability}\t{description}\n'.format(name=name, ebc=ebc, grain_type=grain_type, extract=extract, moisture=moisture, fermentability=fermentability, description=description))
		else:
			with open(resource_path('grain_data.txt'), 'r') as f:
				if brew_data.constants['Replace Defaults']: brew_data.grain_data = {}
				data = [line.strip().split('\t') for line in f]
				for ingredient in data:
					# {'Wheat Flour': {'EBC': 0.0, 'Type': 3.0, 'Extract': 304.0, 'Description': 'No Description', 'Moisture': 11.0, 'Fermentability': 62.0}}
					name = ingredient[0]
					ebc = float(ingredient[1])
					grain_type = float(ingredient[2])
					extract = float(ingredient[3])
					moisture = float(ingredient[4])
					fermentability = float(ingredient[5])
					description = ingredient[6]
					brew_data.grist_data[name] = {'EBC': ebc, 'Type': grain_type, 'Extract': extract, 'Description': description, 'Moisture': moisture, 'Fermentability': fermentability}
				#print('grist_data =', brew_data.grist_data)

		if not os.path.isfile(resource_path('yeast_data.txt')):
			with open(resource_path('yeast_data.txt'), 'w') as f:
				if brew_data.constants['Replace Defaults']: brew_data.yeast_data = {}
				for yeast, value in brew_data.yeast_data.items():
					name = yeast
					yeast_type = value['Type']
					lab = value['Lab']
					flocculation = value['Flocculation']
					attenuation = value['Attenuation']
					temperature = value['Temperature']
					origin = value['Origin']
					description = value['Description']
					f.write('{name}\t{yeast_type}\t{lab}\t{flocculation}\t{attenuation}\t{temperature}\t{origin}\t{description}\n'.format(name=name, yeast_type=yeast_type, lab=lab, flocculation=flocculation, attenuation=attenuation, temperature=temperature, origin=origin, description=description))
		else:
			with open(resource_path('yeast_data.txt'), 'r') as f:
				data = [line.strip().split('\t') for line in f]
				for yeast in data:
					name = yeast[0]
					yeast_type = yeast[1]
					lab = yeast[2]
					flocculation = yeast[3]
					attenuation = yeast[4]
					temperature = yeast[5]
					origin = yeast[6]
					description = yeast[7]
					brew_data.yeast_data[name] = {'Type': yeast_type, 'Lab': lab, 'Flocculation': flocculation, 'Attenuation': attenuation, 'Temperature': temperature, 'Description': description, 'Origin': origin}

		if not os.path.isfile(resource_path('water_chem_data.txt')):
			with open(resource_path('water_chem_data.txt'), 'w') as f:
				for water_chem, values in brew_data.water_chemistry_additions.items():
					value = values['Values']
					name = water_chem
					time = value['Time'] if 'Time' in value else 'N/A'
					#print(value)
					water_chem_type = value['Type']
					f.write('{name}\t{time}\t{water_chem_type}\n'.format(name=name, time=time, water_chem_type=water_chem_type))
		else:
			with open(resource_path('water_chem_data.txt'), 'r') as f:
				if brew_data.constants['Replace Defaults']: brew_data.water_chemistry_additions = {}
				data = [line.strip().split('\t') for line in f]
				for water_chem in data:
					name = water_chem[0]
					time = float(water_chem[1]) if water_chem[1] != 'N/A' else water_chem[1]
					water_chem_type = water_chem[2]
					brew_data.water_chemistry_additions[name] = {'Values': {'Type': water_chem_type}}
					if time != 'N/A': brew_data.water_chemistry_additions[name]['Values']['Time'] = time


		self.style.configure('.',background=_bgcolor)
		self.style.configure('.',foreground=_fgcolor)
		self.style.configure('.',font="TkDefaultFont")
		self.style.map('.',background=
			[('selected', _compcolor), ('active',_ana2color)])

		self.current_file = ''
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.quit)
		if not platform.system() == 'Darwin':
				self.master.tk.call('wm', 'iconphoto', self.master._w, tk.PhotoImage(file=resource_path('logo.png')))
		self.master.geometry("+674+369")
		self.master.title("Wheeler's Wort Works")
		self.master.configure(highlightcolor="black")
		# self.master.resizable(0, 0)
		self.tabbed_frame = ttk.Notebook(self.master, width=800, height=480)

		self.first_tab = tk.Frame(self.tabbed_frame)
		self.second_tab = hops_editor(self.tabbed_frame)
		self.third_tab = grist_editor(self.tabbed_frame)
		self.fourth_tab = yeast_editor(self.tabbed_frame)
		self.fifth_tab = defaults_editor(self.tabbed_frame)
		self.sixth_tab = special_editor(self.tabbed_frame)
		self.seventh_tab = notes_area(self.tabbed_frame)
		self.tabbed_frame.add(self.first_tab, text="Engine Room")
		self.tabbed_frame.add(self.second_tab, text="Hop Editor")
		self.tabbed_frame.add(self.third_tab, text="Grist Editor")
		self.tabbed_frame.add(self.fourth_tab, text="Yeast Editor")
		self.tabbed_frame.add(self.fifth_tab, text="Defaults Editor")
		self.tabbed_frame.add(self.sixth_tab, text="Experimental Attenuation")
		self.tabbed_frame.add(self.seventh_tab, text="Notes Area")
		self.tabbed_frame.grid(row=0, column=0, sticky='nsew')
		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)

		######################### Menu ############################
		self.menubar = tk.Menu(self.master,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
		self.master.configure(menu = self.menubar)

		self.file_menu = tk.Menu(self.master,tearoff=0)
		self.menubar.add_cascade(menu=self.file_menu,
				activebackground="#ececec",
				activeforeground="#000000",
				 background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="File")
		self.sub_menu1 = tk.Menu(self.master,tearoff=0)
		self.file_menu.add_command(
			activebackground="#ececec",
			activeforeground="#000000",
			background=_bgcolor,
			font="TkMenuFont",
			foreground="#000000",
			label="Open",
			command=self.open_dialog,
			accelerator="Ctrl+O")

		self.master.bind("<Control-o>", self.open_dialog)

		self.file_menu.add_command(activebackground="#ececec",
				activeforeground="#000000",
				 background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Save",
				command=self.save,
				accelerator="Ctrl+S")
		self.master.bind("<Control-s>", lambda e: self.save())
		self.file_menu.add_command(activebackground="#ececec",
				activeforeground="#000000",
				 background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Save All",
				command=self.save_all,
				accelerator="Ctrl+A")
		self.master.bind("<Control-a>", lambda e: self.save_all())
		self.file_menu.add_command(activebackground="#ececec",
				activeforeground="#000000",
				 background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Save As",
				command=lambda: self.save_file(filedialog.asksaveasfilename(initialdir = os.path.expanduser('~/.config/Wheelers-Wort-Works-ce/recipes/' if __mode__ == 'deb' else '.'),title = "Select file", defaultextension=".berfx", initialfile='{0}.berf'.format(self.recipe_name_ent.get()))),
				accelerator="Ctrl+Shift+S")
		self.master.bind("<Control-S>", lambda e: self.save_file(filedialog.asksaveasfilename(initialdir = os.path.expanduser('~/.config/Wheelers-Wort-Works-ce/recipes/' if __mode__ == 'deb' else '.'),title = "Select file", defaultextension=".berf", initialfile='{0}.berf'.format(self.recipe_name_ent.get()))))
		self.file_menu.add_cascade(menu=self.sub_menu1,
				activebackground="#ececec",
				activeforeground="#000000",
				 background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Print")
		self.sub_menu1.add_command(
				activebackground="#ececec",
				activeforeground="#000000",
				 background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Simple HTML",
				command=self.create_html,
				accelerator="Ctrl+P")
		self.master.bind("<Control-p>", lambda e: self.create_html())
		self.sub_menu1.add_command(
				activebackground="#ececec",
				activeforeground="#000000",
				 background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Complex HTML",
				command=self.create_complex_html,
				accelerator="Ctrl+Shift+P")
		self.master.bind("<Control-P>", lambda e: self.create_complex_html())

		self.file_menu.add_command(
				activebackground="#ececec",
				activeforeground="#000000",
				 background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Quit",
				command=self.quit,
				accelerator="Ctrl+Q")
		self.master.bind("<Control-q>", lambda e: self.quit())

		self.backup_menu = tk.Menu(self.master,tearoff=0)
		self.menubar.add_cascade(menu=self.backup_menu,
				activebackground="#ececec",
				activeforeground="#000000",
				 background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Backup")
		self.backup_menu.add_command(
				activebackground="#ececec",
				activeforeground="#000000",
				background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Backup",
				command=self.database_to_folder)
		self.backup_menu.add_command(
				activebackground="#ececec",
				activeforeground="#000000",
				background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Restore",
				command=self.restore_backup_dialogue)	

		self.help_menu = tk.Menu(self.master,tearoff=0)
		self.menubar.add_cascade(menu=self.help_menu,
				activebackground="#ececec",
				activeforeground="#000000",
				 background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Help")
		self.help_menu.add_command(
				activebackground="#ececec",
				activeforeground="#000000",
				background=_bgcolor,
				font="TkMenuFont",
				foreground="#000000",
				label="Wheeler's Wort Works Help",
				command=lambda: webbrowser.open_new('https://github.com/jimbob88/wheelers-wort-works/wiki'),
				accelerator="Ctrl+H")
		self.master.bind("<Control-h>", lambda e: webbrowser.open_new('https://github.com/jimbob88/wheelers-wort-works/wiki'))

		######################## First Tab ########################
		self.first_tab.configure(background=_bgcolor)

		self.recipe_name_lbl = tk.Label(self.first_tab)
		self.recipe_name_lbl.place(relx=0.013, rely=0.021, relheight=0.0375, relwidth=0.1125)
		self.recipe_name_lbl.configure(activebackground="#f9f9f9")
		self.recipe_name_lbl.configure(background=_bgcolor)
		self.recipe_name_lbl.configure(text='''Recipe Name:''')

		self.recipe_name_ent = tk.Entry(self.first_tab)
		self.recipe_name_ent.place(relx=0.126, rely=0.021, relheight=0.0479
				, relwidth=0.28)
		self.recipe_name_ent.configure(background="white")
		self.recipe_name_ent.configure(font="TkFixedFont")
		self.recipe_name_ent.configure(selectbackground="#c4c4c4")
		self.recipe_name_ent.configure(justify='center')
		self.recipe_name_ent.insert(0, 'No Name')

		self.volume_lbl = tk.Label(self.first_tab)
		self.volume_lbl.place(relx=0.417, rely=0.021, relheight=0.0375, relwidth=0.0662)
		self.volume_lbl.configure(activebackground="#f9f9f9")
		self.volume_lbl.configure(background=_bgcolor)
		self.volume_lbl.configure(text='''Volume:''')

		self.volume = tk.StringVar()
		self.volume_ent = tk.Entry(self.first_tab)
		self.volume_ent.place(relx=0.492, rely=0.021, relheight=0.0479
				, relwidth=0.07) #relwidth=0.045
		self.volume_ent.configure(background="white")
		self.volume_ent.configure(font="TkFixedFont")
		self.volume_ent.configure(selectbackground="#c4c4c4")
		self.volume_ent.configure(justify='center')
		self.volume_ent.configure(validate="focusout")
		self.volume_ent.configure(textvariable=self.volume)
		self.volume_ent.configure(validatecommand=lambda: self.boil_vol.set(round(float(self.volume.get())*brew_data.constants['Boil Volume Scale'], 2)))
		self.volume_ent.bind('<Return>', lambda event: self.boil_vol.set(round(float(self.volume.get())*brew_data.constants['Boil Volume Scale'], 2)))
		self.volume_ent.insert(0, str(brew_data.constants['Volume']))

		self.boil_volume_lbl = tk.Label(self.first_tab)
		self.boil_volume_lbl.place(relx=0.571, rely=0.021, relheight=0.0375
				, relwidth=0.1062)
		self.boil_volume_lbl.configure(text='''Boil Volume:''')
		self.boil_volume_lbl.configure(background=_bgcolor)

		self.boil_vol = tk.StringVar()
		self.boil_volume_ent = tk.Entry(self.first_tab)
		self.boil_volume_ent.place(relx=0.682, rely=0.021, relheight=0.0479
				, relwidth=0.070)
		self.boil_volume_ent.configure(background="white")
		self.boil_volume_ent.configure(font="TkFixedFont")
		self.boil_volume_ent.configure(width=46)
		self.boil_volume_ent.configure(justify='center')
		self.boil_volume_ent.configure(textvariable=self.boil_vol)
		self.boil_vol.set(str(brew_data.constants['Volume']*brew_data.constants['Boil Volume Scale']))
		
		self.ingredient_rem_butt = tk.Button(self.first_tab)
		self.ingredient_rem_butt.place(relx=0.013, rely=0.402, relheight=0.0604
				, relwidth=0.0950)
		self.ingredient_rem_butt.configure(activebackground="#f9f9f9")
		self.ingredient_rem_butt.configure(background=_bgcolor)
		self.ingredient_rem_butt.configure(cursor="X_cursor")
		self.ingredient_rem_butt.configure(text='''Remove''')
		self.ingredient_rem_butt.configure(command=self.delete_ingredient)

		self.ingredient_add_new_butt = tk.Button(self.first_tab)
		self.ingredient_add_new_butt.place(relx=0.606, rely=0.085, relheight=0.0583
				, relwidth=0.1025)
		self.ingredient_add_new_butt.configure(activebackground="#f9f9f9")
		self.ingredient_add_new_butt.configure(background=_bgcolor)
		self.ingredient_add_new_butt.configure(text='''Add New''')
		self.ingredient_add_new_butt.configure(command=self.add_grist)

		self.adjust_weight_ing_lbl = tk.Label(self.first_tab)
		self.adjust_weight_ing_lbl.place(relx=0.606, rely=0.169, relheight=0.0292
				, relwidth=0.1138)
		self.adjust_weight_ing_lbl.configure(activebackground="#f9f9f9")
		self.adjust_weight_ing_lbl.configure(background=_bgcolor)
		self.adjust_weight_ing_lbl.configure(font=font9)
		self.adjust_weight_ing_lbl.configure(text='''Adjust Weight''')

		self.add_1000g_ing_butt = tk.Button(self.first_tab)
		self.add_1000g_ing_butt.place(relx=0.606, rely=0.211, relheight=0.0583
				, relwidth=0.0563)
		self.add_1000g_ing_butt.configure(activebackground="#f9f9f9")
		self.add_1000g_ing_butt.configure(background=_bgcolor)
		self.add_1000g_ing_butt.configure(text='''+1Kg''')
		self.add_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(1000))
		self.add_1000g_ing_butt.configure(font="TkFixedFont")

		self.add_100g_ing_butt = tk.Button(self.first_tab)
		self.add_100g_ing_butt.place(relx=0.606, rely=0.275, relheight=0.0583
				, relwidth=0.0563)
		self.add_100g_ing_butt.configure(activebackground="#f9f9f9")
		self.add_100g_ing_butt.configure(background=_bgcolor)
		self.add_100g_ing_butt.configure(text='''+100g''')
		self.add_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(100))
		self.add_100g_ing_butt.configure(font="TkFixedFont")

		self.rem_1000g_ing_butt = tk.Button(self.first_tab)
		self.rem_1000g_ing_butt.place(relx=0.669, rely=0.211, relheight=0.0583
				, relwidth=0.0563)
		self.rem_1000g_ing_butt.configure(activebackground="#f9f9f9")
		self.rem_1000g_ing_butt.configure(background=_bgcolor)
		self.rem_1000g_ing_butt.configure(text='''-1Kg''')
		self.rem_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-1000))
		self.rem_1000g_ing_butt.configure(font="TkFixedFont")

		self.rem_100g_ing_butt = tk.Button(self.first_tab)
		self.rem_100g_ing_butt.place(relx=0.669, rely=0.275, relheight=0.0583
				, relwidth=0.0563)
		self.rem_100g_ing_butt.configure(activebackground="#f9f9f9")
		self.rem_100g_ing_butt.configure(background=_bgcolor)
		self.rem_100g_ing_butt.configure(text='''-100g''')
		self.rem_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-100))
		self.rem_100g_ing_butt.configure(font="TkFixedFont")

		self.add_10g_ing_butt = tk.Button(self.first_tab)
		self.add_10g_ing_butt.place(relx=0.606, rely=0.338, relheight=0.0583
				, relwidth=0.0563)
		self.add_10g_ing_butt.configure(activebackground="#f9f9f9")
		self.add_10g_ing_butt.configure(background=_bgcolor)
		self.add_10g_ing_butt.configure(text='''+10g''')
		self.add_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(10))
		self.add_10g_ing_butt.configure(font="TkFixedFont")

		self.rem_10g_ing_butt = tk.Button(self.first_tab)
		self.rem_10g_ing_butt.place(relx=0.669, rely=0.338, relheight=0.0583
				, relwidth=0.0563)
		self.rem_10g_ing_butt.configure(activebackground="#f9f9f9")
		self.rem_10g_ing_butt.configure(background=_bgcolor)
		self.rem_10g_ing_butt.configure(text='''-10g''')
		self.rem_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-10))
		self.rem_10g_ing_butt.configure(font="TkFixedFont")

		self.add_1g_ing_butt = tk.Button(self.first_tab)
		self.add_1g_ing_butt.place(relx=0.606, rely=0.402, relheight=0.0583
				, relwidth=0.0563)
		self.add_1g_ing_butt.configure(activebackground="#f9f9f9")
		self.add_1g_ing_butt.configure(background=_bgcolor)
		self.add_1g_ing_butt.configure(text='''+1g''')
		self.add_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(1))
		self.add_1g_ing_butt.configure(font="TkFixedFont")

		self.rem_1g_ing_butt = tk.Button(self.first_tab)
		self.rem_1g_ing_butt.place(relx=0.669, rely=0.402, relheight=0.0583
				, relwidth=0.0563)
		self.rem_1g_ing_butt.configure(activebackground="#f9f9f9")
		self.rem_1g_ing_butt.configure(background=_bgcolor)
		self.rem_1g_ing_butt.configure(text='''-1g''')
		self.rem_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-1))
		self.rem_1g_ing_butt.configure(font="TkFixedFont")

		self.original_gravity_lbl = tk.Label(self.first_tab)
		self.original_gravity_lbl.place(relx=0.72, rely=0.085, relheight=0.0292
				, relwidth=0.0988)
		self.original_gravity_lbl.configure(activebackground="#f9f9f9")
		self.original_gravity_lbl.configure(background=_bgcolor)
		self.original_gravity_lbl.configure(font=font9)
		self.original_gravity_lbl.configure(text='''Original Gravity''')

		self.original_gravity_ent = tk.Entry(self.first_tab)
		self.original_gravity_ent.place(relx=0.745, rely=0.127, relheight=0.0417
				, relwidth=0.07)
		self.original_gravity_ent.configure(background="white")
		self.original_gravity_ent.configure(font="TkFixedFont")
		self.original_gravity_ent.configure(selectbackground="#c4c4c4")
		self.original_gravity_ent.configure(justify='center')
		self.ingredient_zero_butt = tk.Button(self.first_tab)
		self.ingredient_zero_butt.place(relx=0.745, rely=0.211, relheight=0.0604
				, relwidth=0.0688)
		self.ingredient_zero_butt.configure(activebackground="#f9f9f9")
		self.ingredient_zero_butt.configure(background=_bgcolor)
		self.ingredient_zero_butt.configure(text='''Zero''')
		self.ingredient_zero_butt.configure(command=self.zero_ingredients)

		self.recalc_butt = tk.Button(self.first_tab)
		self.recalc_butt.place(relx=0.859, rely=0.042, relheight=0.0604
				, relwidth=0.1213)
		self.recalc_butt.configure(activebackground="#f9f9f9")
		self.recalc_butt.configure(background=_bgcolor)
		self.recalc_butt.configure(text='''Recalculate''')
		self.recalc_butt.configure(command=self.recalculate)

		self.calculation_frame = ttk.Labelframe(self.first_tab)
		self.calculation_frame.place(relx=0.833, rely=0.106, relheight=0.391
				, relwidth=0.152)
		self.calculation_frame.configure(relief='sunken')
		self.calculation_frame.configure(text='''Calculation''')
		self.calculation_frame.configure(underline="0")
		self.calculation_frame.configure(relief='sunken')
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
		self.calc_lbl.grid(row=0, column=0)
		self.calc_lbl.configure(background=_bgcolor)
		self.calc_lbl.configure(foreground="#000000")
		self.calc_lbl.configure(font=(None, 7))
		self.calc_lbl.configure(relief='flat', wrap=tk.WORD)
		#self.calc_lbl.configure(anchor='nw')
		default_text = '''Efficiency: {efficiency}%{enter}Final Gravity: {final_gravity}{enter}Alcohol (ABV): {abv}{enter}Colour: {colour}EBC{enter}Mash Liquor: {mash_liquor}L{enter}IBU:GU: {ibu_gu}'''.format(efficiency=brew_data.constants['Efficiency']*100, final_gravity=1.000, abv=0, colour=0, mash_liquor=0, ibu_gu=0, enter='\n\n')

		self.calc_lbl.insert('end', default_text)
		self.calc_lbl.configure(state='disabled')
		#self.calc_lbl.configure(width=97)

		self.hop_add_new_butt = tk.Button(self.first_tab)
		self.hop_add_new_butt.place(relx=0.707, rely=0.507, relheight=0.0604
				, relwidth=0.1000)
		self.hop_add_new_butt.configure(activebackground="#f9f9f9")
		self.hop_add_new_butt.configure(background=_bgcolor)
		self.hop_add_new_butt.configure(text='''Add Hop''')
		self.hop_add_new_butt.configure(command=self.add_hop)

		self.adjust_weight_hop_lbl = tk.Label(self.first_tab)
		self.adjust_weight_hop_lbl.place(relx=0.72, rely=0.592, relheight=0.0292
				, relwidth=0.1138)
		self.adjust_weight_hop_lbl.configure(activebackground="#f9f9f9")
		self.adjust_weight_hop_lbl.configure(background=_bgcolor)
		self.adjust_weight_hop_lbl.configure(font=font9)
		self.adjust_weight_hop_lbl.configure(text='''Adjust Weight''')

		self.add_100g_hop_butt = tk.Button(self.first_tab)
		self.add_100g_hop_butt.place(relx=0.72, rely=0.634, relheight=0.0583
				, relwidth=0.0563)
		self.add_100g_hop_butt.configure(activebackground="#f9f9f9")
		self.add_100g_hop_butt.configure(background=_bgcolor)
		self.add_100g_hop_butt.configure(text='''+100g''')
		self.add_100g_hop_butt.configure(command=lambda: self.add_weight_hops(100))
		self.add_100g_hop_butt.configure(font="TkFixedFont")

		self.rem_100g_hop_butt = tk.Button(self.first_tab)
		self.rem_100g_hop_butt.place(relx=0.783, rely=0.634, relheight=0.0583
				, relwidth=0.0563)
		self.rem_100g_hop_butt.configure(activebackground="#f9f9f9")
		self.rem_100g_hop_butt.configure(background=_bgcolor)
		self.rem_100g_hop_butt.configure(text='''-100g''')
		self.rem_100g_hop_butt.configure(command=lambda: self.add_weight_hops(-100))
		self.rem_100g_hop_butt.configure(font="TkFixedFont")

		self.add_25g_hop_butt = tk.Button(self.first_tab)
		self.add_25g_hop_butt.place(relx=0.72, rely=0.698, relheight=0.0583
				, relwidth=0.0563)
		self.add_25g_hop_butt.configure(activebackground="#f9f9f9")
		self.add_25g_hop_butt.configure(background=_bgcolor)
		self.add_25g_hop_butt.configure(text='''+25g''')
		self.add_25g_hop_butt.configure(command=lambda: self.add_weight_hops(25))
		self.add_25g_hop_butt.configure(font="TkFixedFont")

		self.rem_25g_hop_butt = tk.Button(self.first_tab)
		self.rem_25g_hop_butt.place(relx=0.783, rely=0.698, relheight=0.0583
				, relwidth=0.0563)
		self.rem_25g_hop_butt.configure(activebackground="#f9f9f9")
		self.rem_25g_hop_butt.configure(background=_bgcolor)
		self.rem_25g_hop_butt.configure(text='''-25g''')
		self.rem_25g_hop_butt.configure(command=lambda: self.add_weight_hops(-25))
		self.rem_25g_hop_butt.configure(font="TkFixedFont")

		self.add_10g_hop_butt = tk.Button(self.first_tab)
		self.add_10g_hop_butt.place(relx=0.72, rely=0.761, relheight=0.0583
				, relwidth=0.0563)
		self.add_10g_hop_butt.configure(activebackground="#f9f9f9")
		self.add_10g_hop_butt.configure(background=_bgcolor)
		self.add_10g_hop_butt.configure(text='''+10g''')
		self.add_10g_hop_butt.configure(command=lambda: self.add_weight_hops(10))
		self.add_10g_hop_butt.configure(font="TkFixedFont")

		self.rem_10g_hop_butt = tk.Button(self.first_tab)
		self.rem_10g_hop_butt.place(relx=0.783, rely=0.761, relheight=0.0583
				, relwidth=0.0563)
		self.rem_10g_hop_butt.configure(activebackground="#f9f9f9")
		self.rem_10g_hop_butt.configure(background=_bgcolor)
		self.rem_10g_hop_butt.configure(text='''-10g''')
		self.rem_10g_hop_butt.configure(command=lambda: self.add_weight_hops(-10))
		self.rem_10g_hop_butt.configure(font="TkFixedFont")

		self.add_1g_hop_butt = tk.Button(self.first_tab)
		self.add_1g_hop_butt.place(relx=0.72, rely=0.825, relheight=0.0583
				, relwidth=0.0563)
		self.add_1g_hop_butt.configure(activebackground="#f9f9f9")
		self.add_1g_hop_butt.configure(background=_bgcolor)
		self.add_1g_hop_butt.configure(text='''+1g''')
		self.add_1g_hop_butt.configure(command=lambda: self.add_weight_hops(1))
		self.add_1g_hop_butt.configure(font="TkFixedFont")

		self.rem_1g_hop_butt = tk.Button(self.first_tab)
		self.rem_1g_hop_butt.place(relx=0.783, rely=0.825, relheight=0.0583
				, relwidth=0.0563)
		self.rem_1g_hop_butt.configure(activebackground="#f9f9f9")
		self.rem_1g_hop_butt.configure(background=_bgcolor)
		self.rem_1g_hop_butt.configure(text='''-1g''')
		self.rem_1g_hop_butt.configure(command=lambda: self.add_weight_hops(-1))
		self.rem_1g_hop_butt.configure(font="TkFixedFont")

		self.hop_zero_butt = tk.Button(self.first_tab)
		self.hop_zero_butt.place(relx=0.859, rely=0.634, relheight=0.0583
				, relwidth=0.0688)
		self.hop_zero_butt.configure(activebackground="#f9f9f9")
		self.hop_zero_butt.configure(background=_bgcolor)
		self.hop_zero_butt.configure(text='''Zero''')
		self.hop_zero_butt.configure(command=self.zero_hops)

		self.bitterness_ibu_lbl = tk.Label(self.first_tab)
		self.bitterness_ibu_lbl.place(relx=0.846, rely=0.507, relheight=0.0583
				, relwidth=0.0950)
		self.bitterness_ibu_lbl.configure(activebackground="#f9f9f9")
		self.bitterness_ibu_lbl.configure(background=_bgcolor)
		self.bitterness_ibu_lbl.configure(font=font9)
		self.bitterness_ibu_lbl.configure(text='''Bitterness IBU''')

		self.bitterness_ibu_ent = tk.Entry(self.first_tab)
		self.bitterness_ibu_ent.place(relx=0.859, rely=0.55, relheight=0.0417
				, relwidth=0.0580)
		self.bitterness_ibu_ent.configure(background="white")
		self.bitterness_ibu_ent.configure(font="TkFixedFont")
		self.bitterness_ibu_ent.configure(selectbackground="#c4c4c4")
		self.bitterness_ibu_ent.configure(justify='center')

		self.hop_rem_butt = tk.Button(self.first_tab)
		self.hop_rem_butt.place(relx=0.013, rely=0.825, relheight=0.0583
				, relwidth=0.0950)
		self.hop_rem_butt.configure(activebackground="#f9f9f9")
		self.hop_rem_butt.configure(background=_bgcolor)
		self.hop_rem_butt.configure(cursor="X_cursor")
		self.hop_rem_butt.configure(text='''Remove''')
		self.hop_rem_butt.configure(command=self.delete_hop)

		self.quit_btt = tk.Button(self.first_tab)
		self.quit_btt.place(relx=0.922, rely=0.93, relheight=0.0604
				, relwidth=0.0663)
		self.quit_btt.configure(activebackground="#f9f9f9")
		self.quit_btt.configure(background=_bgcolor)
		self.quit_btt.configure(text='''Quit''')
		self.quit_btt.configure(command=self.quit)

		self.add_time_butt_1 = tk.Button(self.first_tab)
		self.add_time_butt_1.place(relx=0.426, rely=0.825, relheight=0.0583
				, relwidth=0.0975)
		self.add_time_butt_1.configure(activebackground="#f9f9f9")
		self.add_time_butt_1.configure(background=_bgcolor)
		self.add_time_butt_1.configure(text='''Time +1''')
		self.add_time_butt_1.configure(command=lambda: self.add_time(1))

		self.rem_time_butt_1 = tk.Button(self.first_tab)
		self.rem_time_butt_1.place(relx=0.426, rely=0.888, relheight=0.0583
				, relwidth=0.0975)
		self.rem_time_butt_1.configure(activebackground="#f9f9f9")
		self.rem_time_butt_1.configure(background=_bgcolor)
		self.rem_time_butt_1.configure(text='''Time -1''')
		self.rem_time_butt_1.configure(command=lambda: self.add_time(-1))

		self.add_time_butt_10 = tk.Button(self.first_tab)
		self.add_time_butt_10.place(relx=0.328, rely=0.825, relheight=0.0583
				, relwidth=0.0975)
		self.add_time_butt_10.configure(activebackground="#f9f9f9")
		self.add_time_butt_10.configure(background=_bgcolor)
		self.add_time_butt_10.configure(text='''Time +10''')
		self.add_time_butt_10.configure(command=lambda: self.add_time(10))

		self.rem_time_butt_10 = tk.Button(self.first_tab)
		self.rem_time_butt_10.place(relx=0.328, rely=0.888, relheight=0.0583
				, relwidth=0.0975)
		self.rem_time_butt_10.configure(activebackground="#f9f9f9")
		self.rem_time_butt_10.configure(background=_bgcolor)
		self.rem_time_butt_10.configure(text='''Time -10''')
		self.rem_time_butt_10.configure(command=lambda: self.add_time(-10))

		self.add_alpha_butt_pt1 = tk.Button(self.first_tab)
		self.add_alpha_butt_pt1.place(relx=0.129, rely=0.825, relheight=0.0583
				, relwidth=0.0975)
		self.add_alpha_butt_pt1.configure(activebackground="#f9f9f9")
		self.add_alpha_butt_pt1.configure(background=_bgcolor)
		self.add_alpha_butt_pt1.configure(text='''Alpha +0.1''')
		self.add_alpha_butt_pt1.configure(command=lambda: self.add_alpha(0.1))

		self.rem_alpha_butt_pt1 = tk.Button(self.first_tab)
		self.rem_alpha_butt_pt1.place(relx=0.129, rely=0.888, relheight=0.0583
				, relwidth=0.0975)
		self.rem_alpha_butt_pt1.configure(activebackground="#f9f9f9")
		self.rem_alpha_butt_pt1.configure(background=_bgcolor)
		self.rem_alpha_butt_pt1.configure(text='''Alpha -0.1''')
		self.rem_alpha_butt_pt1.configure(command=lambda: self.add_alpha(-0.1))

		self.add_alpha_butt_1 = tk.Button(self.first_tab)
		self.add_alpha_butt_1.place(relx=0.227, rely=0.825, relheight=0.0583
				, relwidth=0.0975)
		self.add_alpha_butt_1.configure(activebackground="#f9f9f9")
		self.add_alpha_butt_1.configure(background=_bgcolor)
		self.add_alpha_butt_1.configure(text='''Alpha +1''')
		self.add_alpha_butt_1.configure(width=76)
		self.add_alpha_butt_1.configure(command=lambda: self.add_alpha(1))

		self.rem_alpha_butt_1 = tk.Button(self.first_tab)
		self.rem_alpha_butt_1.place(relx=0.227, rely=0.888, relheight=0.0583
				, relwidth=0.0975)
		self.rem_alpha_butt_1.configure(activebackground="#f9f9f9")
		self.rem_alpha_butt_1.configure(background=_bgcolor)
		self.rem_alpha_butt_1.configure(text='''Alpha -1''')
		self.rem_alpha_butt_1.configure(command=lambda: self.add_alpha(-1))

		self.style.configure('Treeview.Heading',  font="TkDefaultFont")
		self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Deja Vu Sans Mono', 9)) #Calibri
		self.frame_ingredients = tk.Frame(self.first_tab)
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
		self.ingredients_imperial_chk_butt.configure(text='''Imperial Units''')
		self.ingredients_imperial_chk_butt.configure(background=_bgcolor)
		self.ingredients_imperial_chk_butt.configure(command=self.ingredient_to_imperial)
		self.ingredients_imperial_chk_butt.configure(variable=self.is_imperial_ingredient)

		self.hops_imperial_chk_butt = tk.Checkbutton(self.first_tab)
		self.hops_imperial_chk_butt.place(relx=0.53, rely=0.825, relheight=0.044
			, relwidth=0.149)
		self.is_imperial_hop = tk.IntVar()
		self.hops_imperial_chk_butt.configure(text='''Imperial Units''')
		self.hops_imperial_chk_butt.configure(background=_bgcolor)
		self.hops_imperial_chk_butt.configure(command=self.hop_to_imperial)
		self.hops_imperial_chk_butt.configure(variable=self.is_imperial_hop)

		self.ogfixed_chkbutton = tk.Checkbutton(self.first_tab)
		self.is_ogfixed = tk.IntVar()
		self.ogfixed_chkbutton.place(relx=0.71, rely=0.127, relheight=0.044
				, relwidth=0.033)
		self.ogfixed_chkbutton.configure(activebackground="#f9f9f9")
		self.ogfixed_chkbutton.configure(background=_bgcolor)
		self.ogfixed_chkbutton.configure(justify='left')
		self.ogfixed_chkbutton.configure(variable=self.is_ogfixed)
		self.ogfixed_chkbutton.configure(command=self.og_fixed)

		self.ebufixed_chkbutton = tk.Checkbutton(self.first_tab)
		self.is_ebufixed = tk.IntVar()
		self.ebufixed_chkbutton.place(relx=0.821, rely=0.55, relheight=0.044
				, relwidth=0.033)
		self.ebufixed_chkbutton.configure(activebackground="#f9f9f9")
		self.ebufixed_chkbutton.configure(background=_bgcolor)
		self.ebufixed_chkbutton.configure(justify='left')
		self.ebufixed_chkbutton.configure(variable=self.is_ebufixed)
		self.ebufixed_chkbutton.configure(command=self.ebu_fixed)

		self.refresh_grist()
		self.refresh_hop()
		#self.tabbed_frame.bind('<Button-1>', lambda event: self.refresh_all() if self.tabbed_frame.tk.call(self.tabbed_frame._w, "identify", "tab", event.x, event.y) == 1 else False) # print(self.tabbed_frame.tk.call(self.tabbed_frame._w, "identify", "tab", event.x, event.y))
		self.tabbed_frame.bind('<Button-1>', self.refresh_tab_onclick)

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
		tab = self.tabbed_frame.tk.call(self.tabbed_frame._w, "identify", "tab", event.x, event.y)
		print(tab, type(tab))
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
			if 'scrolled_tree_ingredient' in vars(self):
				self.scrolled_tree_ingredient.delete(*self.scrolled_tree_ingredient.get_children())
			else:
				self.scrolled_tree_ingredient = ScrolledTreeView(self.frame_ingredients, style="mystyle.Treeview")
				self.scrolled_tree_ingredient.grid(row=0,column=0, sticky='nsew')
				self.ingredient_columns = ("Ebc", "Grav", "lb:oz", "Grams", "%")
				self.scrolled_tree_ingredient.configure(columns=self.ingredient_columns)
				self.scrolled_tree_ingredient.heading("#0",text="Fermentable Ingredient", command=lambda c="Fermentable Ingredient": self.sort_by_grist(c))
				self.scrolled_tree_ingredient.column("#0",width="170",minwidth="20",stretch="1")
				for column in self.ingredient_columns:
					self.scrolled_tree_ingredient.heading(column, text=column, command=lambda c=column: self.sort_by_grist(c))
					self.scrolled_tree_ingredient.column(column, anchor="center")
					if column != 'lb:oz' and column != '%' and column != 'EBC':
						self.scrolled_tree_ingredient.column(column, width=40)
					elif column == 'lb:oz':
						if len(self.ingredients) > 0:
							self.scrolled_tree_ingredient.column('lb:oz', width=max([len('{lb}:{oz}'.format(lb=int(ingredient['Values']['lb:oz'][0]), oz=round(ingredient['Values']['lb:oz'][1], 1))) for ingredient in self.ingredients])*7)
						else:
							self.scrolled_tree_ingredient.column(column, width=40)
					elif column == 'EBC':
						self.scrolled_tree_ingredient.column(column, width=28)
					elif column == '%':
						self.scrolled_tree_ingredient.column(column, width=35)

		def refresh_percentage():
			total_weight = sum([ingredient['Values']['Grams'] for ingredient in self.ingredients])
			if total_weight > 0:
				for ingredient in self.ingredients:
					weight = ingredient['Values']['Grams']
					percentage = round((weight/total_weight)*100, 1)
					ingredient['Values']['Percent'] = percentage

		def refresh_orig_grav():
			non_mashables = [6.0, 5.0]
			volume = float(self.volume.get())
			points = sum([(brew_data.grist_data[ingredient['Name']]['Extract']*(ingredient['Values']['Grams'])/1000) * (1 if brew_data.grist_data[ingredient['Name']]['Type'] in non_mashables else brew_data.constants['Efficiency']) for ingredient in self.ingredients])

			orig_grav = ((points)/volume)+1000
			self.og = orig_grav
			self.original_gravity_ent.delete(0, tk.END)
			self.original_gravity_ent.insert(0, round(orig_grav, 1))

		def refresh_indiv_grav():
			non_mashables = [6.0, 5.0]
			volume = float(self.volume.get())
			for ingredient in self.ingredients:
				points = brew_data.grist_data[ingredient['Name']]['Extract']*(ingredient['Values']['Grams'])/1000
				eff = (1 if brew_data.grist_data[ingredient['Name']]['Type'] in non_mashables else brew_data.constants['Efficiency'])
				grav = ((points * eff)/volume)
				ingredient['Values']['Grav'] = grav
				#print(grav)

		make_treeview()
		if not self.is_ogfixed.get():
			refresh_orig_grav()
			refresh_percentage()
		else:
			non_mashables = [6.0, 5.0]
			factor = sum([ingredient['Values']['Percent']*brew_data.grist_data[ingredient['Name']]['Extract']*(1 if brew_data.grist_data[ingredient['Name']]['Type'] in non_mashables else brew_data.constants['Efficiency']) for idx, ingredient in enumerate(self.ingredients)])

			for idx, ingredient in enumerate(self.ingredients):
				EBC = int(brew_data.grist_data[ingredient['Name']]['EBC'])
				percent = ingredient['Values']['Percent']
				orig_grav = float(self.original_gravity_ent.get())-1000
				vol = float(self.volume.get())
				try:
					weight = percent*((orig_grav*vol)/factor)*1000
				except:
					weight = 0
				lb = weight/brew_data.constants['Conversion']['lb-g']
				oz = (lb-int(lb))*16
				self.ingredients[idx] = {'Name': ingredient['Name'], 'Values': {'EBC': EBC, 'Grav': 0.0, 'lb:oz': (lb,oz), 'Grams': weight, 'Percent': percent}}
			refresh_percentage()

		refresh_indiv_grav()
		for ingredient in self.ingredients:
			values = (ingredient['Values']['EBC'], round(ingredient['Values']['Grav'], 1), '{lb}:{oz}'.format(lb=int(ingredient['Values']['lb:oz'][0]), oz=round(ingredient['Values']['lb:oz'][1], 1)), round(ingredient['Values']['Grams'], 1), ingredient['Values']['Percent'])
			self.scrolled_tree_ingredient.insert('', 'end', text=ingredient['Name'], values=values)

	def refresh_hop(self):
		def make_treeview():
			if 'scrolled_tree_hops' in vars(self):
				self.scrolled_tree_hops.delete(*self.scrolled_tree_hops.get_children())
			else:
				self.scrolled_tree_hops = ScrolledTreeView(self.frame_hops, style="mystyle.Treeview")
				self.scrolled_tree_hops.grid(row=0, column=0, sticky='nsew')
				self.hop_columns = ("Type", "Alpha", "Time", "% Util", "IBU", "lb:oz", "Grams", "%")
				self.scrolled_tree_hops.configure(columns=self.hop_columns)
				self.scrolled_tree_hops.heading("#0",text="Hop Variety", command=lambda: self.sort_by_hop("Hop Variety"))
				self.scrolled_tree_hops.column("#0",width="90", anchor="w",minwidth="20",stretch="1")

				for column in self.hop_columns:
					self.scrolled_tree_hops.heading(column, text=column, command=lambda column=column: self.sort_by_hop(column))
					if column != 'lb:oz' and column != '%':
						self.scrolled_tree_hops.column(column, width=40, anchor="center")
					elif column == 'lb:oz':
						if len(self.hops) > 0:
							self.scrolled_tree_hops.column(column, width=max([len('{lb}:{oz}'.format(lb=int(hop['Values']['lb:oz'][0]), oz=round(hop['Values']['lb:oz'][1], 1))) for hop in self.hops])*7, anchor="center")
						else:
							self.scrolled_tree_hops.column(column, width=40, anchor="center")
					elif column == '%' or column == '% Util':
						self.scrolled_tree_hops.column(column, width=35, anchor="center")

		def refresh_percentage():
			total_weight = sum([hop['Values']['Grams'] for hop in self.hops])
			if total_weight > 0:
				for hop in self.hops:
					weight = hop['Values']['Grams']
					percentage = round((weight/total_weight)*100, 1)
					hop['Values']['Percent'] = percentage

		def refresh_util():
			def boil_grav():
				volume = float(self.boil_vol.get())
				points = sum([brew_data.grist_data[ingredient['Name']]['Extract']*(ingredient['Values']['Grams'])/1000 for ingredient in self.ingredients])
				boil_grav = ((points * brew_data.constants['Efficiency'])/volume)+1000
				return boil_grav
			'''
			Utilization = f(G) x f(T)
			f(G) = 1.65 x 0.000125^(Gb - 1)
			f(T) = [1 - e^(-0.04 x T)] / 4.15
			Where Gb is boil gravity and T is time
			'''
			for hop in self.hops:
				boil_gravity = boil_grav()/1000 # Temporary Solution
				time = hop['Values']['Time']
				fG = 1.65 * (0.000125**(boil_gravity - 1))
				fT = (1 - math.e**(-0.04 * time)) / 4.15
				hop['Values']['Util'] = (fG * fT)*100

		def refresh_ibu():
			'''
			IBU    =    grams x alpha acid x utilisation rate
				   -------------------------------------------------
									 Volume x 10
			'''
			ibu = sum([(hop['Values']['Grams'] * hop['Values']['Alpha'] * hop['Values']['Util']) / (float(self.boil_vol.get())*10)  for hop in self.hops])
			ibu = (ibu*float(self.boil_vol.get()))/float(self.volume.get())
			self.ibu = ibu
			self.bitterness_ibu_ent.delete(0, tk.END)
			self.bitterness_ibu_ent.insert(0, round(ibu))

		def refresh_indiv_ibu():
			for hop in self.hops:
				ibu = (hop['Values']['Grams'] * hop['Values']['Alpha'] * hop['Values']['Util']) / (float(self.boil_vol.get())*10)
				hop['Values']['ibu'] = ibu



		make_treeview()
		if not self.is_ebufixed.get():
			refresh_percentage()
			refresh_ibu()
		else:
			factor = sum([hop['Values']['Percent']*hop['Values']['Alpha']*hop['Values']['Util'] for idx, hop in enumerate(self.hops)])

			for idx, hop in enumerate(self.hops):
				percent = hop['Values']['Percent']

				alpha =  hop['Values']['Alpha']
				type = brew_data.hop_data[hop['Name']]['Form']
				util = hop['Values']['Util']
				time = hop['Values']['Time']
				if util > 0 and alpha > 0:
					total_ibus = float(self.bitterness_ibu_ent.get())
					vol = float(self.volume.get())
					try:
						weight = percent*((total_ibus*vol*10)/factor) #(((total_ibus*(percent/100))*(vol*10))/util)/alpha
					except:
						weight = 0
					lb = weight/brew_data.constants['Conversion']['lb-g']
					oz = (lb-int(lb))*16
					self.hops[idx] = {'Name': hop['Name'], 'Values': {'Type': type, 'Alpha': alpha, 'Time': time, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (lb, oz), 'Grams': weight, 'Percent': percent}}
			refresh_percentage()
		refresh_util()
		refresh_indiv_ibu()
		for hop in self.hops:
			values = (hop['Values']['Type'], hop['Values']['Alpha'], hop['Values']['Time'], round(hop['Values']['Util'], 1), round(hop['Values']['ibu']),'{lb}:{oz}'.format(lb=int(hop['Values']['lb:oz'][0]), oz=round(hop['Values']['lb:oz'][1], 1)), round(hop['Values']['Grams'], 1), hop['Values']['Percent'])
			self.scrolled_tree_hops.insert('', 'end', text=hop['Name'], values=values)

	def refresh_all(self):
		self.refresh_hop()
		self.refresh_grist()
		self.recalculate()

	def add_grist(self):
		def insert():
			name = grist_options.item(grist_options.focus())['text']
			EBC = int(brew_data.grist_data[name]['EBC'])
			self.ingredients.append({'Name': name, 'Values': {'EBC': EBC, 'Grav': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0, 'Percent': 0.0}})
			self.refresh_grist()

		def bound(event, treeview, list_data): #https://mail.python.org/pipermail/python-list/2002-May/170135.html ADDED TREEVIEW functionality
			key=event.keysym
			if key == 'Escape':
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
					for n in range(start_n+1, len(list_data)):
						item=list_data[n]
						if item[0].lower()==key.lower():
							treeview.selection_set('I{iid}'.format(iid=format(n+1, '03x')))
							treeview.focus('I{iid}'.format(iid=format(n+1, '03x')))
							treeview.yview(n)
							return
						treeview.yview(n)
					else:
						# has not found it so loop from top
						for n in range(len(list_data)):
							item=list_data[n]
							if item[0].lower()==key.lower():
								treeview.yview(n)
								treeview.selection_set('I{iid}'.format(iid=format(n+1, '03x')))
								treeview.focus('I{iid}'.format(iid=format(n+1, '03x')))
								return
						treeview.yview(n)

		add_grist_gui = tk.Toplevel()
		add_grist_gui.resizable(0, 0)
		grist_options = ScrolledTreeView(add_grist_gui, show="tree", columns=("EBC"))
		grist_options.column(column="EBC",width=80)
		grist_options.grid(row=1,column=0)
		for grist in sorted(brew_data.grist_data):
			ebc = str(brew_data.grist_data[grist]['EBC']) + ' EBC'
			grist_options.insert('', tk.END, text=(grist), values=(ebc,))
		grist_add_new = tk.Button(add_grist_gui, text='Add New', command = insert)
		grist_add_new.grid(row=1,column=1)
		add_grist_gui.bind('<Any-Key>', lambda evt: bound(evt, grist_options, sorted(brew_data.grist_data)))
		add_grist_gui.mainloop()

	def add_hop(self):
		def insert():
			name = hop_options.item(hop_options.focus())['text']
			alpha =  brew_data.hop_data[name]['Alpha']
			type = brew_data.hop_data[name]['Form']
			time = brew_data.constants['Hop Time']
			self.hops.append({'Name': name, 'Values': {'Type': type, 'Alpha': alpha, 'Time': time, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0, 'Percent': 0.0}})
			self.refresh_hop()
		def bound(event, treeview, list_data): #https://mail.python.org/pipermail/python-list/2002-May/170135.html
			key=event.keysym
			if key == 'Escape':
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
					for n in range(start_n+1, len(list_data)):
						item=list_data[n]
						if item[0].lower()==key.lower():
							treeview.selection_set('I{iid}'.format(iid=format(n+1, '03x')))
							treeview.focus('I{iid}'.format(iid=format(n+1, '03x')))
							treeview.yview(n)
							return
						treeview.yview(n)
					else:
						# has not found it so loop from top
						for n in range(len(list_data)):
							item=list_data[n]
							if item[0].lower()==key.lower():
								treeview.yview(n)
								treeview.selection_set('I{iid}'.format(iid=format(n+1, '03x')))
								treeview.focus('I{iid}'.format(iid=format(n+1, '03x')))
								return
						treeview.yview(n)
		add_hop_gui = tk.Toplevel()
		add_hop_gui.resizable(0, 0)
		hop_options = ScrolledTreeView(add_hop_gui, show="tree", columns=("Form"))
		hop_options.column(column="Form",width=80)
		hop_options.grid(row=1, column=0)
		for hop in sorted(brew_data.hop_data):
			hop_options.insert('',tk.END, text=(hop), values=(brew_data.hop_data[hop]['Form'],))
		hop_add_new = tk.Button(add_hop_gui, text='Add New', command = insert)
		hop_add_new.grid(row=1,column=1)
		add_hop_gui.bind('<Any-Key>', lambda evt: bound(evt, hop_options, sorted(brew_data.hop_data)))
		add_hop_gui.mainloop()

	def add_weight_ingredients(self, weight): # Selected Item
		try:
			selection = self.scrolled_tree_ingredient.selection()[0]
			id = int(str(selection)[1:], 16)
			#print(id, selection)
			grams = self.ingredients[id-1]['Values']['Grams']+weight
			if grams < 0: grams=0
			lb = grams/brew_data.constants['Conversion']['lb-g']
			oz = (lb-int(lb))*16
			self.ingredients[id-1]['Values']['Grams'] = grams
			self.ingredients[id-1]['Values']['lb:oz'] = (lb, oz)
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
			id = int(str(selection)[1:], 16)
			grams = self.hops[id-1]['Values']['Grams']+weight
			if grams < 0: grams=0
			lb = grams/brew_data.constants['Conversion']['lb-g']
			oz = (lb-int(lb))*16
			self.hops[id-1]['Values']['Grams'] = grams
			self.hops[id-1]['Values']['lb:oz'] = (lb, oz)
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
			id = int(str(selection)[1:], 16)
			EBC = int(brew_data.grist_data[self.ingredients[id-1]['Name']]['EBC'])
			self.ingredients[id-1] = {'Name': self.ingredients[id-1]['Name'], 'Values': {'EBC': EBC, 'Grav': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0, 'Percent': 0.0}}
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
			id = int(str(selection)[1:], 16)
			alpha =  brew_data.hop_data[self.hops[id-1]['Name']]['Alpha']
			type = brew_data.hop_data[self.hops[id-1]['Name']]['Form']
			self.hops[id-1] = {'Name': self.hops[id-1]['Name'], 'Values': {'Type': type, 'Alpha': alpha, 'Time': 0.0, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0, 'Percent': 0.0}}
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
			id = int(str(selection)[1:], 16)
			del self.ingredients[id-1]
			self.refresh_grist()
			self.recalculate()
		except IndexError:
			pass

	def delete_hop(self):
		try:
			selection = self.scrolled_tree_hops.selection()[0]
			id = int(str(selection)[1:], 16)
			del self.hops[id-1]
			self.refresh_hop()
			self.recalculate()
		except IndexError:
			pass
	def add_time(self, time):
		try:
			selection = self.scrolled_tree_hops.selection()[0]
			id = int(str(selection)[1:], 16)
			time = round(self.hops[id-1]['Values']['Time']+time,1)
			if time < 0: time = 0
			self.hops[id-1]['Values']['Time'] = time
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
			id = int(str(selection)[1:], 16)
			alpha = round(self.hops[id-1]['Values']['Alpha']+alpha, 1)
			if alpha < 0: alpha = 0
			self.hops[id-1]['Values']['Alpha'] = alpha
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
			a = sum([((self.attenuation_apply(ingredient)/100)*((ingredient['Values']['Grams']/1000) * brew_data.grist_data[ingredient['Name']]['Extract'])) * (1 if brew_data.grist_data[ingredient['Name']]['Type'] in non_mashables else brew_data.constants['Efficiency']) for ingredient in self.ingredients])
			b = sum([(((100 - self.attenuation_apply(ingredient))/100)*((ingredient['Values']['Grams']/1000) * brew_data.grist_data[ingredient['Name']]['Extract'])) * (1 if brew_data.grist_data[ingredient['Name']]['Type'] in non_mashables else brew_data.constants['Efficiency']) for ingredient in self.ingredients])
			return ((b-(a*0.225))/float(self.volume.get()))+1000
		def alcohol_by_volume(og, fg):
			#return (1.05/0.79) * ((og - fg) / fg) *100
			return (((1.05*(og-fg))/fg/0.79))*100
		def mash_liquor():
			non_mashables = [6.0, 5.0] # ["Copper Sugar", "Malt Extract"]
			grist_mass = sum([0 if brew_data.grist_data[ingredient['Name']]['Type'] in non_mashables else ingredient['Values']['Grams'] for ingredient in self.ingredients])/1000
			return grist_mass*brew_data.constants['Liquor To Grist Ratio']
		def colour_ebc():
			# [{'Name:': 'Wheat Flour', 'Values': {'EBC:': 0.0, 'Grav': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}}]
			def formula(ingredient, efficiency):
				ebc = ingredient['Values']['EBC']
				mass = ingredient['Values']['Grams']/1000
				volume = float(self.volume.get())
				return (ebc*mass*efficiency*10)/volume

			non_mashables = [6.0, 5.0] # Not effected by efficiency  ["Copper Sugar", "Malt Extract"]
			return (sum([formula(ingredient, 1) if brew_data.grist_data[ingredient['Name']]['Type'] in non_mashables else formula(ingredient, brew_data.constants['Efficiency']) for ingredient in self.ingredients]))

		'''
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
		self.calc_lbl.configure(state='normal')
		self.calc_lbl.delete('1.0', 'end')
		self.calc_lbl.insert('end', '''Efficiency: {efficiency}%{enter}Final Gravity: {final_gravity}{enter}Alcohol (ABV): {abv}{enter}Colour: {colour}EBC{enter}Mash Liquor: {mash_liquor}L{enter}IBU:GU: {ibu_gu}'''.format(
			efficiency=round(brew_data.constants['Efficiency']*100, 13), final_gravity=round(self.fg, 1),
			abv=round(self.abv, 1), colour=round(self.colour,1), mash_liquor=round(mash_liquor(),1),
			ibu_gu=round(self.ibu_gu, 2), enter='\n\n'))
		self.calc_lbl.configure(state='disabled')
		self.refresh_hop()
		self.refresh_grist()

	def ingredient_to_imperial(self):
		if self.is_imperial_ingredient.get() == 0:
			self.add_1000g_ing_butt.configure(text='''+1Kg''')
			self.add_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(1000))
			self.add_1000g_ing_butt.configure(font="TkFixedFont")

			self.add_100g_ing_butt.configure(text='''+100g''')
			self.add_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(100))
			self.add_100g_ing_butt.configure(font="TkFixedFont")

			self.rem_1000g_ing_butt.configure(text='''-1Kg''')
			self.rem_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-1000))
			self.rem_1000g_ing_butt.configure(font="TkFixedFont")

			self.rem_100g_ing_butt.configure(text='''-100g''')
			self.rem_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-100))
			self.rem_100g_ing_butt.configure(font="TkFixedFont")

			self.add_10g_ing_butt.configure(text='''+10g''')
			self.add_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(10))
			self.add_10g_ing_butt.configure(font="TkFixedFont")

			self.rem_10g_ing_butt.configure(text='''-10g''')
			self.rem_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-10))
			self.rem_10g_ing_butt.configure(font="TkFixedFont")

			self.add_1g_ing_butt.configure(text='''+1g''')
			self.add_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(1))
			self.add_1g_ing_butt.configure(font="TkFixedFont")

			self.rem_1g_ing_butt.configure(text='''-1g''')
			self.rem_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-1))
			self.rem_1g_ing_butt.configure(font="TkFixedFont")

		elif self.is_imperial_ingredient.get() == 1:
			self.add_1000g_ing_butt.configure(text='''+1lb''')
			self.add_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(brew_data.constants['Conversion']['lb-g']))
			self.add_1000g_ing_butt.configure(font=(None,7))

			self.add_100g_ing_butt.configure(text='''+1oz''')
			self.add_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(brew_data.constants['Conversion']['oz-g']))
			self.add_100g_ing_butt.configure(font=(None,7))

			self.rem_1000g_ing_butt.configure(text='''-1lb''')
			self.rem_1000g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-brew_data.constants['Conversion']['lb-g']))
			self.rem_1000g_ing_butt.configure(font=(None,7))

			self.rem_100g_ing_butt.configure(text='''-1oz''')
			self.rem_100g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-brew_data.constants['Conversion']['oz-g']))
			self.rem_100g_ing_butt.configure(font=(None,7))

			self.add_10g_ing_butt.configure(text='''+1/4oz''')
			self.add_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(brew_data.constants['Conversion']['oz-g']/4))
			self.add_10g_ing_butt.configure(font=(None,7))

			self.rem_10g_ing_butt.configure(text='''-1/4oz''')
			self.rem_10g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-brew_data.constants['Conversion']['oz-g']/4))
			self.rem_10g_ing_butt.configure(font=(None,7))

			self.add_1g_ing_butt.configure(text='''+1/16oz''')
			self.add_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(brew_data.constants['Conversion']['oz-g']/16))
			self.add_1g_ing_butt.configure(font=(None,7))

			self.rem_1g_ing_butt.configure(text='''-1/16oz''')
			self.rem_1g_ing_butt.configure(command=lambda: self.add_weight_ingredients(-brew_data.constants['Conversion']['oz-g']/16))
			self.rem_1g_ing_butt.configure(font=(None,7))

	def hop_to_imperial(self):
		if self.is_imperial_hop.get() == 0:
			self.add_100g_hop_butt.configure(text='''+100g''')
			self.add_100g_hop_butt.configure(command=lambda: self.add_weight_hops(100))
			self.add_100g_hop_butt.configure(font="TkFixedFont")

			self.rem_100g_hop_butt.configure(text='''-100g''')
			self.rem_100g_hop_butt.configure(command=lambda: self.add_weight_hops(-100))
			self.rem_100g_hop_butt.configure(font="TkFixedFont")

			self.add_25g_hop_butt.configure(text='''+25g''')
			self.add_25g_hop_butt.configure(command=lambda: self.add_weight_hops(25))
			self.add_25g_hop_butt.configure(font="TkFixedFont")
			self.rem_25g_hop_butt.configure(text='''-25g''')
			self.rem_25g_hop_butt.configure(command=lambda: self.add_weight_hops(-25))
			self.rem_25g_hop_butt.configure(font="TkFixedFont")

			self.add_10g_hop_butt.configure(text='''+10g''')
			self.add_10g_hop_butt.configure(command=lambda: self.add_weight_hops(10))
			self.add_10g_hop_butt.configure(font="TkFixedFont")

			self.rem_10g_hop_butt.configure(text='''-10g''')
			self.rem_10g_hop_butt.configure(command=lambda: self.add_weight_hops(-10))
			self.rem_10g_hop_butt.configure(font="TkFixedFont")

			self.add_1g_hop_butt.configure(text='''+1g''')
			self.add_1g_hop_butt.configure(command=lambda: self.add_weight_hops(1))
			self.add_1g_hop_butt.configure(font="TkFixedFont")

			self.rem_1g_hop_butt.configure(text='''-1g''')
			self.rem_1g_hop_butt.configure(command=lambda: self.add_weight_hops(-1))
			self.rem_1g_hop_butt.configure(font="TkFixedFont")

		elif self.is_imperial_hop.get() == 1:
			self.add_100g_hop_butt.configure(text='''+4oz''')
			self.add_100g_hop_butt.configure(command=lambda: self.add_weight_hops(brew_data.constants['Conversion']['oz-g']*4))
			self.add_100g_hop_butt.configure(font=(None,7))

			self.rem_100g_hop_butt.configure(text='''-4oz''')
			self.rem_100g_hop_butt.configure(command=lambda: self.add_weight_hops(-brew_data.constants['Conversion']['oz-g']*4))
			self.rem_100g_hop_butt.configure(font=(None,7))

			self.add_25g_hop_butt.configure(text='''+1oz''')
			self.add_25g_hop_butt.configure(command=lambda: self.add_weight_hops(brew_data.constants['Conversion']['oz-g']))
			self.add_25g_hop_butt.configure(font=(None,7))
			self.rem_25g_hop_butt.configure(text='''-1oz''')
			self.rem_25g_hop_butt.configure(command=lambda: self.add_weight_hops(-brew_data.constants['Conversion']['oz-g']))
			self.rem_25g_hop_butt.configure(font=(None,7))

			self.add_10g_hop_butt.configure(text='''+1/4oz''')
			self.add_10g_hop_butt.configure(command=lambda: self.add_weight_hops(brew_data.constants['Conversion']['oz-g']/4))
			self.add_10g_hop_butt.configure(font=(None,7))

			self.rem_10g_hop_butt.configure(text='''-1/4oz''')
			self.rem_10g_hop_butt.configure(command=lambda: self.add_weight_hops(-brew_data.constants['Conversion']['oz-g']/4))
			self.rem_10g_hop_butt.configure(font=(None,7))

			self.add_1g_hop_butt.configure(text='''+1/16oz''')
			self.add_1g_hop_butt.configure(command=lambda: self.add_weight_hops(brew_data.constants['Conversion']['oz-g']/16))
			self.add_1g_hop_butt.configure(font=(None,7))

			self.rem_1g_hop_butt.configure(text='''-1/16oz''')
			self.rem_1g_hop_butt.configure(command=lambda: self.add_weight_hops(-brew_data.constants['Conversion']['oz-g']/16))
			self.rem_1g_hop_butt.configure(font=(None,7))

	def attenuation_apply(self, ingredient):
		#print(brew_data.grist_data[ingredient['Name']]['Fermentability'])
		if int(brew_data.grist_data[ingredient['Name']]['Fermentability']) == 200:
			table_dict = {
				'low-62': 51, 'med-62': 59, 'high-62': 66,
				'low-63': 52, 'med-63': 60, 'high-63': 68,
				'low-64': 53, 'med-64': 61, 'high-64': 69,
				'low-65': 53, 'med-65': 62, 'high-65': 69,
				'low-66': 53, 'med-66': 62, 'high-66': 69,
				'low-67': 53, 'med-67': 62, 'high-67': 69,
				'low-68': 52, 'med-68': 60, 'high-68': 67,
				'low-69': 51, 'med-69': 58, 'high-69': 66,
				'low-70': 49, 'med-70': 56, 'high-70': 63,
				'low-71': 47, 'med-71': 54, 'high-71': 61,
				'low-72': 44, 'med-72': 51, 'high-72': 57
			}
			#print(table_dict[self.fifth_tab.current_attenuation.get()])
			return table_dict[self.sixth_tab.current_attenuation.get()]
		else:
			#print('else')
			return brew_data.grist_data[ingredient['Name']]['Fermentability']

	def sort_by_grist(self, column):
		# [{'Name:': 'Wheat Flour', 'Values': {'EBC:': 0.0, 'Grav': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}}]
		################################### Grist ###################################
		old_ingred = self.ingredients

		if column == 'Fermentable Ingredient':
			self.ingredients = sorted(self.ingredients, key=lambda k: k['Name'])
		elif column == 'Ebc':
			self.ingredients = sorted(self.ingredients, key=lambda k: k['Values']['EBC'])
		elif column == 'Grav':
			self.ingredients = sorted(self.ingredients, key=lambda k: k['Values']['Grav'])
		elif column == 'lb:oz':
			self.ingredients = sorted(self.ingredients, key=lambda k: (k['Values']['lb:oz'][0] + (k['Values']['lb:oz'][1]/16)))
		elif column == 'Grams':
			self.ingredients = sorted(self.ingredients, key=lambda k: k['Values']['Grams'])
		elif column == '%':
			self.ingredients = sorted(self.ingredients, key=lambda k: k['Values']['Percent'])

		if old_ingred == self.ingredients:
			self.ingredients.reverse()

		self.refresh_grist()

	def sort_by_hop(self, column):
		# [{'Name': 'Nelson Sauvin', 'Values': {'Type': 'Whole', 'Alpha': 12.7, 'Time': 0.0, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}}]
		old_hops = self.hops
		if column == 'Hop Variety':
			self.hops = sorted(self.hops, key=lambda k: k['Name'])
		elif column == 'Type':
			self.hops = sorted(self.hops, key=lambda k: k['Values']['Type'])
		elif column == 'Alpha':
			self.hops = sorted(self.hops, key=lambda k: k['Values']['Alpha'])
		elif column == 'Time':
			self.hops = sorted(self.hops, key=lambda k: k['Values']['Time'])
		elif column == '% Util':
			self.hops = sorted(self.hops, key=lambda k: k['Values']['Util'])
		elif column == 'IBU':
			self.hops = sorted(self.hops, key=lambda k: k['Values']['ibu'])
		elif column == 'lb:oz':
			self.hops = sorted(self.hops, key=lambda k: (k['Values']['lb:oz'][0] + (k['Values']['lb:oz'][1]/16)))
		elif column == 'Grams':
			self.hops = sorted(self.hops, key=lambda k: k['Values']['Grams'])
		elif column == '%':
			self.hops = sorted(self.hops, key=lambda k: k['Values']['Percent'])
		if old_hops == self.hops:
			self.hops.reverse()
		self.refresh_hop()

	def create_html(self, start='', open_browser=True, use_sorttable=False):
		self.recalculate()
		if use_sorttable: start += '<script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>'
		start += '<html><head><title>{name}</title><link rel="shortcut icon" href="{logo}" />'.format(name=self.recipe_name_ent.get().replace('&', '&amp;'), logo=resource_path('logo.png'))
		start += r'''
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
		start += '</head><body>'
		start += '<h2>{name}</h2>'.format(name=self.recipe_name_ent.get().replace('&', '&amp;'))
		if use_sorttable:
			start += '<table style="width:800px" class="sortable" id="sortable">'
		else:
			start += '<table style="width:800px">'
		start += '<tr><th class="subhead">Fermentable</th><th class="subhead">Colour</th><th class="subhead">lb:oz</th><th class="subhead">Grams</th><th class="subhead2">Ratio</th></tr>'

		for addition in self.sixth_tab.added_additions:
			try:
				if brew_data.water_chemistry_additions[addition]['Values']['Type'] == 'Malt':
					start += '<tr>'
					start += '<td class="ing1">{name}</td>'.format(name=addition)
					start += '<td class="ing2">N/A</td>'
					start += '<td class="ing3">N/A</td>'
					start += '<td class="ing3">N/A</td>'
					start += '<td class="ing4">N/A</td>'
					start += '</tr>'
			except KeyError:
				pass

		for ingredient in self.ingredients:
			start += '<tr>'
			start += '<td class="ing1">{name}</td>'.format(name=ingredient['Name'])
			start += '<td class="ing2">{colour}</td>'.format(colour=ingredient['Values']['EBC'])
			start += '<td class="ing3">{lb}:{oz}</td>'.format(lb=int(ingredient['Values']['lb:oz'][0]), oz=round(ingredient['Values']['lb:oz'][1], 1))
			start += '<td class="ing3">{grams}</td>'.format(grams=(round(ingredient['Values']['Grams'], 1)) if (ingredient['Values']['Grams']-int(ingredient['Values']['Grams'])) >= 2 else round(ingredient['Values']['Grams']))
			start += '<td class="ing4">{percentage}%</td>'.format(percentage=ingredient['Values']['Percent'])
			start += '</tr>'
		start += '</table><br>'
		if start[-179:] == '<tr><th class="subhead">Fermentable</th><th class="subhead">Colour</th><th class="subhead">lb:oz</th><th class="subhead">Grams</th><th class="subhead2">Ratio</th></tr></table><br>': start = start[:-179]

		if self.sixth_tab.water_boil_is_disabled.get() == 1:
			start += '<p><b>Boil Time: </b>{boil_time}</p>'.format(boil_time=self.sixth_tab.water_boil_time_spinbx.get())

		if use_sorttable:
			start += '<table style="width:800px" class="sortable" id="sortable">'
		else:
			start += '<table style="width:800px">'
		start += '<tr><th class="subhead">Hop Variety</th><th class="subhead">Type</th><th class="subhead">Alpha</th><th class="subhead">Time</th><th class="subhead">lb:oz</th><th class="subhead">Grams</th><th class="subhead2">Ratio</th></tr>'
		#temp_hop = [*self.hops] + [{'Name': addition, 'Values': brew_data.water_chemistry_additions[addition]['Values']} if brew_data.water_chemistry_additions[addition]['Values']['Type'] == 'Hop' else None for addition in self.sixth_tab.added_additions]
		temp_hop = self.hops[:]
		for addition in self.sixth_tab.added_additions:
			try:
				if brew_data.water_chemistry_additions[addition]['Values']['Type'] == 'Hop':
					temp_hop.append({'Name': addition, 'Values': brew_data.water_chemistry_additions[addition]['Values']})
				else:
					temp_hop.append(None)
			except KeyError:
				pass

		temp_hop = list(sorted([x for x in temp_hop if x is not None], key=lambda k: k['Values']['Time']))
		for hop in reversed(temp_hop):
			if hop['Values']['Type'] != 'Hop':
				start += '<tr>'
				start += '<td class="hop1">{name}</td>'.format(name=hop['Name'])
				start += '<td class="hop2">{type}</td>'.format(type=hop['Values']['Type'])
				start += '<td class="hop3">{alpha}</td>'.format(alpha=hop['Values']['Alpha'])
				start += '<td class="hop4">{time}</td>'.format(time=round(hop['Values']['Time']))
				start += '<td class="hop5">{lb}:{oz}</td>'.format(lb=int(hop['Values']['lb:oz'][0]), oz=round(hop['Values']['lb:oz'][1], 1))
				start += '<td class="hop5">{grams}</td>'.format(grams=(round(hop['Values']['Grams'], 1)) if (hop['Values']['Grams']-int(hop['Values']['Grams'])) >= 2 else round(hop['Values']['Grams']))
				start += '<td class="hop6">{percentage}%</td>'.format(percentage=hop['Values']['Percent'])
				start += '</tr>'
			else:
				start += '<tr>'
				start += '<td class="hop1">{name}</td>'.format(name=hop['Name'])
				start += '<td class="hop2">N/A</td>'
				start += '<td class="hop3">N/A</td>'
				start += '<td class="hop4">{time}</td>'.format(time=hop['Values']['Time'])
				start += '<td class="hop5">N/A</td>'
				start += '<td class="hop5">N/A</td>'
				start += '<td class="hop6">N/A</td>'
				start += '</tr>'
		start += '</table><br>'
		if start[-236:] == '<tr><th class="subhead">Hop Variety</th><th class="subhead">Type</th><th class="subhead">Alpha</th><th class="subhead">Time</th><th class="subhead">lb:oz</th><th class="subhead">Grams</th><th class="subhead2">Ratio</th></tr></table><br>': start = start[:-236]


		if use_sorttable:
			start += '<table style="width:800px" class="sortable" id="sortable">'
		else:
			start += '<table style="width:800px">'
		start += '<tr><th class="subhead">Yeast</th><th class="subhead">Lab</th><th class="subhead">Origin</th><th class="subhead">Type</th><th class="subhead">Flocculation</th><th class="subhead">Attenuation</th><th class="subhead2">Temperature</th></tr>'
		for addition in self.sixth_tab.added_additions:
			try:
				if brew_data.yeast_data[addition]['Type'] == 'D':
					yeast_type = 'Dry'
				elif brew_data.yeast_data[addition]['Type'] == 'L':
					yeast_type = 'Liquid'
				else:
					yeast_type = brew_data.yeast_data[addition]['Type']

				lab = brew_data.yeast_data[addition]['Lab']
				origin = brew_data.yeast_data[addition]['Origin']
				flocculation = brew_data.yeast_data[addition]['Flocculation']
				attenuation = brew_data.yeast_data[addition]['Attenuation']
				if len(brew_data.yeast_data[addition]['Temperature'].replace('°', '').split('-')) >= 2:
					temperature = brew_data.yeast_data[addition]['Temperature'].replace('°', '').split('-')[0]
					temperature += '-' + brew_data.yeast_data[addition]['Temperature'].replace('°', '').split('-')[1]
				else:
					temperature = temperature

				start += '<tr>'
				start += '<td class="yst1">{name}</td>'.format(name=addition)
				start += '<td class="yst2">{lab}</td>'.format(lab=lab)
				start += '<td class="yst3">{origin}</td>'.format(origin=origin)
				start += '<td class="yst4">{yeast_type}</td>'.format(yeast_type=yeast_type)
				start += '<td class="yst5">{flocculation}</td>'.format(flocculation=flocculation)
				start += '<td class="yst6">{attenuation}</td>'.format(attenuation=attenuation)
				start += '<td class="yst7">{temperature}</td>'.format(temperature=temperature)
				start += '</tr>'
			except KeyError:
				try:
					if brew_data.water_chemistry_additions[addition]['Values']['Type'] == 'Yeast':
						start += '<tr>'
						start += '<td class="yst1">{name}</td>'.format(name=addition)
						start += '<td class="yst2">N/A</td>'
						start += '<td class="yst3">N/A</td>'
						start += '<td class="yst4">N/A</td>'
						start += '<td class="yst5">N/A</td>'
						start += '<td class="yst6">N/A</td>'
						start += '<td class="yst7">N/A</td>'
						start += '</tr>'
				except KeyError:
					pass
		start += '</table>'
		if start[-245:] == '<tr><th class="subhead">Yeast</th><th class="subhead">Lab</th><th class="subhead">Origin</th><th class="subhead">Type</th><th class="subhead">Flocculation</th><th class="subhead">Attenuation</th><th class="subhead2">Temperature</th></tr></table>': start = start[:-245]

		start += '<p><b>Final Volume: </b>{volume} Litres</p>'.format(volume=self.volume.get())
		start += '<p><b>Original Gravity: </b>{og}</p>'.format(og=round(self.og, 1))
		start += '<p><b>Final Gravity: </b>{fg}</p>'.format(fg=round(self.fg, 1))
		start += '<p><b>Alcohol Content: </b>{abv}% ABV</p>'.format(abv=round(self.abv, 1))
		start += '<p><b>Mash Efficiency: </b>{efficiency}</p>'.format(efficiency=brew_data.constants['Efficiency']*100)
		start += '<p><b>Bitterness: </b>{bitterness} IBU</p>'.format(bitterness=round(self.ibu))
		start += '<p><b>Colour: </b>{colour} EBC</p>'.format(colour=round(self.colour, 1))
		notes = self.seventh_tab.texpert.get('1.0', 'end')
		if self.seventh_tab.html_formatting.get():
			start += '''<hr><h2>Notes</h2>\n{notes}'''.format(notes=notes) if len(notes) >= 1 else ''
		else:
			start += '''<hr><h2>Notes</h2>\n<p>{notes}</p>'''.format(notes=notes.replace('\n', '<br>')) if len(notes) >= 1 else ''
		start += '</body>'
		start += '</html>'

		start = bs4.BeautifulSoup(start, features="html.parser").prettify() if 'bs4' in sys.modules else start
		text_file_name = resource_path('{recipe_name}.html'.format(recipe_name=self.recipe_name_ent.get().replace('/', '⁄')))
		with open(text_file_name, 'w') as hs:
			hs.write(start)
		if open_browser: webbrowser.open('file://' + os.path.realpath(text_file_name), new=1)

	def create_complex_html(self):
		self.create_html(use_sorttable=True)
	
	def open_dialog(self):
		def save_and_open():
			dialog.destroy()
			self.save()
			self.open_file(file_str)
		def j_open(): # JUST OPEN
			dialog.destroy()
			self.open_file(file_str)
		
		file_str = filedialog.askopenfilename(
					initialdir=os.path.expanduser(
						'~/.config/Wheelers-Wort-Works/recipes/' if __mode__ == 'deb' else '.'),
					title="Select file",
					filetypes=(
						("BERF",
						 "*.berf *.berfx"),
						("all files",
						 "*.*")))
		if file_str == '' or file_str is None or type(file_str) == tuple:
			return
		dialog = tk.Toplevel(self.master)
		dialog.resizable(0, 0)
		dialog.title("Open")
		tk.Label(dialog, text='Are you sure you wish to open this file? Any unsaved changes will be lost').grid(row=0, column=0, columnspan=3)
		tk.Button(dialog, text='Save and open', command=save_and_open).grid(row=1, column=0)
		tk.Button(dialog, text='Open without saving', command=j_open).grid(row=1, column=1)
		tk.Button(dialog, text='Cancel', command=dialog.destroy).grid(row=1, column=2)
		dialog.update_idletasks() 
		x = self.master.winfo_x() + (self.master.winfo_width()/2) - (dialog.winfo_width()/2)
		y = self.master.winfo_y() + (self.master.winfo_height()/2) - (dialog.winfo_height()/2)
		dialog.geometry("+{x}+{y}".format(x=int(x), y=int(y)))
		dialog.attributes("-topmost", True)

	def open_file(self, file):
		if file != '' and file != None and type(file) != tuple:
			self.sixth_tab.original_additions = list(sorted(brew_data.water_chemistry_additions)) + list(sorted(brew_data.yeast_data))
			self.sixth_tab.added_additions = []
			self.sixth_tab.refresh_all()
			examples = ['1920s Bitter', 'Bog-Standard Bitter', 'Black-Country Mild', 'Irish Stout', '1920s Mild', '1920s Porter', '1920s Stock Ale', '1920s Stout']
			is_ogfixed = 0
			is_ebufixed = 0
			self.ingredients = []
			self.hops = []
			self.seventh_tab.texpert.delete('1.0', 'end')
			notes = b''
			if file.lower().endswith('.berf') or file.split('/')[-1] in examples:
				self.current_file = file
				with open(file, 'rb') as f:
					#data = [line for line in f]
					data = [line.replace(b'\xa7', b'\t').strip().decode('ISO-8859-1').split('\t') for line in f]
					#print(data)
					for sublist in data:
						if sublist[0] == 'grain':
							grams = float(sublist[7])
							lb = grams/brew_data.constants['Conversion']['lb-g']
							oz = (lb-int(lb))*16
							percent = float(sublist[8])
							EBC = float(sublist[2])
							self.ingredients.append({'Name': sublist[1], 'Values': {'EBC': EBC, 'Grav': 0, 'lb:oz': (lb,oz), 'Grams': grams, 'Percent': percent}})
						elif sublist[0] == 'hop':
							alpha = float(sublist[3])
							grams = float(sublist[5])
							lb = grams/brew_data.constants['Conversion']['lb-g']
							oz = (lb-int(lb))*16
							time = float(sublist[6])
							percent = float(sublist[7])
							self.hops.append({'Name': sublist[1], 'Values': {'Type': sublist[2], 'Alpha': alpha, 'Time': time, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (lb,oz), 'Grams': grams, 'Percent': percent}})
						elif sublist[0] == 'add':
							name = sublist[1]
							dictionary = ast.literal_eval(sublist[2])
							if 'Lab' in dictionary:
								brew_data.yeast_data[name] = dictionary
							else:
								brew_data.water_chemistry_additions[name] = dictionary

							self.sixth_tab.added_additions.append(name)

						elif sublist[1] == 'recipename':
							self.recipe_name_ent.delete(0, tk.END)
							self.recipe_name_ent.insert(0, sublist[2])
						elif sublist[1] == 'volume':
							self.volume_ent.delete(0, tk.END)
							self.volume_ent.insert(0, sublist[2])
							if not any(e[1] == 'boilvol' for e in data):
								self.boil_volume_ent.delete(0, tk.END)
								self.boil_volume_ent.insert(0, float(sublist[2])*brew_data.constants['Boil Volume Scale'])
						elif sublist[1] == 'boilvol':
							self.boil_volume_ent.delete(0, tk.END)
							self.boil_volume_ent.insert(0, sublist[2])
						elif sublist[1] == 'efficiency':
							brew_data.constants['Efficiency'] = float(sublist[2])/100
						elif sublist[0] == 'miscel':
							if sublist[1] == 'ogfixed':
								is_ogfixed = sublist[2]
							elif sublist[1] == 'ebufixed':
								is_ebufixed = sublist[2]
							elif sublist[1] == 'notes':
								# notes += bytes(sublist[2],encoding='utf8')
								# print(notes, str(sublist[2]))
								notes = sublist[2]
								# print(notes, ast.literal_eval("'"+notes+"'"))

			elif file.lower().endswith('.berfx'):
				self.current_file = file
				with open(file, 'r') as f:
					#data = [line.replace(b'\xa7', b'\t').strip().decode().split('\t') for line in f]
					data = [line.replace('\xa7', '\t').strip().split('\t') for line in f]
					for sublist in data:
						if sublist[0] == 'grain':
							self.ingredients.append({'Name': sublist[1] , 'Values': ast.literal_eval(sublist[2])})
						elif sublist[0] == 'hop':
							self.hops.append({'Name': sublist[1] , 'Values': ast.literal_eval(sublist[2])})
						elif sublist[0] == 'add':
							name = sublist[1]
							dictionary = ast.literal_eval(sublist[2])

							if 'Lab' in dictionary:
								brew_data.yeast_data[name] = dictionary
							else:
								brew_data.water_chemistry_additions[name] = dictionary

							self.sixth_tab.added_additions.append(name)
						elif sublist[0] == 'database':
							if sublist[1] == 'grist':
								brew_data.grist_data[sublist[2]] = ast.literal_eval(sublist[3])
							elif sublist[1] == 'hop':
								brew_data.hop_data[sublist[2]] = ast.literal_eval(sublist[3])
							elif sublist[1] == 'yeast':
								brew_data.yeast_data[sublist[2]] = ast.literal_eval(sublist[3])
							elif sublist[1] == 'water_chem':
								brew_data.water_chemistry_additions[sublist[2]] = ast.literal_eval(sublist[3])
							elif sublist[1] == 'constant':
								for constant, value in ast.literal_eval(sublist[2]).items():
									brew_data.constants[constant] = value
						elif sublist[0] == 'miscel':
							if sublist[1] == 'ogfixed':
								is_ogfixed = sublist[2]
							elif sublist[1] == 'ebufixed':
								is_ebufixed = sublist[2]
							elif sublist[1] == 'recipename':
								self.recipe_name_ent.delete(0, tk.END)
								self.recipe_name_ent.insert(0, sublist[2])
							elif sublist[1] == 'notes':
								#notes += bytes(sublist[2],encoding='utf8')
								notes = sublist[2]

			self.seventh_tab.texpert.insert('1.0', ast.literal_eval("'"+notes.replace("'", r'\'').replace('"', r'\"')+"'"))
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
		if file != '' and type(file) == str:
			if file.lower()[-5:] == '.berf':
				self.current_file = file
				with codecs.open(file, 'w', 'ISO-8859-1', errors='ignore') as f:
					for ingredient in self.ingredients:
						ebc = ingredient['Values']['EBC']
						ingred_type = brew_data.grist_data[ingredient['Name']]['Type']
						units = (ingredient['Values']['Grams']/1000)*brew_data.constants['Efficiency']
						moisture = brew_data.grist_data[ingredient['Name']]['Moisture']
						fermentability = brew_data.grist_data[ingredient['Name']]['Fermentability']
						grams = ingredient['Values']['Grams']
						percentage = ingredient['Values']['Percent']
						f.write('grain\xa7{name}\t{ebc}\t{type}\t{units}\t{moisture}\t{fermentability}\t{grams}\t{percentage}\n'.format(name=ingredient['Name'], ebc=ebc, type=ingred_type, units=units, moisture=moisture, fermentability=fermentability, grams=grams, percentage=percentage))
					for hop in self.hops:
						# 'Values': {'Type': 'Whole', 'Alpha': 12.7, 'Time': 0.0, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}
						hop_type = hop['Values']['Type']
						alpha = hop['Values']['Alpha']
						ibu =  hop['Values']['ibu']
						grams = hop['Values']['Grams']
						time = hop['Values']['Time']
						percentage = hop['Values']['Percent']
						f.write('hop\xa7{name}\t{type}\t{alpha}\t{ibu}\t{grams}\t{time}\t{percentage}\n'.format(name=hop['Name'], type=hop_type, alpha=alpha, ibu=ibu, grams=grams, time=time, percentage=percentage))
					for addition in self.sixth_tab.added_additions:
						all_chem = dict(brew_data.water_chemistry_additions)
						all_chem.update(brew_data.yeast_data)
						name = addition
						addition_type = all_chem[name]
						f.write('add\xa7{name}\t{type}\n'.format(name=name, type=addition_type))
					f.write('default\xa7efficiency\t{efficiency}\n'.format(efficiency=brew_data.constants['Efficiency']*100))
					f.write('default\xa7volume\t{volume}\n'.format(volume=self.volume.get()))
					f.write('default\xa7boilvol\t{boilvol}\n'.format(boilvol=self.boil_vol.get()))
					f.write('miscel\xa7recipename\t{recipename}\n'.format(recipename=self.recipe_name_ent.get()))
					f.write('miscel\xa7ogfixed\t{ogfixed}\n'.format(ogfixed=self.is_ogfixed.get()))
					f.write('miscel\xa7ebufixed\t{ebufixed}\n'.format(ebufixed=self.is_ebufixed.get()))
					f.write('miscel\xa7origgrav\t{origgrav}\n'.format(origgrav=self.og))

					notes = repr(self.seventh_tab.texpert.get('1.0', 'end'))#, encoding='utf8')
					# print(notes)
					f.write('miscel\xa7notes\t{notes}\n'.format(notes=notes[1:-1]))

			elif file.lower()[-6:] == '.berfx':
				self.current_file = file
				with open(file, 'w') as f:
					for ingredient in self.ingredients:
						f.write('grain\xa7{name}\t{data}\n'.format(name=ingredient['Name'], data=ingredient['Values']))
					for hop in self.hops:
						# 'Values': {'Type': 'Whole', 'Alpha': 12.7, 'Time': 0.0, 'Util': 0.0, 'ibu': 0.0, 'lb:oz': (0.0,0.0), 'Grams': 0.0, 'Percent': 0.0}
						f.write('hop\xa7{name}\t{data}\n'.format(name=hop['Name'], data=hop['Values']))
					for addition in self.sixth_tab.added_additions:
						all_chem = dict(brew_data.water_chemistry_additions)
						all_chem.update(brew_data.yeast_data)
						name = addition
						addition_type = all_chem[name]
						f.write('add\xa7{name}\t{type}\n'.format(name=name, type=addition_type))

					f.write('miscel\xa7ogfixed\t{ogfixed}\n'.format(ogfixed=self.is_ogfixed.get()))
					f.write('miscel\xa7ebufixed\t{ebufixed}\n'.format(ebufixed=self.is_ebufixed.get()))
					f.write('miscel\xa7recipename\t{recipename}\n'.format(recipename=self.recipe_name_ent.get()))
					f.write('default\xa7boilvol\t{boilvol}\n'.format(boilvol=self.boil_vol.get()))

					notes = repr(self.seventh_tab.texpert.get('1.0', 'end'))
					f.write('miscel\xa7notes\t{notes}\n'.format(notes=notes[1:-1]))

					for key, grist in brew_data.grist_data.items(): f.write('database\xa7grist\xa7{name}\t{data}\n'.format(name=key, data=grist))
					for key, hop in brew_data.hop_data.items(): f.write('database\xa7hop\xa7{name}\t{data}\n'.format(name=key, data=hop))
					for key, yeast in brew_data.yeast_data.items(): f.write('database\xa7yeast\xa7{name}\t{data}\n'.format(name=key, data=yeast))
					for key, water_chem in brew_data.water_chemistry_additions.items(): f.write('database\xa7water_chem\xa7{name}\t{data}\n'.format(name=key, data=water_chem))
					#for key, constant in brew_data.constants.items(): f.write('database\xa7constant\xa7{name}\t{data}\n'.format(name=key, data=constant))
					f.write('database\xa7constant\xa7{constants}'.format(constants=brew_data.constants))

	def save(self):
		if self.current_file != '':
			self.save_file(self.current_file)
		else:
		 	self.save_file(filedialog.asksaveasfilename(initialdir = os.path.expanduser('~/.config/Wheelers-Wort-Works-ce/recipes/' if __mode__ == 'deb' else '.'),title = "Select file", defaultextension=".berf", initialfile='{0}.berf'.format(self.recipe_name_ent.get())))

	def save_all(self):
		self.save()
		self.create_html()

	def quit(self):
		''' Quit Wheeler's Wort Works '''
		def save_and_quit():
			save_cont_win.destroy()
			self.save()
			self.master.destroy()

		if brew_data.constants['Save On Close']:
			save_cont_win = tk.Toplevel(self.master)
			save_cont_win.resizable(0, 0)
			save_cont_win.title("Quit")
			tk.Label(save_cont_win, text='Are you sure you wish to save and quit?').grid(row=0, column=0, columnspan=3)
			tk.Button(save_cont_win, text='Save and quit', command=save_and_quit).grid(row=1, column=0)
			tk.Button(save_cont_win, text='Quit without saving', command=self.master.destroy).grid(row=1, column=1)
			tk.Button(save_cont_win, text='Cancel', command=save_cont_win.destroy).grid(row=1, column=2)
			save_cont_win.update_idletasks() 
			x = self.master.winfo_x() + (self.master.winfo_width()/2) - (save_cont_win.winfo_width()/2)
			y = self.master.winfo_y() + (self.master.winfo_height()/2) - (save_cont_win.winfo_height()/2)
			save_cont_win.geometry("+{x}+{y}".format(x=int(x), y=int(y)))
			save_cont_win.attributes("-topmost", True)

		else:
			if messagebox.askokcancel("Quit",  "Do you want to quit? Any unsaved changes will be lost"):
				self.master.destroy()

	def add_percent_ingredients(self, amount, curr_selection=None):
		try:
			if curr_selection is None:
				selection = self.scrolled_tree_ingredient.selection()[0]
			else:
				selection = curr_selection
			id = int(str(selection)[1:], 16)
			percent = self.ingredients[id-1]['Values']['Percent'] + amount
			if percent < 0: percent = 0
			self.ingredients[id-1]['Values']['Percent'] = percent
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
			id = int(str(selection)[1:], 16)
			percent = self.hops[id-1]['Values']['Percent'] + amount
			if percent < 0: percent = 0
			self.hops[id-1]['Values']['Percent'] = percent
			self.refresh_hop()
			self.scrolled_tree_hops.focus_set()
			self.scrolled_tree_hops.see(selection)
			self.scrolled_tree_hops.selection_set(selection)
		except IndexError:
			pass

	def ebu_fixed(self):
		if self.is_ebufixed.get() == 1:
			self.add_100g_hop_butt.configure(text='''+10%''')
			self.add_100g_hop_butt.configure(command=lambda: self.add_percent_hops(10))
			self.add_100g_hop_butt.configure(font="TkFixedFont")

			self.rem_100g_hop_butt.configure(text='''-10%''')
			self.rem_100g_hop_butt.configure(command=lambda: self.add_percent_hops(-10))
			self.rem_100g_hop_butt.configure(font="TkFixedFont")

			self.add_25g_hop_butt.configure(text='''+5%''')
			self.add_25g_hop_butt.configure(command=lambda: self.add_percent_hops(5))
			self.add_25g_hop_butt.configure(font="TkFixedFont")

			self.rem_25g_hop_butt.configure(text='''-5%''')
			self.rem_25g_hop_butt.configure(command=lambda: self.add_percent_hops(-5))
			self.rem_25g_hop_butt.configure(font="TkFixedFont")

			self.add_10g_hop_butt.configure(text='''+1%''')
			self.add_10g_hop_butt.configure(command=lambda: self.add_percent_hops(1))
			self.add_10g_hop_butt.configure(font="TkFixedFont")

			self.rem_10g_hop_butt.configure(text='''-1%''')
			self.rem_10g_hop_butt.configure(command=lambda: self.add_percent_hops(-1))
			self.rem_10g_hop_butt.configure(font="TkFixedFont")

			self.add_1g_hop_butt.configure(text='''+0.1%''')
			self.add_1g_hop_butt.configure(command=lambda: self.add_percent_hops(0.1))
			self.add_1g_hop_butt.configure(font="TkFixedFont")

			self.rem_1g_hop_butt.configure(text='''-0.1%''')
			self.rem_1g_hop_butt.configure(command=lambda: self.add_percent_hops(-0.1))
			self.rem_1g_hop_butt.configure(font="TkFixedFont")
		else:
			self.hop_to_imperial()

	def og_fixed(self):
		if self.is_ogfixed.get() == 1:
			self.add_1000g_ing_butt.configure(text='''+10%''')
			self.add_1000g_ing_butt.configure(command=lambda: self.add_percent_ingredients(10))
			self.add_1000g_ing_butt.configure(font="TkFixedFont")

			self.add_100g_ing_butt.configure(text='''+5%''')
			self.add_100g_ing_butt.configure(command=lambda: self.add_percent_ingredients(5))
			self.add_100g_ing_butt.configure(font="TkFixedFont")

			self.rem_1000g_ing_butt.configure(text='''-10%''')
			self.rem_1000g_ing_butt.configure(command=lambda: self.add_percent_ingredients(-10))
			self.rem_1000g_ing_butt.configure(font="TkFixedFont")

			self.rem_100g_ing_butt.configure(text='''-5%''')
			self.rem_100g_ing_butt.configure(command=lambda: self.add_percent_ingredients(-5))
			self.rem_100g_ing_butt.configure(font="TkFixedFont")

			self.add_10g_ing_butt.configure(text='''+1%''')
			self.add_10g_ing_butt.configure(command=lambda: self.add_percent_ingredients(1))
			self.add_10g_ing_butt.configure(font="TkFixedFont")

			self.rem_10g_ing_butt.configure(text='''-1%''')
			self.rem_10g_ing_butt.configure(command=lambda: self.add_percent_ingredients(-1))
			self.rem_10g_ing_butt.configure(font="TkFixedFont")

			self.add_1g_ing_butt.configure(text='''+0.1%''')
			self.add_1g_ing_butt.configure(command=lambda: self.add_percent_ingredients(0.1))
			self.add_1g_ing_butt.configure(font="TkFixedFont")

			self.rem_1g_ing_butt.configure(text='''-0.1%''')
			self.rem_1g_ing_butt.configure(command=lambda: self.add_percent_ingredients(-0.1))
			self.rem_1g_ing_butt.configure(font="TkFixedFont")
		else:
			self.ingredient_to_imperial()

	def database_to_folder(self, folder=None):
		if folder == None: 
			if not os.path.exists(os.path.join(os.path.dirname(resource_path('hop_data.txt')), 'backups')):
				try:
					os.makedirs(os.path.join(os.path.dirname(resource_path('hop_data.txt')), 'backups'))
					folder = os.path.join(os.path.dirname(resource_path('hop_data.txt')), 'backups')
				except:
					folder = os.path.dirname(resource_path('hop_data.txt')) 
			else:
				folder = os.path.join(os.path.dirname(resource_path('hop_data.txt')), 'backups')
		if type(folder) != tuple: print(folder)
		curr_time = datetime.datetime.today().strftime('%d-%m-%Y %H-%M-%S')
		print(curr_time)
		# HOP DATA
		with open(os.path.join(folder, 'hop_data {curr_time}.txt'.format(curr_time=curr_time)), 'w') as f:
			for hop, value in brew_data.hop_data.items():
				name = hop
				hop_type = value['Form']
				origin = value['Origin']
				alpha = value['Alpha']
				use = value['Use']
				description = value['Description']
				f.write('{name}\t{type}\t{origin}\t{alpha}\t{use}\t{description}\n'.format(name=name, type=hop_type, origin=origin, alpha=alpha, use=use, description=description))
		# GRAIN DATA
		with open(os.path.join(folder, 'grain_data {curr_time}.txt'.format(curr_time=curr_time)), 'w') as f:
			for ingredient, value in brew_data.grist_data.items():
				name = ingredient
				ebc = value['EBC']
				grain_type = value['Type']
				extract = value['Extract']
				moisture = value['Moisture']
				fermentability = value['Fermentability']
				description = value['Description']
				f.write('{name}\t{ebc}\t{type}\t{extract}\t{moisture}\t{fermentability}\t{description}\n'.format(name=name, ebc=ebc, type=grain_type, extract=extract, moisture=moisture, fermentability=fermentability, description=description))
		# HOP DATA
		with open(os.path.join(folder, 'yeast_data {curr_time}.txt'.format(curr_time=curr_time)), 'w') as f:
			for yeast, value in brew_data.yeast_data.items():
				name = yeast
				yeast_type = value['Type']
				lab = value['Lab']
				flocculation = value['Flocculation']
				attenuation = value['Attenuation']
				temperature = value['Temperature']
				origin = value['Origin']
				description = value['Description']
				f.write('{name}\t{yeast_type}\t{lab}\t{flocculation}\t{attenuation}\t{temperature}\t{origin}\t{description}\n'.format(name=name, yeast_type=yeast_type, lab=lab, flocculation=flocculation, attenuation=attenuation, temperature=temperature, origin=origin, description=description))
		# DEFAULTS
		with open(os.path.join(folder, 'defaults {curr_time}.txt'.format(curr_time=curr_time)), 'w') as f:
				volume = brew_data.constants['Volume']
				efficiency = brew_data.constants['Efficiency']*100
				evaporation = round((brew_data.constants['Boil Volume Scale']-1)*100, 1)
				LGratio = brew_data.constants['Liquor To Grist Ratio']
				attenuation = brew_data.constants['Attenuation Default']
				save_close = brew_data.constants['Save On Close']
				boil_time = brew_data.constants['Default Boil Time']
				replace_defaults = brew_data.constants['Replace Defaults']
				f.write('efficiency={efficiency}\nvolume={volume}\nevaporation={evaporation}\nLGratio={LGratio}\nattenuation={attenuation}\nsave_close={save_close}\nboil_time={boil_time}\nreplace_defaults={replace_defaults}'.format(efficiency=efficiency, volume=volume, evaporation=evaporation, LGratio=LGratio,
																																																										attenuation=attenuation, save_close=save_close, boil_time=boil_time, replace_defaults=replace_defaults))	# WATER CHEM DATA
		
		with open(os.path.join(folder, 'water_chem_data {curr_time}.txt'.format(curr_time=curr_time)), 'w') as f:
			for water_chem, values in brew_data.water_chemistry_additions.items():
				value = values['Values']
				name = water_chem
				time = value['Time'] if 'Time' in value else 'N/A'
				#print(value)
				water_chem_type = value['Type']
				f.write('{name}\t{time}\t{water_chem_type}\n'.format(name=name, time=time, water_chem_type=water_chem_type))
		
		with open(resource_path('backups.txt'), 'a+') as f:
			f.write('{curr_time}\n'.format(curr_time=curr_time))

		messagebox.showinfo('Backup Successful', 'Backup {time} Created Successfully'.format(time=curr_time))		

	def restore_backup_dialogue(self):
		def restore(folder=None):
			if folder == None: 
				if os.path.exists(os.path.join(os.path.dirname(resource_path('hop_data.txt')), 'backups')):
					folder = os.path.join(os.path.dirname(resource_path('hop_data.txt')), 'backups')
				else:
					folder = os.path.dirname(resource_path('hop_data.txt'))
			file_starts = ['grain_data', 'hop_data', 'water_chem_data', 'yeast_data', 'defaults']
			try:			
				selection = backups.selection()[0]
				for file_start in file_starts:
					if file_start in selection:
						file_starts = [file_start]
						selection = selection[len(file_start):]
				id = int(str(selection)[1:], 16)
			except Exception as e:
				messagebox.showwarning('No Backup Selected', 'Please select a Restore Point', parent=restore_backup_dia)
				return
			if messagebox.askquestion('Verify', 'This operation will overwrite current database. Are you sure you wish to Restore Database?', parent=restore_backup_dia) == 'no':
				return
			try:	
				time = backup_list[id-1]
				for file_start in file_starts:
					print('{file_start} {time}.txt'.format(file_start=file_start, time=time))
					if os.path.isfile(os.path.join(folder, '{file_start} {time}.txt'.format(file_start=file_start, time=time))):
						with open(resource_path(file_start+'.txt'), 'w') as f:
							for line in open(os.path.join(folder, '{file_start} {time}.txt'.format(file_start=file_start, time=time))).readlines():
								f.write(line)
					else:
						messagebox.showerror('File Not Found', 'File Not Found: {file}'.format(file=os.path.join(folder, '{file_start} {time}.txt'.format(file_start=file_start, time=time))))
				messagebox.showinfo('Restore Successful', 'Backup {time} Restored Successfully'.format(time=time), parent=restore_backup_dia)
			except Exception as e:
				print(e)


		restore_backup_dia = tk.Toplevel()
		restore_backup_dia.resizable(0, 0)
		backups = ScrolledTreeView(restore_backup_dia, custom_insert=False, show="tree")
		backups.grid(row=0,column=0)
		if os.path.isfile(resource_path('backups.txt')):
			backup_list = [backup.strip() for backup in open(resource_path('backups.txt')).readlines()]
		else:
			backup_list = []
		for backup in backup_list:
			curr_insert = backups.insert('', tk.END, text=(backup))
			print(curr_insert)
			for idx, file_start in enumerate(['grain_data', 'hop_data', 'water_chem_data', 'yeast_data', 'defaults']):
				if os.path.exists(os.path.join(os.path.dirname(resource_path('hop_data.txt')), 'backups')):
					file_name = os.path.join(os.path.dirname(resource_path('hop_data.txt')), 'backups/{file_start} {time}.txt'.format(file_start=file_start, time=backup))
				else:
					file_name = resource_path('{file_start} {time}.txt'.format(file_start=file_start, time=backup))
				print(file_name)
				if os.path.isfile(file_name):
					print(idx)
					backups.insert(curr_insert, 'end', text='{file_start}.txt'.format(file_start=file_start), iid='{file_start}{iid}'.format(file_start=file_start, iid=curr_insert))
		backups_res_butt = tk.Button(restore_backup_dia, text='Restore', command = restore)
		backups_res_butt.grid(row=0,column=1)

class hops_editor(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.widgets()

	def widgets(self):
		'''This class configures and populates the toplevel window.
		   top is the toplevel containing window.'''
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85'
		_ana2color = '#ececec' # Closest X11 color: 'gray92'
		font9 = "-family {DejaVu Sans} -size 10 -weight bold -slant "  \
			"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()
		self.style.configure('.',background=_bgcolor)
		self.style.configure('.',foreground=_fgcolor)
		self.style.configure('.',font="TkDefaultFont")
		self.style.map('.',background=
			[('selected', _compcolor), ('active',_ana2color)])

		self.hop_panedwindow1 = tk.LabelFrame(self, text='Hops:', background=_bgcolor)
		self.hop_panedwindow1.place(relx=0.005, rely=0.005, relheight=0.990, relwidth=0.5)

		self.hop_panedwindow2 = tk.LabelFrame(self, text='Modifications:', background=_bgcolor)
		self.hop_panedwindow2.place(relx=0.510, rely=0.005, relheight=0.990, relwidth=0.485)		

		self.hop_lstbx = ScrolledListBox(self.hop_panedwindow1)
		self.hop_lstbx.place(relx=0.025, rely=0.043, relheight=0.887
				, relwidth=0.94, bordermode='ignore')
		self.hop_lstbx.configure(background="white")
		self.hop_lstbx.configure(font="TkFixedFont")
		self.hop_lstbx.configure(highlightcolor="#d9d9d9")
		self.hop_lstbx.configure(selectbackground="#c4c4c4")

		self.hop_delete_butt = tk.Button(self.hop_panedwindow1)
		self.hop_delete_butt.place(relx=0.025, rely=0.929, relheight=0.0589, relwidth=0.2075
				, bordermode='ignore')
		self.hop_delete_butt.configure(takefocus="")
		self.hop_delete_butt.configure(text='''Delete''')
		self.hop_delete_butt.configure(command=self.delete)

		self.hop_modify_butt = tk.Button(self.hop_panedwindow1)
		self.hop_modify_butt.place(relx=0.35, rely=0.93, relheight=0.0589, relwidth=0.2075
				, bordermode='ignore')
		self.hop_modify_butt.configure(takefocus="")
		self.hop_modify_butt.configure(text='''Modify''')
		self.hop_modify_butt.configure(command=lambda: self.input_state(1))

		self.hop_new_butt = tk.Button(self.hop_panedwindow1)
		self.hop_new_butt.place(relx=0.725, rely=0.93, relheight=0.0589, relwidth=0.2075
				, bordermode='ignore')
		self.hop_new_butt.configure(takefocus="")
		self.hop_new_butt.configure(text='''New''')
		self.hop_new_butt.configure(command=self.new)

		############################ Config Section ############################

		self.hop_name_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_name_lbl.place(relx=0.056, rely=0.087, bordermode='ignore')
		self.hop_name_lbl.configure(background=_bgcolor)
		self.hop_name_lbl.configure(foreground="#000000")
		self.hop_name_lbl.configure(font=font9)
		self.hop_name_lbl.configure(relief='flat')
		self.hop_name_lbl.configure(text='''Name:''')

		self.hop_name_ent = tk.Entry(self.hop_panedwindow2)
		self.hop_name_ent.place(relx=0.222, rely=0.087, relheight=0.046
				, relwidth=0.511, bordermode='ignore')
		self.hop_name_ent.configure(justify='center')
		self.hop_name_ent.configure(width=184)
		self.hop_name_ent.configure(foreground="#000000")
		self.hop_name_ent.configure(takefocus="")
		self.hop_name_ent.configure(cursor="xterm")

		self.hop_form_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_form_lbl.place(relx=0.056, rely=0.152, bordermode='ignore')
		self.hop_form_lbl.configure(background=_bgcolor)
		self.hop_form_lbl.configure(foreground="#000000")
		self.hop_form_lbl.configure(font=font9)
		self.hop_form_lbl.configure(relief='flat')
		self.hop_form_lbl.configure(text='''Form:''')

		self.hop_form_combo = ttk.Combobox(self.hop_panedwindow2)
		self.hop_form_combo.place(relx=0.222, rely=0.152, relheight=0.046
				, relwidth=0.511, bordermode='ignore')
		self.hop_form_combo.configure(justify='center')
		self.hop_form_combo.configure(width=187)
		self.hop_form_combo.configure(takefocus="")
		self.hop_form_combo_values = ["Whole", "Pellet"]
		self.hop_form_combo.configure(values=self.hop_form_combo_values)

		self.hop_origin_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_origin_lbl.place(relx=0.056, rely=0.217, bordermode='ignore')
		self.hop_origin_lbl.configure(background=_bgcolor)
		self.hop_origin_lbl.configure(foreground="#000000")
		self.hop_origin_lbl.configure(font=font9)
		self.hop_origin_lbl.configure(relief='flat')
		self.hop_origin_lbl.configure(text='''Origin:''')

		self.hop_origin_ent = tk.Entry(self.hop_panedwindow2)
		self.hop_origin_ent.place(relx=0.222, rely=0.217, relheight=0.046
				, relwidth=0.511, bordermode='ignore')
		self.hop_origin_ent.configure(justify='center')
		self.hop_origin_ent.configure(width=184)
		self.hop_origin_ent.configure(takefocus="")
		self.hop_origin_ent.configure(cursor="xterm")

		self.hop_alpha_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_alpha_lbl.place(relx=0.056, rely=0.283, bordermode='ignore')
		self.hop_alpha_lbl.configure(background=_bgcolor)
		self.hop_alpha_lbl.configure(foreground="#000000")
		self.hop_alpha_lbl.configure(font=font9)
		self.hop_alpha_lbl.configure(relief='flat')
		self.hop_alpha_lbl.configure(text='''Alpha:''')

		self.hop_alpha_ent = tk.Entry(self.hop_panedwindow2)
		self.hop_alpha_ent.place(relx=0.222, rely=0.283, relheight=0.046
				, relwidth=0.456, bordermode='ignore')
		self.hop_alpha_ent.configure(justify='center')
		self.hop_alpha_ent.configure(takefocus="")
		self.hop_alpha_ent.configure(cursor="xterm")

		self.hop_alpha_percent = tk.Label(self.hop_panedwindow2)
		self.hop_alpha_percent.place(relx=0.694, rely=0.283, bordermode='ignore')
		self.hop_alpha_percent.configure(background=_bgcolor)
		self.hop_alpha_percent.configure(foreground="#000000")
		self.hop_alpha_percent.configure(font=font9)
		self.hop_alpha_percent.configure(relief='flat')
		self.hop_alpha_percent.configure(text='''%''')

		self.hop_use_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_use_lbl.place(relx=0.056, rely=0.348, bordermode='ignore')
		self.hop_use_lbl.configure(background=_bgcolor)
		self.hop_use_lbl.configure(foreground="#000000")
		self.hop_use_lbl.configure(font=font9)
		self.hop_use_lbl.configure(relief='flat')
		self.hop_use_lbl.configure(text='''Use:''')

		self.hop_use_combo = ttk.Combobox(self.hop_panedwindow2)
		self.hop_use_combo.place(relx=0.222, rely=0.348, relheight=0.046
				, relwidth=0.511, bordermode='ignore')
		self.hop_use_combo.configure(justify='center')
		self.hop_use_combo_values = ["Bittering", "Aroma", "General Purpose"]
		self.hop_use_combo.configure(values=self.hop_use_combo_values)
		self.hop_use_combo.configure(takefocus="")
		self.hop_comm_ent = tk.Entry(self.hop_panedwindow2)
		self.hop_comm_ent.place(relx=0.028, rely=0.5, relheight=0.046
				, relwidth=0.956, bordermode='ignore')
		self.hop_comm_ent.configure(width=344)
		self.hop_comm_ent.configure(takefocus="")
		self.hop_comm_ent.configure(cursor="xterm")

		self.hop_comm_lbl = tk.Label(self.hop_panedwindow2)
		self.hop_comm_lbl.place(relx=0.056, rely=0.453, bordermode='ignore')
		self.hop_comm_lbl.configure(background=_bgcolor)
		self.hop_comm_lbl.configure(foreground="#000000")
		self.hop_comm_lbl.configure(font=font9)
		self.hop_comm_lbl.configure(relief='flat')
		self.hop_comm_lbl.configure(text='''Comments:''')

		self.hop_cancel_butt = tk.Button(self.hop_panedwindow2)
		self.hop_cancel_butt.place(relx=0.028, rely=0.565, height=28, width=83
				, bordermode='ignore')
		self.hop_cancel_butt.configure(takefocus="")
		self.hop_cancel_butt.configure(text='''Cancel''')
		self.hop_cancel_butt.configure(command=lambda: self.show_data(self.hop_lstbx.get(tk.ACTIVE)))

		self.hop_clear_butt = tk.Button(self.hop_panedwindow2)
		self.hop_clear_butt.place(relx=0.389, rely=0.565, height=28, width=83
				, bordermode='ignore')
		self.hop_clear_butt.configure(takefocus="")
		self.hop_clear_butt.configure(text='''Clear Form''')
		self.hop_clear_butt.configure(command=self.clear_form)

		self.hop_done_butt = tk.Button(self.hop_panedwindow2)
		self.hop_done_butt.place(relx=0.75, rely=0.565, height=28, width=83
				, bordermode='ignore')
		self.hop_done_butt.configure(takefocus="")
		self.hop_done_butt.configure(text='''Done''')
		self.hop_done_butt.configure(command=self.done)

		self.hop_save_data_butt = tk.Button(self.hop_panedwindow2)
		self.hop_save_data_butt.place(relx=0.222, rely=0.696, relwidth=0.5713
				, relheight=0.2312, bordermode='ignore')
		self.hop_save_data_butt.configure(takefocus="")
		self.hop_save_data_butt.configure(text='''Save to Database''')
		self.hop_save_data_butt.configure(command=self.save)

		self.hop_lstbx.bind('<<ListboxSelect>>', self.select_listbox)
		self.show_data(list(sorted(brew_data.hop_data.keys()))[0])

	def __adjust_sash0(self, event):
		paned = event.widget
		pos = [400, ]
		i = 0
		for sash in pos:
			paned.sashpos(i, sash)
			i += 1
		paned.unbind('<map>', self.__funcid0)
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
		form = brew_data.hop_data[name]['Form']
		origin = brew_data.hop_data[name]['Origin']
		description = brew_data.hop_data[name]['Description']
		use = brew_data.hop_data[name]['Use']
		alpha = brew_data.hop_data[name]['Alpha']

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
		state = "disabled" if state == 0 else "normal"

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
		del brew_data.hop_data[self.name]
		brew_data.hop_data[name] = {'Form': form, 'Origin': origin, 'Description': description, 'Use': use, 'Alpha': alpha}
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
		name = 'New Hop {num}'.format(num=sum('New Hop' in s for s in brew_data.hop_data))
		self.hop_lstbx.insert(tk.END, name)
		try:
			brew_data.hop_data[name] = brew_data.hop_data[self.hop_lstbx.get(self.hop_lstbx.curselection())]
		except:
			try:
				brew_data.hop_data[name] = brew_data.hop_data[tk.ACTIVE]
			except:
				brew_data.hop_data[name] = {'Form': 'Whole', 'Origin': 'Unknown', 'Description': '', 'Use': 'General Purpose', 'Alpha': 12.7}
		self.show_data(name)
		self.hop_lstbx.select_set(tk.END)
		self.hop_lstbx.activate(tk.END)
		self.hop_lstbx.yview(tk.END)

	def save(self):
		with open(resource_path('hop_data.txt'), 'w') as f:
			for hop, value in brew_data.hop_data.items():
				name = hop
				type = value['Form']
				origin = value['Origin']
				alpha = value['Alpha']
				use = value['Use']
				description = value['Description']
				f.write('{name}\t{type}\t{origin}\t{alpha}\t{use}\t{description}\n'.format(name=name, type=type, origin=origin, alpha=alpha, use=use, description=description))

	def reinsert(self):
		self.hop_lstbx.delete(0, tk.END)
		for hop in sorted(brew_data.hop_data, key=lambda kv: kv.lower()):
			self.hop_lstbx.insert(tk.END, hop)

class grist_editor(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.widgets()

	def widgets(self):
		'''This class configures and populates the selflevel window.
		   self is the selflevel containing window.'''
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85'
		_ana2color = '#ececec' # Closest X11 color: 'gray92'
		font10 = "-family {DejaVu Sans} -size 10 -weight bold -slant "  \
			"roman -underline 0 -overstrike 0"
		font9 = "-family {DejaVu Sans} -size 9 -weight bold -slant "  \
			"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()
		self.style.configure('.',background=_bgcolor)
		self.style.configure('.',foreground=_fgcolor)
		self.style.configure('.',font="TkDefaultFont")
		self.style.map('.',background=
			[('selected', _compcolor), ('active',_ana2color)])

		self.grist_panedwindow1 = tk.LabelFrame(self, text='Fermentable Ingredients:', background=_bgcolor)
		self.grist_panedwindow1.place(relx=0.005, rely=0.005, relheight=0.990, relwidth=0.5)
		self.grist_panedwindow2 = tk.LabelFrame(self, text='Modifications:', background=_bgcolor)
		self.grist_panedwindow2.place(relx=0.510, rely=0.005, relheight=0.990, relwidth=0.485)		

		self.grist_lstbx = ScrolledListBox(self.grist_panedwindow1)
		self.grist_lstbx.place(relx=0.025, rely=0.043, relheight=0.887
				, relwidth=0.94, bordermode='ignore')
		self.grist_lstbx.configure(background="white")
		self.grist_lstbx.configure(font="TkFixedFont")
		self.grist_lstbx.configure(highlightcolor="#d9d9d9")
		self.grist_lstbx.configure(selectbackground="#c4c4c4")

		self.grist_delete_butt = tk.Button(self.grist_panedwindow1)
		self.grist_delete_butt.place(relx=0.025, rely=0.93, relheight=0.0589, relwidth=0.2075
				, bordermode='ignore')
		self.grist_delete_butt.configure(takefocus="")
		self.grist_delete_butt.configure(text='''Delete''')
		self.grist_delete_butt.configure(command=self.delete)

		self.grist_modify_butt = tk.Button(self.grist_panedwindow1)
		self.grist_modify_butt.place(relx=0.35, rely=0.93, relheight=0.0589, relwidth=0.2075
				, bordermode='ignore')
		self.grist_modify_butt.configure(takefocus="")
		self.grist_modify_butt.configure(text='''Modify''')
		self.grist_modify_butt.configure(command=lambda: self.input_state(1))

		self.grist_new_butt = tk.Button(self.grist_panedwindow1)
		self.grist_new_butt.place(relx=0.725, rely=0.93, relheight=0.0589, relwidth=0.2075
				, bordermode='ignore')
		self.grist_new_butt.configure(takefocus="")
		self.grist_new_butt.configure(text='''New''')
		self.grist_new_butt.configure(command=self.new)

		############################ Config Section ############################

		self.grist_name_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_name_lbl.place(relx=0.056, rely=0.087, bordermode='ignore')
		self.grist_name_lbl.configure(background=_bgcolor)
		self.grist_name_lbl.configure(foreground="#000000")
		self.grist_name_lbl.configure(font=font10)
		self.grist_name_lbl.configure(relief='flat')
		self.grist_name_lbl.configure(text='''Name:''')

		self.grist_name_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_name_ent.place(relx=0.222, rely=0.087, relheight=0.046
				, relwidth=0.511, bordermode='ignore')
		self.grist_name_ent.configure(justify='center')
		self.grist_name_ent.configure(foreground="#000000")
		self.grist_name_ent.configure(takefocus="")
		self.grist_name_ent.configure(cursor="xterm")

		self.grist_colour_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_colour_lbl.place(relx=0.056, rely=0.152, bordermode='ignore')
		self.grist_colour_lbl.configure(background=_bgcolor)
		self.grist_colour_lbl.configure(foreground="#000000")
		self.grist_colour_lbl.configure(font=font10)
		self.grist_colour_lbl.configure(relief='flat')
		self.grist_colour_lbl.configure(text='''Colour:''')

		self.grist_colour_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_colour_ent.place(relx=0.222, rely=0.152, relheight=0.046
				, relwidth=0.511, bordermode='ignore')
		self.grist_colour_ent.configure(justify='center')
		self.grist_colour_ent.configure(foreground="#000000")
		self.grist_colour_ent.configure(takefocus="")
		self.grist_colour_ent.configure(cursor="xterm")

		self.grist_colour_ebc = tk.Label(self.grist_panedwindow2)
		self.grist_colour_ebc.place(relx=0.75, rely=0.152, bordermode='ignore')
		self.grist_colour_ebc.configure(background=_bgcolor)
		self.grist_colour_ebc.configure(foreground="#000000")
		self.grist_colour_ebc.configure(font=font10)
		self.grist_colour_ebc.configure(relief='flat')
		self.grist_colour_ebc.configure(text='''EBC''')

		self.grist_extract_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_extract_lbl.place(relx=0.056, rely=0.217, bordermode='ignore')
		self.grist_extract_lbl.configure(background=_bgcolor)
		self.grist_extract_lbl.configure(foreground="#000000")
		self.grist_extract_lbl.configure(font=font10)
		self.grist_extract_lbl.configure(relief='flat')
		self.grist_extract_lbl.configure(text='''Extract:''')

		self.grist_extract_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_extract_ent.place(relx=0.222, rely=0.217, relheight=0.046
				, relwidth=0.511, bordermode='ignore')
		self.grist_extract_ent.configure(justify='center')
		self.grist_extract_ent.configure(foreground="#000000")
		self.grist_extract_ent.configure(takefocus="")
		self.grist_extract_ent.configure(cursor="xterm")

		self.grist_extract_ldk = tk.Label(self.grist_panedwindow2)
		self.grist_extract_ldk.place(relx=0.75, rely=0.217, bordermode='ignore')
		self.grist_extract_ldk.configure(background=_bgcolor)
		self.grist_extract_ldk.configure(foreground="#000000")
		self.grist_extract_ldk.configure(font=font10)
		self.grist_extract_ldk.configure(relief='flat')
		self.grist_extract_ldk.configure(text='''LDK''')

		self.grist_moisture_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_moisture_lbl.place(relx=0.056, rely=0.283, bordermode='ignore')
		self.grist_moisture_lbl.configure(background=_bgcolor)
		self.grist_moisture_lbl.configure(foreground="#000000")
		self.grist_moisture_lbl.configure(font=font10)
		self.grist_moisture_lbl.configure(relief='flat')
		self.grist_moisture_lbl.configure(text='''Moisture:''')

		self.grist_moisture_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_moisture_ent.place(relx=0.278, rely=0.283, relheight=0.046
				, relwidth=0.456, bordermode='ignore')
		self.grist_moisture_ent.configure(justify='center')
		self.grist_moisture_ent.configure(foreground="#000000")
		self.grist_moisture_ent.configure(takefocus="")
		self.grist_moisture_ent.configure(cursor="xterm")

		self.grist_moisture_percent = tk.Label(self.grist_panedwindow2)
		self.grist_moisture_percent.place(relx=0.75, rely=0.283, bordermode='ignore')
		self.grist_moisture_percent.configure(background=_bgcolor)
		self.grist_moisture_percent.configure(foreground="#000000")
		self.grist_moisture_percent.configure(font=font10)
		self.grist_moisture_percent.configure(relief='flat')
		self.grist_moisture_percent.configure(text='''%''')


		self.grist_ferment_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_ferment_lbl.place(relx=0.056, rely=0.348, bordermode='ignore')
		self.grist_ferment_lbl.configure(background=_bgcolor)
		self.grist_ferment_lbl.configure(foreground="#000000")
		self.grist_ferment_lbl.configure(font=font9)
		self.grist_ferment_lbl.configure(relief='flat')
		self.grist_ferment_lbl.configure(text='''Fermentability:''')

		self.grist_ferment_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_ferment_ent.place(relx=0.361, rely=0.348, relheight=0.046
				, relwidth=0.372, bordermode='ignore')
		self.grist_ferment_ent.configure(takefocus="")
		self.grist_ferment_ent.configure(cursor="xterm")
		self.grist_ferment_ent.configure(justify='center')

		self.grist_ferment_percent = tk.Label(self.grist_panedwindow2)
		self.grist_ferment_percent.place(relx=0.75, rely=0.348, bordermode='ignore')
		self.grist_ferment_percent.configure(background=_bgcolor)
		self.grist_ferment_percent.configure(foreground="#000000")
		self.grist_ferment_percent.configure(font=font10)
		self.grist_ferment_percent.configure(relief='flat')
		self.grist_ferment_percent.configure(text='''%''')

		self.grist_type_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_type_lbl.place(relx=0.056, rely=0.413, bordermode='ignore')
		self.grist_type_lbl.configure(background=_bgcolor)
		self.grist_type_lbl.configure(foreground="#000000")
		self.grist_type_lbl.configure(font=font10)
		self.grist_type_lbl.configure(relief='flat')
		self.grist_type_lbl.configure(text='''Type:''')

		self.grist_type_combo = ttk.Combobox(self.grist_panedwindow2)
		self.grist_type_combo.place(relx=0.194, rely=0.413, relheight=0.046
				, relwidth=0.547, bordermode='ignore')
		self.grist_type_combo.configure(width=197)
		self.grist_type_combo.configure(takefocus="")
		self.grist_type_combo_values = ['Primary Malt', 'Secondary Malt', 'Mash Tun Adjunct', 'Can Be Steeped', 'Malt Extract', 'Copper Sugar']
		#print([vals['Type'] for (grist, vals) in brew_data.grist_data.items()])
		#print([grist['Type'] for key, grist in brew_data.grist_data.items() if grist['Type'] not in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]])
		self.grist_type_combo_values.append([grist['Type'] for key, grist in brew_data.grist_data.items() if grist['Type'] not in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]])
		self.grist_type_combo.configure(values=self.grist_type_combo_values)

		self.grist_comm_lbl = tk.Label(self.grist_panedwindow2)
		self.grist_comm_lbl.place(relx=0.056, rely=0.543, bordermode='ignore')
		self.grist_comm_lbl.configure(background=_bgcolor)
		self.grist_comm_lbl.configure(foreground="#000000")
		self.grist_comm_lbl.configure(font=font10)
		self.grist_comm_lbl.configure(relief='flat')
		self.grist_comm_lbl.configure(text='''Comments:''')

		self.grist_comm_ent = tk.Entry(self.grist_panedwindow2)
		self.grist_comm_ent.place(relx=0.028, rely=0.587, relheight=0.046
				, relwidth=0.956, bordermode='ignore')
		self.grist_comm_ent.configure(foreground="#000000")
		self.grist_comm_ent.configure(takefocus="")
		self.grist_comm_ent.configure(cursor="xterm")

		self.grist_cancel_butt = tk.Button(self.grist_panedwindow2)
		self.grist_cancel_butt.place(relx=0.028, rely=0.652, height=28, width=83
				, bordermode='ignore')
		self.grist_cancel_butt.configure(takefocus="")
		self.grist_cancel_butt.configure(text='''Cancel''')
		self.grist_cancel_butt.configure(command=lambda: self.show_data(self.grist_lstbx.get(tk.ACTIVE)))

		self.grist_clear_butt = tk.Button(self.grist_panedwindow2)
		self.grist_clear_butt.place(relx=0.389, rely=0.652, height=28, width=83
				, bordermode='ignore')
		self.grist_clear_butt.configure(takefocus="")
		self.grist_clear_butt.configure(text='''Clear Form''')
		self.grist_clear_butt.configure(command=self.clear_form)

		self.grist_done_butt = tk.Button(self.grist_panedwindow2)
		self.grist_done_butt.place(relx=0.75, rely=0.652, height=28, width=83
				, bordermode='ignore')
		self.grist_done_butt.configure(takefocus="")
		self.grist_done_butt.configure(text='''Done''')
		self.grist_done_butt.configure(command=self.done)

		self.grist_save_data_butt = tk.Button(self.grist_panedwindow2)
		self.grist_save_data_butt.place(relx=0.222, rely=0.739, relwidth=0.5713
				, relheight=0.2312, bordermode='ignore')
		self.grist_save_data_butt.configure(takefocus="")
		self.grist_save_data_butt.configure(text='''Save to Database''')
		self.grist_save_data_butt.configure(command=self.save)


		self.input_state(0)

		self.grist_lstbx.bind('<<ListboxSelect>>', self.select_listbox)

		self.show_data(list(sorted(brew_data.grist_data.keys()))[0])
	def __adjust_sash0(self, event):
		paned = event.widget
		pos = [400, ]
		i = 0
		for sash in pos:
			paned.sashpos(i, sash)
			i += 1
		paned.unbind('<map>', self.__funcid0)
		del self.__funcid0

	def select_listbox(self, event):
		try:
			self.show_data(self.grist_lstbx.get(self.grist_lstbx.curselection()))
		except:
			pass

	def show_data(self, grist):
		self.name = grist
		name = grist
		colour = brew_data.grist_data[name]['EBC']
		extract = brew_data.grist_data[name]['Extract']
		moisture = brew_data.grist_data[name]['Moisture']
		fermentability = brew_data.grist_data[name]['Fermentability']
		description = brew_data.grist_data[name]['Description']
		type = int(float(brew_data.grist_data[name]['Type']))

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

		state = "disabled" if state == 0 else "normal"

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
		name = 'New Grist {num}'.format(num=sum('New Grist' in s for s in brew_data.grist_data))
		self.grist_lstbx.insert(tk.END, name)
		try:
			brew_data.grist_data[name] = brew_data.grist_data[self.grist_lstbx.get(self.grist_lstbx.curselection())]
		except:
			try:
				brew_data.grist_data[name] = brew_data.grist_data[tk.ACTIVE]
			except:
				brew_data.grist_data[name] = {'EBC': 0.0, 'Type': 3.0, 'Extract': 0.0, 'Description': 'No Description', 'Moisture': 0.0, 'Fermentability': 62.0}

		self.show_data(name)
		self.grist_lstbx.select_set(tk.END)
		self.grist_lstbx.activate(tk.END)
		self.grist_lstbx.yview(tk.END)

	def save(self):
		with open(resource_path('grain_data.txt'), 'w') as f:
			for ingredient, value in brew_data.grist_data.items():
				name = ingredient
				ebc = value['EBC']
				type = value['Type']
				extract = value['Extract']
				moisture = value['Moisture']
				fermentability = value['Fermentability']
				description = value['Description']
				f.write('{name}\t{ebc}\t{type}\t{extract}\t{moisture}\t{fermentability}\t{description}\n'.format(name=name, ebc=ebc, type=type, extract=extract, moisture=moisture, fermentability=fermentability, description=description))

	def done(self):
		name = self.grist_name_ent.get()
		colour = float(self.grist_colour_ent.get())
		extract = float( self.grist_extract_ent.get())
		moisture = float(self.grist_moisture_ent.get())
		fermentability = float(self.grist_ferment_ent.get())
		description = self.grist_comm_ent.get()
		type = self.grist_type_combo_values.index(self.grist_type_combo.get()) + 1
		del brew_data.grist_data[self.name]
		brew_data.grist_data[name] = {'EBC': colour, 'Type': type, 'Extract': extract, 'Description': description, 'Moisture': moisture, 'Fermentability': fermentability}
		#print(brew_data.grist_data[name])
		idx = list(sorted(brew_data.grist_data.keys())).index(name)
		self.reinsert()
		self.show_data(name)

	def reinsert(self):
		self.grist_lstbx.delete(0, tk.END)
		for hop in sorted(brew_data.grist_data, key=lambda kv: kv.lower()):
			self.grist_lstbx.insert(tk.END, hop)

class defaults_editor(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, background=_bgcolor)

		self.widgets()
		self.reset_to_defaults()

	def widgets(self):
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85'
		_ana2color = '#ececec' # Closest X11 color: 'gray92'
		font9 = "-family {DejaVu Sans} -size 10 -weight bold -slant "  \
			"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()
		self.style.configure('.',background=_bgcolor)
		self.style.configure('.',foreground=_fgcolor)
		self.style.configure('.',font="TkDefaultFont")
		self.style.map('.',background=
			[('selected', _compcolor), ('active',_ana2color)])

		self.target_vol_lbl = tk.Label(self)
		self.target_vol_lbl.place(relx=0.038, rely=0.063, height=19, width=118)
		self.target_vol_lbl.configure(background=_bgcolor)
		self.target_vol_lbl.configure(foreground="#000000")
		self.target_vol_lbl.configure(font=font9)
		self.target_vol_lbl.configure(relief='flat')
		self.target_vol_lbl.configure(text='''Target Volume:''')

		self.boil_vol_lbl = tk.Label(self)
		self.boil_vol_lbl.place(relx=0.038, rely=0.148, height=19, width=143)
		self.boil_vol_lbl.configure(background=_bgcolor)
		self.boil_vol_lbl.configure(foreground="#000000")
		self.boil_vol_lbl.configure(font=font9)
		self.boil_vol_lbl.configure(relief='flat')
		self.boil_vol_lbl.configure(text='''Boil Volume Scale:''')

		self.liquor_to_grist_lbl = tk.Label(self)
		self.liquor_to_grist_lbl.place(relx=0.038, rely=0.317, height=19
				, width=165)
		self.liquor_to_grist_lbl.configure(background=_bgcolor)
		self.liquor_to_grist_lbl.configure(foreground="#000000")
		self.liquor_to_grist_lbl.configure(font=font9)
		self.liquor_to_grist_lbl.configure(relief='flat')
		self.liquor_to_grist_lbl.configure(text='''Liquor To Grist Ratio:''')

		self.target_vol_ent = tk.Entry(self)
		self.target_vol_ent.place(relx=0.202, rely=0.063, relheight=0.044
				, relwidth=0.106)
		self.target_vol_ent.configure(justify='center')
		self.target_vol_ent.configure(width=84)
		self.target_vol_ent.configure(takefocus="")
		self.target_vol_ent.configure(cursor="xterm")

		self.boil_vol_ent = tk.Entry(self)
		self.boil_vol_ent.place(relx=0.227, rely=0.148, relheight=0.044
				, relwidth=0.106)
		self.boil_vol_ent.configure(justify='center')
		self.boil_vol_ent.configure(takefocus="")
		self.boil_vol_ent.configure(cursor="xterm")

		self.liquor_to_grist_ent = tk.Entry(self)
		self.liquor_to_grist_ent.place(relx=0.253, rely=0.317, relheight=0.044
				, relwidth=0.106)
		self.liquor_to_grist_ent.configure(justify='center')
		self.liquor_to_grist_ent.configure(takefocus="")
		self.liquor_to_grist_ent.configure(cursor="xterm")

		self.target_vol_litres_lbl = tk.Label(self)
		self.target_vol_litres_lbl.place(relx=0.316, rely=0.063, height=19
				, width=46)
		self.target_vol_litres_lbl.configure(background=_bgcolor)
		self.target_vol_litres_lbl.configure(foreground="#000000")
		self.target_vol_litres_lbl.configure(font=font9)
		self.target_vol_litres_lbl.configure(relief='flat')
		self.target_vol_litres_lbl.configure(text='''Litres''')

		self.mash_efficiency_lbl = tk.Label(self)
		self.mash_efficiency_lbl.place(relx=0.038, rely=0.233, height=19
				, width=125)
		self.mash_efficiency_lbl.configure(background=_bgcolor)
		self.mash_efficiency_lbl.configure(foreground="#000000")
		self.mash_efficiency_lbl.configure(font=font9)
		self.mash_efficiency_lbl.configure(relief='flat')
		self.mash_efficiency_lbl.configure(text='''Mash Efficiency:''')

		self.mash_efficiency_ent = tk.Entry(self)
		self.mash_efficiency_ent.place(relx=0.215, rely=0.233, relheight=0.044
				, relwidth=0.106)
		self.mash_efficiency_ent.configure(justify='center')
		self.mash_efficiency_ent.configure(takefocus="")
		self.mash_efficiency_ent.configure(cursor="xterm")

		self.boil_vol_percent_lbl = tk.Label(self)
		self.boil_vol_percent_lbl.place(relx=0.341, rely=0.148, height=19
				, width=15)
		self.boil_vol_percent_lbl.configure(background=_bgcolor)
		self.boil_vol_percent_lbl.configure(foreground="#000000")
		self.boil_vol_percent_lbl.configure(font=font9)
		self.boil_vol_percent_lbl.configure(relief='flat')
		self.boil_vol_percent_lbl.configure(text='''%''')

		self.mash_efficiency_percent_lbl = tk.Label(self)
		self.mash_efficiency_percent_lbl.place(relx=0.328, rely=0.233, height=19
				, width=15)
		self.mash_efficiency_percent_lbl.configure(background=_bgcolor)
		self.mash_efficiency_percent_lbl.configure(foreground="#000000")
		self.mash_efficiency_percent_lbl.configure(font=font9)
		self.mash_efficiency_percent_lbl.configure(relief='flat')
		self.mash_efficiency_percent_lbl.configure(text='''%''')

		self.liquor_to_grist_lperkg_lbl = tk.Label(self)
		self.liquor_to_grist_lperkg_lbl.place(relx=0.366, rely=0.317, height=19
				, width=35)
		self.liquor_to_grist_lperkg_lbl.configure(background=_bgcolor)
		self.liquor_to_grist_lperkg_lbl.configure(foreground="#000000")
		self.liquor_to_grist_lperkg_lbl.configure(font=font9)
		self.liquor_to_grist_lperkg_lbl.configure(relief='flat')
		self.liquor_to_grist_lperkg_lbl.configure(text='''L/kg''')

		self.save_all_butt = tk.Button(self)
		self.save_all_butt.place(relx=0.808, rely=0.93, height=28, width=143)
		self.save_all_butt.configure(takefocus="")
		self.save_all_butt.configure(text='''Save All As Defaults''')
		self.save_all_butt.configure(command=self.save_all)

		self.done_button = tk.Button(self)
		self.done_button.place(relx=0.694, rely=0.93, height=28, width=83)
		self.done_button.configure(takefocus="")
		self.done_button.configure(text='''Done''')
		self.done_button.configure(command=self.temp_save)

		self.reset_to_defaults_butt = tk.Button(self)
		self.reset_to_defaults_butt.place(relx=0.013, rely=0.93, height=28, width=190)
		self.reset_to_defaults_butt.configure(takefocus="")
		self.reset_to_defaults_butt.configure(text='''Reset to Local Database''')
		self.reset_to_defaults_butt.configure(command=self.reset_to_defaults)

		self.attenuation_defaults_lbl= tk.Label(self)
		self.attenuation_defaults_lbl.place(relx=0.038, rely=0.402, height=19
				, width=155)
		self.attenuation_defaults_lbl.configure(background=_bgcolor)
		self.attenuation_defaults_lbl.configure(foreground="#000000")
		self.attenuation_defaults_lbl.configure(font=font9)
		self.attenuation_defaults_lbl.configure(relief='flat')
		self.attenuation_defaults_lbl.configure(text='''Attenuation Default:''')
		self.attenuation_defaults_lbl.configure(width=155)

		self.attenuation_types = ['Low', 'Medium', 'High']
		self.attenuation_type_var = tk.StringVar()
		self.attenuation_type_combo = tk.OptionMenu(self, self.attenuation_type_var, *self.attenuation_types)
		self.attenuation_type_combo.place(relx=0.253, rely=0.402, relheight=0.064
				, relwidth=0.16)
		self.attenuation_type_combo.configure(width=127)
		self.attenuation_type_combo.configure(takefocus="")

		self.attenuation_temps = [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]
		self.attenuation_temp_var = tk.StringVar()
		self.attenuation_temp_combo = tk.OptionMenu(self, self.attenuation_temp_var, *self.attenuation_temps)
		self.attenuation_temp_combo.place(relx=0.429, rely=0.402, relheight=0.064
				, relwidth=0.072)
		self.attenuation_temp_combo.configure(width=57)
		self.attenuation_temp_combo.configure(takefocus="")

		self.save_on_close_lbl = tk.Label(self)
		self.save_on_close_lbl.place(relx=0.038, rely=0.486)
		self.save_on_close_lbl.configure(background=_bgcolor)
		self.save_on_close_lbl.configure(foreground="#000000")
		self.save_on_close_lbl.configure(font=font9)
		self.save_on_close_lbl.configure(relief='flat')
		self.save_on_close_lbl.configure(text='''Save on Close:''')

		self.save_on_close_var = tk.StringVar()
		self.save_on_close_combo = tk.OptionMenu(self, self.save_on_close_var, 'True', 'False')
		self.save_on_close_combo.place(relx=0.202, rely=0.486, relheight=0.064
				, relwidth=0.122)
		self.save_on_close_combo.configure(width=97)
		self.save_on_close_combo.configure(takefocus="")

		self.default_boil_time_lbl = tk.Label(self)
		self.default_boil_time_lbl.place(relx=0.038, rely=0.571)
		self.default_boil_time_lbl.configure(background=_bgcolor)
		self.default_boil_time_lbl.configure(foreground="#000000")
		self.default_boil_time_lbl.configure(font=font9)
		self.default_boil_time_lbl.configure(relief='flat')
		self.default_boil_time_lbl.configure(text='''Default Boil Time:''')

		self.default_boil_time_spinbox = tk.Spinbox(self, from_=1.0, to=100.0)
		self.default_boil_time_spinbox.place(relx=0.227, rely=0.571, relheight=0.049
				, relwidth=0.086)
		self.default_boil_time_spinbox.configure(activebackground="#f9f9f9")
		self.default_boil_time_spinbox.configure(background="white")
		self.default_boil_time_spinbox.configure(highlightbackground="black")
		self.default_boil_time_spinbox.configure(selectbackground="#c4c4c4")
		self.default_boil_time_spinbox.configure(width=68)

		self.default_boil_time_min_lbl = tk.Label(self)
		self.default_boil_time_min_lbl.place(relx=0.328, rely=0.571, height=19
				, width=65)
		self.default_boil_time_min_lbl.configure(background=_bgcolor)
		self.default_boil_time_min_lbl.configure(foreground="#000000")
		self.default_boil_time_min_lbl.configure(font=font9)
		self.default_boil_time_min_lbl.configure(relief='flat')
		self.default_boil_time_min_lbl.configure(text='''Minutes''')

		self.replace_default_vars = tk.Label(self)
		# self.replace_default_vars.place(relx=0.038, rely=0.655)
		self.replace_default_vars.configure(background=_bgcolor)
		self.replace_default_vars.configure(foreground="#000000")
		self.replace_default_vars.configure(font=font9)
		self.replace_default_vars.configure(relief='flat')
		self.replace_default_vars.configure(text='''Update Default Configuration:''')

		self.replace_default_vars_chckbutt = tk.Checkbutton(self)
		# self.replace_default_vars_chckbutt.place(relx=0.328, rely=0.655
				# , relheight=0.049, relwidth=0.034)
		self.replace_default_vars_chckbutt.configure(background=_bgcolor)
		self.replace_default_vars_chckbutt.configure(justify='left')
		self.replace_default_vars_variable = tk.BooleanVar()
		self.replace_default_vars_chckbutt.configure(variable=self.replace_default_vars_variable)


	def reset_to_defaults(self):
		self.target_vol_ent.delete(0, tk.END)
		self.boil_vol_ent.delete(0, tk.END)
		self.mash_efficiency_ent.delete(0, tk.END)
		self.liquor_to_grist_ent.delete(0, tk.END)

		with open(resource_path('defaults.txt'), 'r') as f:
			data = [line.strip().split('=') for line in f]
			for constants in data:
				if constants[0] == 'efficiency': self.mash_efficiency_ent.insert(0, float(constants[1])) #float(constants[1])/100
				elif constants[0] == 'volume': self.target_vol_ent.insert(0, float(constants[1]))
				elif constants[0] == 'evaporation': self.boil_vol_ent.insert(0, float(constants[1])+100) #(float(constants[1])/100)+1
				elif constants[0] == 'LGratio': self.liquor_to_grist_ent.insert(0, float(constants[1]))
				elif constants[0] == 'attenuation':
					type = constants[1].split('-')[0]
					self.attenuation_type_var.set(type if type != 'med' else 'Medium')
					temp = constants[1].split('-')[1]
					self.attenuation_temp_var.set(temp)
				elif constants[0] == 'save_close':
					self.save_on_close_var.set(constants[1])
				elif constants[0] == 'boil_time':
					self.default_boil_time_spinbox.delete(0, tk.END)
					self.default_boil_time_spinbox.insert(0, constants[1])
				elif constants[0] == 'replace_defaults':
					self.replace_default_vars_variable.set(False if constants[1] == 'True' else True)

	def save_all(self):
		with open(resource_path('defaults.txt'), 'w') as f:
			volume = float(self.target_vol_ent.get())
			efficiency = float(self.mash_efficiency_ent.get())
			evaporation = (float(self.boil_vol_ent.get())-100) #round((brew_data.constants['Boil Volume Scale']-1)*100, 1)
			LGratio = float(self.liquor_to_grist_ent.get())
			attenuation_type = self.attenuation_type_var.get().lower()
			attenuation_temp = self.attenuation_temp_var.get()
			attenuation = (attenuation_type if attenuation_type != 'medium' else 'med') + '-' + (attenuation_temp)
			save_close = self.save_on_close_var.get()
			boil_time = self.default_boil_time_spinbox.get()
			replace_defaults = not self.replace_default_vars_variable.get()
			f.write('efficiency={efficiency}\nvolume={volume}\nevaporation={evaporation}\nLGratio={LGratio}\nattenuation={attenuation}\nsave_close={save_close}\nboil_time={boil_time}\nreplace_defaults={replace_defaults}'.format(efficiency=efficiency, volume=volume, evaporation=evaporation, LGratio=LGratio,
																																																									attenuation=attenuation, save_close=save_close, boil_time=boil_time, replace_defaults=replace_defaults))
		self.temp_save()

	def temp_save(self):
		brew_data.constants['Volume'] = float(self.target_vol_ent.get())
		brew_data.constants['Efficiency'] = float(self.mash_efficiency_ent.get())/100
		brew_data.constants['Boil Volume Scale'] = (float(self.boil_vol_ent.get())/100)
		brew_data.constants['Liquor To Grist Ratio'] = float(self.liquor_to_grist_ent.get())
		brew_data.constants['Save On Close'] = True if self.save_on_close_var.get() == 'True' else False
		brew_data.constants['Default Boil Time'] = int(self.default_boil_time_spinbox.get())
		brew_data.constants['Replace Defaults'] = True if self.save_on_close_var.get() == 'True' else False

	def open_locals(self):
		self.target_vol_ent.delete(0, tk.END)
		self.boil_vol_ent.delete(0, tk.END)
		self.mash_efficiency_ent.delete(0, tk.END)
		self.liquor_to_grist_ent.delete(0, tk.END)
		self.default_boil_time_spinbox.delete(0, tk.END)

		self.mash_efficiency_ent.insert(0, brew_data.constants['Efficiency']*100)
		self.target_vol_ent.insert(0, brew_data.constants['Volume'])
		self.boil_vol_ent.insert(0, round(brew_data.constants['Boil Volume Scale']*100, 1))
		self.liquor_to_grist_ent.insert(0,  brew_data.constants['Liquor To Grist Ratio'])
		self.default_boil_time_spinbox.insert(0, brew_data.constants['Default Boil Time'])
		self.replace_default_vars_variable.set(not brew_data.constants['Replace Defaults'])
class special_editor(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, background=_bgcolor)
		self.current_attenuation = tk.StringVar()
		self.widgets()
		#self.attenuation_frame.bind('<Button-1>', lambda evt: print(self.current_attenuation.get()))
		self.current_attenuation.set(brew_data.constants['Attenuation Default'])
		self.original_additions = list(sorted(brew_data.water_chemistry_additions)) + list(sorted(brew_data.yeast_data))
		self.added_additions = []
		self.refresh_orig()
		self.refresh_add()

	def widgets(self):
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85'
		_ana2color = '#ececec' # Closest X11 color: 'gray92'
		font9 = "-family {DejaVu Sans} -size 9 -weight normal -slant "  \
			"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()
		self.style.configure('.',background=_bgcolor)
		self.style.configure('.',foreground=_fgcolor)
		self.style.configure('.',font="TkDefaultFont")
		self.style.map('.',background=
			[('selected', _compcolor), ('active',_ana2color)])
		'''
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
		  'low-62': 51, 'med-62': 59, 'high-62': 66,
		  'low-63': 52, 'med-63': 60, 'high-63': 68,
		  'low-64': 53, 'med-64': 61, 'high-64': 69,
		  'low-65': 53, 'med-65': 61, 'high-65': 69,
		  'low-66': 53, 'med-66': 61, 'high-66': 69,
		  'low-67': 53, 'med-67': 61, 'high-67': 69,
		  'low-68': 52, 'med-68': 60, 'high-68': 67,
		  'low-69': 51, 'med-69': 58, 'high-69': 66,
		  'low-70': 49, 'med-70': 56, 'high-70': 63,
		  'low-71': 47, 'med-71': 54, 'high-71': 61,
		  'low-72': 44, 'med-72': 51, 'high-72': 57
		}

		self.attenuation_frame = tk.LabelFrame(self)
		self.attenuation_frame.place(relx=0.013, rely=0.021, relheight=0.591
			, relwidth=0.227)
		#self.attenuation_frame.configure(relief='')
		self.attenuation_frame.configure(text='''Yeast Attenuation''')
		self.attenuation_frame.configure(width=180)
		self.attenuation_frame.configure(background=_bgcolor)

		self.attenuation_low_lbl = tk.Label(self.attenuation_frame)
		self.attenuation_low_lbl.place(relx=0.278, rely=0.109, height=19
			, width=28, bordermode='ignore')
		self.attenuation_low_lbl.configure(background=_bgcolor)
		self.attenuation_low_lbl.configure(foreground="#000000")
		self.attenuation_low_lbl.configure(font="TkDefaultFont")
		self.attenuation_low_lbl.configure(relief='flat')
		self.attenuation_low_lbl.configure(text='''Low''')

		self.attenuation_med_lbl = tk.Label(self.attenuation_frame)
		self.attenuation_med_lbl.place(relx=0.5, rely=0.109, height=19, width=30
			, bordermode='ignore')
		self.attenuation_med_lbl.configure(background=_bgcolor)
		self.attenuation_med_lbl.configure(foreground="#000000")
		self.attenuation_med_lbl.configure(font="TkDefaultFont")
		self.attenuation_med_lbl.configure(relief='flat')
		self.attenuation_med_lbl.configure(text='''Med''')

		self.attenuation_high_lbl = tk.Label(self.attenuation_frame)
		self.attenuation_high_lbl.place(relx=0.722, rely=0.109, height=19
			, width=42, bordermode='ignore')
		self.attenuation_high_lbl.configure(background=_bgcolor)
		self.attenuation_high_lbl.configure(foreground="#000000")
		self.attenuation_high_lbl.configure(font="TkDefaultFont")
		self.attenuation_high_lbl.configure(relief='flat')
		self.attenuation_high_lbl.configure(text='''High''')
		self.attenuation_high_lbl.configure(width=42)


		self.attenuation_62_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_62_degrees.place(relx=0.056, rely=0.182, height=19
			, width=34, bordermode='ignore')
		self.attenuation_62_degrees.configure(background=_bgcolor)
		self.attenuation_62_degrees.configure(foreground="#000000")
		self.attenuation_62_degrees.configure(font="TkDefaultFont")
		self.attenuation_62_degrees.configure(relief='flat')
		self.attenuation_62_degrees.configure(text='''62°C''')

		self.attenuation_63_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_63_degrees.place(relx=0.056, rely=0.255, height=19
			, width=34, bordermode='ignore')
		self.attenuation_63_degrees.configure(background=_bgcolor)
		self.attenuation_63_degrees.configure(foreground="#000000")
		self.attenuation_63_degrees.configure(font="TkDefaultFont")
		self.attenuation_63_degrees.configure(relief='flat')
		self.attenuation_63_degrees.configure(text='''63°C''')

		self.attenuation_64_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_64_degrees.place(relx=0.056, rely=0.327, height=19
			, width=34, bordermode='ignore')
		self.attenuation_64_degrees.configure(background=_bgcolor)
		self.attenuation_64_degrees.configure(foreground="#000000")
		self.attenuation_64_degrees.configure(font="TkDefaultFont")
		self.attenuation_64_degrees.configure(relief='flat')
		self.attenuation_64_degrees.configure(text='''64°C''')

		self.attenuation_65_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_65_degrees.place(relx=0.056, rely=0.4, height=19
			, width=34, bordermode='ignore')
		self.attenuation_65_degrees.configure(background=_bgcolor)
		self.attenuation_65_degrees.configure(foreground="#000000")
		self.attenuation_65_degrees.configure(font="TkDefaultFont")
		self.attenuation_65_degrees.configure(relief='flat')
		self.attenuation_65_degrees.configure(text='''65°C''')

		self.attenuation_66_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_66_degrees.place(relx=0.056, rely=0.473, height=19
			, width=34, bordermode='ignore')
		self.attenuation_66_degrees.configure(background=_bgcolor)
		self.attenuation_66_degrees.configure(foreground="#000000")
		self.attenuation_66_degrees.configure(font="TkDefaultFont")
		self.attenuation_66_degrees.configure(relief='flat')
		self.attenuation_66_degrees.configure(text='''66°C''')

		self.attenuation_67_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_67_degrees.place(relx=0.056, rely=0.545, height=19
			, width=34, bordermode='ignore')
		self.attenuation_67_degrees.configure(background=_bgcolor)
		self.attenuation_67_degrees.configure(foreground="#000000")
		self.attenuation_67_degrees.configure(font="TkDefaultFont")
		self.attenuation_67_degrees.configure(relief='flat')
		self.attenuation_67_degrees.configure(text='''67°C''')


		self.attenuation_68_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_68_degrees.place(relx=0.056, rely=0.618, height=19
			, width=34, bordermode='ignore')
		self.attenuation_68_degrees.configure(background=_bgcolor)
		self.attenuation_68_degrees.configure(foreground="#000000")
		self.attenuation_68_degrees.configure(font="TkDefaultFont")
		self.attenuation_68_degrees.configure(relief='flat')
		self.attenuation_68_degrees.configure(text='''68°C''')

		self.attenuation_69_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_69_degrees.place(relx=0.056, rely=0.691, height=19
			, width=34, bordermode='ignore')
		self.attenuation_69_degrees.configure(background=_bgcolor)
		self.attenuation_69_degrees.configure(foreground="#000000")
		self.attenuation_69_degrees.configure(font="TkDefaultFont")
		self.attenuation_69_degrees.configure(relief='flat')
		self.attenuation_69_degrees.configure(text='''69°C''')

		self.attenuation_70_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_70_degrees.place(relx=0.056, rely=0.764, height=19
			, width=34, bordermode='ignore')
		self.attenuation_70_degrees.configure(background=_bgcolor)
		self.attenuation_70_degrees.configure(foreground="#000000")
		self.attenuation_70_degrees.configure(font="TkDefaultFont")
		self.attenuation_70_degrees.configure(relief='flat')
		self.attenuation_70_degrees.configure(text='''70°C''')

		self.attenuation_71_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_71_degrees.place(relx=0.056, rely=0.836, height=19
			, width=34, bordermode='ignore')
		self.attenuation_71_degrees.configure(background=_bgcolor)
		self.attenuation_71_degrees.configure(foreground="#000000")
		self.attenuation_71_degrees.configure(font="TkDefaultFont")
		self.attenuation_71_degrees.configure(relief='flat')
		self.attenuation_71_degrees.configure(text='''71°C''')

		self.attenuation_72_degrees = tk.Label(self.attenuation_frame)
		self.attenuation_72_degrees.place(relx=0.056, rely=0.909, height=19
			, width=34, bordermode='ignore')
		self.attenuation_72_degrees.configure(background=_bgcolor)
		self.attenuation_72_degrees.configure(foreground="#000000")
		self.attenuation_72_degrees.configure(font="TkDefaultFont")
		self.attenuation_72_degrees.configure(relief='flat')
		self.attenuation_72_degrees.configure(text='''72°C''')

		####################################### Low #######################################
		self.attenuation_low_62 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_62.place(relx=0.278, rely=0.182, relheight=0.084
			, relwidth=0.172, bordermode='ignore')
		self.attenuation_low_62.configure(justify='left')
		self.attenuation_low_62.configure(value='low-62')
		self.attenuation_low_62.configure(activebackground="#f9f9f9")
		self.attenuation_low_62.configure(background=_bgcolor)
		self.attenuation_low_62.configure(variable=self.current_attenuation)

		self.attenuation_low_63 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_63.place(relx=0.278, rely=0.255, relheight=0.084
			, relwidth=0.172, bordermode='ignore')
		self.attenuation_low_63.configure(activebackground="#f9f9f9")
		self.attenuation_low_63.configure(background=_bgcolor)
		self.attenuation_low_63.configure(justify='left')
		self.attenuation_low_63.configure(value='low-63')
		self.attenuation_low_63.configure(variable=self.current_attenuation)

		self.attenuation_low_64 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_64.place(relx=0.278, rely=0.327, relheight=0.084
			, relwidth=0.172, bordermode='ignore')
		self.attenuation_low_64.configure(activebackground="#f9f9f9")
		self.attenuation_low_64.configure(background=_bgcolor)
		self.attenuation_low_64.configure(justify='left')
		self.attenuation_low_64.configure(value='low-64')
		self.attenuation_low_64.configure(variable=self.current_attenuation)

		self.attenuation_low_65 = tk.Radiobutton(self)
		self.attenuation_low_65.place(relx=0.076, rely=0.254, relheight=0.049
			, relwidth=0.039)
		self.attenuation_low_65.configure(activebackground="#f9f9f9")
		self.attenuation_low_65.configure(background=_bgcolor)
		self.attenuation_low_65.configure(justify='left')
		self.attenuation_low_65.configure(value='low-65')
		self.attenuation_low_65.configure(variable=self.current_attenuation)
		self.attenuation_low_66 = tk.Radiobutton(self)
		self.attenuation_low_66.place(relx=0.076, rely=0.296
			, relheight=0.049, relwidth=0.039)
		self.attenuation_low_66.configure(activebackground="#f9f9f9")
		self.attenuation_low_66.configure(background=_bgcolor)
		self.attenuation_low_66.configure(justify='left')
		self.attenuation_low_66.configure(value='low-66')
		self.attenuation_low_66.configure(variable=self.current_attenuation)

		self.attenuation_low_67 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_67.place(relx=0.278, rely=0.545, relheight=0.084
			, relwidth=0.172, bordermode='ignore')
		self.attenuation_low_67.configure(activebackground="#f9f9f9")
		self.attenuation_low_67.configure(background=_bgcolor)
		self.attenuation_low_67.configure(justify='left')
		self.attenuation_low_67.configure(value='low-67')
		self.attenuation_low_67.configure(variable=self.current_attenuation)

		self.attenuation_low_68 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_68.place(relx=0.278, rely=0.618, relheight=0.084
			, relwidth=0.172, bordermode='ignore')
		self.attenuation_low_68.configure(activebackground="#f9f9f9")
		self.attenuation_low_68.configure(background=_bgcolor)
		self.attenuation_low_68.configure(justify='left')
		self.attenuation_low_68.configure(value='low-68')
		self.attenuation_low_68.configure(variable=self.current_attenuation)

		self.attenuation_low_69 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_69.place(relx=0.278, rely=0.691, relheight=0.084
			, relwidth=0.172, bordermode='ignore')
		self.attenuation_low_69.configure(activebackground="#f9f9f9")
		self.attenuation_low_69.configure(background=_bgcolor)
		self.attenuation_low_69.configure(justify='left')
		self.attenuation_low_69.configure(value='low-69')
		self.attenuation_low_69.configure(variable=self.current_attenuation)

		self.attenuation_low_70 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_low_70.place(relx=0.278, rely=0.764, relheight=0.084
			, relwidth=0.172, bordermode='ignore')
		self.attenuation_low_70.configure(activebackground="#f9f9f9")
		self.attenuation_low_70.configure(background=_bgcolor)
		self.attenuation_low_70.configure(justify='left')
		self.attenuation_low_70.configure(value='low-70')
		self.attenuation_low_70.configure(variable=self.current_attenuation)

		self.attenuation_low_71 = tk.Radiobutton(self)
		self.attenuation_low_71.place(relx=0.076, rely=0.507, relheight=0.049
			, relwidth=0.039)
		self.attenuation_low_71.configure(activebackground="#f9f9f9")
		self.attenuation_low_71.configure(background=_bgcolor)
		self.attenuation_low_71.configure(justify='left')
		self.attenuation_low_71.configure(variable=self.current_attenuation)
		self.attenuation_low_71.configure(value='low-71')

		self.attenuation_low_72 = tk.Radiobutton(self)
		self.attenuation_low_72.place(relx=0.076, rely=0.55, relheight=0.049
			, relwidth=0.039)
		self.attenuation_low_72.configure(activebackground="#f9f9f9")
		self.attenuation_low_72.configure(background=_bgcolor)
		self.attenuation_low_72.configure(justify='left')
		self.attenuation_low_72.configure(value='low-72')
		self.attenuation_low_72.configure(variable=self.current_attenuation)

		####################################### MEDIUM #######################################
		self.attenuation_med_62 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_med_62.place(relx=0.5, rely=0.182, relheight=0.084
			, relwidth=0.172, bordermode='ignore')
		self.attenuation_med_62.configure(activebackground="#f9f9f9")
		self.attenuation_med_62.configure(background=_bgcolor)
		self.attenuation_med_62.configure(justify='left')
		self.attenuation_med_62.configure(value='med-62')
		self.attenuation_med_62.configure(variable=self.current_attenuation)

		self.attenuation_med_63 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_med_63.place(relx=0.5, rely=0.255, relheight=0.084
			, relwidth=0.172, bordermode='ignore')
		self.attenuation_med_63.configure(activebackground="#f9f9f9")
		self.attenuation_med_63.configure(background=_bgcolor)
		self.attenuation_med_63.configure(justify='left')
		self.attenuation_med_63.configure(value='med-63')
		self.attenuation_med_63.configure(variable=self.current_attenuation)

		self.attenuation_med_64 = tk.Radiobutton(self.attenuation_frame)
		self.attenuation_med_64.place(relx=0.5, rely=0.327, relheight=0.084
			, relwidth=0.172, bordermode='ignore')
		self.attenuation_med_64.configure(activebackground="#f9f9f9")
		self.attenuation_med_64.configure(background=_bgcolor)
		self.attenuation_med_64.configure(justify='left')
		self.attenuation_med_64.configure(value='med-64')
		self.attenuation_med_64.configure(variable=self.current_attenuation)

		self.attenuation_med_65 = tk.Radiobutton(self)
		self.attenuation_med_65.place(relx=0.126, rely=0.254, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_65.configure(activebackground="#f9f9f9")
		self.attenuation_med_65.configure(background=_bgcolor)
		self.attenuation_med_65.configure(justify='left')
		self.attenuation_med_65.configure(value='med-65')
		self.attenuation_med_65.configure(variable=self.current_attenuation)

		self.attenuation_med_66 = tk.Radiobutton(self)
		self.attenuation_med_66.place(relx=0.126, rely=0.296, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_66.configure(activebackground="#f9f9f9")
		self.attenuation_med_66.configure(background=_bgcolor)
		self.attenuation_med_66.configure(justify='left')
		self.attenuation_med_66.configure(value='med-66')
		self.attenuation_med_66.configure(variable=self.current_attenuation)

		self.attenuation_med_67 = tk.Radiobutton(self)
		self.attenuation_med_67.place(relx=0.126, rely=0.338, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_67.configure(activebackground="#f9f9f9")
		self.attenuation_med_67.configure(background=_bgcolor)
		self.attenuation_med_67.configure(justify='left')
		self.attenuation_med_67.configure(value='med-67')
		self.attenuation_med_67.configure(variable=self.current_attenuation)

		self.attenuation_med_68 = tk.Radiobutton(self)
		self.attenuation_med_68.place(relx=0.126, rely=0.381, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_68.configure(activebackground="#f9f9f9")
		self.attenuation_med_68.configure(background=_bgcolor)
		self.attenuation_med_68.configure(justify='left')
		self.attenuation_med_68.configure(value='med-68')
		self.attenuation_med_68.configure(variable=self.current_attenuation)

		self.attenuation_med_69 = tk.Radiobutton(self)
		self.attenuation_med_69.place(relx=0.126, rely=0.423, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_69.configure(activebackground="#f9f9f9")
		self.attenuation_med_69.configure(background=_bgcolor)
		self.attenuation_med_69.configure(justify='left')
		self.attenuation_med_69.configure(value='med-69')
		self.attenuation_med_69.configure(variable=self.current_attenuation)

		self.attenuation_med_70 = tk.Radiobutton(self)
		self.attenuation_med_70.place(relx=0.126, rely=0.465, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_70.configure(activebackground="#f9f9f9")
		self.attenuation_med_70.configure(background=_bgcolor)
		self.attenuation_med_70.configure(justify='left')
		self.attenuation_med_70.configure(value='med-70')
		self.attenuation_med_70.configure(variable=self.current_attenuation)

		self.attenuation_med_71 = tk.Radiobutton(self)
		self.attenuation_med_71.place(relx=0.126, rely=0.507, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_71.configure(activebackground="#f9f9f9")
		self.attenuation_med_71.configure(background=_bgcolor)
		self.attenuation_med_71.configure(justify='left')
		self.attenuation_med_71.configure(value='med-71')
		self.attenuation_med_71.configure(variable=self.current_attenuation)

		self.attenuation_med_72 = tk.Radiobutton(self)
		self.attenuation_med_72.place(relx=0.126, rely=0.55, relheight=0.049
			, relwidth=0.039)
		self.attenuation_med_72.configure(activebackground="#f9f9f9")
		self.attenuation_med_72.configure(background=_bgcolor)
		self.attenuation_med_72.configure(justify='left')
		self.attenuation_med_72.configure(value='med-72')
		self.attenuation_med_72.configure(variable=self.current_attenuation)

		####################################### HIGH #######################################
		self.attenuation_high_62 = tk.Radiobutton(self)
		self.attenuation_high_62.place(relx=0.177, rely=0.127, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_62.configure(activebackground="#f9f9f9")
		self.attenuation_high_62.configure(background=_bgcolor)
		self.attenuation_high_62.configure(justify='left')
		self.attenuation_high_62.configure(value='high-62')
		self.attenuation_high_62.configure(variable=self.current_attenuation)

		self.attenuation_high_63 = tk.Radiobutton(self)
		self.attenuation_high_63.place(relx=0.177, rely=0.169, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_63.configure(activebackground="#f9f9f9")
		self.attenuation_high_63.configure(background=_bgcolor)
		self.attenuation_high_63.configure(justify='left')
		self.attenuation_high_63.configure(value='high-63')
		self.attenuation_high_63.configure(variable=self.current_attenuation)

		self.attenuation_high_64 = tk.Radiobutton(self)
		self.attenuation_high_64.place(relx=0.177, rely=0.211, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_64.configure(activebackground="#f9f9f9")
		self.attenuation_high_64.configure(background=_bgcolor)
		self.attenuation_high_64.configure(justify='left')
		self.attenuation_high_64.configure(value='high-64')
		self.attenuation_high_64.configure(variable=self.current_attenuation)

		self.attenuation_high_65 = tk.Radiobutton(self)
		self.attenuation_high_65.place(relx=0.177, rely=0.254, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_65.configure(activebackground="#f9f9f9")
		self.attenuation_high_65.configure(background=_bgcolor)
		self.attenuation_high_65.configure(justify='left')
		self.attenuation_high_65.configure(value='high-65')
		self.attenuation_high_65.configure(variable=self.current_attenuation)

		self.attenuation_high_66 = tk.Radiobutton(self)
		self.attenuation_high_66.place(relx=0.177, rely=0.296, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_66.configure(activebackground="#f9f9f9")
		self.attenuation_high_66.configure(background=_bgcolor)
		self.attenuation_high_66.configure(justify='left')
		self.attenuation_high_66.configure(value='high-66')
		self.attenuation_high_66.configure(variable=self.current_attenuation)

		self.attenuation_high_67 = tk.Radiobutton(self)
		self.attenuation_high_67.place(relx=0.177, rely=0.338, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_67.configure(activebackground="#f9f9f9")
		self.attenuation_high_67.configure(background=_bgcolor)
		self.attenuation_high_67.configure(justify='left')
		self.attenuation_high_67.configure(value='high-67')
		self.attenuation_high_67.configure(variable=self.current_attenuation)

		self.attenuation_high_68 = tk.Radiobutton(self)
		self.attenuation_high_68.place(relx=0.177, rely=0.381, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_68.configure(activebackground="#f9f9f9")
		self.attenuation_high_68.configure(background=_bgcolor)
		self.attenuation_high_68.configure(justify='left')
		self.attenuation_high_68.configure(value='high-68')
		self.attenuation_high_68.configure(variable=self.current_attenuation)

		self.attenuation_high_69 = tk.Radiobutton(self)
		self.attenuation_high_69.place(relx=0.177, rely=0.423, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_69.configure(activebackground="#f9f9f9")
		self.attenuation_high_69.configure(background=_bgcolor)
		self.attenuation_high_69.configure(justify='left')
		self.attenuation_high_69.configure(value='high-69')
		self.attenuation_high_69.configure(variable=self.current_attenuation)

		self.attenuation_high_70 = tk.Radiobutton(self)
		self.attenuation_high_70.place(relx=0.177, rely=0.465, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_70.configure(activebackground="#f9f9f9")
		self.attenuation_high_70.configure(background=_bgcolor)
		self.attenuation_high_70.configure(justify='left')
		self.attenuation_high_70.configure(value='high-70')
		self.attenuation_high_70.configure(variable=self.current_attenuation)

		self.attenuation_high_71 = tk.Radiobutton(self)
		self.attenuation_high_71.place(relx=0.177, rely=0.507, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_71.configure(activebackground="#f9f9f9")
		self.attenuation_high_71.configure(background=_bgcolor)
		self.attenuation_high_71.configure(justify='left')
		self.attenuation_high_71.configure(value='high-71')
		self.attenuation_high_71.configure(variable=self.current_attenuation)

		self.attenuation_high_72 = tk.Radiobutton(self)
		self.attenuation_high_72.place(relx=0.177, rely=0.55, relheight=0.049
			, relwidth=0.039)
		self.attenuation_high_72.configure(activebackground="#f9f9f9")
		self.attenuation_high_72.configure(background=_bgcolor)
		self.attenuation_high_72.configure(justify='left')
		self.attenuation_high_72.configure(value='high-72')
		self.attenuation_high_72.configure(variable=self.current_attenuation)


		########################################### Water Chemistry ###########################################

		self.water_chem_add_frame = ttk.Labelframe(self)
		self.water_chem_add_frame.place(relx=0.253, rely=0.021, relheight=0.591 #relheight=0.591
				, relwidth=0.568)
		self.water_chem_add_frame.configure(relief='')
		self.water_chem_add_frame.configure(text='''Water Chemistry Additions''')
		self.water_chem_add_frame.configure(width=450)

		self.water_chem_orig_lstbx = ScrolledListBox(self.water_chem_add_frame)
		self.water_chem_orig_lstbx.place(relx=0.022, rely=0.073, relheight=0.865
				, relwidth=0.391, bordermode='ignore')
		self.water_chem_orig_lstbx.configure(background="white")
		self.water_chem_orig_lstbx.configure(font="TkFixedFont")
		self.water_chem_orig_lstbx.configure(highlightcolor="#d9d9d9")
		self.water_chem_orig_lstbx.configure(selectbackground="#c4c4c4")
		self.water_chem_orig_lstbx.configure(width=10)

		self.water_chem_new = tk.Button(self.water_chem_add_frame)
		self.water_chem_new.place(relx=0.444, rely=0.073, height=28, width=53
				, bordermode='ignore')
		self.water_chem_new.configure(takefocus="")
		self.water_chem_new.configure(text='''+''')
		self.water_chem_new.configure(command=self.new_water_chem)

		self.move_all_right = tk.Button(self.water_chem_add_frame)
		self.move_all_right.place(relx=0.444, rely=0.218, height=28, width=53
				, bordermode='ignore')
		self.move_all_right.configure(takefocus="")
		self.move_all_right.configure(text='''>>''')
		self.move_all_right.configure(width=53)
		self.move_all_right.configure(command=self.move_all_left_right)

		self.move_one_right = tk.Button(self.water_chem_add_frame)
		self.move_one_right.place(relx=0.444, rely=0.364, height=28, width=53
				, bordermode='ignore')
		self.move_one_right.configure(takefocus="")
		self.move_one_right.configure(text='''>''')
		self.move_one_right.configure(command=self.move_one_left_right)

		self.move_one_left = tk.Button(self.water_chem_add_frame)
		self.move_one_left.place(relx=0.444, rely=0.509, height=28, width=53 #  relx=0.444, rely=0.655
				, bordermode='ignore')
		self.move_one_left.configure(takefocus="")
		self.move_one_left.configure(text='''<''')
		self.move_one_left.configure(command=self.move_one_right_left)

		self.move_all_left = tk.Button(self)
		self.move_all_left.place(relx=0.505, rely=0.402, height=28, width=53)  # , height=28, width=53  relx=0.505, rely=0.317
		self.move_all_left.configure(takefocus="")
		self.move_all_left.configure(text='''<<''')
		self.move_all_left.configure(command=self.move_all_right_left)

		self.water_chem_added_lstbx = ScrolledListBox(self.water_chem_add_frame)
		self.water_chem_added_lstbx.place(relx=0.578, rely=0.073, relheight=0.865
				, relwidth=0.391, bordermode='ignore')
		self.water_chem_added_lstbx.configure(background="white")
		self.water_chem_added_lstbx.configure(font="TkFixedFont")
		self.water_chem_added_lstbx.configure(highlightcolor="#d9d9d9")
		self.water_chem_added_lstbx.configure(selectbackground="#c4c4c4")
		self.water_chem_added_lstbx.configure(width=10)

		#########################################################################################
		self.water_boil_frame = ttk.Labelframe(self)
		self.water_boil_frame.place(relx=0.013, rely=0.613, relheight=0.159
				, relwidth=0.227)
		self.water_boil_frame.configure(relief='')
		self.water_boil_frame.configure(text='''Water Boil:''')
		self.water_boil_frame.configure(width=180)

		self.water_boil_disable = tk.Checkbutton(self.water_boil_frame)
		self.water_boil_is_disabled = tk.IntVar()
		self.water_boil_disable.place(relx=0.778, rely=0.4, relheight=0.307
				, relwidth=0.15, bordermode='ignore')
		self.water_boil_disable.configure(justify='left')
		self.water_boil_disable.configure(variable=self.water_boil_is_disabled)
		self.water_boil_disable.configure(command=self.water_boil_check)

		self.water_boil_time_spinbx = tk.Spinbox(self.water_boil_frame, from_=1.0, to=9999.0)
		self.water_boil_time_spinbx.place(relx=0.444, rely=0.4, relheight=0.307, relwidth=0.322
				, bordermode='ignore')
		self.water_boil_time_spinbx.configure(activebackground="#f9f9f9")
		self.water_boil_time_spinbx.configure(background="white")
		self.water_boil_time_spinbx.configure(highlightbackground="black")
		self.water_boil_time_spinbx.configure(selectbackground="#c4c4c4")
		self.water_boil_time_spinbx.configure(width=58)
		#self.water_boil_time_spinbx.set(brew_data.constants['Default Boil Time'])
		self.water_boil_time_spinbx.delete(0, tk.END)
		self.water_boil_time_spinbx.insert(0,brew_data.constants['Default Boil Time'])

		self.water_boil_time_lbl = tk.Label(self.water_boil_frame)
		self.water_boil_time_lbl.place(relx=0.056, rely=0.4, height=17, width=65
				, bordermode='ignore')
		self.water_boil_time_lbl.configure(background=_bgcolor)
		self.water_boil_time_lbl.configure(foreground="#000000")
		self.water_boil_time_lbl.configure(font=font9)
		self.water_boil_time_lbl.configure(relief='flat')
		self.water_boil_time_lbl.configure(text='''Boil Time:''')
		self.water_boil_check()

	@staticmethod
	def popup1(event, *args, **kwargs):
		Popupmenu1 = tk.Menu(root, tearoff=0)
		Popupmenu1.configure(activebackground="#f9f9f9")
		Popupmenu1.post(event.x_root, event.y_root)

	def refresh_orig(self):
		self.water_chem_orig_lstbx.delete(0, tk.END)
		for idx, addition in enumerate(self.original_additions):
			self.water_chem_orig_lstbx.insert(tk.END, addition)
			if addition in brew_data.yeast_data:
				self.water_chem_orig_lstbx.itemconfig(idx, {'bg':'lightblue'})

	def refresh_add(self):
		self.water_chem_added_lstbx.delete(0, tk.END)
		for idx, addition in enumerate(self.added_additions):
			self.water_chem_added_lstbx.insert(tk.END, addition)
			if addition in brew_data.yeast_data:
				self.water_chem_added_lstbx.itemconfig(idx, {'bg':'lightblue'})

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
		for _ in range(len(self.original_additions)):
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
		for _ in range(len(self.added_additions)):
			self.original_additions.append(self.added_additions.pop(0))
		self.refresh_all()

	def water_boil_check(self):
		if self.water_boil_is_disabled.get() == 0:
			self.water_boil_time_spinbx.configure(state="disabled")
		else:
			self.water_boil_time_spinbx.configure(state="normal")

	def new_water_chem(self):
		def on_type_change(*args):
			if type_var.get() != 'Hop':
				time_spnbx.configure(state='disabled')
			else:
				time_spnbx.configure(state='normal')
		def done():
			brew_data.water_chemistry_additions[name_var.get()] = {'Values': {'Type': type_var.get()}}
			if type_var.get() == 'Hop': brew_data.water_chemistry_additions[name_var.get()]['Values']['Time'] = float(time_var.get())
			self.original_additions = list(set(sorted(brew_data.water_chemistry_additions))-set(self.added_additions)) + list((set(sorted(brew_data.yeast_data))-set(self.added_additions)))
			self.refresh_all()

		def cancel():
			new_water_chem_win.destroy()

		def save_to_database():
			done()
			with open(resource_path('water_chem_data.txt'), 'w') as f:
				for water_chem, values in brew_data.water_chemistry_additions.items():
					value = values['Values']
					name = water_chem
					time = value['Time'] if 'Time' in value else 'N/A'
					#print(value)
					water_chem_type = value['Type']
					f.write('{name}\t{time}\t{water_chem_type}\n'.format(name=name, time=time, water_chem_type=water_chem_type))
			new_water_chem_win.destroy()

		new_water_chem_win = tk.Toplevel()
		name_var = tk.StringVar(value='New Item {num}'.format(num=sum('New Item' in s for s in brew_data.water_chemistry_additions)))
		time_var = tk.IntVar()
		type_var = tk.StringVar(value='Hop')
		tk.Label(new_water_chem_win, text="Name: ").grid(row=0, column=0)
		name_entry = tk.Entry(new_water_chem_win, textvariable=name_var, justify='center')
		name_entry.grid(row=0, column=1, sticky='nsew')
		tk.Label(new_water_chem_win, text="Time: ").grid(row=1, column=0)
		time_spnbx = tk.Spinbox(new_water_chem_win, from_=0, to=1000000000, textvariable=time_var, justify='center')
		time_spnbx.grid(row=1, column=1, sticky='nsew')
		tk.Label(new_water_chem_win, text="Type: ").grid(row=2, column=0)
		type_opt = tk.OptionMenu(new_water_chem_win, type_var, "Hop", "Malt", "Yeast")
		type_opt.grid(row=2, column=1, sticky='nsew')

		type_var.trace('w', on_type_change)

		tk.Button(new_water_chem_win, text="Cancel", command=cancel).grid(row=3, column=0)
		tk.Button(new_water_chem_win, text="Done", command=done).grid(row=3, column=1, sticky='nsew')
		tk.Button(new_water_chem_win, text="Save To Database", command=save_to_database).grid(row=4, column=0, columnspan=2, sticky='nsew')

class yeast_editor(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.widgets()

	def widgets(self):
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85'
		_ana2color = '#ececec' # Closest X11 color: 'gray92'
		font9 = "-family {DejaVu Sans} -size 10 -weight bold -slant "  \
			"roman -underline 0 -overstrike 0"
		self.style = ttk.Style()
		self.style.configure('.',background=_bgcolor)
		self.style.configure('.',foreground=_fgcolor)
		self.style.configure('.',font="TkDefaultFont")
		self.style.map('.',background=
			[('selected', _compcolor), ('active',_ana2color)])

		# self.TPanedwindow1 = tk.PanedWindow(self, orient="horizontal",  background=_bgcolor)
		# self.TPanedwindow1.place(relx=0.013, rely=0.0, relheight=0.973
		# 		, relwidth=0.966)
		self.yeast_panedwindow1 = tk.LabelFrame(self, text='Yeasts:', background=_bgcolor)
		self.yeast_panedwindow1.place(relx=0.005, rely=0.005, relheight=0.990, relwidth=0.5)
		self.yeast_panedwindow2 = tk.LabelFrame(self, text='Modifications:', background=_bgcolor)
		self.yeast_panedwindow2.place(relx=0.510, rely=0.005, relheight=0.990, relwidth=0.485)	


		self.yeast_lstbx = ScrolledListBox(self.yeast_panedwindow1)
		self.yeast_lstbx.place(relx=0.025, rely=0.043, relheight=0.887
				, relwidth=0.94, bordermode='ignore')
		self.yeast_lstbx.configure(background="white")
		self.yeast_lstbx.configure(font="TkFixedFont")
		self.yeast_lstbx.configure(highlightcolor="#d9d9d9")
		self.yeast_lstbx.configure(selectbackground="#c4c4c4")

		self.yeast_delete_butt = tk.Button(self.yeast_panedwindow1)
		self.yeast_delete_butt.place(relx=0.025, rely=0.929, relheight=0.0589, relwidth=0.2075
				, bordermode='ignore')
		self.yeast_delete_butt.configure(takefocus="")
		self.yeast_delete_butt.configure(text='''Delete''')
		self.yeast_delete_butt.configure(command=self.delete)

		self.yeast_modify_butt = tk.Button(self.yeast_panedwindow1)
		self.yeast_modify_butt.place(relx=0.35, rely=0.93, relheight=0.0589, relwidth=0.2075
				, bordermode='ignore')
		self.yeast_modify_butt.configure(takefocus="")
		self.yeast_modify_butt.configure(text='''Modify''')
		self.yeast_modify_butt.configure(command=lambda: self.input_state(1))

		self.yeast_new_butt = tk.Button(self.yeast_panedwindow1)
		self.yeast_new_butt.place(relx=0.725, rely=0.93, relheight=0.0589, relwidth=0.2075
				, bordermode='ignore')
		self.yeast_new_butt.configure(takefocus="")
		self.yeast_new_butt.configure(text='''New''')
		self.yeast_new_butt.configure(command=self.new)

		############################ Config Section ############################

		self.yeast_name_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_name_lbl.place(relx=0.056, rely=0.087, bordermode='ignore')
		self.yeast_name_lbl.configure(background=_bgcolor)
		self.yeast_name_lbl.configure(foreground="#000000")
		self.yeast_name_lbl.configure(font=font9)
		self.yeast_name_lbl.configure(relief='flat')
		self.yeast_name_lbl.configure(text='''Name:''')

		self.yeast_name_ent = tk.Entry(self.yeast_panedwindow2)
		self.yeast_name_ent.place(relx=0.222, rely=0.087, relheight=0.046
				, relwidth=0.511, bordermode='ignore')
		self.yeast_name_ent.configure(justify='center')
		self.yeast_name_ent.configure(foreground="#000000")
		self.yeast_name_ent.configure(takefocus="")
		self.yeast_name_ent.configure(cursor="xterm")

		self.yeast_type_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_type_lbl.place(relx=0.056, rely=0.152, bordermode='ignore')
		self.yeast_type_lbl.configure(background=_bgcolor)
		self.yeast_type_lbl.configure(foreground="#000000")
		self.yeast_type_lbl.configure(font=font9)
		self.yeast_type_lbl.configure(relief='flat')
		self.yeast_type_lbl.configure(text='''Type:''')

		self.yeast_type_combo = ttk.Combobox(self.yeast_panedwindow2)
		self.yeast_type_combo.place(relx=0.222, rely=0.152, relheight=0.046
				, relwidth=0.519, bordermode='ignore')
		self.yeast_type_combo.configure(width=187)
		self.yeast_type_combo_values = ['Dry', 'Liquid']
		self.yeast_type_combo.configure(values=self.yeast_type_combo_values)
		self.yeast_type_combo.configure(takefocus="")
		self.yeast_type_combo.configure(justify='center')

		self.yeast_lab_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_lab_lbl.place(relx=0.056, rely=0.217, bordermode='ignore')
		self.yeast_lab_lbl.configure(background=_bgcolor)
		self.yeast_lab_lbl.configure(foreground="#000000")
		self.yeast_lab_lbl.configure(font=font9)
		self.yeast_lab_lbl.configure(relief='flat')
		self.yeast_lab_lbl.configure(text='''Lab:''')

		self.yeast_lab_ent = tk.Entry(self.yeast_panedwindow2)
		self.yeast_lab_ent.place(relx=0.222, rely=0.217, relheight=0.046
				, relwidth=0.511, bordermode='ignore')
		self.yeast_lab_ent.configure(justify='center')
		self.yeast_lab_ent.configure(foreground="#000000")
		self.yeast_lab_ent.configure(takefocus="")
		self.yeast_lab_ent.configure(cursor="xterm")

		self.yeast_origin_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_origin_lbl.place(relx=0.056, rely=0.283, bordermode='ignore')
		self.yeast_origin_lbl.configure(background=_bgcolor)
		self.yeast_origin_lbl.configure(foreground="#000000")
		self.yeast_origin_lbl.configure(font=font9)
		self.yeast_origin_lbl.configure(relief='flat')
		self.yeast_origin_lbl.configure(text='''Origin:''')

		self.yeast_origin_ent = tk.Entry(self.yeast_panedwindow2)
		self.yeast_origin_ent.place(relx=0.222, rely=0.283, relheight=0.046
				, relwidth=0.511, bordermode='ignore')
		self.yeast_origin_ent.configure(justify='center')
		self.yeast_origin_ent.configure(foreground="#000000")
		self.yeast_origin_ent.configure(takefocus="")
		self.yeast_origin_ent.configure(cursor="xterm")

		self.yeast_flocc_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_flocc_lbl.place(relx=0.056, rely=0.348, height=19, width=100
				, bordermode='ignore')
		self.yeast_flocc_lbl.configure(background=_bgcolor)
		self.yeast_flocc_lbl.configure(foreground="#000000")
		self.yeast_flocc_lbl.configure(font=font9)
		self.yeast_flocc_lbl.configure(relief='flat')
		self.yeast_flocc_lbl.configure(text='''Flocculation:''')
		self.yeast_flocc_lbl.configure(width=100)

		self.yeast_flocc_combo = ttk.Combobox(self.yeast_panedwindow2)
		self.yeast_flocc_combo.place(relx=0.361, rely=0.348, relheight=0.046
				, relwidth=0.381, bordermode='ignore')
		self.yeast_flocc_combo.configure(width=137)
		self.yeast_flocc_combo_values = ['Low', 'Low/Medium', 'Medium', 'Medium/High', 'High']
		self.yeast_flocc_combo.configure(values=self.yeast_flocc_combo_values)
		self.yeast_flocc_combo.configure(takefocus="")
		self.yeast_flocc_combo.configure(justify='center')

		self.yeast_attenuation_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_attenuation_lbl.place(relx=0.056, rely=0.413, bordermode='ignore')
		self.yeast_attenuation_lbl.configure(background=_bgcolor)
		self.yeast_attenuation_lbl.configure(foreground="#000000")
		self.yeast_attenuation_lbl.configure(font=font9)
		self.yeast_attenuation_lbl.configure(relief='flat')
		self.yeast_attenuation_lbl.configure(text='''Attenuation:''')

		self.yeast_temperature_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_temperature_lbl.place(relx=0.056, rely=0.478, height=19
				, width=110, bordermode='ignore')
		self.yeast_temperature_lbl.configure(background=_bgcolor)
		self.yeast_temperature_lbl.configure(foreground="#000000")
		self.yeast_temperature_lbl.configure(font=font9)
		self.yeast_temperature_lbl.configure(relief='flat')
		self.yeast_temperature_lbl.configure(text='''Temperature:''')
		self.yeast_temperature_lbl.configure(width=110)

		self.yeast_attenuation_ent = tk.Entry(self.yeast_panedwindow2)
		self.yeast_attenuation_ent.place(relx=0.333, rely=0.413, relheight=0.046
				, relwidth=0.4, bordermode='ignore')
		self.yeast_attenuation_ent.configure(justify='center')
		self.yeast_attenuation_ent.configure(width=144)
		self.yeast_attenuation_ent.configure(foreground="#000000")
		self.yeast_attenuation_ent.configure(takefocus="")
		self.yeast_attenuation_ent.configure(cursor="xterm")

		self.yeast_temperature_spinbox1 = tk.Spinbox(self.yeast_panedwindow2, from_=1.0, to=100.0)
		self.yeast_temperature_spinbox1_value = tk.DoubleVar()
		self.yeast_temperature_spinbox1.place(relx=0.389, rely=0.478
				, relheight=0.05, relwidth=0.133, bordermode='ignore')
		self.yeast_temperature_spinbox1.configure(activebackground="#f9f9f9")
		self.yeast_temperature_spinbox1.configure(background="white")
		self.yeast_temperature_spinbox1.configure(highlightbackground="black")
		self.yeast_temperature_spinbox1.configure(selectbackground="#c4c4c4")
		self.yeast_temperature_spinbox1.configure(width=48)
		self.yeast_temperature_spinbox1.configure(textvariable=self.yeast_temperature_spinbox1_value)

		self.yeast_temperature_spinbox2 = tk.Spinbox(self.yeast_panedwindow2, from_=1.0, to=100.0)
		self.yeast_temperature_spinbox2_value = tk.DoubleVar()
		self.yeast_temperature_spinbox2.place(relx=0.528, rely=0.478
				, relheight=0.05, relwidth=0.133, bordermode='ignore')
		self.yeast_temperature_spinbox2.configure(activebackground="#f9f9f9")
		self.yeast_temperature_spinbox2.configure(background="white")
		self.yeast_temperature_spinbox2.configure(highlightbackground="black")
		self.yeast_temperature_spinbox2.configure(selectbackground="#c4c4c4")
		self.yeast_temperature_spinbox2.configure(width=48)
		self.yeast_temperature_spinbox2.configure(textvariable=self.yeast_temperature_spinbox2_value)

		self.yeast_comm_lbl = tk.Label(self.yeast_panedwindow2)
		self.yeast_comm_lbl.place(relx=0.056, rely=0.543, bordermode='ignore')
		self.yeast_comm_lbl.configure(background=_bgcolor)
		self.yeast_comm_lbl.configure(foreground="#000000")
		self.yeast_comm_lbl.configure(font=font9)
		self.yeast_comm_lbl.configure(relief='flat')
		self.yeast_comm_lbl.configure(text='''Comments:''')

		self.yeast_comm_ent = tk.Entry(self.yeast_panedwindow2)
		self.yeast_comm_ent.place(relx=0.028, rely=0.587, relheight=0.046
		, relwidth=0.956, bordermode='ignore')
		self.yeast_comm_ent.configure(takefocus="")
		self.yeast_comm_ent.configure(cursor="xterm")

		self.yeast_cancel_butt = tk.Button(self.yeast_panedwindow2)
		self.yeast_cancel_butt.place(relx=0.028, rely=0.652, height=28, width=83
				, bordermode='ignore')
		self.yeast_cancel_butt.configure(takefocus="")
		self.yeast_cancel_butt.configure(text='''Cancel''')
		self.yeast_cancel_butt.configure(command=lambda: self.show_data(self.yeast_lstbx.get(tk.ACTIVE)))

		self.yeast_clear_butt = tk.Button(self.yeast_panedwindow2)
		self.yeast_clear_butt.place(relx=0.389, rely=0.652, height=28, width=83
				, bordermode='ignore')
		self.yeast_clear_butt.configure(takefocus="")
		self.yeast_clear_butt.configure(text='''Clear Form''')
		self.yeast_clear_butt.configure(command=self.clear_form)

		self.yeast_done_butt = tk.Button(self.yeast_panedwindow2)
		self.yeast_done_butt.place(relx=0.75, rely=0.652, height=28, width=83
				, bordermode='ignore')
		self.yeast_done_butt.configure(takefocus="")
		self.yeast_done_butt.configure(text='''Done''')
		self.yeast_done_butt.configure(command=self.done)

		self.yeast_save_data_butt = tk.Button(self.yeast_panedwindow2)
		self.yeast_save_data_butt.place(relx=0.222, rely=0.739, relwidth=0.5713
				, relheight=0.2312, bordermode='ignore')
		self.yeast_save_data_butt.configure(takefocus="")
		self.yeast_save_data_butt.configure(text='''Save to Database''')
		self.yeast_save_data_butt.configure(command=self.save)


		self.yeast_lstbx.bind('<<ListboxSelect>>', self.select_listbox)
		self.input_state(0)

	def __adjust_sash0(self, event):
		paned = event.widget
		pos = [400, ]
		i = 0
		for sash in pos:
			paned.sashpos(i, sash)
			i += 1
		paned.unbind('<map>', self.__funcid0)
		del self.__funcid0

	def show_data(self, yeast):
		self.name = yeast
		name = yeast
		yeast_type = brew_data.yeast_data[name]['Type']
		yeast_type = 'Dry' if yeast_type == 'D' else yeast_type
		yeast_type = 'Liquid' if yeast_type == 'L' else yeast_type
		lab = brew_data.yeast_data[name]['Lab']
		flocculation = brew_data.yeast_data[name]['Flocculation']
		attenuation = brew_data.yeast_data[name]['Attenuation']

		if brew_data.yeast_data[name]['Temperature'] != 'Unknown':
			temperature1 = float(brew_data.yeast_data[name]['Temperature'].replace('°', '').split('-')[0])
			temperature2 = float(brew_data.yeast_data[name]['Temperature'].replace('°', '').split('-')[1])
		else:
			temperature1 = 20
			temperature2 = 20

		origin = brew_data.yeast_data[name]['Origin']
		description = brew_data.yeast_data[name]['Description']

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

		state = "disabled" if state == 0 else "normal"

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
		name = 'New Yeast {num}'.format(num=sum('New Yeast' in s for s in brew_data.yeast_data))
		self.yeast_lstbx.insert(tk.END, name)
		try:
			brew_data.yeast_data[name] = brew_data.yeast_data[self.yeast_lstbx.get(self.yeast_lstbx.curselection())]
		except:
			try:
				brew_data.yeast_data[name] = brew_data.yeast_data[tk.ACTIVE]
			except:
				brew_data.yeast_data[name] = {'Type': 'D', 'Lab': 'Lallemand', 'Flocculation': 'Low', 'Attenuation': 'High', 'Temperature': '66-72°', 'Description': 'Unknown', 'Origin': 'Unknown'}

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
		temperature = '{temp1}-{temp2}°'.format(temp1=temp1, temp2=temp2)
		description = self.yeast_comm_ent.get()
		flocculation = self.yeast_flocc_combo.get()
		yeast_type = 'D' if self.yeast_type_combo.get() == 'Dry' else self.yeast_type_combo.get()
		yeast_type = 'L' if yeast_type == 'Liquid' else yeast_type
		del brew_data.yeast_data[self.name]
		brew_data.yeast_data[name] = {'Type': yeast_type, 'Lab': lab, 'Flocculation': flocculation, 'Attenuation': attenuation, 'Temperature': temperature, 'Description': description, 'Origin': origin}
		self.reinsert()
		self.show_data(name)

	def save(self):
		with open(resource_path('yeast_data.txt'), 'w') as f:
			for yeast, value in brew_data.yeast_data.items():
				name = yeast
				yeast_type = value['Type']
				lab = value['Lab']
				flocculation = value['Flocculation']
				attenuation = value['Attenuation']
				temperature = value['Temperature']
				origin = value['Origin']
				description = value['Description']
				f.write('{name}\t{yeast_type}\t{lab}\t{flocculation}\t{attenuation}\t{temperature}\t{origin}\t{description}\n'.format(name=name, yeast_type=yeast_type, lab=lab, flocculation=flocculation, attenuation=attenuation, temperature=temperature, origin=origin, description=description))
		self.done()

	def reinsert(self):
		self.yeast_lstbx.delete(0, tk.END)
		for yeast in sorted(brew_data.yeast_data, key=lambda kv: kv.lower()):
			self.yeast_lstbx.insert(tk.END, yeast)

class notes_area(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.widgets()

	def widgets(self):
		########################################################################################
		#				Salvaged from https://github.com/jimbob88/texpert/					   #
		########################################################################################
		self.texpert = ScrolledText(self, bg="white", undo=True, maxundo=-1, font=("Arial", 11))
		self.texpert.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
		self.texpert.focus_set()
		#edit menu
		self.editmenu = tk.Menu(tearoff=0)
		self.editmenu.add_command(label="Undo", command=self.undo_com, accelerator="Ctrl+Z")
		self.editmenu.add_command(label="Redo", command=self.redo_com, accelerator="Shift+Ctrl+Z")
		self.editmenu.add_separator()
		self.editmenu.add_command(label="Cut", command=self.cut_com, accelerator="Ctrl+X")
		self.texpert.bind("<Control-Key-x>", lambda e: self.undo_com)
		self.editmenu.add_command(label="Copy", command=self.copy_com, accelerator="Ctrl+C")
		self.texpert.bind("<Control-Key-c>", lambda e: self.undo_com)
		self.editmenu.add_command(label="Paste", command=self.paste_com, accelerator="Ctrl+V")
		self.texpert.bind("<Control-Key-v>", lambda e: self.undo_com)
		self.editmenu.add_separator()
		self.editmenu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
		self.editmenu.add_separator()
		self.html_formatting = tk.BooleanVar()
		self.editmenu.add_checkbutton(label="HTML Mode", variable=self.html_formatting)
		# self.editmenu.add_separator()
		# self.editmenu.add_command(label="Find", command=self.find_win, accelerator="Ctrl+F")



		self.texpert.bind("<Control-Key-a>", self.select_all)
		self.texpert.bind("<Control-Key-A>", self.select_all)
		self.texpert.bind("<Button-3>", self.r_click)

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
		try: self.texpert.event_generate("<<Undo>>")
		except tk.TclError: print('Undo Failed')

	def redo_com(self):
		try: self.texpert.event_generate("<<Redo>>")
		except tk.TclError: print('Redo Failed')

	def cut_com(self):
		try: self.texpert.event_generate("<<Cut>>")
		except tk.TclError: pass

	def copy_com(self):
		try: self.texpert.event_generate("<<Copy>>")
		except tk.TclError: pass

	def paste_com(self):
		try: self.texpert.event_generate("<<Paste>>")
		except tk.TclError: pass

	def select_all(self, event=None):
		self.texpert.tag_add(tk.SEL, '1.0', 'end-1c')
		self.texpert.mark_set(tk.INSERT, '1.0')
		self.texpert.see(tk.INSERT)
		return 'break'



class AutoScroll(object):
	'''Configure the scrollbars for a widget.'''

	def __init__(self, master):
		#  Rozen. Added the try-except clauses so that this class
		#  could be used for scrolled entry widget for which vertical
		#  scrolling is not supported. 5/7/14.
		try:
			vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
		except:
			pass
		hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

		#self.configure(yscrollcommand=_autoscroll(vsb),
		#    xscrollcommand=_autoscroll(hsb))
		try:
			self.configure(yscrollcommand=self._autoscroll(vsb))
		except:
			pass
		self.configure(xscrollcommand=self._autoscroll(hsb))

		self.grid(column=0, row=0, sticky='nsew')
		try:
			vsb.grid(column=1, row=0, sticky='ns')
		except:
			pass
		hsb.grid(column=0, row=1, sticky='ew')

		master.grid_columnconfigure(0, weight=1)
		master.grid_rowconfigure(0, weight=1)

		if sys.version_info >= (3, 0):
			methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
				  | tk.Place.__dict__.keys()
		else:
			methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
				+ tk.Place.__dict__.keys()

		for meth in methods:
			if meth[0] != '_' and meth not in ('config', 'configure'):
				setattr(self, meth, getattr(master, meth))

	@staticmethod
	def _autoscroll(sbar):
		'''Hide and show scrollbar as needed.'''
		def wrapped(first, last):
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
	'''Creates a ttk Frame with a given master, and use this new frame to
	place the scrollbars and the widget.'''
	def wrapped(cls, master, **kw):
		container = ttk.Frame(master)
		container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
		container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
		return func(cls, container, **kw)
	return wrapped

class ScrolledTreeView(AutoScroll, ttk.Treeview):
	'''A standard ttk Treeview widget with scrollbars that will
	automatically show/hide as needed.'''
	@_create_container
	def __init__(self, master, custom_insert=True, **kw):
		ttk.Treeview.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)
		self.custom_insert = custom_insert

	def insert(self, parent, index, iid=None, **kw):
		opts = ttk._format_optdict(kw)
		if iid is not None:
			res = self.tk.call(self._w, "insert", parent, index,
				"-id", iid, *opts)
		else:
			if self.custom_insert:
				iid = 'I{iid}'.format(iid=format(len(self.get_children())+1, '03x')) #hex(len(self.get_children())).split('x')[-1]
				res = self.tk.call(self._w, "insert", parent, index,
					"-id", iid, *opts)
			else:
				res = self.tk.call(self._w, "insert", parent, index, *opts)
		return res

class ScrolledListBox(AutoScroll, tk.Listbox):
	'''A standard Tkinter Text widget with scrollbars that will
	automatically show/hide as needed.'''
	@_create_container
	def __init__(self, master, **kw):
		tk.Listbox.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

class ScrolledText(AutoScroll, tk.Text):
	'''A standard Tkinter Text widget with scrollbars that will
	automatically show/hide as needed.'''
	@_create_container
	def __init__(self, master, **kw):
		tk.Text.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)


def _bound_to_mousewheel(event, widget):
	child = widget.winfo_children()[0]
	if platform.system() == 'Windows' or platform.system() == 'Darwin':
		child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
	else:
		child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
		child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
	if platform.system() == 'Windows' or platform.system() == 'Darwin':
		widget.unbind_all('<MouseWheel>')
		widget.unbind_all('<Shift-MouseWheel>')
	else:
		widget.unbind_all('<Button-4>')
		widget.unbind_all('<Button-5>')
		widget.unbind_all('<Shift-Button-4>')
		widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
	if platform.system() == 'Windows':
		widget.yview_scroll(-1*int(event.delta/120),'units')
	elif platform.system() == 'Darwin':
		widget.yview_scroll(-1*int(event.delta),'units')
	else:
		if event.num == 4:
			widget.yview_scroll(-1, 'units')
		elif event.num == 5:
			widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
	if platform.system() == 'Windows':
		widget.xview_scroll(-1*int(event.delta/120), 'units')
	elif platform.system() == 'Darwin':
		widget.xview_scroll(-1*int(event.delta), 'units')
	else:
		if event.num == 4:
			widget.xview_scroll(-1, 'units')
		elif event.num == 5:
			widget.xview_scroll(1, 'units')

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	if __mode__ in ['pyinstaller', 'local']:
		try:
			# PyInstaller creates a temp folder and stores path in _MEIPASS
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.abspath(".")

		return os.path.join(base_path, relative_path)
	elif __mode__ == 'deb':
		if os.path.basename(relative_path) == 'logo.png':
			return '/usr/include/wheelers-wort-works-ce/logo.png'
		elif os.path.splitext(os.path.basename(relative_path))[1] == '.html':
			return os.path.join(os.path.expanduser('~/.config/Wheelers-Wort-Works-ce/recipes/html'), relative_path)
		else:
			return os.path.join(os.path.expanduser('~/.config/Wheelers-Wort-Works-ce/'), relative_path)
def main(file=None, update_available=False):
	root = tk.Tk()
	gui = beer_engine_mainwin(root)
	root.config(cursor="arrow")
	if file != None:
		gui.open_file(file)
	if update_available:		
		update_win = tk.Toplevel(root)
		update_win.title('Update Available')
		update_win.resizable(0, 0)
		tk.Label(update_win, text='An update has become available, it is recommended you run the command:', font=('TkFixedFont', 12)).grid(row=0, column=0, columnspan=3, sticky='nsew')
		command = "{command}".format(
			command=(
				'sudo wheelers-wort-works-ce --coreupdate' if __mode__ == 'deb' else 'python3 main.py --coreupdate'))
		command_box = tk.Text(update_win, height=1, width=50, font=('TkFixedFont', 12), background='lightgray')
		command_box.grid(row=1, column=0, columnspan=3, sticky='nsew')
		command_box.insert('1.0', command, "center")
		command_box['state'] = 'disabled'
		command_box.tag_configure('center_text', justify='center')
		command_box.tag_add('center_text', 1.0, 'end')
		editmenu = tk.Menu(tearoff=0)
		editmenu.add_command(
			label="Copy",
			command=lambda: copy_command(root, command),
			accelerator="Ctrl+C")
		command_box.bind("<Control-Key-c>", lambda event: copy_command(root, command))
		command_box.bind("<Button-3>", lambda event: editmenu.tk_popup(event.x_root, event.y_root))

		tk.Button(update_win, text='Okay', command=update_win.destroy).grid(row=2, column=1, sticky='nsew')		
		update_win.update_idletasks() 
		x = root.winfo_x() + (root.winfo_width()/2) - (update_win.winfo_width()/2)
		y = root.winfo_y() + (root.winfo_height()/2) - (update_win.winfo_height()/2)
		update_win.geometry("+{x}+{y}".format(x=int(x), y=int(y)))
		update_win.attributes("-topmost", True)

	root.mainloop()


if __name__ == '__main__':
	main()
