# Grouplytics
Grouplytics is a fun way to learn about any of your GroupMe groups. We sift through (but don't store!) your group messages and create various reports along the way. Currently this is only available as a command line tool, but live site is in the works.

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
- Most active day/week/month of all time
- Serial Name Changer

### How To Use Command Line Tool:
1. Go to dev.groupme.com
2. Log in with your GroupMe account information.
3. In the top right corner, you should see 'Access Token' located next to your name. Click on it and copy it.
4. Download the project.
5. Open the example config.txt file and replace everything with your information. The command line tool isn't very robust, so make sure the formatting is spot on. If you have emojis in your group name, this won't work. Fix coming soon.
6. Run python3 CommandLineTool.py from your terminal, enter config.txt when prompted.
7. Reports take about a minute to generate depending on your internet speed.
8. Enjoy!
