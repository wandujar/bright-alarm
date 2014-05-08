#!/usr/bin/env python

from urllib import urlopen
import urllib
import pygame
import webbrowser
import datetime
import time
import feedparser
import sys
from subprocess import call

def meteo_podcast_rtl():
   print "Retrieving podcast url..."
   url = "http://www.rtl.fr/meteo.rss"
   raw = urlopen(url).read()
   begin = raw.find('type="audio/mpeg"')
   address = raw[begin+23:begin+114]
   return address

def news_podcast_france_culture():
   print "Retrieving podcast url..."
   base_url = "http://www.franceculture.fr/emission-le-5-a-7-le-5-a-7-"
   url = base_url + datetime.date.today().strftime("%Y") + "-" + datetime.date.today().strftime("%m") + "-" + datetime.date.today().strftime("%d")
   raw = urlopen(url).read()
   begin = raw.find('<div id="node-')
   address_key = raw[begin+14:begin+21]
   address = 'http://www.franceculture.fr/player/reecouter?play=' + address_key
   webbrowser.open(address)
   return

def news_podcast_france_bleu():
   print "Retrieving podcast url..."
   raw_url = "http://www.francebleu.fr/rss/emission/779636.rss"
   feed = feedparser.parse( raw_url )
   url =  feed[ "items" ][0][ "link" ]
   raw = urlopen(url).read()
   begin = raw.find('urlAOD=')
   address_key = raw[begin+7:begin+95]
   address = 'http://www.francebleu.fr/' + address_key
   return address

def news_sport_podcast():
   print "Retrieving podcast url..."
   url = "http://www.rtl.fr/emission/le-journal-des-sports/ecouter.rss"
   feed = feedparser.parse( url )
   media =  feed[ "items" ][0][ "link" ]
   return media


def internet_connection():
   print "Checking Internet Connection..."
   try:
      response=urllib.urlopen('http://google.fr')
      print "Ok"
      return True
   except:
      print "No Internet connection"
      answer = raw_input("Do you want to continue ? (Y/n)")       
      if(answer == "Y" or answer == ""):
         pass
      else:
         sys.exit()
      return False

def play(media):
   pause = 0
   pygame.mixer.music.load(media)
   print "Playing audio..."
   pygame.mixer.music.play()
   print "Press space bar to pause or unpause"
   is_playing = 1
   while (is_playing == 1):
      pygame.time.Clock().tick(10)
      key = raw_input()
      if(key == " " and pause == 0):
         pause = 1
         pygame.mixer.music.pause()
         print "Paused"
      elif(key == " " and pause == 1):
         pause = 0
         pygame.mixer.music.unpause()
         print "Unpaused"
      is_playing = pygame.mixer.music.get_busy()
   return

def retrieve_data():
   internet_connection = internet_connection()
   if(internet_connection):
      media0 = meteo_podcast_rtl()
      media1 = news_sport_podcast()
      media2 = news_podcast_france_bleu()
      print "Downloading..."
      urllib.urlretrieve(media0,'files/media0.mp3') 
      urllib.urlretrieve(media1,'files/media1.mp3') 
      urllib.urlretrieve(media2,'files/media2.mp3') 
      print "Data downloaded"

print "Initialising player..."
pygame.init()
print "Player launched"
pygame.mixer.init() 
play("files/wake_me_up.mp3")
play("files/media0.mp3")
play("files/media1.mp3")
play("files/media2.mp3")

print "Execution terminated"
pygame.quit ()
