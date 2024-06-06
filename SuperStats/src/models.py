from typing import Dict

from flask_login import UserMixin
from psycopg2 import sql

from src import login_manager, db_cursor, conn, app


@login_manager.user_loader
def load_user(user_id):
    user_sql = sql.SQL("""
    SELECT * FROM Users
    WHERE pk = %s
    """).format(sql.Identifier('pk'))

    db_cursor.execute(user_sql, (int(user_id),))
    return User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None


class ModelUserMixin(dict, UserMixin):
    @property
    def id(self):
        return self.pk


class ModelMixin(dict):
    pass


class User(ModelUserMixin):
    def __init__(self, user_data: Dict):
        super(User, self).__init__(user_data)
        self.pk = user_data.get('pk')
        self.full_name = user_data.get('full_name')
        self.user_name = user_data.get('user_name')
        self.club_name = user_data.get('club_name')
        self.password = user_data.get('password')


class Customer(User):
    def __init__(self, user_data: Dict):
        super().__init__(user_data)


class Manager(User):
    def __init__(self, user_data: Dict):
        super().__init__(user_data)


class Match(ModelMixin):
    def __init__(self, match_data: Dict):
        super(Match, self).__init__(match_data)
        self.match_id = match_data.get('match_id')
        self.home_team_name = match_data.get('home_team_name')
        self.away_team_name = match_data.get('away_team_name')
        self.home_team_goals = match_data.get('home_team_goals')
        self.away_team_goals = match_data.get('away_team_goals')

class MatchInfo(ModelMixin):
    def __init__(self, match_info_data: Dict):
        super(MatchInfo, self).__init__(match_info_data)
        self.pk = match_info_data.get('pk')
        self.match_id = match_info_data.get('match_id')
        self.shirt_number = match_info_data.get('shirt_number')
        self.club_name = match_info_data.get('club_name')
        self.goals_scored = match_info_data.get('goals_scored')


class DeleteMatchInfo(ModelMixin):
    def __init__(self, match_id: int):
        super(DeleteMatchInfo, self).__init__()
        self.match_id = match_id

class Players(ModelMixin):
    def __init__(self, player_data: Dict):
        super(Players, self).__init__(player_data)
        self.shirt_number = player_data.get('shirt_number')
        self.club_name = player_data.get('club_name')
        self.player_name = player_data.get('player_name')
        self.nationality = player_data.get('nationality')
        self.goals = player_data.get('goals')

class Clubs(ModelMixin):
    def __init__(self, club_data: Dict):
        super(Clubs, self).__init__(club_data)
        self.club_name = club_data.get('club_name')
        self.manager_name = club_data.get('manager_name')
        self.games_played = club_data.get('games_played')
        self.wins = club_data.get('wins')
        self.draws = club_data.get('draws')
        self.losses = club_data.get('losses')
        self.points = club_data.get('points')
        self.goals_scored = club_data.get('goals_scored')
        self.goals_conceded = club_data.get('goals_conceded')
        self.goal_difference = club_data.get('goal_difference')



