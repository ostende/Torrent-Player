# -*- coding: utf8 -*-
#from __future__ import unicode_literals 
import sys
import urllib,urllib2,re,os,ast
from Plugins.Extensions.torrentPlayer.addons.iTools import CBaseAddonClass,printD,printE
extra={}
################''


##########################################parsing tools


class zooqle(CBaseAddonClass):
    
        def __init__(self,cParams={}):
                
                CBaseAddonClass.__init__(self,{'cookie':'zooqle.cookie','module_path':__file__})
                self.cParams=cParams
                self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
                self.MAIN_URL = 'https://zooqle.com/mov/'
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
                self.addDir('Movies','https://zooqle.com/mov/',100,'img/1.png','',1)
                #self.addDir('TV','https://zooqle.com/browse/tv/',200,'img/3.png','',1)
               

                return
                 


                                
        ###################################movies
                                  
        def search_103(self,name,sterm,page):##may pastte code of getmovies here
                        page_url='https://zooqle.com/search?q='+sterm

                        if page>1:
                                page_url='https://zooqle.com/search?pg=%s&q=%s'%(str(page),sterm)


                       
                        
                       
                        data=self.getPage( page_url)
                                    
                        if data is None:
                            return
                       
                        blocks=data.split('class="text-muted3 smaller pad-l2"')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                           
                            #link
                            regx='''href="(.*?)"'''                    
                            href='https://zooqle.com'+self.getSM(block,regx)                
                           
                            regx='''<a class=" small" href=".*?"><hl>(.*?)</hl>(.*?)</a>'''
                          
                            title=self.getDM(block,'<hl>',"</a>")
                            
                            title=self.cleanhtml(title)
                            print "title",title
                             
                            
                            
                            regx='''src="(.*?)"'''                    
                            image='https://zooqle.com'+self.getSM(block,regx) 



                            info=''
                            try:#desc
                                    regx='''class="mov_descr">(.*?)</div>'''
                                    desc=self.getSM(block,regx) 
                                    
                                    
                            except:

                                    desc=''                             
                            print "desc",desc
                            info=''
                            try:#year
                                    regx='''<span class=".*?">(.*?)</span>'''
                                    quality=self.getSM(block,regx) 
                                    info=quality
                                    
                            except:

                                    pass                          
                                                 
                            
                            
                                 
                            
                                                
                            #title=self.colorize(title)
                            
                            self.addDir(title,href,1,image,name,1,True,desc=desc)
                           
                        if len(blocks)>18:
                            
                           self.addDir("next page",sterm,103,'/img/next.png','',str(page+1))
                       
                     
                
        def getmovies(self,name,url,page):
                                          
                        if page>1:
                           #url+"page/2/"     
                           url_page=url+'?pg='+str(page)
                        else:
                        
                           url_page=url
                        print "url_page",url_page
                       
                        data=self.getPage(url_page)
                                    
                        if data is None:
                            return
                       
                        blocks=data.split('class="smaller text-muted3"')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                           
                            #link
                            regx='''href="(.*?)"'''                    
                            href='https://zooqle.com'+self.getSG(block,regx)[0]                 
                           
                            regx='''<td><a href=".*?">(.*?)</a><div'''
                          
                            title=self.getSG(block,regx)[0]
                            
                            regx='''src="(.*?)"'''                    
                            image='https://zooqle.com'+self.getSG(block,regx)[0]



                            info=''
                            try:#desc
                                    regx='''class="mov_descr">(.*?)</div>'''
                                    desc=self.getSG(block,regx)[0]
                                    
                                    
                            except:

                                    desc=''                             
                            print "desc",desc
                            info=''
                            try:#year
                                    regx='''<span class=".*?">(.*?)</span>'''
                                    quality=self.getSG(block,regx)[0]
                                    info=quality
                                    
                            except:

                                    pass                          
                                                 
                            
                            
                            title=self.cleanhtml(title)        
                            if info!='':    
                                title=title+"("+info+")"
                                                
                            #title=self.colorize(title)
                            
                            self.addDir(title,href,1,image,name,1,True,desc=desc)
                           
                        if len(blocks)>18:
                            
                           self.addDir("next page",url,100,'/img/next.png','',str(page+1))

                        
                        



                       
                
        def getseries(self,name,url,page):
                                          
                        if page>1:
                           #url+"page/2/"     
                           url_page=url+'?pg='+str(page)
                        else:
                        
                           url_page=url
                        print "url_page",url_page
                       
                        data=self.getPage(url_page)
                                    
                        if data is None:
                            return
                       
                        blocks=data.split('class="mov_info')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                           
                            #link
                            regx='''href="(.*?)"'''                    
                            href='https://zooqle.com'+self.getSG(block,regx)[0]                 
                           
                            regx='''class="mov_head"><a href=".*?">(.*?)</a>'''
                          
                            title=self.getSG(block,regx)[0]
                            
                            regx='''src="(.*?)"'''                    
                            image='https://zooqle.com'+self.getSG(block,regx)[0]



                            info=''
                            try:#desc
                                    regx='''class="mov_descr">(.*?)</div>'''
                                    desc=self.getSG(block,regx)[0]
                                    
                                    
                            except:

                                    desc=''                             
                            print "desc",desc
                            info=''
                            try:#year
                                    regx='''<span class=".*?">(.*?)</span>'''
                                    quality=self.getSG(block,regx)[0]
                                    info=quality
                                    
                            except:

                                    pass                          
                                                 
                            
                            
                            title=self.cleanhtml(title)        
                            if info!='':    
                                title=title+"("+info+")"
                                                
                            #title=self.colorize(title)
                            
                            self.addDir(title,href,1,image,name,1,True,desc=desc)
                           
                        if len(blocks)>18:
                            
                           self.addDir("next page",url,200,'/img/next.png','',str(page+1))

                        
                       







                                

        def getLinks(self,name,url,img,extra,desc):

               data=self.getPage(url)
               print "data",data
              # regx='''<a class="small " href="(.*?)">.*?</a>'''
               #link='https://zooqle.com'+self.getSM(data,regx)
               #print "match",link
               #data=self.getPage(link)
               
               regx='''<a rel="nofollow" href="(.*?)"><i class="spr dl-magnet pad-r2">'''
               link=self.getSM(data,regx)
               print "link",link
               self.addDir(name,link,-7,img,name,desc=desc,dialog='torrentLink')
                

    
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
                desc=self.cParams.get('desc','')
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

                        
                elif mode==100:
                        print ""+url
                        self.getmovies(name,url,page)

                        
                elif mode==103:
                        if sterm.strip()=='':
                           sterm = self.getsearchtext()      
                         
                        self.search_103("Search",sterm,page)       


                elif mode==200:

                        self.getseries(name,url,page)
                        
               
                return self.endDir()

def start(cParams=None):
    addon=zooqle(cParams)
    return addon.run(cParams)               
