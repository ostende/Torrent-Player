# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/torrentPlayer/screens/kodiaddon.py
import xml.etree.cElementTree
from Plugins.Extensions.torrentPlayer.lib.gimports import *

def getaddonpath_params(item = None):
    try:
        module_path = sys.argv[0]
    except:
        return str(None)

    count = module_path.count('/')
    addon_path, module_name = os.path.split(module_path)
    if count == 11:
        section_path, addon_id = os.path.split(addon_path)
        main_addons_path, section_name = os.path.split(section_path)
        plugin_path, addons_name = os.path.split(main_addons_path)
        scripts_path = plugin_path + '/scripts'
        addons_path = section_path
    else:
        addons_path, addon_id = os.path.split(addon_path)
        plugin_path, addons_name = os.path.split(addons_path)
        if addons_name == 'XBMC':
            scripts_path = plugin_path + '/XBMC'
        else:
            scripts_path = plugin_path + '/scripts'
    if item == 'plugin_path':
        return plugin_path
    elif item == 'addons_path':
        return addons_path
    elif item == 'scripts_path':
        return scripts_path
    elif item == 'addon_id':
        return addon_id
    elif item is None:
        return (plugin_path,
         addons_path,
         scripts_path,
         addon_id)
    else:
        return
        return


class Addon:

    def __init__(self, id = None):
        if id is not None:
            if id.startswith('script'):
                self.id = id
                self.path = getaddonpath_params('scripts_path') + '/' + str(self.id)
            elif id.startswith('plugin'):
                self.id = getaddonpath_params('addon_id')
                self.path = getaddonpath_params('addons_path') + '/' + str(self.id)
            else:
                self.id = getaddonpath_params('addon_id')
                self.path = getaddonpath_params('addons_path') + '/' + str(self.id)
        else:
            self.id = getaddonpath_params('addon_id')
            self.path = getaddonpath_params('addons_path') + '/' + str(self.id)
        self.plugin_path = getaddonpath_params('plugin_path')
        return

    def getLocalizedString(self, idx = ' '):
        if True:
            xfile = self.path + '/resources/language/English/strings.xml'
            if os.path.exists(xfile) == False:
                xfile = self.path + '/resources/language/english/strings.xml'
                if os.path.exists(xfile) == False:
                    xfile = self.plugin_path + '/resources/defaults/strings.xml'
            tree = xml.etree.cElementTree.parse(xfile)
            root = tree.getroot()
        try:
            for string in root.iter('string'):
                id = string.get('id')
                text = string.text
                if int(id) == int(idx):
                    xtxt = text
                    return xtxt

        except:
            for string in root.getiterator('string'):
                id = string.get('id')
                text = string.text
                if int(id) == int(idx):
                    xtxt = text
                    return xtxt

    def getSetting(self, id = None):
        item = id
        xfile = self.path + '/resources/settings.xml'
        if not os.path.exists(xfile):
            return None
        else:
            f = open(xfile, 'r')
            xfile2 = f.read()
            f.close()
            if '&' in xfile2:
                xfile2 = xfile2.replace('&', 'AxNxD')
                f2 = open('/tmp/torrentPlayer/temp.xml', 'w')
                f2.write(xfile2)
                f2.close()
                cmd = "mv '/tmp/torrentPlayer/temp.xml' " + xfile
                os.system(cmd)
            try:
                tree = xml.etree.cElementTree.parse(xfile)
            except:
                return None

            root = tree.getroot()
            try:
                for setting in root.iter('setting'):
                    type = setting.get('type')
                    if type == 'bool':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'action':
                        idx = setting.get('label')
                        action = setting.get('action')
                        if idx == item:
                            xtxt = action
                            return xtxt
                    elif type == 'text':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'enum':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            ix = default
                            return ix
                    elif type == 'folder':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'labelenum':
                        idx = setting.get('id')
                        values = setting.get('values')
                        if idx == item:
                            vals = values.split('|')
                            n = len(vals) - 1
                            xtxt = vals[n]
                            return xtxt
                    elif type == 'number':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'select':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt

            except:
                for setting in root.getiterator('setting'):
                    type = setting.get('type')
                    if type == 'bool':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'action':
                        idx = setting.get('label')
                        action = setting.get('action')
                        if idx == item:
                            xtxt = action
                            return xtxt
                    elif type == 'text':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'enum':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            ix = default
                            return ix
                    elif type == 'folder':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'labelenum':
                        idx = setting.get('id')
                        values = setting.get('values')
                        if idx == item:
                            vals = values.split('|')
                            n = len(vals) - 1
                            xtxt = vals[n]
                            return xtxt
                    elif type == 'number':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'select':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt

            return None
            return None

    def getSetting2(self, setting_id = None):
        settings_xml = self.path + '/resources/settings.xml'
        if settings_xml is None:
            return
        else:
            tree = xml.etree.cElementTree.parse(settings_xml)
            root = tree.getroot()
            for setting in root.iter('setting'):
                type = setting.get('type')
                id = setting.get('id')
                if setting_id == id:
                    return setting.get('default')

            return ''
            return

    def setSetting(self, setting_id, value):
        """Sets a script setting."""
        if value is None:
            return False
        else:
            settings_xml = self.path + '/resources/settings.xml'
            if settings_xml is None:
                return False
            tree = xml.etree.cElementTree.parse(settings_xml)
            root = tree.getroot()
            for setting in root.iter('setting'):
                id = setting.get('id')
                if setting_id == id:
                    try:
                        setting.set('default', value)
                        tree.write(settings_xml)
                        return True
                    except:
                        return False

            return False
            return

    def openSettings(self, arg = None):
        """get all settings."""
        settings_xml = self.path + '/resources/settings.xml'
        tree = xml.etree.cElementTree.parse(settings_xml)
        root = tree.getroot()
        i = 0
        list = []
        for setting in root.iter('setting'):
            list.append((i, setting.attrib))
            i = i + 1

        return list

    def getAddonInfo(self, item):
        cachefold = None
        try:
            myfile = file('/tmp/torrentPlayer/xbmc.txt')
            icount = 0
            for line in myfile.readlines():
                cachefold = line
                break

        except:
            pass

        if cachefold is None:
            try:
                cachefold = sys.argv[3]
            except:
                cachefold = '/media/hdd'

        profile = cachefold + '/xbmc/profile/addon_data/' + str(self.id)
        cmd = 'mkdir -p ' + profile
        os.system(cmd)
        xfile = self.path + '/addon.xml'
        if not os.path.exists(xfile):
            return
        else:
            tree = xml.etree.cElementTree.parse(xfile)
            root = tree.getroot()
            version = str(root.get('version'))
            author = str(root.get('provider-name'))
            name = str(root.get('name'))
            id = str(root.get('id'))
            if item == 'path':
                return self.path
            if item == 'Path':
                return self.path
            if item == 'version':
                return version
            if item == 'author':
                return author
            if item == 'name':
                return name
            if item == 'id':
                return id
            if item == 'profile':
                return profile
            return 'xxx'
            return