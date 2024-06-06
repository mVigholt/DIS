import os
import pandas as pd
from flask import jsonify
from src import app

PLAYER_DATASET_PATH = os.path.join(app.root_path, 'dataset', 'Players.csv')
CLUB_DATASET_PATH = os.path.join(app.root_path, 'dataset', 'Clubs.csv')

def get_label_name(string):
    
    string = string.replace("_", " ")
    return ' '.join(word.capitalize() for word in string.split())


class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, item, get_label_name(item))

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]


player_df = pd.read_csv(PLAYER_DATASET_PATH, sep=';')
PlayerChoices = ModelChoices(player_df.player_name.unique())

club_df = pd.read_csv(CLUB_DATASET_PATH, sep=';')
ClubChoices = ModelChoices(club_df.club_name)

# ClubChoices = ModelChoices([
#     "Brøndby IF",
#     "FC København",
#     "FC Midtjylland",
#     "FC Nordsjælland",
#     "AGF",
#     "Silkeborg IF",
#     "Randers FC",
#     "Viborg FF",
#     "OB",
#     "Lyngby",
#     "Vejle BK",
#     "Hvidovre IF"
# ])


if __name__ == '__main__':
    #print(df.Name.unique())
    print(PlayerChoices.choices())
