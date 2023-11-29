import pandas as pd
import os
import re
import sys

from tqdm import tqdm

def validate_args(args) -> tuple[str, str, str]:
    if len(args) > 3:
        print("Too many args provided.")
        exit(1)
    if len(args) < 2:
        print("Too few args provided.")
        exit(1)
    if not os.path.isdir(args[0]):
        print("Not a valid search directory.")
        exit(1)
    if not os.path.isfile(args[1]):
        print("Not a valid plays.csv file.")
        exit(1)
    if len(args) == 3:
        return (os.path.abspath(args[0]), os.path.abspath(args[1]), args[2])
    return (os.path.abspath(args[0]), os.path.abspath(args[1]), "^tracking_week")

def gather_remove_data(filename: str) -> list[tuple[int, int]]:
    game_and_play_ids = []
    with open(filename) as f:
        lineno = 1
        for line in f:
            line = line.split(',')
            game_and_play_ids.append((int(line[0]), int(line[1])))
    return game_and_play_ids

def clean(remove_from: list[tuple[int, int]], search_dir: str, regex: str):
    weekno = 1
    remove_from_copy = remove_from.copy()
    file_regex = re.compile(regex)

    for file_name in os.listdir(search_dir):
        if file_regex.match(file_name):
            file = os.path.join(search_dir, file_name)
            print(f"Found file {file_name}")
            df = pd.read_csv(file)
            curr_size = df.size
            pop_list = []
            for index, row in tqdm((df.iterrows())):
                info = (row['gameId'], row['playId'])
                if info in remove_from:
                    try:
                        remove_from_copy.remove(info)
                    except:
                        pass
                    pop_list.append(index)
            df = df.drop(pop_list)
            print("df size reduced by ", curr_size - df.size)
            df.to_csv(f'week_{weekno}.csv')
            print(f"Written to week_{weekno}.csv\n")
            weekno += 1

def main():
    search_dir, remove_file, regex_pattern = validate_args(sys.argv[1::])
    remove_data = gather_remove_data(remove_file)
    clean(remove_data, search_dir, regex_pattern)

if __name__ == "__main__":
    main()
