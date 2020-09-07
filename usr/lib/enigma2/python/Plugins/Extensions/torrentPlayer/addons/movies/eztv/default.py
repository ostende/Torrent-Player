# -*- coding: utf8 -*-
#from __future__ import unicode_literals 
import sys
import urllib,urllib2,re,os,ast
from Plugins.Extensions.torrentPlayer.addons.iTools import CBaseAddonClass,printD,printE
extra={}
################''


##########################################parsing tools


class eztv(CBaseAddonClass):
    
        def __init__(self,cParams={}):
                
                CBaseAddonClass.__init__(self,{'cookie':'eztv.cookie','module_path':__file__})
                self.cParams=cParams
                self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
                self.MAIN_URL = 'https://eztv.io/'
                self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
                self.AJAX_HEADER = dict(self.HEADER)
                self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
                self.cacheLinks  = {}
                self.defaultParams = {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
                self.module_path=__file__
                #self.getPage=self.cm.getPage#(self, url, addParams = {}, post_data = None)
               
        def showmenu(self):
                baseurl=self.getMainUrl()
                self.addDir('search',"https://eztv.io/search/see",103,'img/search.png','',1,searchall=True)
                self.addDir(' TV series','https://eztv.io/',100,'','',1)
               

                return
                 


                                
        ###################################movies
                                  
        def search_103(self,name,sterm,page):##may pastte code of getmovies here
                        surl='https://eztv.io/search/%s'%sterm

                        
                        print "url_page",surl
                        data=self.getPage(surl)
                                    
                        if data is None:
                            return
                       
                        blocks=data.split('name="hover" class="forum_header_border"')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                            #print "block",block
                            
                            block=block.split('class="forum_thread_post">')[1]
                            #link
                            regx='''href="(.*?)"'''
                            href=self.getSM(block,regx)
                            
                            href='https://eztv.io'+href
                           
                            print "href",href
                            
                            regx='''alt="(.*?)"'''
                          
                            title=self.getSM(block,regx)  
                            
                            


                            self.addDir(title,href,1,'',name,1,True)
                        
                       
                        
                
        def getmovies(self,name,url,page):
                                          
                        if page>1:
                           #url+"page/2/"     
                           url_page="https://eztv.io/page_%s"%str(page)
                        else:
                        
                           url_page=url
                        print "url_page",url_page
                       
                        data=self.getPage(url_page)
                                    
                        if data is None:
                            return
                       
                        blocks=data.split('name="hover" class="forum_header_border"')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                            #print "block",block
                            
                            block=block.split('class="forum_thread_post">')[1]
                            #link
                            regx='''href="(.*?)"'''
                            href=self.getSM(block,regx)
                            
                            href='https://eztv.io'+href
                           
                            print "href",href
                            
                            regx='''alt="(.*?)"'''
                          
                            title=self.getSM(block,regx)  
                            
                            


                            self.addDir(title,href,1,'',name,1,True)
                        
                           
                        if len(blocks)>45:
                            
                           self.addDir("next page",url,100,'/img/next.png','',str(page+1))

                        
                       






                                                  
        def extrainfo(self,data=None,extra={}):
                    desc=''
               
                    #regx='''<b>(.*?)</b>(.*?)<br />'''

                    #info=self.getSM(data,regx)  
                    #print "info",info
                    regx='''b>Filesize:</b>(.*?)<br />'''
                    size=self.getSM(data,regx) 
                    extra['size']=size
                    
                    regx='''<b>Resolution:</b>(.*?)<br />'''
                    resolution=self.getSM(data,regx) 
                    extra['quality']=resolution
                    regx='''Seeds: <span class=".*?">(.*?)</span><br />'''
                    seeds=self.getSM(data,regx)
                    extra['seeds']=seeds
                    regx='''<Peers: <span class="stat_green">0</span><br />'''
                    peers=self.getSM(data,regx)  
                    
                    extra['peers']=peers
                    regx='''<p>(.*?)</p>'''
                    desc=self.getSM(data,regx)
                
                                          
                                          
                 
                   
                      
                    return extra ,desc                                    

        def getLinks(self,name,url,img,extra):
              data=self.getPage(url)
              extra,desc=self.extrainfo(data,extra)
              regx='''<a href=".*?" title=".*?"><img src="(.*?)" alt=".*?".*?/></a>'''
              img='https://eztv.io'+self.getSM(data,regx) 
              print "img",img
              regx='''<a href="(.*?)" title="Magnet Link">'''#<img src=".*?" alt="Magnet Download".*?/></a>'''
              data=data.split('alt="Torrent Download"')[1]
              magLink=self.getSM(data,regx)
              print "magLink",magLink
              
              
              
              self.addDir(name,magLink,-7,img,name,extra=extra,desc=desc,dialog='torrentLink')                            
                                          
                                        
            
                
        def resolve_host(self,name,url):
     
           self.resolvehost(name,url)
               

    
        def run(self,cParams):  
                self.cParams=cParams
                url=self.cParams.get('url','')
                name=self.cParams.get('name','')
                try:mode=int(self.cParams.get('mode',None))
                except:mode=None
                page=int(self.cParams.get('page',1))
                category=self.cParams.get('category','')
                extra=self.cParams.get("extra",{})
                try:extra=ast.literal_eval(extra)
                except:pass
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
                        
                        self.getLinks(name,url,image,extra)
                elif mode==2:
                        print ""+url
                        self.resolve_host(name,url)        

                        
                elif mode==100:
                        print ""+url
                        self.getmovies(name,url,page)

                        
                elif mode==103:
                        if sterm.strip()=='':
                           sterm = self.getsearchtext()      
                         
                        self.search_103("Search",sterm,page)       


                
                return self.endDir()

def start(cParams=None):
    addon=eztv(cParams)
    return addon.run(cParams)               
