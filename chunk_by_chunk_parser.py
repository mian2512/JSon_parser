"""
This code does the following: 

    1) Opens a url and retrieve provider_urls
    2) Saves the provider_urls in a list 
    3) Follow the first link in the provider_urls list
    4) Divide the JSon object in #3 above into list of chunks separated by "npi"
    5) Defines the starting point of the chunk
    6) Loads all JSON objects in chunk 
  
@author: Paul Sirma 
"""



#The necessary packages needed to run this code
######################################
import pandas as pd
import urllib, json
import urllib2
import mechanize
import re
from requests import get
import ssl
from pandas.io.json import json_normalize
from operator import itemgetter
import pprint
from csv import DictWriter
import csv
import sys
import fileinput
from collections import OrderedDict
import sys, traceback, logging
from xlwt.antlr import ifelse
################################
#1) Opens a url and retrieve provider_urls
url = "http://www.bestlife.com/exchange/cms-data-index.json" 
gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  #Avoiding failed to verify certificate error



#Now we need to follow provider url in all links_list
#####
#WARNIGN!!
#Do not load these json file this time. Your computer will crush!!
#We only want to open the response, we will later read the provider json info bit by bit 
#####

response = urllib.urlopen(url , context=gcontext)
data = json.loads(response.read())

#2)Saves the provider_urls in a list called links  
#Storing all the links that I need to follow
links = data['provider_urls']
print 'all links: ' + str(links)
print "all provider links are shown above"
print "##################"
print


#3) Follow the first link in the provider_urls list
# req = urllib2.Request(links[0]) #we will have to open all the links, but right now I am just looking at the first provider link 
req = urllib2.Request('https://download.getjsonfile.com/data/prov/HCR_ProviderPhcy_CLOrg.json') #we will have to open all the links, but right now I am just looking at the first provider link 
response = urllib2.urlopen(req , context = gcontext )  
print 'response: ' + str(response)  
print 
num = 0
start = ''
unique_npi = ''


def get_first_key(my_response): 

        '''
        This function returns the first key of a JSon Object that will be passed into regular expression parser to split chunks 

        ********
        Parameter:
        my_response = JSon object we want to get the first key from 

        ********
        Return 
        first_key
        '''
        #Declaring variable 
        first_key = ""
        chunk = my_response.read(4*8) #Divide the JSon object into chunks separated by npi
        #Using regular expression to search for the first key in chunk
        first_key =  re.search("^[\W_]+([\w_]+)" , chunk ).group(1)
        return first_key

key = get_first_key(response)
print key 


while True:
    num = 0
    start = ''
    unique_npi = ''
    #4) Divide the JSon object in #3 above into chunks separated by "npi"
    # PLease DON'T delete this comment for now,    chunk = re.sub('[\n\t\r\f]+','',response.read(64*1024)).split('"npi"')
    chunk = response.read(64*2024).strip().split('"%s"' % key )  #Divide the JSon object into chunks separated by npi

        #5)Defines the starting point of the chunk  
    if num == 0: 
        # print chunk[0]
        del chunk[0]
        num = 1

    chunk[0] = start+chunk[0]
    start = chunk[-1]
    print len(chunk)

    #6) Loads all JSON objects in chunk 
    #When length of chunk is >1 we need to loop through chunk

    print "***"
    print len(chunk)
    print chunk[0]

    if  len(chunk) !=1 :     
        # C is an individual provider object, so for each object in the chunk
        for c in chunk[:-1]:
           
            try:
                # Instade c object that has neen clena of whitespace and the leading ,{ , 
                # Substatute ,{$ with a balnk space
                # concatanate npi to the front of the resulting string 
                resp_dict = json.loads('{"%s"' % key+re.sub(',{$','',c.strip().lstrip(',{'))) 
            except:
                try: # alternate Syntax 1 
                    c =  re.sub('{$','', c.strip())
                    c = re.sub(',$','',c.strip())
                    resp_dict = json.loads('{"%s"' % key+ c) 

                except Exception as e:
                    print e 
                    break

        if not chunk:  
            exit()
            
    #Parsing the last chunk as a stand alone, if there is only one object in the chunk... 
    elif len(chunk) ==1 :
        #print chunk 

        # Attenpt to clean the data, will throw error is inapprpate parser is used 
        try:
            # Instade c object that has neen clena of whitespace and the leading ,{ , 
            # Substatute ,{$ with a balnk space
            # concatanate npi to the front of the resulting string 
            resp_dict = json.loads('{"%s"' %key +re.sub(',{$','',c.strip().lstrip(',{'))) 
        except:
            try: # alternate Syntax 1 
                c =  re.sub('{$','', c.strip())
                c = re.sub(',$','',c.strip())
                resp_dict = json.loads('{"%s"' %key + c) 
                print cake 
                
            except Exception as e:
                print e 
                break

    else :
        exit()

print "* The End ** "




