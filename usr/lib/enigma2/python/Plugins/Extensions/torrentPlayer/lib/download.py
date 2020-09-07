# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/torrentPlayer/lib/download.py
from Plugins.Extensions.torrentPlayer.lib.gimports import *

def makevalid_filename(s):
    import re
    badchars = re.compile('[^A-Za-z0-9_. ]+|^\\.|\\.$|^ | $|^$')
    badnames = re.compile('(aux|com[1-9]|con|lpt[1-9]|prn)(\\.|$)')
    try:
        name = badchars.sub('_', s)
        if badnames.match(name):
            name = '_' + name
        try:
            name = name.split('_')[0]
        except:
            pass

        return name
    except:
        try:
            name = s.split('_')[0]
        except:
            pass

        return name


def IsValidFileName(name, NAME_MAX = 255):
    prohibited_characters = ['/',
     '\x00',
     '\\',
     ':',
     '*',
     '<',
     '>',
     '|',
     '"']
    if isinstance(name, basestring) and 1 <= len(name) <= NAME_MAX:
        for it in name:
            if it in prohibited_characters:
                return False

        return True
    return False


def RemoveDisallowedFilenameChars(name, replacment = '.'):
    prohibited_characters = ['/',
     '\x00',
     '\\',
     ':',
     '*',
     '<',
     '>',
     '|',
     '"']
    for item in prohibited_characters:
        name = name.replace(item, replacment).replace(replacment + replacment, replacment)

    return name


def checkdownloadPath(path = None):
    try:
        if os.path.exists(path) == False:
            return (False, 'Download direcotry is not available')
        if path is None:
            return (False, 'No Download direcotry given')
        sp = []
        sp = path.split('/')
        print sp
        if len(sp) > 1:
            if sp[1] != 'media':
                return (False, mounted_string % path)
        mounted = False
        swappable = False
        sp2 = []
        f = open('/proc/mounts', 'r')
        m = f.readline()
        while m and not mounted:
            if m.find('/%s/%s' % (sp[1], sp[2])) is not -1:
                mounted = True
                print m
                sp2 = m.split(' ')
                print sp2
                if sp2[2].startswith('ext') or sp2[2].endswith('fat'):
                    print '[stFlash] swappable'
                    swappable = True
            m = f.readline()

        f.close()
        if not mounted:
            return (False, mounted_string + str(path))
        freespace, spacestr = getfreespace(path)
        if freespace < 200:
            return (False, 'Download is not allowed with freespace less than 200mb')
        return (True, 'success')
    except:
        return (False, 'invalid download folder ')

    return


def getfreespace(downloadlocation = None):
    if os.path.exists(downloadlocation) == False:
        return (0, 'Download location is not available')
    else:
        try:
            diskSpace = os.statvfs(downloadlocation)
            capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
            available = float(diskSpace.f_bsize * diskSpace.f_bavail)
            fspace = round(float(available / 1048576.0), 2)
            tspace = round(float(capacity / 1048576.0), 1)
            spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
            return (fspace, spacestr)
        except:
            return (None, None)

        return None
        return None


class torrentPlayerdownload2(Screen):
    skin = '    <screen\n        name = "torrentPlayerdownload2"\n        position = "center,center"\n        size = "1050,450"\n        title = "Download menu">\n        <widget\n            name = "text"\n            position = "105,12"\n            size = "1050,120"\n            font = "Regular;33"\n            transparent = "1"/>\n        <widget\n            name = "list"\n            position = "22,150"\n            itemHeight = "50"            \n            size = "975,300"\n            transparent = "1"/>\n    </screen>'

    def __init__(self, session, url = None, name = None):
        self.session = session
        self.url = url
        self.name = name
        Screen.__init__(self, session)
        self.list = [(_('Download'), 0),
         (_('Current downloading'), 1),
         (_('Select Download location'), 2),
         (_('Downloads'), 3),
         (_('General settings'), 34)]
        text = 'Download location:' + config.torrentPlayer.downloadlocation.value + '\nFreespace:' + self.calfreespace()
        self['text'] = Label(text)
        self.lines = []
        print '102', self.url
        self['list'] = MenuList(self.list)
        self['actions'] = ActionMap(['MsgBoxActions', 'DirectionActions'], {'cancel': self.cancel,
         'ok': self.ok,
         'alwaysOK': self.alwaysOK,
         'up': self.up,
         'down': self.down,
         'left': self.left,
         'right': self.right,
         'upRepeated': self.up,
         'downRepeated': self.down,
         'leftRepeated': self.left,
         'rightRepeated': self.right}, -1)

    def refresh(self, result = None):
        text = 'Download location:' + config.torrentPlayer.downloadlocation.value + '\nFreespace:' + self.calfreespace()
        self['text'].setText(text)

    def progress_callback(self, data):
        print data

    def startdownload(self, action = 'download'):
        if action == 'view':
            from tsdownload import startdownload
            startdownload(self.session, 'view', '', '', '', PLUGIN_PATH)
            return
        lines = []
        lines.append((self.name, self.name))
        lines.append(('User input', 'user input'))
        from Screens.ChoiceBox import ChoiceBox
        self.session.openWithCallback(self.choicesback, ChoiceBox, _('select download file name'), lines)

    def choicesback(self, select):
        if select:
            if select[0] == 'User input':
                from Screens.VirtualKeyBoard import VirtualKeyBoard
                import os
                self.session.openWithCallback(self.begindownload, VirtualKeyBoard, title=_('Enter your movie title(s)'), text='')
            else:
                self.begindownload(select[0])

    def begindownload(self, select):
        if select:
            from tsdownload import startdownload
            dlocation = config.torrentPlayer.downloadlocation.value
            success, txt = checkdownloadPath(dlocation)
            if success == False:
                self.session.open(MessageBox, txt, MessageBox.TYPE_ERROR)
                return
            name = str(select)
            if '/' in name:
                name.replace('/', '_')
            name = name.replace('/', '-').replace('.', '-').replace('|', '-')
            title = name
            extension = '.mp4'
            if self.url.endswith('.flv'):
                extension = '.flv'
            elif self.url.endswith('.mp4'):
                extension = '.mp4'
            elif self.url.endswith('.mp3'):
                extension = '.mp3'
            elif self.url.endswith('.png'):
                extension = '.png'
            elif self.url.endswith('.jpg'):
                extension = '.hpg'
            elif self.url.endswith('.mkv'):
                extension = '.mkv'
            elif self.url.endswith('.ts'):
                extension = '.ts'
            dname = name + extension
            try:
                dname = dname.encode('utf-8', 'ignore')
            except:
                pass

            target = os.path.join(dlocation, dname)
            from tsdownload import startdownload
            val = startdownload(self.session, 'download', self.url, target, name, PLUGIN_PATH, wget=True)
            if val == True:
                self.close()
            return

    def calfreespace(self):
        freespace, freespacestr = getfreespace(config.torrentPlayer.downloadlocation.value)
        if freespace is not None:
            return freespacestr
        else:
            return 'Free space unknown'
            return

    def ok(self):
        if self['list'].getCurrent()[1] == 0:
            self.startdownload('download')
        elif self['list'].getCurrent()[1] == 1:
            self.startdownload('view')
        elif self['list'].getCurrent()[1] == 2:
            from DownloadLocation import TStvdownloadLocation
            self.session.openWithCallback(self.refresh, TStvdownloadLocation)
        elif self['list'].getCurrent()[1] == 3:
            from filesexplorer import torrentPlayerFiles
            self.session.open(torrentPlayerFiles)
        else:
            from Plugins.Extensions.torrentPlayer.lib.torrentPlayerSetup import torrentPlayerSetup
            self.session.open(torrentPlayerSetup)

    def cancel(self):
        self.close(False)

    def alwaysOK(self):
        self.close(True)

    def up(self):
        self.move(self['list'].instance.moveUp)

    def down(self):
        self.move(self['list'].instance.moveDown)

    def left(self):
        self.move(self['list'].instance.pageUp)

    def right(self):
        self.move(self['list'].instance.pageDown)

    def move(self, direction):
        self['list'].instance.moveSelection(direction)


torrentPlayerdownload = torrentPlayerdownload2