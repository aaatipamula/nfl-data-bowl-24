import pandas as pd
import numpy as np
import os
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button

train = pd.read_csv('cleantracking_week_1.csv', low_memory=False)
plays = pd.read_csv('plays.csv', low_memory=False)

def create_football_field(linenumbers=True,
                          endzones=True,
                          highlight_line=False,
                          highlight_line_number=50,
                          highlighted_name='Line of Scrimmage',
                          fifty_is_los=False,
                          figsize=(12, 6.33)):
    """
    Function that plots the football field for viewing plays.
    Allows for showing or hiding endzones.
    """
    rect = patches.Rectangle((0, 0), 120, 53.3, linewidth=0.1,
                             edgecolor='r', facecolor='darkgreen', zorder=0)

    fig, ax = plt.subplots(1, figsize=figsize)
    ax.add_patch(rect)

    plt.plot([10, 10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80,
              80, 90, 90, 100, 100, 110, 110, 120, 0, 0, 120, 120],
             [0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3,
              53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 53.3, 0, 0, 53.3],
             color='white')
    if fifty_is_los:
        plt.plot([60, 60], [0, 53.3], color='gold')
        plt.text(62, 50, '<- Player Yardline at Snap', color='gold')
    # Endzones
    if endzones:
        ez1 = patches.Rectangle((0, 0), 10, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='blue',
                                alpha=0.2,
                                zorder=0)
        ez2 = patches.Rectangle((110, 0), 120, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='blue',
                                alpha=0.2,
                                zorder=0)
        ax.add_patch(ez1)
        ax.add_patch(ez2)
    plt.xlim(0, 120)
    plt.ylim(-5, 58.3)
    plt.axis('off')
    if linenumbers:
        for x in range(20, 110, 10):
            numb = x
            if x > 50:
                numb = 120 - x
            plt.text(x, 5, str(numb - 10),
                     horizontalalignment='center',
                     fontsize=20,  # fontname='Arial',
                     color='white')
            plt.text(x - 0.95, 53.3 - 5, str(numb - 10),
                     horizontalalignment='center',
                     fontsize=20,  # fontname='Arial',
                     color='white', rotation=180)
    if endzones:
        hash_range = range(11, 110)
    else:
        hash_range = range(1, 120)

    for x in hash_range:
        ax.plot([x, x], [0.4, 0.7], color='white')
        ax.plot([x, x], [53.0, 52.5], color='white')
        ax.plot([x, x], [22.91, 23.57], color='white')
        ax.plot([x, x], [29.73, 30.39], color='white')

    if highlight_line:
        hl = highlight_line_number + 10
        plt.plot([hl, hl], [0, 53.3], color='yellow')
        plt.text(hl + 2, 50, '<- {}'.format(highlighted_name),
                 color='yellow')
    return fig, ax

def get_teams(gameId, playId):
    home = train.query(f"gameId == {gameId} and playId == {playId} and club != 'football'")['club'].unique()[0]
    away = train.query(f"gameId == {gameId} and playId == {playId} and club != 'football'")['club'].unique()[1]
    return home, away

def yes_button_clicked(event):
    global playID, gameID
    # Log the gameId and playId
    print(f"Logged: gameId={gameID}, playId={playID}")
    # Move to the next plot
    plt.close()

def maybe_button_clicked(event):
    global playID, gameID
    # Log the gameId and playId
    print(f"Logged: gameId={gameID}, playId={playID}")
    # Move to the next plot
    plt.close()

def no_button_clicked(event):
    # Just close the current plot
    plt.close()

gameID = 2022090800
for playID in range(5100):
    a = train.query(f"gameId == {gameID} and playId == {playID}")
    if a.empty:
        continue
    b = plays.query(f"gameId == {gameID} and playId == {playID}")['playDescription'].values[0]
    fig, ax = create_football_field()
    teams = get_teams(gameID, playID)
    train.query(f"gameId == {gameID} and playId == {playID} and club == 'football'") \
        .plot(x='x', y='y', kind='scatter', ax=ax, color='brown', s=30, label='Ball')
    train.query(f"gameId == {gameID} and playId == {playID} and club == '{teams[1]}'") \
        .plot(x='x', y='y', kind='scatter', ax=ax, color='white', s=5, label={teams[1]})
    train.query(f"gameId == {gameID} and playId == {playID} and club == '{teams[0]}'") \
        .plot(x='x', y='y', kind='scatter', ax=ax, color='blue', s=5, label={teams[0]})
    
    plt.title(f'Play #{playID} at Game #{gameID}\n{b}')
    plt.legend(loc='center right', bbox_to_anchor=(1.09, .5))
    

    button_width, button_height = 0.1, 0.075  # You can adjust these as needed
    ax_yes = plt.axes([.345, 0.05, button_width, button_height])
    ax_no = plt.axes([.58, 0.05, button_width, button_height])
    ax_maybe = plt.axes([.463, 0.05, button_width, button_height])
    btn_yes = Button(ax_yes, 'Yes')
    btn_no = Button(ax_no, 'No')
    btn_maybe = Button(ax_maybe, 'Maybe')
    btn_yes.on_clicked(yes_button_clicked)
    btn_no.on_clicked(no_button_clicked)
    btn_maybe.on_clicked(maybe_button_clicked)



    plt.show()

