# -*- coding: utf8 -*-
#from __future__ import unicode_literals 
import sys
import urllib,urllib2,re,os,ast,json

extra={}
################''
url='https://yts.lt/api/v2/list_movies.json?limit=50&page=1'

##########################################parsing tools
jsonFile=os.path.split(__file__)[0]+"/data.json"

class ytsltAPI():
    
        def __init__(self,cParams={}):
                

                self.cParams=cParams
                
        def getJData(self,url):
                
                print "url_page",url
                data=self.getPage(url)
                
                with open(jsonFile, 'w') as outfile:
                    json.dump(data, outfile)
                
                Jdata = json.loads(data)
                return Jdata
                                
               
                                

        def getMovies(self,url):          
            Jdata=self.getJData(url)
            #print "jData",jData
            movies=Jdata["data"]["movies"]
            
            for movie in movies:
                #print "movie",movie.keys()
                #break
                
                extra={}    
                href=''
                try:
                        title=movie.get('title','')
                        href=movie.get('url','')
                        year=movie.get('year',20)
                        rating=movie.get('rating',6)
                        duration=movie.get('runtime',90)
                        
                        #genres=movie.get('genres',[])
                        desc=movie.get('description_full','')
                        
                        yt_trailer_code=movie.get('yt_trailer_code','')
                        language=movie.get('language','')
                        image=movie.get('medium_cover_image','')
                        torrents=movie.get('torrents',[])
                        extra['torrents']=torrents
                        title=title+"("+str(rating)+" "+str(year)+")"
                        title=self.colorize(title,"green")

                        self.addDir(title,href,1,image,"",1,True,desc=desc,extra=extra)
            
                except Exception as error:
                        print "error:",str(error)
                        continue
            
