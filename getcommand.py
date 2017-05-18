#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import api
from lxml import etree
from api import Data
from subprocess import call
import time
import subprocess
import urllib.request, urllib.error, urllib.parse
import wikipedia
from random import randint
import getpass
import os
import configparser
import xml.etree.ElementTree as ET
from pykeyboard import PyKeyboard
import datetime

def command(speech_object):
	previous_command = ""
	while(True):
		
		line = speech_object.readline()
		if(line.startswith("sentence1: ")):
			com = line[15:-6]
			#if (previous_command == com):
			#	continue
			print(com)

                	Config = configparser.ConfigParser()
                	Config.read("config.ini")
                	user_prefix = Config.get("BasicUserData","Prefix")

			if (com == "DRAGON FIRE"):
				tts_kill()
				userin = Data([" "]," ")
				words_dragonfire = {
					0 : "Yes, " + user_prefix + ".",
					1 : "Yes. I'm waiting.",
					2 : "What is your orders?"
				}
				userin.say(words_dragonfire[randint(0,2)])
			elif (com == "ENOUGH" or com == "OKAY"):
				tts_kill()
			elif (com == "STOP"):
                                tts_kill()
				os.system("xbmc-send --action=\"Stop\"")
			elif (com == "WHO AM I" or com == "WHAT IS MY NAME"):
                                tts_kill()
				user_full_name = os.popen("getent passwd $LOGNAME | cut -d: -f5 | cut -d, -f1").read()
				user_full_name = user_full_name[:-1]
                                userin = Data(["echo"], user_full_name)
                                userin.say("Your name is " + user_full_name + "," + user_prefix + ".")
				userin.interact(0)
                                previous_command = com
			elif (com == "I'M A WOMAN" or com == "I'M A GIRL" or com == "I'M A LADY"):
				tts_kill()
				cfgfile = open("config.ini",'w')
				Config.set("BasicUserData","Prefix","My Lady")
				Config.write(cfgfile)
				cfgfile.close()
				userin = Data([" "]," ")
				userin.say("Pardon, My Lady.")
                        elif (com == "I'M A MAN" or com == "I'M A BOY"):
                                tts_kill()
                                cfgfile = open("config.ini",'w')
                                Config.set("BasicUserData","Prefix","Sir")
                                Config.write(cfgfile)
                                cfgfile.close()
                                userin = Data([" "]," ")
                                userin.say("Pardon, Sir.")
			elif (com == "WHAT IS YOUR NAME"):
				tts_kill()
				userin = Data([" "]," ")
				userin.say("My name is Dragon Fire.")
				previous_command = com
			elif (com == "WHAT IS YOUR GENDER"):
				tts_kill()
                                userin = Data([" "]," ")
                                userin.say("I have a female voice but I don't have a gender identity. I'm a computer program, " + user_prefix + ".")
                                previous_command = com
        		elif (com == "OPEN FILE MANAGER"):
				tts_kill()
				userin = Data(["pantheon-files"],"File Manager")
				userin.say("File Manager")
				userin.interact(0)
				previous_command = com
			elif (com == "OPEN WEB BROWSER"):
				tts_kill()
				userin = Data(["sensible-browser"],"Web Browser")
				userin.say("Web Browser")
				userin.interact(0)
				previous_command = com
			elif (com == "SHUT DOWN THE COMPUTER" or com == "SHUT DOWN THE HELMET"):
				tts_kill()
                                #userin = Data(["sudo","poweroff"],"Shutting down")
				userin = Data(["echo"],"Shutting down")
                                userin.say("Shutting down")
				userin.interact(0)
				time.sleep(3)
				os.system("xbmc-send --action=\"Powerdown\"")
                                previous_command = com
			elif (com.startswith("WIKI PEDIA SEARCH FOR")):
				tts_kill()
				#userin = Data(["sensible-browser","http://en.wikipedia.org/wiki/"+com[22:].lower()],com[22:])
				#userin.interact(0)
				print("wkhtmltopdf http://en.wikipedia.org/wiki/"+com[22:].lower().replace(" ", "%20")+" /tmp/dragonfire/"+com[22:].lower().replace(" ", "%20")+".pdf")
				os.system("wkhtmltopdf http://en.wikipedia.org/wiki/"+com[22:].lower().replace(" ", "%20")+" /tmp/dragonfire/"+com[22:].lower().replace(" ", "%20")+".pdf")
				#os.system("convert -density 300 oxford.pdf[0] oxford.jpg")
				os.system("convert -density 300 /tmp/dragonfire/"+com[22:].lower().replace(" ", "%20")+".pdf[0] /tmp/dragonfire/"+com[22:].lower().replace(" ", "%20")+".jpg")
				os.system("xbmc-send --action=\"ShowPicture(/tmp/dragonfire/"+com[22:].lower().replace(" ", "%20")+".jpg)\"")
				os.system("sleep 2 && xbmc-send --action=\"ZoomLevel3\"")
				try:
					wikipage = wikipedia.page(com[22:].lower())
					wikicontent = "".join([i if ord(i) < 128 else ' ' for i in wikipage.content])
					userin.say(wikicontent)
            				previous_command = com
				except:
					pass
			elif (com.startswith("YOU TUBE SEARCH FOR")):
				tts_kill()
				root = ET.fromstring(urllib.request.urlopen("http://gdata.youtube.com/feeds/api/videos?vq=" + com[20:].lower().replace(" ", "%20") + "&racy=include&orderby=relevance&start-index=1&max-results=2").read())
				
				for child in root[16]:
					if child.tag == "{http://www.w3.org/2005/Atom}title":
						youtube_title = child.text
					if child.tag == "{http://www.w3.org/2005/Atom}link":
						youtube_url = child.attrib["href"]
						break				
				
				youtube_id = youtube_url.replace("http://www.youtube.com/watch?v=","").replace("&feature=youtube_gdata","")
				print(youtube_id)
				os.system("xbmc-send --action=\"ActivateWindow(Videos,plugin://plugin.video.youtube/kodion/search/query/?q=" + com[20:].lower().replace(" ", "%20") + ")\"")
				#userin = Data(["sensible-browser",youtube_url],youtube_title)
				userin = Data(["echo"],youtube_title)
				youtube_title = "".join([i if ord(i) < 128 else ' ' for i in youtube_title])
				#k = PyKeyboard()
				#k.tap_key('space')
				time.sleep(5)
				os.system("xbmc-send --action=\"PlayMedia(plugin://plugin.video.youtube/play/?video_id=" + youtube_id + ")\"")
				userin.say(youtube_title)
				userin.interact(0)
				#k.tap_key(k.tab_key)
				#k.tap_key(k.tab_key)
				#k.tap_key(k.tab_key)
				#k.tap_key(k.tab_key)
				#k.tap_key('f')
                        elif (com == "LEFT"):
				userin = Data([" "]," ")
				os.system("xbmc-send --action=\"Left\"")
                                #userin.say("Left")
                                previous_command = com
                        elif (com == "RIGHT"):
                                userin = Data([" "]," ")
                                os.system("xbmc-send --action=\"Right\"")
                                #userin.say("Right")
                                previous_command = com
                        elif (com == "UP"):
                                userin = Data([" "]," ")
                                os.system("xbmc-send --action=\"Up\"")
                                #userin.say("Up")
                                previous_command = com
                        elif (com == "DOWN"):
                                userin = Data([" "]," ")
                                os.system("xbmc-send --action=\"Down\"")
                                #userin.say("Down")
                                previous_command = com
                        elif (com == "SELECT"):
                                tts_kill()
                                userin = Data(["echo"],"Select")
				userin.interact(0)
                                os.system("xbmc-send --action=\"Select\"")
                                userin.say("Select")
                                previous_command = com
                        elif (com == "BACK"):
                                tts_kill()
                                userin = Data(["echo"],"Back")
				userin.interact(0)
                                os.system("xbmc-send --action=\"back\"")
                                userin.say("Back")
                                previous_command = com
                        elif (com == "GO TO HOME"):
                                tts_kill()
                                userin = Data(["echo"],"Home")
				userin.interact(0)
                                os.system("xbmc-send --action=\"ActivateWindow(10000)\"")
                                userin.say("Home")
                                previous_command = com
                        elif (com == "GO TO PROGRAMS"):
                                tts_kill()
                                userin = Data(["echo"],"Programs")
				userin.interact(0)
                                os.system("xbmc-send --action=\"ActivateWindow(10001)\"")
                                userin.say("Programs")
                                previous_command = com
                        elif (com == "GO TO PICTURES"):
                                tts_kill()
                                userin = Data(["echo"],"Pictures")
				userin.interact(0)
                                os.system("xbmc-send --action=\"ActivateWindow(10002)\"")
                                userin.say("Pictures")
                                previous_command = com
                        elif (com == "GO TO FILEMANAGER"):
                                tts_kill()
                                userin = Data(["echo"],"File manager")
				userin.interact(0)
                                os.system("xbmc-send --action=\"ActivateWindow(10003)\"")
                                userin.say("File manager")
                                previous_command = com
                        elif (com == "GO TO SETTINGS"):
                                tts_kill()
                                userin = Data(["echo"],"Settings")
				userin.interact(0)
                                os.system("xbmc-send --action=\"ActivateWindow(10004)\"")
                                userin.say("Settings")
                                previous_command = com
                        elif (com == "GO TO MUSIC"):
                                tts_kill()
                                userin = Data(["echo"],"Music")
				userin.interact(0)
                                os.system("xbmc-send --action=\"ActivateWindow(10005)\"")
                                userin.say("Music")
                                previous_command = com
                        elif (com == "GO TO VIDEO"):
                                tts_kill()
                                userin = Data(["echo"],"Video")
				userin.interact(0)
                                os.system("xbmc-send --action=\"ActivateWindow(10006)\"")
                                userin.say("Videos")
                                previous_command = com

			else:
				tts_kill()
                                userin = Data(["echo"],com + " ?")
                                userin.say("Unrecognized command.")
                                userin.interact(0)
                                previous_command = com

def tts_kill():
	call(["pkill", "audsp"])
	call(["pkill", "aplay"])

def dragon_greet():
	time = datetime.datetime.now().time()

	Config = configparser.ConfigParser()
        Config.read("config.ini")
        user_prefix = Config.get("BasicUserData","Prefix")
	
	if time < datetime.time(12):
		userin = Data([" "],"Good morning " + user_prefix)
		userin.say("Good morning " + user_prefix)
	elif datetime.time(12) < time  and time < datetime.time(18):
                userin = Data([" "],"Good afternoon " + user_prefix)
                userin.say("Good afternoon " + user_prefix)
	else:
                userin = Data([" "],"Good evening " + user_prefix)
                userin.say("Good evening " + user_prefix)

if __name__ == '__main__':
	try:
		os.system("./run_kodi.sh")
		#os.system("./camera_stream.sh")
		#p = subprocess.Popen(['./camera_stream.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		#os.system("sleep 4 && xbmc-send --action=\"PlayMedia(/tmp/test.mpg)\" && sleep 2 && xbmc-send --action=\"SkipForward\"")
		dragon_greet()
		
		try: 
    			os.makedirs("/tmp/dragonfire")
		except OSError:
			if not os.path.isdir("/tmp/dragonfire"):
        			raise
		command(sys.stdin)


	except KeyboardInterrupt:
		sys.exit(1)
