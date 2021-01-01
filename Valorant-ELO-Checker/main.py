import json
from valApi import ValorantAPI
import time
import socket
import tkinter as tk
hostname = socket.gethostname()
from tkinter import *
from functools import partial
from PIL import ImageTk, Image
global matchHistory
import sys
match_movement_hash = {
  'INCREASE': ['Increase', 'Victory'],
  'MINOR_INCREASE': ['Minor Increase', 'Victory'],
  'MAJOR_INCREASE': ['Major Increase', 'Victory'],
  'DECREASE': ['Decrease', 'Defeat'],
  'MAJOR_DECREASE': ['Major Decrease', 'Defeat'],
  'MINOR_DECREASE': ['Minor Decrease', 'Defeat'],
  'PROMOTED': ['Promoted', 'Victory'],
  'DEMOTED': ['Demoted', 'Defeat'],
  'STABLE': ['Stable', 'Draw']
}

# Gives map name
maps_hash = {
  '/Game/Maps/Duality/Duality': 'Bind',
  '/Game/Maps/Bonsai/Bonsai': 'Split',
  '/Game/Maps/Ascent/Ascent': 'Ascent',
  '/Game/Maps/Port/Port': 'Icebox',
  '/Game/Maps/Triad/Triad': 'Haven',
  '': 'Unknown'
}


def normalMode(usernameText, passwordText, regionText):
        username=usernameText.get()
        password=passwordText.get()
        region = regionText.get()
        client_ip = socket.gethostbyname(hostname)

        # Attempt login
        try:
            valorant = ValorantAPI(username, password, region, client_ip)
        except:
            print('A login error occurred. F')
            print('Invalid username/password or incorrect region.')

        # Attempt to acquire match history data
        try:
            json_res = valorant.get_match_history()
        except:
            print('Cannot get match history.')
            

        # Attempt to parse through match history data

        posts = []
        for match in json_res['Matches']:
          # print(match)
          if match['CompetitiveMovement'] == 'MOVEMENT_UNKNOWN':
            continue
          match_movement, game_outcome = match_movement_hash[match['CompetitiveMovement']]
          lp_change = ''

          game_map = maps_hash[match['MapID']]

          tier = match['TierAfterUpdate']
          
          epoch_time = match['MatchStartTime'] // 1000
          date = time.strftime('%m-%d-%Y', time.localtime(epoch_time))

          before = match['TierProgressBeforeUpdate']
          after = match['TierProgressAfterUpdate']

          # calculate ELO change
          if match['CompetitiveMovement'] == 'PROMOTED':
            lp_change = '+' + str(after + 100 - before)
          elif match['CompetitiveMovement'] == 'DEMOTED':
            lp_change = '-' + str(before + 100 - after)
          else:
            if before < after:
              # won
              lp_change = '+' + str(after - before)
            else:
              # lost
              lp_change = str(after - before)

          match_data = {
            'lp_change': lp_change,
            'current_lp': after,
            'game_outcome': game_outcome,
            'movement': match_movement,
            'tier': tier,
            'date': date,
            'game_map': game_map,        
          }

          posts.append(match_data)

        #print(posts)
        matchHistory = tk.Toplevel(tkWindow)
        matchHistory.iconbitmap('favicon.ico')
        matchHistory.title('Match History for ' + username)
        for i, n in enumerate(posts):
                MyLabel(matchHistory,(posts[i]["game_map"]+", "+posts[i]["date"]), str(posts[i]["current_lp"]), posts[i]["tier"], posts[i]["lp_change"], posts[i]["movement"]).pack(expand=True, fill='x')
        Button(matchHistory, text="Switch to Overlay Mode", command=lambda:[matchHistory.destroy(), overlayMode(username, password, region)]).pack()
        Button(matchHistory, text="Refresh", command=lambda:[matchHistory.destroy(), normalMode()]).pack()
        return

def overlayMode(username, password, region):
        client_ip = socket.gethostbyname(hostname)

        # Attempt login
        try:
            valorant = ValorantAPI(username, password, region, client_ip)
        except:
            print('A login error occurred. F')
            print('Invalid username/password or incorrect region.')

        # Attempt to acquire match history data
        try:
            json_res = valorant.get_match_history()
        except:
            print('Cannot get match history.')
            

        # Attempt to parse through match history data

        posts = []
        for match in json_res['Matches']:
          if match['CompetitiveMovement'] == 'MOVEMENT_UNKNOWN':
            continue
          match_movement, game_outcome = match_movement_hash[match['CompetitiveMovement']]
          lp_change = ''

          game_map = maps_hash[match['MapID']]

          tier = match['TierAfterUpdate']
          
          epoch_time = match['MatchStartTime'] // 1000
          date = time.strftime('%m-%d-%Y', time.localtime(epoch_time))

          before = match['TierProgressBeforeUpdate']
          after = match['TierProgressAfterUpdate']

          # calculate ELO change
          if match['CompetitiveMovement'] == 'PROMOTED':
            lp_change = '+' + str(after + 100 - before)
          elif match['CompetitiveMovement'] == 'DEMOTED':
            lp_change = '-' + str(before + 100 - after)
          else:
            if before < after:
              # won
              lp_change = '+' + str(after - before)
            else:
              # lost
              lp_change = str(after - before)

          match_data = {
            'lp_change': lp_change,
            'current_lp': after,
            'game_outcome': game_outcome,
            'movement': match_movement,
            'tier': tier,
            'date': date,
            'game_map': game_map,        
          }

          posts.append(match_data)

        matchHistory = tk.Toplevel(tkWindow)
        matchHistory.title('Match History for ' + username)
        matchHistory.iconbitmap('favicon.ico')
        matchHistory.attributes("-topmost", True)
        matchHistory.geometry('-0-0')  
        matchHistory.overrideredirect(1)
        MyLabel(matchHistory,(posts[0]["game_map"]+", "+posts[0]["date"]), str(posts[0]["current_lp"]), posts[0]["tier"], posts[0]["lp_change"], posts[0]["movement"]).pack(expand=True, fill='x')
        refresh = lambda _:[matchHistory.destroy(),overlayMode(username,password,region)]
        normal = lambda _:[matchHistory.destroy(),normalMode()]
        quit = lambda _:[tkWindow.destroy(),sys.exit()]
        matchHistory.bind("<Alt_L><r>", refresh)
        matchHistory.bind("<Alt_L><n>", normal)
        matchHistory.bind("<Alt_L><q>", quit)
        return

class MyLabel(Frame):
  def __init__(self, master, mapDate, currentELO, currentRank, eloChange, rankChange):
    Frame.__init__(self, master, bd=2, relief='raised')
    self.rankPic = ImageTk.PhotoImage(Image.open("ranks/"+str(currentRank)+'.png'))
    Label(self, image = self.rankPic).grid(row=0, column=0, rowspan=2)
    Label(self, text=mapDate, font=('Aria', 16, 'bold'), fg='black', anchor='w').grid(row=0, column=1)
    Label(self, text="Current ELO (out of 100): "+currentELO, font=('Aria', 10), fg='black').grid(row=1, column=1)
    if int(eloChange)==0:
            Label(self, text=rankChange+", "+eloChange, fg='white', bg='#848785').grid(row=0, column=2, rowspan=2, padx=10)
    if int(eloChange)>0:
            Label(self, text=rankChange+", "+eloChange, fg='white', bg='#3ac75f').grid(row=0, column=2, rowspan=2, padx=10)
    else:
            Label(self, text=rankChange+", "+eloChange, fg='white', bg='#bf4747').grid(row=0, column=2, rowspan=2, padx=10)
    self.columnconfigure(1, weight=1)


#window
tkWindow = Tk()  
tkWindow.geometry('230x190')  
tkWindow.title('Login to Riot')

#username label and text entry box
usernameLabel = Label(tkWindow, text="Username").grid(row=0, column=0)
usernameText = StringVar()
usernameEntry = Entry(tkWindow, textvariable=usernameText).grid(row=0, column=1)  

#password label and password entry box
passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0, pady=13)  
passwordText = StringVar()
passwordEntry = Entry(tkWindow, textvariable=passwordText, show='•').grid(row=1, column=1,pady=13)

regionLabel = Label(tkWindow,text="Region").grid(row=2, column=0, pady=0)  
regionText = StringVar()
regionEntry = Entry(tkWindow, textvariable=regionText).grid(row=2, column=1,pady=00)
normalMode= partial(normalMode, usernameText, passwordText, regionText)
#login button
loginButton = Button(tkWindow, text="Login", command=normalMode, height=5).place(x=185,y=0)  
notice = Label(tkWindow,text="This application is not affiliated with Riot Games, or any of its games. This application simply uses Riot's API to find your ELO. No personal info is gathered or saved by this application.\n~ Created by Arnav Ambre ~", wraplength=230, justify="left").place(x=0,y=90)  
tkWindow.iconbitmap('favicon.ico')
tkWindow.mainloop()
