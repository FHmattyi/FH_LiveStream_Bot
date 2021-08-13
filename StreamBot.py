#------------------
#StreamBotv1.py

# This bot checks to see if the Youtube Funhaus Channel is currently livestreaming.  If it is, it scrapes Youtube for a unique url and video title, and then posts it to /r/Funhaus


# Created by /u/Mattyi on 8/9/2021
#
# To DO:  Current error handling will yield an exception for any action that reads "funhaus is not live."  99% of the time, that's correct, but should be cleaned up.
#------------------

import streamlink           #for checking if there's a live stream
import urllib               #for opening a live stream
import praw                 #for posting to reddit
from time import time,sleep #for running code on a timer
from datetime import datetime #for logging
import config



#Reddit bot's login info from config.py.  If you're a /r/funhaus mod, contact /u/Mattyi for the sub's streambot credentials.  If not, rename EXAMPLE_config.py to config.py and enter credentials for your own bot.
r=praw.Reddit(                                                      
    client_id=config.BotClientID,
    client_secret=config.BotClientSecret,
    password=config.BotPassword,
    username=config.BotUsername,
    user_agent=config.BotUserAgent
)

subreddit= r.subreddit("Funhaus")                                               #praw subreddit reference
YTlink='https://www.youtube.com/channel/UCboMX_UNgaPBsUOIgasn3-Q/live'          #Youtube channel name + '/live' link automatically takes user to current live stream if it's available
#YTlink='https://www.youtube.com/channel/UCSJ4gkVC6NrvII8umztf0Ow/live'         #(test link using a stream that's nearly always on)             


while True:
    sleep(30-time() % 30)                                                              #wait 30 sec before executing
    streams=streamlink.streams(YTlink)                                                  #Grab any current streams using the url for the channel + '/live'.
    
    try:
        stream=streams["best"]                                                          #grab stream with best quality. Throws error if no stream found.
    except:
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': Funhaus is not live.') 
    else:
        weburl=urllib.request.urlopen(YTlink)                                           #Open the 'funhaus/live' url.
        data=str(weburl.read())                                                         #Grab the html response.  Inside here are the unique Broadcast url & title to use for our reddit post.
        BroadcastURL= data.split('="canonical" href="',1)[1].split('"',1)[0]            #parse html for the broadcast url.
        BroadcastTitle= data.split('meta name="title" content="',1)[1].split('"',1)[0]  #parse html for video title.

        streamlist = open('streams.txt', 'r')                                           #check last line of streams.txt to see if this link's already been posted
        linelist=streamlist.readlines()
        streamlist.close()
        if linelist[-1]!=BroadcastURL:                                                  #if not already posted, post the link to the subreddit and add the link to streams.txt.

            #reddit post
            title=BroadcastTitle
            url=BroadcastURL
            subreddit.submit(title,url=url, flair_id='5debe1c2-b1cd-11eb-a63a-0ec3d5715665') #flair ID is for the Livestream flair on the sub.

            #append stream url to streams.txt
            streamlist = open('streams.txt','a+')
            streamlist.write('\n' + BroadcastURL)
            streamlist.close()

            print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': Funhaus is LIVE!  A post has been created in the sub.')              
        else:
            print (str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ':Funhous is live, but stream has already been posted.')



    


