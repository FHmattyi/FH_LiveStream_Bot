*FH_LiveStream_Bot* is a reddit bot that checks the Funhaus youtube channel to see whether is is livestreaming.  When it is, it posts the link and title to /r/Funhaus

To run a similar bot on your own subreddit:

1. create a new account for your bot, generate a Script app in the settings and follow the praw documentation to generate your secret key.
2. rename EXAMPLE_config.py to config.py and fill in the file with your account's info including secret key.
3. in StreamBot.py, change the value of YTlink to "http://www.youtube.com/c/[desired channel name]/live"
4. find somehwere to host the script.  It is built to run continuously, so make sure to add it to your machine's startup routine.
