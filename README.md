# Valorant ELO Checker
Check your hidden ELO in Valorant with a desktop application! This repo is the source code for my Valorant Elo checker.
Want to install an .exe file instead? I got you covered: https://github.com/clikbait295/Valorant-ELO-Checker-Installer
# Installation
1. Make sure you have Python 3 and pip installed on your computer. Download it [here](https://www.python.org/downloads/) for Windows. It should be pre-installed on Macs.
2. Clone the repo (download as a zip, use git clone, etc) If you downloaded as a zip, unzip the file.
3. Use pip to install the "requests" package. (Depending on your system, it'll look something like "py -m pip install requests" or "python3 -m pip install requests"...you might need to do a little troubleshooting here.)
4. After it's finished installing, you can simply double click the "main.py" file. 
5. Enter in your username and password, and check out your rank and internal ELO rating! See the manual below for more info.

# Manual
To run this program, simply double click the "main.py" file in the installation folder. When you see the window open up, enter in your username and password and hit the login button. Then, you should see your match history, along with your internal ELO and ELO change each match. You can refresh your info after a competitive game by clicking the refresh button at the bottom of the page. 

To switch to overlay mode, click on "Switch to Overlay Mode." In this mode, your match info for the previous game is displayed at the botton left of your screen in an "always on top" window. You can use this as an overlay while you play Valorant. To refresh the overlay, hit Alt+R while the overlay is active (click on the window). To switch back to normal mode, hit Alt+N. To quit the application, hit Alt+Q. 

Note: To use this overlay while playing Valorant, you have to switch your graphics settings to "Windowed Fullscreen." To use the keyboard shortcuts while in game, hit your escape key (so you can see your mouse) and click on the overlay mode. Then, use the keyboard shortcuts to refresh, quit, or switch to overlay mode.

# Inspiration
I always wanted a way to check my Valorant ranked ELO, and when I saw dylantheriot's and RumbleMikee's code, I felt I could add a little pizzaz to the process. So I created a spiffing (not really) tkinter program so the program could be used without a browser and an overlay mode for easy viewing in-game. Check out the following repos by dylantheriot, RubmleMikee, and Luc1412 from which I got my inspiration:
- https://github.com/dylantheriot/valorant-match-history
- The valAPI.py file is from the previous link, and some of the code in main.py is cannibalized from the code in the previous link. Dylantheriot's code was vital in creating this repo.
- https://github.com/RumbleMike/ValorantRankedPoints
- https://gist.github.com/Luc1412/1f93257a2a808679ff014f258db6c35b. 

# Disclaimer
This program does **NOT** steal **ANY** personal info, including passwords or usernames. This program is not malicious in any way, it is just a way for you to check your internal ELO in Valorant!
