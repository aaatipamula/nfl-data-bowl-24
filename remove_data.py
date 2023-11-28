import pandas as pd
import os

game_and_play = []
with open('remove_second.txt') as f:
    for line in f:
        line = line.split(',')
        game_and_play.append((int(line[0]), int(line[1])))
print(len(game_and_play))
game_and_play_copy = game_and_play.copy()

def old_clean():
    for file_name in os.listdir(".\\original_data"):
        if file_name.startswith("tracking_week"):
            df = pd.read_csv(".\\original_data\\" + file_name)
            curr_size = df.size
            pop_list = []
            for index, row in (df.iterrows()):
                info = (row['gameId'], row['playId'])
                if info in game_and_play:
                    try:
                        game_and_play_copy.remove(info)
                    except:
                        pass
                    pop_list.append(index)
            df = df.drop(pop_list)
            print(file_name, curr_size - df.size)
            df.to_csv('clean' + file_name)

def new_clean():
    weekno = 1
    for file_name in os.listdir(".\\"):
        if file_name.endswith(".csv"):
            df = pd.read_csv(".\\" + file_name)
            curr_size = df.size
            pop_list = []
            for index, row in (df.iterrows()):
                info = (row['gameId'], row['playId'])
                if info in game_and_play:
                    try:
                        game_and_play_copy.remove(info)
                    except:
                        pass
                    pop_list.append(index)
            df = df.drop(pop_list)
            print(file_name, curr_size - df.size)
            df.to_csv(f'week_{weekno}.csv')
            weekno += 1
new_clean()
print(len(game_and_play_copy))
