## code automates content gathering for reddit youtubers

## need to install praw, pandas and gtts modules

## Theres an external program called Balcon that I used for a block of code i #'d out.
## I don't know how to integrate other exe's when the code is not on my PC, so currently
## Google TTS makes the program functional still.

## I don't know how to take user defined directories yet.

## I don't know how to use reddit api without auth

import sys
import os
from gtts import gTTS
import praw
import pandas as pd
import datetime as dt
import subprocess
import string

reddit = praw.Reddit(client_id = 'stpzhsW96nKKuw', \
                     client_secret = '6OLTWSaiwQfla8qPA4O-Vn_b_Gs', \
                     user_agent = 'TTS Scraper for reddit', \
                     username = 'botbottybotter',\ # Please be nice and don't change this
                     password = 'botterbot123') # Please be nice and don't change this
 
print("Login Succesful.")
print("Enter Subreddit to get the top result")

subreddit = reddit.subreddit(input())

print("Enter the amount of threads")
limitnum = int(input())


top_subreddit = subreddit.top(limit=1)
i=0

for submission in subreddit.top(limit=limitnum):
    print(submission.title)
    print()
    print(submission.selftext)
    print()
    print()
    print()
    print()
    print()
    mytext = (submission.title + submission.selftext)
    language = 'en-US'
    myobj = gTTS(text=mytext, lang= language, slow=False) #
    myobj.save(str(submission)+".mp3")  #Will save audio files wherever this code exists
    #ttsfeed = open(str(submission.title.translate(str.maketrans('', '', string.whitespace)))+".txt","a")
    #ttsfeed.write(mytext)
    #ttsfeed.close()
    #batfeed = open("balcon.bat","w")
    #batfeed.write(str("balcon -f "+ (str(submission.title.translate(str.maketrans('', '', string.whitespace))))+ '.txt -n Daniel' " -w  C:\\Users\\Edviser\\Downloads\\balcon\\Audio\\" + str(submission.title.translate(str.maketrans('', '', string.whitespace)))+ ".mp3")) #Define your own directory here. This bit modifies the bat responsible for making the TTS file.
    #batfeed.close()
    #os.system(r"C:\Users\Edviser\Downloads\balcon\balcon.bat" ) #Define this wherever the bat file exists
    


    
               
    
    
