#!/usr/bin/python
# -*- coding: utf-8 -*-
#
__author__="atareao"
__date__ ="$22-jan-2012$"
#
# Script to replace string in files
#
# Copyright (C) 2012 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
from gi.repository import Nautilus, GObject, Gtk, GdkPixbuf
import sys
import urllib
import codecs
import os
import json

import locale
import gettext

__author__ = 'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'
__date__ ='$15/03/2011'
__copyright__ = 'Copyright (c) 2011, 2012 Lorenzo Carbonell'
__license__ = 'GPLV3'
__url__ = 'http://www.atareao.es'

######################################

def is_package():
	return (os.getcwd().find('/usr/share/nautilus-python/extensions/')>0 or \
	__file__.startswith('/usr/share/nautilus-python/extensions/'))

######################################


APPNAME = 'MovieTitle'
APP = 'movietitle'
ICON = 'movietitle.svg'
APP_CONF=APP+'.conf'
CONFIG_DIR = os.path.join(os.path.expanduser('~'),'.config')
CONFIG_APP_DIR = os.path.join(CONFIG_DIR, APP)
CONFIG_FILE = os.path.join(CONFIG_APP_DIR, APP_CONF)

EXTENSIONS = ['.avi', '.mkv', '.mpg']
PARAMS = {
	'file_dir':'',
	'replacements':[
	{'value':'anio','with':'a\u00f1o'},
	{'value':'anios','with':'a\u00f1os'},
	{'value':'.','with':' '},
	{'value':'_','with':' '},
	{'value':'spanish','with':''},
	{'value':'xvid','with':''},
	{'value':'mp3','with':''},
	{'value':'dvdrip','with':''},
	{'value':'hdrip','with':''},
	{'value':'by','with':''},
	{'value':'freak','with':''},
	{'value':'team','with':''},
	{'value':'[','with':''},
	{'value':'microhd','with':''},
	{'value':'hd','with':''},
	{'value':'dvd','with':''},
	{'value':']','with':''},
	{'value':'1080p','with':''},
	{'value':'1080','with':''},
	{'value':'x264','with':''},
	{'value':'english','with':''},
	{'value':'ac3','with':''},
	{'value':'emuleteca','with':''},
	{'value':'hdgroup','with':''},
	{'value':'group','with':''},
	{'value':'bdrip','with':''},
	{'value':'dxva','with':''},
	{'value':'centraldivx','with':''},
	{'value':'screener','with':''},
	{'value':'-','with':''},
	{'value':'subs','with':''},
	{'value':'720','with':''},
	{'value':'rip','with':''},
	{'value':'2000','with':''},
	{'value':'2001','with':''},
	{'value':'2002','with':''},
	{'value':'2003','with':''},
	{'value':'2004','with':''},
	{'value':'2005','with':''},
	{'value':'2006','with':''},
	{'value':'2007','with':''},
	{'value':'2008','with':''},
	{'value':'2009','with':''},
	{'value':'2010','with':''},
	{'value':'2011','with':''},
	{'value':'2012','with':''},
	{'value':'2013','with':''},
	{'value':'2014','with':''},
	{'value':'2015','with':''},
	{'value':'2016','with':''},
	{'value':'2017','with':''}]}

# check if running from source
if is_package():
	print(1)
	ROOTDIR = '/opt/extras.ubuntu.com/%s/share/'%APP
	LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
	APPDIR = os.path.join(ROOTDIR, APP)
	CHANGELOG = os.path.join(APPDIR,'changelog')
	ICONDIR = os.path.join(ROOTDIR, 'icons') 
else:
	print(2)
	ROOTDIR = os.path.dirname(__file__)
	LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../po'))
	DEBIANDIR = os.path.normpath(os.path.join(ROOTDIR, '../debian'))
	CHANGELOG = os.path.join(DEBIANDIR,'changelog')	
	APPDIR = ROOTDIR
	ICONDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons'))
ICON = os.path.join(ICONDIR, ICON)

f = open(CHANGELOG,'r')
line = f.readline()
f.close()
pos=line.find('(')
posf=line.find(')',pos)
VERSION = line[pos+1:posf].strip()
if not is_package():
	VERSION = VERSION + '-src'


locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP, LANGDIR)
gettext.textdomain(APP)
_ = gettext.gettext

def get_files(files_in):
	files = []
	for file_in in files_in:
		mfile = (urllib.url2pathname(file_in.get_uri())[7:])
		if os.path.isfile(mfile):
			files.append(mfile)
	if len(files)>0:
		return files
	return None

class Configuration(object):
	def __init__(self):
		self.params = PARAMS
		self.read()
	
	def get(self,key):
		try:
			return self.params[key]
		except KeyError:
			self.params[key] = PARAMS[key]
			return self.params[key]
		
	def set(self,key,value):
		self.params[key] = value
			
	def read(self):		
		try:
			f=codecs.open(CONFIG_FILE,'r','utf-8')
		except IOError:
			self.save()
			f=codecs.open(CONFIG_FILE,'r','utf-8')
		try:
			self.params = json.loads(f.read())
		except ValueError:
			self.save()
		f.close()

	def save(self):
		if not os.path.exists(CONFIG_APP_DIR):
			os.makedirs(CONFIG_APP_DIR)
		f=codecs.open(CONFIG_FILE,'w','utf-8')
		f.write(json.dumps(self.params))
		f.close()
		
class Preferences(Gtk.Dialog):
	def __init__(self,parent):
		Gtk.Dialog.__init__(self, APP + ' | '+_('Preferences'),parent,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
		self.ok = False
		self.set_size_request(500, 320)
		self.set_resizable(False)
		self.set_icon_name(ICON)
		self.connect('destroy', self.close_application)
		#
		vbox0 = Gtk.VBox(spacing = 5)
		vbox0.set_border_width(5)
		self.get_content_area().add(vbox0)
		#
		notebook = Gtk.Notebook()
		vbox0.add(notebook)
		#
		frame0 = Gtk.Frame()
		notebook.append_page(frame0, Gtk.Label.new(_('Replacements')))
		#
		hbox = Gtk.HBox()
		frame0.add(hbox)
		#
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_size_request(400,300)
		scrolledwindow.set_border_width(2)
		scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolledwindow.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)				
		hbox.pack_start(scrolledwindow,True,True,0)
		self.treeview = Gtk.TreeView()
		scrolledwindow.add(self.treeview)
		#
		self.model = Gtk.ListStore(str,str)
		self.treeview.set_model(self.model)
		#
		renderer_editabletext = Gtk.CellRendererText()
		renderer_editabletext.set_property("editable", True)
		renderer_editabletext.connect("edited", self.text_edited_value)
		column = Gtk.TreeViewColumn(_('Replace'),renderer_editabletext,text=0)
		self.treeview.append_column(column)		
		#
		renderer_editabletext2 = Gtk.CellRendererText()
		renderer_editabletext2.set_property("editable", True)
		renderer_editabletext2.connect("edited", self.text_edited_width)
		column = Gtk.TreeViewColumn(_('With'),renderer_editabletext2,text=1)
		self.treeview.append_column(column)		
		#
		vbox1 = Gtk.VBox(spacing = 0)
		hbox.pack_start(vbox1,False,False,0)
		#
		button_add = Gtk.Button()
		button_add.set_size_request(40,40)
		button_add.set_tooltip_text(_('Add'))	
		button_add.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_ADD,Gtk.IconSize.BUTTON))
		button_add.connect('clicked',self.on_button_add_clicked)
		vbox1.pack_start(button_add,False,False,0)
		#
		button_remove = Gtk.Button()
		button_remove.set_size_request(40,40)
		button_remove.set_tooltip_text(_('Remove'))		
		button_remove.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_REMOVE,Gtk.IconSize.BUTTON))
		button_remove.connect('clicked',self.on_button_remove_clicked)
		vbox1.pack_start(button_remove,False,False,0)		
		#
		self.load_preferences()
		#
		self.show_all()		

	def on_button_add_clicked(self,widget):
		self.model.append(['',''])	

	def on_button_remove_clicked(self,widget):
		model,treeiter = self.treeview.get_selection().get_selected()
		if treeiter:
			model.remove(treeiter)
		
	def load_preferences(self):		
		self.model.clear()
		configuration = Configuration()
		for replacement in configuration.get('replacements'):
			self.model.append([replacement['value'],replacement['with']])
				
	def save_preferences(self):
		configuration = Configuration()
		replacements = []
		itera=self.model.get_iter_first()
		while(itera!=None):
			replace_this = self.model.get(itera, 0)[0]
			replace_with = self.model.get(itera, 1)[0]
			replacement = {}
			replacement['value'] = replace_this
			replacement['with'] = replace_with
			replacements.append(replacement)
			itera=self.model.iter_next(itera)	
		configuration.set('replacements',replacements)
		configuration.save()	

	def text_edited_value(self, widget, path, text):
		self.model[path][0] = text

	def text_edited_width(self, widget, path, text):
		self.model[path][1] = text
	
	def close_application(self,widget):
		self.hide()

	def toInt(self,valor):
		if len(valor)>0 and valor.isdigit():
			return int(float(valor))
		else:
			return 0

class MovieTitleDialog(Gtk.Dialog): # needs GTK, Python, Webkit-GTK
	def __init__(self,files = None):
		#***************************************************************
		Gtk.Dialog.__init__(self,'Movietitle',None,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_size_request(900, 400)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_icon_name(ICON)
		self.connect('destroy', self.on_close_dialog)
		#
		vbox0 = Gtk.VBox(spacing = 5)
		vbox0.set_border_width(5)
		self.get_content_area().add(vbox0)
		#
		frame4 = Gtk.Frame()
		vbox0.pack_start(frame4,True,True,0)
		#
		hbox4 = Gtk.HBox(spacing = 5)
		hbox4.set_border_width(5)
		frame4.add(hbox4)
		#
		button20 = Gtk.Button()
		button20.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_DIRECTORY,Gtk.IconSize.BUTTON))
		button20.set_size_request(32,32)
		button20.set_tooltip_text(_('Load files'))
		button20.connect('clicked',self.on_button_load_clicked)
		hbox4.pack_start(button20,False,False,0)			
		#
		self.button23 = Gtk.Button()
		self.button23.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_FIND,Gtk.IconSize.BUTTON))
		self.button23.set_size_request(32,32)
		self.button23.set_tooltip_text(_('Preview'))
		self.button23.set_sensitive(False)
		self.button23.connect('clicked',self.on_button_preview_clicked)
		hbox4.pack_start(self.button23,False,False,0)			
		#
		button21 = Gtk.Button()
		button21.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_PROPERTIES,Gtk.IconSize.BUTTON))
		button21.set_size_request(32,32)
		button21.set_tooltip_text(_('Set preferences'))
		button21.connect('clicked',self.on_button_preferences_clicked)
		hbox4.pack_start(button21,False,False,0)			
		#
		button22 = Gtk.Button()
		button22.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_ABOUT,Gtk.IconSize.BUTTON))
		button22.set_size_request(32,32)
		button22.set_tooltip_text(_('About'))
		button22.connect('clicked',self.on_button_about_clicked)
		hbox4.pack_start(button22,False,False,0)			
		#
		self.button24 = Gtk.Button()
		self.button24.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_EXECUTE,Gtk.IconSize.BUTTON))
		self.button24.set_size_request(32,32)
		self.button24.set_tooltip_text(_('Run'))
		self.button24.set_sensitive(False)
		self.button24.connect('clicked',self.on_button_rename_clicked)
		hbox4.pack_end(self.button24,False,False,0)			
		#
		frame3 = Gtk.Frame()
		vbox0.pack_start(frame3,True,True,0)
		#
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_size_request(600,300)
		scrolledwindow.set_border_width(2)
		frame3.add(scrolledwindow)
		self.treeview = Gtk.TreeView()
		scrolledwindow.add(self.treeview)
		#
		model = Gtk.ListStore(str,str,str)
		self.treeview.set_model(model)
		#
		column = Gtk.TreeViewColumn(_('Source'),Gtk.CellRendererText(),text=1)
		self.treeview.append_column(column)		
		#
		renderer_editabletext = Gtk.CellRendererText()
		renderer_editabletext.set_property("editable", True)
		renderer_editabletext.connect("edited", self.text_edited_width)		
		column = Gtk.TreeViewColumn(_('Modified'),renderer_editabletext,text=2)
		self.treeview.append_column(column)		
		#
		self.about_dialog = None
		#
		if files:
			for file in files:
				if os.path.isfile(file):
					head,tail = os.path.split(file)
				model.append([head,tail,''])	
		self.show_all()
		configuration = Configuration()
		self.file_dir = configuration.get('file_dir')
		if len(self.file_dir)<=0 or os.path.exists(self.file_dir)==False:
			self.file_dir = os.getenv('HOME')				
	
	def text_edited_width(self, widget, path, text):
		model = self.treeview.get_model()
		model[path][2] = text

	def on_button_about_clicked(self,widget):
		if self.about_dialog:
			self.about_dialog.present()
		else:
			self.about_dialog = self.get_about_dialog()
			self.about_dialog.run()
			self.about_dialog.destroy()
			self.about_dialog = None

	# Build application about dialog
	def get_about_dialog(self):
		"""Create and populate the about dialog."""
		about_dialog = Gtk.AboutDialog()
		about_dialog.set_name(_(APPNAME))
		about_dialog.set_version(VERSION)
		about_dialog.set_copyright('Copyrignt (c) 2016\nLorenzo Carbonell')
		about_dialog.set_comments(_('An extension for Nautilus to clean movie title'))
		about_dialog.set_license('' +
								 'This program is free software: you can redistribute it and/or modify it\n' +
								 'under the terms of the GNU General Public License as published by the\n' +
								 'Free Software Foundation, either version 3 of the License, or (at your option)\n' +
								 'any later version.\n\n' +
								 'This program is distributed in the hope that it will be useful, but\n' +
								 'WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY\n' +
								 'or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for\n' +
								 'more details.\n\n' +
								 'You should have received a copy of the GNU General Public License along with\n' +
								 'this program.  If not, see <http://www.gnu.org/licenses/>.')
		about_dialog.set_website('http://www.atareao.es')
		about_dialog.set_website_label('http://www.atareao.es')		
		about_dialog.set_authors(['Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
		about_dialog.set_documenters(['Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
		about_dialog.set_translator_credits('')
		about_dialog.set_icon(GdkPixbuf.Pixbuf.new_from_file(ICON))
		about_dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(ICON))
		about_dialog.set_program_name(_(APPNAME))
		return about_dialog
		
		
	def on_button_preferences_clicked(self,widget):
		preferences = Preferences(self)
		if preferences.run() == Gtk.ResponseType.ACCEPT:
			preferences.save_preferences()
		preferences.destroy()	

	def on_button_preview_clicked(self,widget):
		model = self.treeview.get_model()
		itera=model.get_iter_first()
		configuration = Configuration()
		canRun = True
		while(itera!=None):
			source = model.get(itera, 1)[0]
			print(source)
			try:
				destination = self.evalua(source,configuration)
			except  Exception as e:
				print(e)
				destination = 'Error'
				anError = False
			model.set(itera,2,destination)
			itera=model.iter_next(itera)
		self.button24.set_sensitive(canRun)
		
	def on_close_dialog(self,widget):
		configuration = Configuration()
		configuration.set('file_dir',self.file_dir)
		configuration.save()
		self.hide()

	def on_button_load_clicked(self,widget):		
		dialog = Gtk.FileChooserDialog(_('Select one or more movie files to rename'),
										self,
									   Gtk.FileChooserAction.OPEN,
									   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
										Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		dialog.set_default_response(Gtk.ResponseType.OK)
		dialog.set_select_multiple(True)
		dialog.set_current_folder(self.file_dir)
		filter = Gtk.FileFilter()
		filter.set_name(_('Movie files'))
		filter.add_mime_type('video/mpeg')
		filter.add_mime_type('video/x-msvideo')
		filter.add_mime_type('video/x-matroska')
		filter.add_pattern('*.mpeg')
		filter.add_pattern('*.mpg')
		filter.add_pattern('*.avi')
		filter.add_pattern('*.mkv')
		dialog.add_filter(filter)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.button23.set_sensitive(False)
			filenames = dialog.get_filenames()
			if len(filenames)>0:
				model = self.treeview.get_model()
				model.clear()
				self.button24.set_sensitive(False)
				for filename in filenames:
					if os.path.isfile(filename):
						head,tail = os.path.split(filename)
					model.append([head,tail,''])	
				self.button23.set_sensitive(True)
				self.file_dir = os.path.dirname(filenames[0])
				if len(self.file_dir)<=0 or os.path.exists(self.file_dir)==False:
					self.file_dir = os.getenv('HOME')				
					
			
		dialog.destroy()
	
	def on_button_rename_clicked(self,widget):
		model = self.treeview.get_model()
		itera=model.get_iter_first()
		while(itera!=None):
			head = model.get(itera, 0)[0]
			source = os.path.join(head,model.get(itera, 1)[0])
			destination = os.path.join(head,model.get(itera, 2)[0])
			print ('from %s to %s'%(source,destination))
			try:
				if model.get(itera, 2)[0]!= 'Error':
					os.rename(source,destination)
					model.set(itera,1,model.get(itera, 2)[0])
			except Exception as e:
				print(e)
				model.set(itera,2,'Error')
			itera=model.iter_next(itera)
					
	def evalua(self,mfile,configuration):
		filename,ext=os.path.splitext(mfile)
		filename = filename.lower()
		ext = ext.lower()
		for replacement in configuration.get('replacements'):
			filename = filename.replace(replacement['value'],replacement['with'].lower())
			filename=filename.strip()
			filename=filename.rstrip()
			filename=filename.lstrip()
			filename=filename.capitalize()
			filename=filename.replace('( )','')
			filename=filename.replace('()','')
			filename=filename.rstrip()
			filename=filename.lstrip()
		return filename+ext

class MovieTitleMenuProvider(GObject.GObject, Nautilus.MenuProvider):
	"""Implements the 'movietitle' extension to the nautilus right-click menu"""
	def __init__(self):
		"""Nautilus crashes if a plugin doesn't implement the __init__ method"""
		pass

	def rename_files(self, menu, selected):		
		"""Runs the movietitle in Filenames on the given Directory"""
		files = get_files(selected)
		if files:
			dialog = MovieTitleDialog(files)
			dialog.run()
			dialog.hide()
			dialog.destroy()
	
	def get_file_items(self, window, sel_items):
		"""Adds the 'Replace in Filenames' menu item to the Nautilus right-click menu,
		   connects its 'activate' signal to the 'run' method passing the selected Directory/File"""
		#if len(sel_items) != 1 or sel_items[0].get_uri_scheme() not in ['file', 'smb']: return
		item = Nautilus.MenuItem(name='MovieTitleMenuProvider::Gtk-rename-movie-files',
								 label='Renombra archivos de pelicula',
								 tip='Renombra archivos de pelicula',
								 icon='Gtk-find-and-replace')
		item.connect('activate', self.rename_files, sel_items)
		return item,

if __name__ == '__main__':
	rd = MovieTitleDialog(None)
	rd.run()
	rd.hide()
	rd.destroy()	
	exit(0)
