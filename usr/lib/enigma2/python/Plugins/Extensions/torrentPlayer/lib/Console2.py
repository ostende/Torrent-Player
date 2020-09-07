# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/torrentPlayer/lib/Console2.py
from Plugins.Extensions.torrentPlayer.lib.gimports import *
from enigma import eConsoleAppContainer
from Components.ScrollLabel import ScrollLabel
import os
from Screens.Standby import TryQuitMainloop

class torrentPlayerConsole2(Screen):
    global HD_Res
    try:
        sz_w = getDesktop(0).size().width()
        if sz_w == 1280:
            fullHD_Res = False
        elif sz_w == 1920:
            fullHD_Res = True
        else:
            fullHD_Res = False
    except:
        HD_Res = False

    if fullHD_Res == False:
        skin = '\n        \t\n                <screen name="torrentPlayerConsole3"  backgroundColor="#380038" position="center,center" size="920,600" title=""   >\n                \n\t\t<widget name="text" backgroundColor="#380038" position="30,30" size="865,570" font="Regular;22"   zPosition="2"  />\n                </screen>'
    else:
        skin = '\n        \t\n                <screen name="torrentPlayerConsole3" position="center,center" size="1380,675" title=""   >\n                \n\t\t<widget name="text" position="28,33" size="831,640" font="Regular;33"  transparent="1" zPosition="2"  />\n                </screen>'

    def __init__(self, session, title = 'Console', cmdlist = None, finishedCallback = None, closeOnSuccess = False, instr = None, endstr = None, restartE2 = False):
        Screen.__init__(self, session)
        self.color = '#800080'
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.restartE2 = restartE2
        self.endstr = 'Press OK to exit'
        instr = 'Installing please wait\nEnigma will be restarted after finishing' + '\n*************************************\n'
        self['text'] = ScrollLabel(instr)
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions', 'ColorActions'], {'blue': self.restartenigma,
         'ok': self.cancel,
         'back': self.cancel,
         'up': self['text'].pageUp,
         'down': self['text'].pageDown}, -1)
        self.cmdlist = cmdlist
        self.newtitle = title
        self.onShown.append(self.updateTitle)
        self.container = eConsoleAppContainer()
        self.run = 0
        if enigmaos == 'oe2.0':
            self.container.appClosed.append(self.runFinished)
            self.container.dataAvail.append(self.dataAvail)
        else:
            self.contianer_closed = self.container.appClosed.connect(self.runFinished)
            self.contianer_dataAvail = self.container.dataAvail.connect(self.dataAvail)
        self.onShown.append(self.onWindowShow)

    def onWindowShow(self):
        self.onShown.remove(self.onWindowShow)
        self.startRun()

    def restartenigmold(self):
        os.system('killall -9 enigma2')

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def startRun(self):
        print 'Console: executing in run', self.run, ' the command:', self.cmdlist[self.run]
        if self.container.execute(self.cmdlist[self.run]):
            self.runFinished(-1)

    def runFinished(self, retval):
        self.run += 1
        self.setTitle('Execution Finished')
        if self.run != len(self.cmdlist):
            if self.container.execute(self.cmdlist[self.run]):
                self.runFinished(-1)
        else:
            str = self['text'].getText()
            str += '\n' + _('Execution finished!!')
            self['text'].setText(str)
            self['text'].lastPage()
            if self.finishedCallback is not None and not retval:
                self.finishedCallback(True)
            if not retval and self.closeOnSuccess == False and self.restartE2 == True:
                self.restartenigma()
                self.cancel()
            else:
                str += '\n' + _(self.endstr)
                self['text'].setText(str)
                self['text'].lastPage()
        return

    def cancel(self):
        if self.finishedCallback is not None:
            self.finishedCallback(True)
        try:
            if enigmaos == 'oe2.0':
                self.container.appClosed.remove(self.runFinished)
                self.container.dataAvail.remove(self.dataAvail)
                self.close()
            else:
                self.contianer_closed = None
                self.contianer_dataAvail = None
                self.close()
            if self.run == len(self.cmdlist):
                self.close()
        except:
            pass

        return

    def dataAvail(self, str):
        self['text'].setText(self['text'].getText() + str)

    def restartenigma(self):
        if self.finishedCallback is not None:
            self.finishedCallback(True)
        self.session.open(TryQuitMainloop, 3)
        return