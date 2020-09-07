# -*- coding: utf8 -*-
#from __future__ import unicode_literals 
import sys
import urllib,urllib2,re,os,ast

from Plugins.Extensions.torrentPlayer.addons.iTools import CBaseAddonClass,printD,printE,getos,downloadfile,getDownloadPath

extra={}
################''
from ytsltAPI import ytsltAPI 

##########################################parsing tools
def printE(msg=''):
    import traceback,sys
    printD("===============================================")
    printD("                   EXCEPTION                   ")
    printD("===============================================")
    msg = msg + ': \n%s' % traceback.format_exc()
    traceback.print_exc(file=sys.stdout)
    printD("Error",msg)
    printD("===============================================")
log_file='/tmp/TSmedia/ytlist.log'    
def getcaller_name():
    try:
        import inspect
        import os
        frame = inspect.currentframe()
        frame = frame.f_back.f_back
        code = frame.f_code
        calling_module = os.path.basename(code.co_filename)
        return calling_module
    except:
        return ''
def printD(label='', Ddata='' ):
       
        Ddata=str(Ddata)
        label=str(label)
        import traceback
    
   
        try:
            caller_name = getcaller_name() 
            f = open(log_file, 'a')
            
            f.write(caller_name+":"+label+'->'+Ddata + '\n')
            f.close
        except Exception:
            print("======================EXC printD======================")
            print("Log: %s" % traceback.format_exc())
            print("========================================================")
            try:
                msg = '%s' % traceback.format_exc()
                f = open(log_file, 'a')
                f.write(Ddata + '\n')
                f.close
            except Exception:
                print("======================EXC printD======================")
                print("logII: %s" % traceback.format_exc())
                print("========================================================")
########################################


class ytslt(CBaseAddonClass,ytsltAPI):
    
        def __init__(self,cParams={}):
                
                CBaseAddonClass.__init__(self,{'cookie':'ytslt.cookie','module_path':__file__})
                ytsltAPI.__init__(self)
                self.cParams=cParams
                self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
                self.MAIN_URL = 'https://yts.lt/'
                self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
                self.AJAX_HEADER = dict(self.HEADER)
                self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
                self.cacheLinks  = {}
                self.defaultParams = {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
                self.module_path=__file__
                #self.getPage=self.cm.getPage#(self, url, addParams = {}, post_data = None)
                
        def showmenu(self):
                baseurl=self.getMainUrl()
                self.addDir('search','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=date_added&quality=all&genre=all',103,'img/search.png','',1,searchall=True)
                self.addDir('Most Downloads','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=date_added&quality=all&genre=all',100,'img/1.png','',1)
                self.addDir('Recent','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=download_count&quality=all&genre=all',100,'img/2.png','',1)
                self.addDir('Top rated','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=rating&quality=all&genre=all',100,'img/3.png','',1)
                self.addDir('Most liked','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=like_count&quality=all&genre=all',100,'img/4.png','',1)


                self.addDir('Movies 720','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=download_count&quality=720p&genre=all',100,'img/5.png','',1)
                self.addDir('Movies 1080','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=download_count&quality=1080p&genre=all',100,'img/6.png','',1)
                self.addDir('Movies 4k','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=download_count&quality=2160p&genre=all',100,'img/7.png','',1)
                self.addDir('Movies 3d','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=download_count&quality=3D&genre=all',100,'img/8.png','',1)

                self.addDir('Genre','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=like_count&quality=all&genre=action',101,'img/9.png','',1)
                                 
                #self.addDir('Action','https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=like_count&quality=all&genre=action',100,'img/5.png','',1)
                 


                                
        ###################################movies
                
        def getGenre(self):
            genres=[('all', 'All'), ('action', 'Action'), ('adventure', 'Adventure'), ('animation', 'Animation'), ('biography', 'Biography'), ('comedy', 'Comedy'), ('crime', 'Crime'), ('documentary', 'Documentary'), ('drama', 'Drama'), ('family', 'Family'), ('fantasy', 'Fantasy'), ('film-noir', 'Film-Noir'), ('game-show', 'Game-Show'), ('history', 'History'), ('horror', 'Horror'), ('music', 'Music'), ('musical', 'Musical'), ('mystery', 'Mystery'), ('news', 'News'), ('reality-tv', 'Reality-TV'), ('romance', 'Romance'), ('sci-fi', 'Sci-Fi'), ('sport', 'Sport'), ('talk-show', 'Talk-Show'), ('thriller', 'Thriller'), ('war', 'War'), ('western', 'Western')]
            for genre in genres:
                title=genre[1]
                href=genre[0]
                href='https://yts.mx/api/v2/list_movies.json?limit=50&sort_by=like_count&quality=all&genre=%s'%href
                self.addDir(title,href,100,'','movies',1)


            
        def search_103(self,name,sterm,page):##may pastte code of getmovies here

                         url='https://yts.lt/api/v2/list_movies.json?limit=50&sort_by=date_added&quality=all&genre=all&query_term=%s&page=%s'%(sterm,str(page))
                         
                           
                         self.getMovies(url)
                         self.addDir("next page",sterm,103,'/img/next.png','',str(page+1))


                       
                        
                
        def getmovies(self,name,mainurl,page):
                        url=mainurl+"&page=%s"%str(page)                  
                        self.getMovies(url)
                        self.addDir("next page",mainurl,100,'/img/next.png','',str(page+1))



                
        def getLinks(self,name,url,image,extra,desc):
            
                regx='''<a class="icon" href="https://www.imdb.com/title/(.*?)/" title="IMDb Rating" target="_blank">'''
                
                data=self.getPage(url)
                imdb_id=self.getSM(data,regx)
                regx='''<img class="img-responsive" itemprop="image" src="(.*?)" alt=".*?" />'''
                img=self.getSM(data,regx)
                extra['imdb_id']=imdb_id
                printD('imdb_id',imdb_id)
                
               
                if imdb_id!='':
                   subLink,subName=self.getSubsapiLink(imdb_id,sub_lng_id='')#sub_lng_id will be the default in TSmedia
                   printD("subapi link",subLink)
                   printD("subapi subName",subName)
                   extra['subLink']=subLink
                   extra['subName']=subName
                   #imdbTrailer,imdb_id,videoURL=getIMDBParams(imdbTrailer='',imdb_id=imdb_id)
                   #extra['trailer']=imdbTrailer
              

                regx='''<h2>(.*?)</h2>'''
                info=self.getMM(data,regx)
                print "info",info
                try:
                        extra['year']=info[0]
                        extra['genres']=[info[1]]
                except:
                        pass
                regx='''<span itemprop="ratingValue">(.*?)</span>'''
                extra['rating']=self.getSM(data,regx)
                ##############################
                torrents=extra['torrents']
                for torrent in torrents:
                    href=''    
                    title=torrent['quality']
                    href=torrent['url']
                    extra['seeds']=torrent['seeds']
                    extra['peers']=torrent['peers']
                    extra['size']=torrent['size']
                    extra['age']=torrent["date_uploaded"]
                    
                    self.addDir(title,href,2,img,name,1,desc=desc,extra=extra,dialog='servers')                     
        def getLinks2(self,name,url,image,extra,desc):
                 self.addDir(name,url,-7,image,name,1,desc=desc,extra=extra,dialog='torrentLink') 
        def getLinks22(self,name,url,image,extra,desc):
                torrentFile=downloadFile(url,"/tmp/tmp.torrent")
                self.addDir(title,"/tmp/tmp.torrent",6,image,name,1,desc=desc,extra=extra,dialog='torrentLink')                          

            
                
  
        def run(self):  
                if self.cParams is None:
                        self.cParams=self.get_params()
                url=self.cParams.get('url','')
                name=self.cParams.get('name','')
                try:mode=int(self.cParams.get('mode',None))
                except:mode=None
                page=int(self.cParams.get('page',1))
                category=self.cParams.get('category','')
                extra=self.cParams.get("extra",{})
                try:extra=ast.literal_eval(extra)
                except:pass
                desc=self.cParams.get('desc','')
                show=self.cParams.get('show','')
                image=self.cParams.get('image','')
                sterm=self.cParams.get('sterm','')
                print "Mode: "+str(mode)
                print "URL: "+str(url)
                print "Name: "+str(name)
                print "sterm: "+str(sterm)
                print "page: "+str(page)
                print "cacategory: "+str(category)
                print "extra: "+str(extra)
                print "show: "+str(show)
                print "image: "+str(image.encode("utf-8","ignore"))

                if mode==None:
                        print ""
                        self.showmenu()
                elif mode==1:
                        print ""+url
                        
                        self.getLinks(name,url,image,extra,desc)
                elif mode==2:
                        print ""+url
                        self.getLinks2(name,url,image,extra,desc)     

                        
                elif mode==100:
                        print ""+url
                        self.getmovies(name,url,page)
           
                elif mode==101:
                        print ""+url
                        self.getGenre()


                elif mode==103:
                        if sterm.strip()=='':
                           sterm = self.getsearchtext()      
                         
                        self.search_103("Search",sterm,page)       



                return self.endDir()

def start(cParams=None):
    addon=ytslt(cParams)
    return addon.run()               
