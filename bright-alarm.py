#!/usr/bin/env python

from urllib import urlopen
import urllib
import pygame
import webbrowser
import datetime
import time
import feedparser
from subprocess import call

def meteo_podcast_rtl():
   url = "http://www.rtl.fr/meteo.rss"
   raw = urlopen(url).read()
   begin = raw.find('type="audio/mpeg"')
   address = raw[begin+23:begin+114]
   return address

def news_podcast_france_culture():
   base_url = "http://www.franceculture.fr/emission-le-5-a-7-le-5-a-7-"
   url = base_url + datetime.date.today().strftime("%Y") + "-" + datetime.date.today().strftime("%m") + "-" + datetime.date.today().strftime("%d")
   raw = urlopen(url).read()
   begin = raw.find('<div id="node-')
   address_key = raw[begin+14:begin+21]
   address = 'http://www.franceculture.fr/player/reecouter?play=' + address_key
   webbrowser.open(address)
   return

def news_podcast_france_bleu():
   raw_url = "http://www.francebleu.fr/rss/emission/779636.rss"
   feed = feedparser.parse( raw_url )
   url =  feed[ "items" ][0][ "link" ]
   raw = urlopen(url).read()
   begin = raw.find('urlAOD=')
   address_key = raw[begin+7:begin+95]
   address = 'http://www.francebleu.fr/' + address_key
   return address

def news_sport_podcast():
   url = "http://www.rtl.fr/emission/le-journal-des-sports/ecouter.rss"
   feed = feedparser.parse( url )
   media =  feed[ "items" ][0][ "link" ]
   return media

media0 = meteo_podcast_rtl()
media1 = news_sport_podcast()
media2 = news_podcast_france_bleu()

urllib.urlretrieve(media0,'files/temp.mp3') 

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('files/wake_me_up.mp3')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy(): 
    pygame.time.Clock().tick(10)
#call("cvlc --volume 1024 " + media0 + " " + media1 + " " + media2, shell=True)
pygame.quit ()

