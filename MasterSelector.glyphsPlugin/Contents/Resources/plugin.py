# encoding: utf-8

###########################################################################################################
#
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################


from GlyphsApp.plugins import *
from vanilla import *



class MasterSelectorWindow(GeneralPlugin):
	def settings(self):
		self.name = Glyphs.localize({'en': u'Master Selector'})
	
	def start(self):
		try: 
			# new API in Glyphs 2.3.1-910
			newMenuItem = NSMenuItem(self.name, self.showWindow)
			Glyphs.menu[WINDOW_MENU].append(newMenuItem)
		except:
			mainMenu = Glyphs.mainMenu()
			s = objc.selector(self.showWindow,signature='v@:@')
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, s, "")
			newMenuItem.setTarget_(self)
			mainMenu.itemWithTag_(5).submenu().addItem_(newMenuItem)
	
	def showWindow(self, sender):
		
		mastersList = []
		for m in Glyphs.font.masters:
			mastersList.append(m.name)
		currentMasterIndex = Glyphs.font.masterIndex

		self.windowWidth = 200
		self.windowHeight = 25*len(mastersList)+23+30

		self.w = FloatingWindow((self.windowWidth, self.windowHeight), "Master Selector")
		
		
		#self.w.masters = PopUpButton((spX, spY*2+edY, -spX, edY), mastersList, callback=self.changeMaster)
		self.w.radiomasters = RadioGroup((10, 10, -10, 25*len(mastersList)),
                                mastersList,
                                callback=self.changeMaster)
		self.w.slider = Slider((10, -35, -10, 23),
                            tickMarkCount=len(mastersList),
                            stopOnTickMarks = True,
                            value = currentMasterIndex,
                            minValue = 0,
                            maxValue = len(mastersList)-1,
                            sizeStyle = "small",
                            callback=self.changeMasterSlider)

		self.w.open()

	def changeMaster(self, sender):
		currentChoice = self.w.radiomasters.get()
		try:
			Glyphs.font.parent.windowController().setMasterIndex_(currentChoice)
		except:
			print 'BROKEN'
			pass

	def changeMasterSlider(self, sender):
		currentChoice = self.w.slider.get()
		try:
			Glyphs.font.parent.windowController().setMasterIndex_(currentChoice)
		except:
			print 'BROKEN'
			pass


	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__


