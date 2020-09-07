# -*- coding: utf8 -*-
#from __future__ import unicode_literals

import sys
import urllib,urllib2,re,os,ast
from Plugins.Extensions.torrentPlayer.addons.iTools import CBaseAddonClass,printD,printE
extra={}
################''


##########################################parsing tools


class rarbg(CBaseAddonClass):
    
        def __init__(self,cParams={}):
                
                CBaseAddonClass.__init__(self,{'cookie':'rarbg.cookie','module_path':__file__})
                self.cParams=cParams
                self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
                self.MAIN_URL = 'https://rarbg.to/'
                self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
                self.AJAX_HEADER = dict(self.HEADER)
                self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
                self.cacheLinks  = {}
                self.defaultParams = {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
                self.module_path=__file__
                #self.getPage=self.cm.getPage#(self, url, addParams = {}, post_data = None)
               
        def showmenu(self):
                baseurl=self.getMainUrl()
                self.addDir('search',baseurl+"/?s=",103,'img/search.png','',1,searchall=True)
                self.addDir('Movies catalog','https://rargb.to/catalog/movies/',100,'img/1.png','',1)
                self.addDir('Movies','https://rargb.to/movies/',100,'img/2.png','',1)
               
                self.addDir('Movies top 100 popular','https://rargb.to/top100?category=movies',100,'img/2.png','',1)
                self.addDir('TV shows catalog','https://rargb.to/tv/',100,'img/3.png','',1)
                self.addDir('TV shows','https://rargb.to/tv/',100,'img/4.png','',1)
                self.addDir('Music','https://rargb.to/music/',100,'img/5.png','',1)
                self.addDir('Anime','https://rargb.to/anime/',100,'img/6.png','',1)
   

                return
                 


                                
        ###################################movies
                                  
        def search_103(self,name,sterm,page):##may pastte code of getmovies here
                        page_url='https://rargb.to/search/?search=%s'%sterm

                        if page>1:
                                page_url='https://rargb.to/search/?search=%s'%(sterm,str(page))


                        
                             
                        print "url_page",page_url
                        data=self.getPage(page_url)
                                 
                        if data is None:
                                return
                        
                       
               
                       
                        blocks=data.split('class="lista2"')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                            
                            #link
                            regx='''href="(.*?)"'''                    
                            href='https://rargb.to/'+re.findall(regx,block)[1]               
                           
                            regx='''title="(.*?)"'''
                          
                            title=self.getSM(block,regx) 
                            
                            regx='''src="(.*?)"'''                    
                            image=self.getSM(block,regx)
                            print "image",image



                            info=''
                            try:#desc
                                    regx='''<div class="contentBoxSing">(.*?)</div>'''
                                    desc=self.getDM(block,'"contentBoxSing">','<',False)
                                    desc=desc.strip()
                                    
                            except:

                                    desc=''                             
                            print "desc",desc
                            info=''
                            try:#year
                                    regx='''class="lista">(.*?)</td><td '''
                                    extra=re.findall(regx,block)
                                    print "extra",extra
                                    
                            except:

                                    pass                          
                            try:#rating
                                    regx='''<span style="color:DarkSlateGray">(.*?)</span>'''
                                    rating=self.getSG(block,regx)[0]
                                    info=info+" "+rating
                            except:

                                    pass
                                                      
                            
                           
                                
                            if info!='':    
                                title=title+"("+info+")"
                            title=self.cleanhtml(title)                        
                            #title=self.colorize(title)
                            mode=1
                            self.addDir(title,href,mode,image,name,1,True,desc=desc)
                           
                        if len(blocks)>10:
                            
                           self.addDir("next page",sterm,103,'/img/next.png','',str(page+1))

                        
                       
                       
                        
                
        def getmovies(self,name,url,page):
                                          
                        if page>1:
                           #url+"page/2/"     
                           url_page=url+"%s/"%str(page)
                        else:
                        
                           url_page=url
                        print "url_page",url_page
                       
                        data=self.getPage(url_page)
                        print "data",data            
                        if data is None:
                                return
                        
                       
               
                       
                        blocks=data.split('class="lista2"')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                            
                            #link
                            regx='''href="(.*?)"'''                    
                            href='https://rargb.to/'+re.findall(regx,block)[1]               
                           
                            regx='''title="(.*?)"'''
                          
                            title=self.getSM(block,regx) 
                            
                            regx='''src="(.*?)"'''                    
                            try:
                                    image="https://rargb.to/"+self.getMM(block,regx)[1]
                            except:
                                    image=''



                            info=''
                            try:#desc
                                    regx='''<div class="contentBoxSing">(.*?)</div>'''
                                    desc=self.getDM(block,'"contentBoxSing">','<',False)
                                    desc=desc.strip()
                                    
                            except:

                                    desc=''                             
                            print "desc",desc
                            info=''
                            try:#year
                                    regx='''class="lista">(.*?)</td><td '''
                                    extra=re.findall(regx,block)
                                    print "extra",extra
                                    
                            except:

                                    pass                          
                            try:#rating
                                    regx='''<span style="color:DarkSlateGray">(.*?)</span>'''
                                    rating=self.getSG(block,regx)[0]
                                    info=info+" "+rating
                            except:

                                    pass
                                                      
                            
                           
                                
                            if info!='':    
                                title=title+"("+info+")"
                            title=self.cleanhtml(title)                        
                            #title=self.colorize(title)
                            mode=1
                            self.addDir(title,href,mode,image,name,1,True,desc=desc)
                           
                        if len(blocks)>10:
                            
                           self.addDir("next page",url,100,'/img/next.png','',str(page+1))

                        
                        if len(blocks)==1:
                            self.addDir("Error:no items found",url,-1,'','',str(page+1))



        def getLinks(self,name,url,img,extra):
                        data=self.getPage(url)
                        extra,desc,poster=self.metaData(data=data)
                        regx='''<a href="magnet:(.*?)">'''
                        link='magnet:'+self.getSM(data,regx)
                        print "link",link
                        
                        self.addDir(name,link,-7,'',name,dialog='torrentLink',extra=extra)
                        
                       
        def metaData(self,url='',data='',extra={},desc='',image='',show='movie'):                            

                  regx='<a.*?href="https://www.imdb.com/title/(.*?)">'''
                  extra['imdb_id']=self.getSM(data,regx)
                  regx='''<br> Filesize =(.*?)<br>'''
                  extra['size']=self.getSM(data,regx)
                  regx='''<td class="lista">Seeders :(.*?), Leechers :(.*?)</td>'''
                  extra['seeds']=self.getSM(data,regx)[0]
                  extra['leechs']=self.getSM(data,regx)[1]
                  return extra,desc,image
                  
                
    
               

    
        def run(self):  
                if self.cParams is None:
                        self.cParams=self.get_params()
                url=self.cParams.get('url','')
                name=self.cParams.get('name','')
                try:mode=int(self.cParams.get('mode',None))
                except:mode=None
                page=int(self.cParams.get('page',1))
                
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
              
                print "extra: "+str(extra)
                print "show: "+str(show)
                print "image: "+str(image.encode("utf-8","ignore"))

                if mode==None:
                        print ""
                        self.showmenu()
                elif mode==1:
                        print ""+url
                        
                        self.getLinks(name,url,image,extra)

                elif mode==100:
                        print ""+url
                        self.getmovies(name,url,page)

                        
                elif mode==103:
                        if sterm.strip()=='':
                           sterm = self.getsearchtext()      
                         
                        self.search_103("Search",sterm,page)       



                return self.endDir()

def start(cParams=None):
    addon=rarbg(cParams)
    return addon.run()               
