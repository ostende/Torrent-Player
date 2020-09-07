# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/torrentPlayer/lib/tSelecter.py
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
import os
from enigma import loadPNG, getDesktop, RT_WRAP, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, gFont
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
reswidth = getDesktop(0).size().width()
resheight = getDesktop(0).size().height()

class tSelecter(Screen):
    if reswidth == 1920:
        skin = '\n                <screen name="tSelecter" position="center,center" size="900,720" backgroundColor="#16000000" transparent="0" title="Addkey" >\n                       <widget name="menu" position="30,30" size="900,720" backgroundColor="#16000000" transparent = "0" />\n                </screen>'
    else:
        skin = '\n                <screen name="tSelecter" position="center,center" size="600,520" backgroundColor="#16000000" transparent="0" title="Addkey" >\n                       <widget name="menu" position="20,20" size="600,520" backgroundColor="#16000000" transparent = "0" />\n                </screen>'

    def __init__(self, session, title, datalist = []):
        Screen.__init__(self, session)
        self['menu'] = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self['actions'] = ActionMap(['ColorActions', 'WizardActions'], {'back': self.close,
         'ok': self.exit,
         'back': self.close}, -1)
        self.settitle(title, datalist)

    def settitle(self, title, datalist):
        self.setTitle(title)
        self.showmenulist(datalist)

    def exit(self):
        index = self['menu'].getSelectionIndex()
        self.close(index)

    def showmenulist(self, datalist):
        cacolor = 16776960
        cbcolor = 16753920
        cccolor = 15657130
        cdcolor = 16711680
        cecolor = 16729344
        cfcolor = 65407
        cgcolor = 11403055
        chcolor = 13047173
        cicolor = 13789470
        scolor = cbcolor
        res = []
        menulist = []
        if reswidth == 1280:
            self['menu'].l.setItemHeight(50)
            self['menu'].l.setFont(0, gFont('Regular', 28))
        else:
            self['menu'].l.setItemHeight(75)
            self['menu'].l.setFont(0, gFont('Regular', 42))
        for i in range(0, len(datalist)):
            txt = datalist[i][1]
            if reswidth == 1280:
                png = os.path.join('/usr/lib/enigma2/python/Plugins/Extensions/torrentPlayer/interface/tselecter_icons/hd40/%s.png' % datalist[i][2])
            else:
                png = os.path.join('/usr/lib/enigma2/python/Plugins/Extensions//torrentPlayer/interface/tselecter_icons/fhd75/%s.png' % datalist[i][2])
            res.append(MultiContentEntryText(pos=(0, 1), size=(0, 0), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text='', color=scolor, color_sel=cccolor, border_width=3, border_color=806544))
            if reswidth == 1280:
                res.append(MultiContentEntryText(pos=(60, 1), size=(723, 50), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text=str(txt), color=16777215, color_sel=16777215))
                res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(40, 40), png=loadPNG(png)))
            else:
                res.append(MultiContentEntryText(pos=(100, 1), size=(1080, 75), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text=str(txt), color=16777215, color_sel=16777215))
                res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(75, 75), png=loadPNG(png)))
            menulist.append(res)
            res = []

        self['menu'].l.setList(menulist)
        self['menu'].show()