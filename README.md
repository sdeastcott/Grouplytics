# Grouplytics
Grouplytics is a fun way to learn about any of your GroupMe groups. We sift through (but don't store!) your group messages and generate various reports along the way. Currently this is only available as a command line tool, but a live site is in the works.

### Available Reports
- Most Liked
- Biggest Liker
- Potty Mouth
- The Donald Trump Report
- GF/BF Mentions
- The 'Dude' Report
- Meme Lord 
- Overall message count with per member breakdown

### Coming Soon!
- Biggest Complainer
- Longest period of inactivity
- Most active hour/day/month of all time
- Serial Name Changer

### How To Use Command Line Tool:
1. Go to dev.groupme.com
2. Log in with your GroupMe account information.
3. In the top right corner, you should see 'Access Token' located next to your name. Click on it and copy it.
4. Download the project.
5. Open the example config.txt file and replace everything with your information. The command line tool isn't very robust, so make sure the formatting is spot on. No need to enter emojis if your group name has them.
6. Run python3 CommandLineTool.py from your terminal, enter config.txt when prompted.
7. Reports take about a minute to generate depending on your internet speed.
8. Enjoy!

### To use the server.
#### NOTE: This is just an attempt at getting something working. This will probably break stuff.
```bash
    pip install -r requirements.txt
    python Server.py
```

Send an HTTP POST at one of the routes with the following json as the body.
```json
{
    "token": "ACCESS TOKEN HERE",
    "name": "GROUP NAME",
    "members": [
        "Strings of form name:username"
    ]
}
```