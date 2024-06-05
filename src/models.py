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


if __name__ == '__main__':
    user_data = dict(full_name='a', user_name='b', password='c')
    user = Manager(user_data)
    print(user)




class Produce(ModelMixin):
    def __init__(self, produce_data: Dict):
        super(Produce, self).__init__(produce_data)
        self.pk = produce_data.get('pk')
        self.category = produce_data.get('category')
        self.item = produce_data.get('item')
        self.unit = produce_data.get('unit')
        self.variety = produce_data.get('variety')
        self.price = produce_data.get('price')
        # From JOIN w/ Sell relation
        self.available = produce_data.get('available')
        self.farmer_name = produce_data.get('farmer_name')
        self.farmer_pk = produce_data.get('farmer_pk')


class Sell(ModelMixin):
    def __init__(self, sell_data: Dict):
        super(Sell, self).__init__(sell_data)
        self.available = sell_data.get('available')
        self.manager_pk = sell_data.get('manager_pk')
        self.produce_pk = sell_data.get('produce_pk')


class ProduceOrder(ModelMixin):
    def __init__(self, produce_order_data: Dict):
        super(ProduceOrder, self).__init__(produce_order_data)
        self.pk = produce_order_data.get('pk')
        self.customer_pk = produce_order_data.get('customer_pk')
        self.farmer_pk = produce_order_data.get('farmer_pk')
        self.produce_pk = produce_order_data.get('produce_pk')