# coding: utf-8
# v1.0

import tingbot
from tingbot import *
import urllib, json
from datetime import datetime
import time

state = {}

screenList = {
    0: 'main'
}
currentScreen = 0
state['screen'] = screenList[currentScreen]

baseUrl = "http://" + tingbot.app.settings['IP'] + ":" + str(tingbot.app.settings['PORT']) + "/api?mode=qstatus&output=json&apikey=" + tingbot.app.settings['API']
reqUrl = None
response = None

statsList = {
    0: {'statName': 'Current State', 'statJSON': 'state'},
    1: {'statName': 'Downloads', 'statJSON': 'noofslots_total'},
    2: {'statName': 'Speed', 'statJSON': 'speed'},
    3: {'statName': 'Timeleft on Queue', 'statJSON': 'timeleft'},
    4: {'statName': 'Warnings', 'statJSON': 'have_warnings'},
    5: {'statName': 'Timeleft to Resume', 'statJSON': 'pause_int'},
}

@tingbot.every(seconds=5)
def refresh():
    reqUrl = baseUrl
    response = urllib.urlopen(reqUrl)
    
    state['stats'] = json.loads(response.read())
 
def showMain():
    screen.fill(color=(26,26,26))

    screen.rectangle(
        xy=(0,16),
        align='left',
        size=(320,31),
        color=(255,165,0),
    )
    
    screen.text(
        'SABznb Status',
        xy=(160, 15),
        align='center',
        color='white',
        font='font/Arial Rounded Bold.ttf',
        font_size=18, 
    )
    
    row_y = 31

    for i in range(0,4):

        screen.rectangle(
            xy=(0,row_y),
            align='topleft',
            size=(320,51),
            color=(39,40,34),
        )

        if i == 0:
            if state['stats'][statsList[0]['statJSON']] == 'Paused':
                if state['stats'][statsList[5]['statJSON']] > '0':
                    statText = 'Paused for ' + state['stats'][statsList[5]['statJSON']]
                else:
                    statText = state['stats'][statsList[i]['statJSON']]
            elif state['stats'][statsList[0]['statJSON']] == 'IDLE':
                statText = 'Idle'
            else:
                statText = str(state['stats'][statsList[i]['statJSON']]).rstrip()
        else:
            statText = str(state['stats'][statsList[i]['statJSON']]).rstrip()

        statDisplay = statsList[i]['statName']
                
        screen.text(
            statDisplay,
            xy=(20,row_y+27),
            align='left',
            color=(220,220,220),
            font='font/Arial Rounded Bold.ttf',
            font_size=17,
        )

        screen.text(
            statText,
            xy=(300,row_y+27),
            align='right',
            color='white',
            font='font/Arial Rounded Bold.ttf',
            font_size=18,
        )

        row_y += 52

@every(seconds=1.0/30)
def loop():
    if 'stats' not in state or not state['stats']:
        screen.fill('yellow')
        screen.text(
            'Loading SABznb Please Wait ....',
            xy=(160, 220),
            font_size=12,
            color='white',
        )
        return
    
    if state['screen'] == 'main':
        showMain()

tingbot.run()