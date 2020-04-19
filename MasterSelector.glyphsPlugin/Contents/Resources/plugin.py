# encoding: utf-8
from __future__ import division, print_function, unicode_literals

##############################################################################
#
#
#  Master Selector Plugin
#
#  With this plugin you can navigate multi-master Glyphs Files more easily.
#  Slider included.
#
#  Benedikt Bramboeck, 2018
#
##############################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import Slider, FloatingWindow, RadioGroup

class MasterSelectorWindow(GeneralPlugin):
	
	@objc.python_method
	def settings(self):
		self.name = 'Master Selector'
		self.warningOnlyOneMaster = Glyphs.localize({
			"en": "Your font has only one master.",
			"de": "Die Schrift hat nur einen Master.",
			"fr": "La police contient seulement un master.",
			"es": "La fuente tiene solamente un máster.",
		})
		self.warningNoFontOpen = Glyphs.localize({
			"en": "Please open a font first.",
			"de": "Bitte öffnen Sie erst eine Schrift.",
			"fr": "Veuillez ouvrir un fichier de police.",
			"es": "Por favor, primero abrir una fuente.",
		})
	
	@objc.python_method
	def start(self):
		try: 
			targetMenu = WINDOW_MENU
			newMenuItem = NSMenuItem(self.name, self.showWindow_)
			Glyphs.menu[targetMenu].append(newMenuItem)
		except:
			mainMenu = Glyphs.mainMenu()
			s = objc.selector(self.showWindow,signature='v@:@')
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, s, "")
			newMenuItem.setTarget_(self)
			mainMenu.itemWithTag_(5).submenu().addItem_(newMenuItem)
	
	def showWindow_(self, sender):
		if Glyphs.font is None:
			self.helperWindow(self.warningNoFontOpen)
		elif len(Glyphs.font.masters) < 2:
			self.helperWindow(self.warningOnlyOneMaster)
		else:
			mastersList = []
			for m in Glyphs.font.masters:
				mastersList.append(m.name)
			currentMasterIndex = Glyphs.font.masterIndex

			self.windowWidth = 250
			self.windowHeight = 25*len(mastersList)+23+30
			self.w = FloatingWindow((self.windowWidth, self.windowHeight), self.name)
			self.w.radiomasters = RadioGroup((10, 10, -10, 25*len(mastersList)),
				mastersList,
				callback=self.changeMaster)
			self.w.slider = Slider((10, -35, -10, 23),
				tickMarkCount=len(mastersList),
				stopOnTickMarks=True,
				value=currentMasterIndex,
				minValue=0,
				maxValue=len(mastersList)-1,
				sizeStyle="small",
				continuous=False,
				callback=self.changeMasterSlider)
			
			self.w.open()

	@objc.python_method
	def helperWindow(self, message):
		Message(title=self.name, message=message, OKButton=None)

	@objc.python_method
	def changeMaster(self, sender):
		currentChoice = self.w.radiomasters.get()
		try:
			Glyphs.font.parent.windowController().setMasterIndex_(currentChoice)
			self.w.slider.set(currentChoice)
		except:
			print('BROKEN')
			pass

	@objc.python_method
	def changeMasterSlider(self, sender):
		currentChoice = int(self.w.slider.get())
		try:
			Glyphs.font.parent.windowController().setMasterIndex_(currentChoice)
			self.w.radiomasters.set(currentChoice)
		except:
			print('BROKEN')
			pass

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__


