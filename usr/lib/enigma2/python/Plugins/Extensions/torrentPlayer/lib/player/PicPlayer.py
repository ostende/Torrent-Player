# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/lib/player/PicPlayer.py
from Plugins.Extensions.TSmedia.lib.gimports import *
from Components.AVSwitch import AVSwitch
from enigma import gPixmapPtr
from twisted.web.client import downloadPage, getPage
from Plugins.Extensions.TSmedia.lib.pltools import logdata, trace_error
from Plugins.Extensions.TSmedia.screens.adTools import adTools

def getScale():
    return AVSwitch().getFramebufferScale()


import random
from enigma import eServiceReference, iServiceInformation, gPixmapPtr
from Tools.Directories import copyfile

def getrandom(cmax = 10, list1 = []):
    rand = 0
    try:
        rand = random.randrange(0, cmax)
        if rand in list1:
            rand = random.randrange(0, cmax)
    except:
        rand = 0

    return rand


class picplayer(Screen, adTools):

    def __init__(self, session, picurl, picname = None, addon_params = {}, plugin_id = None, playlist = [], playindex = 0, playall = True, sender = None):
        Screen.__init__(self, session)
        self.playlist = playlist
        self.playIdx = playindex
        self.page = 1
        self.addon_params = addon_params
        try:
            section = addon_params['section']
        except:
            section = None

        self.slideshow = False
        try:
            self.module = addon_params['module']
        except:
            self.module = None

        self.sender = sender
        self.section = section
        self.long_plugin_id = plugin_id
        self.skinName = 'TSPplayer'
        self['cover'] = Pixmap()
        self.session = session
        self.plugin_id = plugin_id
        self.plugin_path = PLUGIN_PATH
        self['programm'] = Label('Showing picture..')
        playlist = []
        self.randomplay = False
        self.forcenext = False
        self['channel_number'] = Label(str(self.page) + '/' + str(playindex))
        self['actions'] = ActionMap(['ColorActions',
         'WizardActions',
         'MediaPlayerSeekActions',
         'InfobarInstantRecord',
         'MediaPlayerActions',
         'EPGSelectActions',
         'MoviePlayerActions',
         'ColorActions',
         'InfobarActions',
         'MenuActions',
         'NumberActions'], {'leavePlayer': self.leavePlayer,
         'info': self.openinfo,
         'instantRecord': self.startdownload,
         'back': self.leavePlayer,
         'left': self.seekBack,
         '0': self.playnext,
         'right': self.seekFwd}, -1)
        self.playAll = playall
        self.icon_showed = False
        self.slideshow = False
        self.randomlist = []
        self.totalresults = 0
        self.startindex = self.playIdx
        self.playLen = len(self.playlist)
        self.shown = False
        try:
            self.picurl = self.playllist[0].get('url', '')
        except:
            self.picurl = ''

        self.music_running = False
        self.picname = picname
        self.onClose.append(self.playExit)
        self.timer = eTimer()
        if enigmaos == 'oe2.0':
            self.timer.callback.append(self.shownextimage)
        else:
            self.timer_connect = self.timer.timeout.connect(self.shownextimage)
        adTools.__init__(self, self.session, addon_params, self.showCallback)
        self.newindex = self.playIdx
        self.onLayoutFinish.append(self.playStream)
        return

    def playnext(self):
        if self.slideshow == True:
            self.startslideshow()
        else:
            try:
                self.timer.stop()
            except:
                pass

            self.slideshow = False

    def loadPic(self, sTitle = None):
        if sTitle is None or sTitle.strip() == '':
            try:
                streamPic = self.playlist[self.playIdx]['image']
            except:
                streamPic = None

            print '320', streamPic
            if streamPic is None or streamPic == '':
                fanart = PLUGIN_PATH + '/' + self.long_plugin_id + '/fanart.jpg'
                if os.path.exists(fanart):
                    cover = fanart
                else:
                    cover = PLUGIN_PATH + '/interface/TSMplayer/radio.png'
                os.system('cp ' + cover + '/tmp/cover.jpg')
                copyfile(cover, '/tmp/cover.jpg')
                self.ShowCover(streamPic)
            else:
                downloadPage(streamPic, '/tmp/cover.jpg').addCallback(self.ShowCover).addErrback(self.showerror)
        else:
            sTitle = sTitle.replace('\n', ' ')
            sTitle = sTitle.replace('-', ' ')
            sTitle = sTitle[:50]
            sTitle = sTitle.replace(' ', '+')
            gimage_url = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + sTitle + '&imgsz=xlarge'
            getPage(gimage_url).addCallback(self.ShowCover2).addErrback(self.showerror)
        return

    def showgoogleimage(self):
        gimage_url = str(self.playlist[self.newindex]['url'])
        print 'gimage_urlxx', gimage_url
        getPage(gimage_url).addCallback(self.ShowCover2).addErrback(self.showerror)

    def ShowCover2(self, imagedata):
        if imagedata:
            match = re.findall('"url":"(.*?)"', imagedata, re.M | re.I)
            print 'match', match
            if match:
                for imageurl in match:
                    if imageurl.endswith('.jpg') or imageurl.endswith('.jpeg') or imageurl.endswith('.png') or 'images' in imageurl:
                        print '346', imageurl
                        downloadPage(imageurl, '/tmp/cover.jpg').addCallback(self.ShowCover).addErrback(self.showerror)
                        return

            self.showerror(None)
        else:
            self.showerror(None)
        return

    def showerror(self, error):
        fanart = PLUGIN_PATH + '/' + self.long_plugin_id + '/fanart.jpg'
        if os.path.exists(fanart):
            cover = fanart
        else:
            cover = PLUGIN_PATH + '/interface/TSMplayer/radio.png'
        copyfile(cover, '/tmp/cover.jpg')
        self.ShowCover(None)
        return

    def ShowCover(self, picfile = None):
        if picfile:
            pass
        elif fileExists('/tmp/cover.jpg'):
            picfile = '/tmp/cover.jpg'
        if picfile:
            self['cover'].instance.setPixmap(gPixmapPtr())
            self.scale = AVSwitch().getFramebufferScale()
            self.picload = ePicLoad()
            size = self['cover'].instance.size()
            self.picload.setPara((size.width(),
             size.height(),
             self.scale[0],
             self.scale[1],
             False,
             1,
             '#FF000000'))
            if enigmaos == 'oe2.0':
                value = self.picload.startDecode(picfile, 0, 0, False)
            else:
                value = self.picload.startDecode(picfile, False)
            if value == 0:
                ptr = self.picload.getData()
                if ptr != None:
                    self['cover'].instance.setPixmap(ptr)
                    self['cover'].show()
                    del self.picload
        return

    def showimageCover(self, streamPic):
        print 'streamPic32', streamPic
        if streamPic.lower().startswith('http'):
            try:
                os.path.remove('/tmp/cover.jpg')
            except:
                pass

            print "fileExists('/tmp/cover.jpg')1", fileExists('/tmp/cover.jpg')
            downloadPage(streamPic, '/tmp/cover.jpg').addCallback(self.ShowCover).addErrback(self.showerror)
            return
        if streamPic.lower().startswith('/'):
            self.ShowCover(streamPic)

    def ShowPlugin_icon(self):
        return
        micon = PLUGIN_PATH + '/addons/' + self.long_plugin_id + '/icon.png'
        if not os.path.exists(micon):
            micon = PLUGIN_PATH + '/interface/micons/tv.png'
        if os.path.exists(micon):
            print '279', 'ok'
            self['plugin_icon'].instance.setPixmapFromFile(micon)

    def startdownload(self):
        serviceurl = self.playlist[self.playIdx]['url']
        servicename = self.playlist[self.playIdx]['name']
        if servicename is None:
            servicename = 'No title'
        if serviceurl is None:
            return
        else:
            from Plugins.Extensions.TSmedia.lib.download import TSmediadownload
            self.session.open(TSmediadownload, serviceurl, servicename)
            return
            return

    def startslideshow(self):
        self.slideshow = True
        self.timer.start(5000, False)

    def shownextimage(self):
        logdata('self.slideshow7777', self.slideshow)
        if self.slideshow == False:
            return
        self.seekFwd()
        self.timer.start(7000, False)

    def seekBack(self):
        try:
            if self.forcenext == True:
                self.process_playlist('back')
                return
            if len(self.playlist) > 0:
                try:
                    self.process_playlist('back')
                except:
                    self['programm'].setText('Unable to play previous picture')

            else:
                self['programm'].setText('playlist not supported or empty')
                return
        except:
            self['programm'].setText('Unable to play previous picture')

    def seekFwd(self, playrandom = False):
        self.randomplay = playrandom
        if True:
            if len(self.playlist) > 0:
                self.process_playlist('forward')
            else:
                self['programm'].setText('playlist is empty')
                return
        else:
            self['programm'].setText('unable to play next video-2')

    def openinfo(self):
        pass

    def playStream(self):
        logdata('self.playlist888', self.playlist)
        logdata('self.playIdx888', self.playIdx)
        logdata('self.picurl888', self.picurl)
        logdata('self.icon_showed', self.icon_showed)
        if self.icon_showed == False:
            self.icon_showed = True
            self.ShowPlugin_icon()
            self.slideshow = True
            self.playnext()
        logdata('self.playlist888', self.playlist)
        logdata('self.playIdx888', self.playIdx)
        logdata('show', self.icon_showed)
        logdata('self.picurl888', self.picurl)
        self.showimageCover(self.picurl)
        show = self.playlist[self.playIdx].get('show', None)
        logdata('show888', show)
        if show:
            sref = eServiceReference(4097, 0, str(show))
            sref.setName('music')
            self.music_running = True
            self.session.nav.playService(sref)
        return

    def leavePlayer(self):
        self.playExit()
        self.is_closing = True
        if self.music_running:
            self.session.nav.stopService()
        self.close(self.playIdx)

    def leavePlayerConfirmed(self, answer):
        self.is_closing = True

    def handleLeave(self, how = 'noask'):
        self.is_closing = True
        self.leavePlayerConfirmed([True, how])

    def playExit(self):
        print 'playExit:'
        if fileExists('/tmp/cover.jpg'):
            try:
                os.remove('/tmp/cover.jpg')
            except:
                pass

    def showCallback(self, result = False, datalist = [], msg = '', newindex = 0):
        if result == False:
            self['programm'].setText('Failed to process next item')
        elif len(datalist) == 1:
            mode = datalist[0].get('mode', -10)
            url = datalist[0].get('url', '')
            title = datalist[0].get('name', '')
        elif len(datalist) > 1:
            self.playlist = datalist
            self.playIdx = 0
            self.page = self.page + 1
            self.startindex = 0
            url = datalist[0].get('url', '')
            self.picurl = url
            self.timer.stop()
            self.icon_showed == False
            logdata('self.playlist999', self.playlist)
            logdata('self.playIdx999', self.playIdx)
            logdata('self.picurl999', self.picurl)
            self.playStream()
            self.process_playlist('forward')
            self.timer.stop()
            if enigmaos == 'oe2.0':
                self.timer.callback.append(self.shownextimage)
            else:
                self.timer_connect = None
                self.timer_connect = self.timer.timeout.connect(self.shownextimage)
            self.timer.start(7000, False)
        else:
            trace_error()
            self['programm'].setText('Failed to process next item')
        return

    def process_playlist(self, action):
        self['programm'].setText('Please wait..')
        self.count = 1
        self.previndex = self.playIdx
        self.playLen = len(self.playlist)
        if action == 'forward':
            self.randomplay = False
            if self.randomplay == True:
                self.newindex = getrandom(self.playLen - 1, self.randomlist)
                self.randomlist.append(self.newindex)
            else:
                self.newindex += 1
                print 'self.newidex333', self.newindex, self.playLen
                logdata('self.newidex333', self.newindex)
                logdata('self.playLen333', self.playLen)
                if self.newindex > self.playLen - 1:
                    self.newindex = 0
                logdata('self.newidex333a', self.newindex)
        elif action == 'current':
            pass
        else:
            self.newindex -= 1
            if self.newindex < 0:
                self.newindex = self.playLen - 1
        try:
            url = self.playlist[self.newindex]['url']
            logdata('url333a', url)
        except:
            trace_error()
            try:
                url = self.playlist[0]['url']
            except:
                trace_error()
                self['programm'].setText('Unable to play next picture')
                return

        try:
            title = self.playlist[self.newindex]['name']
        except:
            trace_error()
            title = 'Unknown'

        mode = self.playlist[self.newindex].get('mode', -10)
        self['programm'].setText(title)
        self['channel_number'].setText(str(self.page) + '/' + str(self.newindex))
        self.title = title
        self['programm'].setText(title)
        logdata('mode333', mode)
        if mode == 0:
            self.showimageCover(url)
        else:
            scs, msg = self.getAddonData(self.playlist[self.newindex])
            if not scs:
                msg = msg.replace('Error:', '')
                self['handlung'].setText(_(msg))

    def playstream_back(self, url):
        print 'playstream_back', url
        try:
            if url == None:
                self['programm'].setText('Sorry unable to show ' + self.title)
                self.playIdx = self.previndex
                return
            self['programm'].setText('Showing picture ' + self.title)
            if url.startswith('Error'):
                self['programm'].setText(str(url))
                self.playIdx = 0
                return
            if url.startswith('Complete'):
                self['programm'].setText(str(url))
                return
            self.picname = self.title
            self.picurl = url
            self.playStream()
        except:
            pass

        return