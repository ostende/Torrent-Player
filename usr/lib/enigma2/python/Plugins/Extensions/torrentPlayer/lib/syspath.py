# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/torrentPlayer/lib/syspath.py
import sys
from os import path as os_path, listdir as os_listdir
scripts = '/usr/lib/enigma2/python/Plugins/Extensions/torrentPlayer/scripts'
try:
    if os_path.exists(scripts):
        for name in os_listdir(scripts):
            if 'script.' in name:
                fold = scripts + '/' + name + '/lib'
                sys.path.append(fold)

except:
    pass