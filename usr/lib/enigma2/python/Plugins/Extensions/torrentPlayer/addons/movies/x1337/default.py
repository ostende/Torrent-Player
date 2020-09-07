# -*- coding: utf8 -*-
#from __future__ import unicode_literals
#ttps://pythonhosted.org/transmissionrpc/reference/transmissionrpc.html#attributes
import sys
import urllib,urllib2,re,os,requests
from Plugins.Extensions.torrentPlayer.addons.iTools import CBaseAddonClass,printD,printE

extra={}
################''
def getmb(b):
    return str(b/(1024*1024))+"MB"

##########################################parsing tools

sgn = requests.Session()

def getmagneData(mhash):
       
        params={'hash':mhash,'category':"all"}
        data = sgn.post('https://hashtomagnet.xyz/',data=params).content
        return data
def getDataPage(sterm=None,page=None,url=''):


    hdr = {'Host': 'torrentz2eu.pw',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Content-Length': '23',
           'Origin': 'https://torrentz2eu.pw',
           'Connection': 'keep-alive',
           'Referer': 'https://torrentz2eu.pw/',
           'Upgrade-Insecure-Requests': '1',
           'TE': 'Trailers'}
    if page:
       prm = {'q':sterm,'category':'movies','page':page}
    else:   
       prm = {'q':sterm,'category':'movies'}
    print "prm",prm   
    data = sgn.post(url,headers=hdr,data=prm).content
    #print "datta",data
    return data
    
def getData(sterm=None,page=None):


    hdr = {'Host': 'torrentz2eu.pw',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Content-Length': '23',
           'Origin': 'https://torrentz2eu.pw',
           'Connection': 'keep-alive',
           'Referer': 'https://torrentz2eu.pw/',
           'Upgrade-Insecure-Requests': '1',
           'TE': 'Trailers'}
    if page:
       prm = {'q':sterm,'category':'movies','page':page}
    else:   
       prm = {'q':sterm,'category':'movies'}
    print "prm",prm   
    data = sgn.post("https://torrentz2eu.pw/",headers=hdr,data=prm).content
    #print "datta",data
    return data

class x1337(CBaseAddonClass):
    
        def __init__(self,cParams={}):
                
                CBaseAddonClass.__init__(self,{'cookie':'x1337.cookie','module_path':__file__})
                self.cParams=cParams
                self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
                self.MAIN_URL = 'http://1337x.to'
                self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
                self.AJAX_HEADER = dict(self.HEADER)
                self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
                self.cacheLinks  = {}
                self.defaultParams = {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
                self.module_path=__file__
                self.download_dir="/media/hdd"
                #self.getPage=self.cm.getPage#(self, url, addParams = {}, post_data = None)
               
        def showmenu(self):
                baseurl=self.getMainUrl()


                
                self.addDir('search','https://www.1337x.to/search/lion/1/',103,'img/search.png','',1,searchall=True)
                self.addDir('Movies','https://www.1337x.to/movie-library/',100,'img/1.png','',1)
                self.addDir('Popular Movies','https://www.1337x.to/popular-movies',102,'img/2.png','',1)
                self.addDir('4k Movies','https://www.1337x.to/search/movie+4k/',101,'img/3.png','',1)

                self.addDir('Top 100 Movies','https://www.1337x.to/top-100-movies',102,'img/4.png','',1)
                

                self.addDir('Television','https://www.1337x.to/cat/TV/',101,'img/5.png','',1)
                self.addDir('Popular TV','https://www.1337x.to/popular-tv',102,'img/6.png','',1)

                self.addDir('Top 100 TV','https://www.1337x.to/top-100-television',102,'img/7.png','',1)
 
                self.addDir('Music','https://www.1337x.to/cat/Music/',101,'img/8.png','',1)



                self.addDir('Top 100 torrents','https://www.1337x.to/top-100',102,'img/9.png','',1)



                self.addDir('Anime','https://www.1337x.to/cat/Anime/',101,'img/10.png','',1)

                self.addDir('Documentery','https://www.1337x.to/cat/Documentaries/',101,'img/11.png','',1)


                self.addDir("Show Torrents",'listTorrents',2,'','Torrents List',dialog="listTorrents")
                


                return
                
                 


                                
        ###################################movies
                                  
        def search_103(self,name,sterm,page):##may pastte code of getmovies here
                                          
                        url='https://www.1337x.to/search/%s/1/'%sterm
                        if page>1:
                           url='https://www.1337x.to/search/%s/%s/'%(sterm,str(page))

                                

                        extra={}
                        print "url",url
                        data=self.getPage(url)
                        
                        
                                   
                        if data is None:
                            return
                        blocks=data.split('class="icon"')
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                            extra={}
                            #link
                                          
                           
                            regx='''<a href="(.*?)">(.*?)</a>'''
                          
                            match=re.findall(regx,block)
                            href='https://www.1337x.to'+match[0][0]
                            
                            title=match[0][1]
                            
                                              
                            image=''

                            #seed
                            regx='''<td class="coll-2 seeds">(.*?)</td>'''
                            seed=match=re.findall(regx,block)[0]
                            print "seed",seed
                            
                            extra['seed']=seed
                            
                                                 
                           
                            regx='''<td class="coll-2 seeds">(.*?)</td>'''
                            leech=match=re.findall(regx,block)[0]
                            print "leech",leech
                            
                            extra['leech']=leech
                            
                          
                            
                            regx='''<td class="coll-4 size mob-uploader">(.*?)<span'''
                            
                            try:
                                size=re.findall(regx,block)[0]
                                #print "block",block
                                
                                extra['size']=size
                                
                                
                            except:
                               
                                size=''

                            try:
                                regx='''<td class="coll-date">(.*?)</td>'''
                                age=re.findall(regx,block)[0]
                                
                                
                                extra['age']=age
                                
                                
                            except:
                               
                                age=''


                                
                            title=self.cleanhtml(title)        
                           
                           
                            
                            self.addDir(title,href,1,image,name,1,True,extra=extra)
                        
                        if len(blocks)>19:
                            
                           self.addDir("next page",url,103,'/img/next.png','',str(page+1),dialog='nextpage')

           
           
               

                        
                        
                       
                        
                
        def getMovies_100(self,name,url,page):
                                          
                        extra={}
                        
                        url=url+'%s/'%page+"/"
                        
                        data=self.getPage(url)           
                        if data is None:
                            return
                        print "data",data
                        blocks=data.split('data-target')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                            extra={}
                            #link
                                          
                           
                            regx='''<h3><a href="(.*?)">(.*?)</a></h3>'''
                          
                            match=re.findall(regx,block)
                            try:href='https://www.1337x.to'+match[0][0]
                            except:continue
                            title=match[0][1]
                            regx='''data-original="(.*?)"'''
                                              
                            image="http:"+self.getSM(block,regx)
                            regx='''<p>(.*?)</p>'''
                            desc=self.getSM(block,regx)
                            desc=self.cleanhtml(desc)
                            #seed

                                
                            
                            title=self.cleanhtml(title)        
                           
                           
                            
                            self.addDir(title,href,104,image,name,1,True,desc=desc)
                           
                        if len(blocks)>19:
                            
                           self.addDir("next page",url,100,'/img/next.png','',str(page+1),dialog='nextpage')

        def getMovies_104(self,name,url,img,desc):
                                          
                       
                      
                        
                        data=self.getPage(url)           
                        if data is None:
                            return
                        
                        blocks=data.split('class="icon"')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                            extra={}
                            #link
                                          
                           
                            regx='''<a href="(.*?)">(.*?)</a>'''
                          
                            match=re.findall(regx,block)
                            try:href='https://www.1337x.to'+match[0][0]
                            except:continue
                            title=match[0][1]
                            
                                              
                            image=''

                            #seed
                            regx='''<td class="coll-2 seeds">(.*?)</td>'''
                            seed=match=re.findall(regx,block)[0]
                            print "seed",seed
                            
                            extra['seed']=seed
                            
                                                 
                           
                            regx='''<td class="coll-2 seeds">(.*?)</td>'''
                            leech=match=re.findall(regx,block)[0]
                            print "leech",leech
                            
                            extra['leech']=leech
                            
                          
                            
                            regx='''<td class="coll-4 size mob-uploader">(.*?)<span'''
                            
                            try:
                                size=re.findall(regx,block)[0]
                                #print "block",block
                                
                                extra['size']=size
                                
                                
                            except:
                               
                                size=''

                            try:
                                regx='''<td class="coll-date">(.*?)</td>'''
                                age=re.findall(regx,block)[0]
                                
                                
                                extra['age']=age
                                
                                
                            except:
                               
                                age=''

    
                                
                            title=self.cleanhtml(title)        
                           
                           
                            
                            self.addDir(title,href,1,img,name,1,True,extra=extra,desc=desc)
                           
                                
           
               
                      
        def getMovies_101(self,name,url,page,desc):
                                          
                        extra={}
                        url=url+'%s/'%page
                        
                        data=self.getPage(url)           
                        if data is None:
                            return
                        
                        blocks=data.split('class="icon"')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                            extra={}
                            #link
                                          
                           
                            regx='''<a href="(.*?)">(.*?)</a>'''
                          
                            match=re.findall(regx,block)
                            try:href='https://www.1337x.to'+match[0][0]
                            except:continue
                            title=match[0][1]
                            
                                              
                            image=''

                            #seed
                            regx='''<td class="coll-2 seeds">(.*?)</td>'''
                            seed=match=re.findall(regx,block)[0]
                            print "seed",seed
                            
                            extra['seed']=seed
                            
                                                 
                           
                            regx='''<td class="coll-2 seeds">(.*?)</td>'''
                            leech=match=re.findall(regx,block)[0]
                            print "leech",leech
                            
                            extra['leech']=leech
                            
                          
                            
                            regx='''<td class="coll-4 size mob-uploader">(.*?)<span'''
                            
                            try:
                                size=re.findall(regx,block)[0]
                                #print "block",block
                                
                                extra['size']=size
                                
                                
                            except:
                               
                                size=''

                            try:
                                regx='''<td class="coll-date">(.*?)</td>'''
                                age=re.findall(regx,block)[0]
                                
                                
                                extra['age']=age
                                
                                
                            except:
                               
                                age=''


                                
                            title=self.cleanhtml(title)        
                           
                           
                            
                            self.addDir(title,href,1,image,name,1,True,extra=extra,desc=desc)
                           
                        if len(blocks)>19:
                            
                           self.addDir("next page",url,101,'/img/next.png','',str(page+1),dialog='nextpage')
                        

        def getMovies_102(self,name,url,page):
                                          
                        extra={}
                        
                        
                        data=self.getPage(url)           
                        if data is None:
                            return
                        blocks=data.split('class="icon"')
                        i=0
                        print "blocks",len(blocks)
                        blocks.pop(0)
                        for block in blocks:
                            extra={}
                            #link
                                          
                           
                            regx='''<a href="(.*?)">(.*?)</a>'''
                           
                            match=re.findall(regx,block)
                            print "match",match
                            try:
                                href='https://www.1337x.to'+match[0][0]
                            except:
                                printE()
                                continue
                            print "href",href
                            try:title=match[0][1]
                            except:continue
                            
                                              
                            image=''



                            try:
                                #seed
                                regx='''<td class="coll-2 seeds">(.*?)</td>'''
                                seed=match=re.findall(regx,block)[0]
                                
                                
                                extra['seed']=seed
                            
                            except:
                                 pass

                            
                            
                                                 
                            try:
                                regx='''<td class="coll-2 seeds">(.*?)</td>'''
                                leech=match=re.findall(regx,block)[0]
                               
                                
                                extra['leech']=leech
                            
                            except:
                                 pass
                            
                            regx='''<td class="coll-4 size mob-uploader">(.*?)<span'''
                            
                            try:
                                size=re.findall(regx,block)[0]                               
                                
                                extra['size']=size

                            except:
                               
                                size=''

                            try:
                                regx='''<td class="coll-date">(.*?)</td>'''
                                age=re.findall(regx,block)[0]
                                
                                
                                extra['age']=age
                                
                                
                            except:
                               
                                age=''


                                
                            title=self.cleanhtml(title)        
                           
                           
                            print "title2",title
                            self.addDir(title,href,1,image,name,1,True,extra=extra,dialog='files',show='noposter')
                           
                       
             
        def getLinks(self,name,url,extra={}):
      
           
            data=self.getPage(url)
            regx='''<li><i class="flaticon-.+?"></i>(.+?)</li>'''
            try:files=re.findall(regx,data)
            except:files=[]
            print "files",files
            extra['files']=files
            regx='''<a target="_blank" href="https://www.imdb.com/title/(.*?)/">'''
            imdb_id=self.getSM(data,regx)
            extra['imdb_id']=imdb_id
         
            if 'name="description"' in data:
                 regx='''<meta name="description" content="(.+?)">'''
            else:

                 regx='''>Storyline : </span><span style="color:#1F2FBD;">(.+?)</span>'''
            desc=self.getSM(data,regx)
           
            
            desc=self.cleanhtml(desc)
            genreText=self.getDM(data,'div class="torrent-category clearfix">','</div>',False)
            genres=self.cleanhtml(genreText)
            desc=genres+"----"+desc
            print "desc",desc
            regx='''<img src="(.+?)" alt="">'''
            try:image=re.findall(regx,data)[0]
            except:image=''


            
            if not data:
               
               self.addDir("Error:Unable to get magnet link","Error:Unable to get magnet link",-1)
            tmx ='''href="magnet:(.+?)"'''
            
            try:
                magnetLink = 'magnet:'+re.findall(tmx,data)[0]
            except:
                printE()
                self.addDir("Error:Unable to get magnet link","Error:Unable to get magnet link",-1)
                return
            regx='''<p> <strong>Infohash :</strong> <span>(.+?)</span></p>'''
            try:
                tHash = re.findall(regx,data)[0]
            except:
                printE()
                tHash=None
            extra['tHash']=tHash
            self.addDir(name,magnetLink,-7,image,extra=extra,dialog='torrentLink',show='poster',desc=desc)
    
        def run(self,cParams):
               
                #if self.cParams is None:
                        #self.cParams=self.get_params()
                self.cParams =cParams       
                url=cParams.get('url','')
                name=cParams.get('name','')
                try:mode=int(cParams.get('mode',None))
                except:mode=None
                page=int(self.cParams.get('page',1))
                category=self.cParams.get('category','')
                extra=self.cParams.get("extra",{})
                desc=self.cParams.get("desc",'')
                show=self.cParams.get('show','')
                image=self.cParams.get('image','')
                sterm=self.cParams.get('sterm','')
                print "Mode: "+str(mode)
                print "URL: "+str(url)
                print "Name: "+str(name)
                print "sterm: "+str(sterm)
                print "page: "+str(page)
                #print "cacategory: "+str(category)
                print "extra: "+str(extra)
                print "show: "+str(show)
                print "image: "+str(image.encode("utf-8","ignore"))

                if mode==None:
                        print ""
                        self.showmenu()

                        
                elif mode==1:
                        print ""+url
                        self.getLinks(name,url,extra)

                elif mode==-7:
                        print ""+url
                        self.addTorrentLink(url)                  
                    
                elif mode==100:
                        print ""+url
                        self.getMovies_100(name,url,page)

                elif mode==101:
                        print ""+url
                        self.getMovies_101(name,url,page)

                elif mode==102:
                        self.getMovies_102(name,url,page)
                        
                        #sterm ='4k+Movies'     
                         
                        #self.search_103("4k Movies",sterm,page)       
                elif mode==104:
                        print ""+url
                        self.getMovies_104(name,url,image,desc)
                        
                elif mode==103:
                        if sterm.strip()=='':
                           sterm = self.getsearchtext()      
                         
                        self.search_103("Search",sterm,page)       



                return self.endDir()

def start(cParams=None):
    
    addon=x1337(cParams)
    return addon.run(cParams)               
