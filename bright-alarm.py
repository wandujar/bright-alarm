#!/usr/bin/env python

from urllib import urlopen
from threading import Timer
import curses
import urllib
import pygame
import webbrowser
import datetime
import time
import feedparser
import sys
from subprocess import call

def meteo_podcast_rtl():
   screen.addstr("Retrieving podcast url...\n")
   screen.refresh()
   url = "http://www.rtl.fr/meteo.rss"
   raw = urlopen(url).read()
   begin = raw.find('type="audio/mpeg"')
   address = raw[begin+23:begin+114]
   return address

def news_podcast_france_culture():
   screen.addstr("Retrieving podcast url...\n")
   screen.refresh()
   base_url = "http://www.franceculture.fr/emission-le-5-a-7-le-5-a-7-"
   url = base_url + datetime.date.today().strftime("%Y") + "-" + datetime.date.today().strftime("%m") + "-" + datetime.date.today().strftime("%d")
   raw = urlopen(url).read()
   begin = raw.find('<div id="node-')
   address_key = raw[begin+14:begin+21]
   address = 'http://www.franceculture.fr/player/reecouter?play=' + address_key
   webbrowser.open(address)
   return

def news_podcast_france_bleu():
   screen.addstr("Retrieving podcast url...\n")
   screen.refresh()
   raw_url = "http://www.francebleu.fr/rss/emission/779636.rss"
   feed = feedparser.parse( raw_url )
   url =  feed[ "items" ][0][ "link" ]
   raw = urlopen(url).read()
   begin = raw.find('urlAOD=')
   address_key = raw[begin+7:begin+95]
   address = 'http://www.francebleu.fr/' + address_key
   return address

def news_sport_podcast():
   screen.addstr("Retrieving podcast url...\n")
   screen.refresh()
   url = "http://www.rtl.fr/emission/le-journal-des-sports/ecouter.rss"
   feed = feedparser.parse( url )
   media =  feed[ "items" ][0][ "link" ]
   return media


def internet_connection():
   screen.addstr("Checking Internet Connection...\n")
   screen.refresh()
   try:
      response=urllib.urlopen('http://google.fr')
      screen.addstr("Ok\n")
      screen.refresh()
      return True
   except:
      screen.addstr("No Internet connection\n")
      screen.refresh()
      answer = raw_input("Do you want to continue ? (Y/n)")       
      if(answer == "Y" or answer == ""):
         pass
      else:
         sys.exit()
      return False

def play(media):
   pause = 0
   pygame.mixer.music.load(media)
   screen.addstr("Playing audio...\n")
   screen.refresh()
   pygame.mixer.music.play()
   screen.addstr("Press space bar to pause or unpause\n")
   screen.refresh()
   is_playing = pygame.mixer.music.get_busy()
   while (is_playing):
      is_playing = pygame.mixer.music.get_busy()
      pygame.time.Clock().tick(10)
      screen.timeout(1)
      event = screen.getch()
      if event == ord(" ") and pause == 0:
         pause = 1
         pygame.mixer.music.pause()
         screen.addstr("Paused\n")     
      elif event == ord(" ") and pause == 1:
         pause = 0
         pygame.mixer.music.unpause()
         screen.addstr("Unpaused\n")   
      elif event == curses.KEY_LEFT:
         screen.addstr("Playing again from start\n")
         play(media)            
      elif event == curses.KEY_RIGHT:
         screen.addstr("Skipping\n")
         is_playing = 0
      elif event == curses.KEY_BACKSPACE:
         pygame.quit ()
         curses.endwin()
         sys.exit()
   return


def retrieve_data():
   internet_connection_var = internet_connection()
   if(internet_connection_var):
      media0 = meteo_podcast_rtl()
      media1 = news_sport_podcast()
      media2 = news_podcast_france_bleu()
      screen.addstr("Downloading...\n")
      screen.refresh()
      urllib.urlretrieve(media0,'files/media0.mp3') 
      urllib.urlretrieve(media1,'files/media1.mp3') 
      urllib.urlretrieve(media2,'files/media2.mp3') 
      screen.addstr("Data downloaded\n\n")
      screen.refresh()

def synchronisation_seconds():
    "Wait for the seconds to be at 00"
    second = int(time.strftime("%S",time.localtime()))
    if(second != 0):
        time.sleep(60-second)
    return

def synchronisation_minutes():
    "Wait for the minutes to be at 00"
    minute = int(time.strftime("%M",time.localtime()))
    if(minute != 0):
        time.sleep((60-minute)*60)
    return

def wait(hour_defined, minute_defined):
   "Wait for execution time defined by the user"
   hour_defined = int(hour_defined)
   minute_defined = int(minute_defined)
   current_hour = int(time.strftime("%H",time.localtime()))
   synchronisation_seconds()
   
   if(current_hour != hour_defined):
       synchronisation_minutes()
       hour_difference = hour_defined  - int(time.strftime("%H",time.localtime()))
       if(hour_difference > 0):
           print "let's sleep for %d hours !" %((hour_difference))
           time.sleep((hour_difference)*60*60)
       elif(hour_difference < 0):
           hour_difference = hour_difference%24
           print "let's sleep for %d hours !" %((hour_difference))
           time.sleep((hour_difference)*60*60)
   print "Less than an hour to sleep..."
   while(int(time.strftime("%M",time.localtime())) != minute_defined):
       time.sleep(59)
   return

alarm_time = raw_input("When do you plan to wake up ? (hh:mm)")
if(alarm_time != ""):
    print "Alarm will ring at %s" % alarm_time
    alarm_minute = alarm_time[3:5]
    alarm_hour = alarm_time[0:2]
    wait(alarm_hour, alarm_minute);
   
screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
screen.addstr("Executing bright-alarm script...\n\n") 
screen.refresh()
retrieve_data()
screen.addstr("Initialising player...\n")
screen.refresh()
pygame.init()
screen.addstr("Player launched\n\n")
screen.refresh()
pygame.mixer.init() 
play("files/wake_me_up.mp3")
play("files/media0.mp3")
play("files/media1.mp3")
play("files/media2.mp3")

screen.addstr("Execution terminated\n")
screen.refresh()
pygame.quit ()
curses.endwin()
