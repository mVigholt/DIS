from src import db_cursor, conn
from src.models import User, Manager, Customer, Produce, Sell, ProduceOrder , Match , MatchInfo, Players, Clubs , DeleteMatchInfo


# INSERT QUERIES
def insert_user(user: User):
    sql = """
    INSERT INTO Users(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (user.user_name, user.full_name, user.password))
    conn.commit()


def insert_manager(manager: Manager):
    sql = """
    INSERT INTO Managers(user_name, full_name, password, club_name)
    VALUES (%s, %s, %s, %s)
    """
    db_cursor.execute(sql, (manager.user_name, manager.full_name, manager.password, manager.club_name))
    conn.commit()

def delete_match_by_id(deletematchinfo: DeleteMatchInfo):
    # Ensure parameters are passed correctly
    sql = """ 
    DELETE FROM Matchinfo WHERE match_id = %s
    """
    db_cursor.execute(sql, (deletematchinfo.match_id,))  # Use comma to create a single-element tuple
    
    sql2 = """
    DELETE FROM Matches WHERE match_id = %s
    """
    db_cursor.execute(sql2, (deletematchinfo.match_id,))  # Use comma to create a single-element tuple

    conn.commit()



def insert_match(match: Match):
    print('HAAAAAAAALLOOO')
    sql = """
    INSERT INTO Matches(match_id ,home_team_name, away_team_name , home_team_goals , away_team_goals)
    VALUES (%s , %s, %s , %s , %s)
    """
    db_cursor.execute(sql, (match.match_id, match.home_team_name, match.away_team_name , match.home_team_goals , match.away_team_goals))
    
    conn.commit()


def insert_match_info(match_info: MatchInfo):
    sql = """
    INSERT INTO MatchInfo(match_id, shirt_number, club_name, goals_scored)
    VALUES (%s, %s, %s, %s)
    """
    db_cursor.execute(sql, (match_info.match_id, match_info.shirt_number, match_info.club_name, match_info.goals_scored))
    conn.commit()

def update_club_stats():
    # Reset club stats to zero
    reset_sql = """
    UPDATE Clubs
    SET 
        games_played = 0,
        wins = 0,
        draws = 0,
        losses = 0,
        points = 0,
        goals_scored = 0,
        goals_conceded = 0,
        goal_difference = 0
    """
    db_cursor.execute(reset_sql)

    # Update home team stats
    sql_home = """
    UPDATE Clubs
    SET 
        games_played = games_played + 1,
        wins = wins + CASE
            WHEN Matches.home_team_goals > Matches.away_team_goals THEN 1
            ELSE 0
        END,
        draws = draws + CASE
            WHEN Matches.home_team_goals = Matches.away_team_goals THEN 1
            ELSE 0
        END,
        losses = losses + CASE
            WHEN Matches.home_team_goals < Matches.away_team_goals THEN 1
            ELSE 0
        END,
        points = points + CASE
            WHEN Matches.home_team_goals > Matches.away_team_goals THEN 3
            WHEN Matches.home_team_goals = Matches.away_team_goals THEN 1
            ELSE 0
        END,
        goals_scored = goals_scored + Matches.home_team_goals,
        goals_conceded = goals_conceded + Matches.away_team_goals,
        goal_difference = (goals_scored + Matches.home_team_goals) - (goals_conceded + Matches.away_team_goals)
    FROM Matches
    WHERE Clubs.club_name = Matches.home_team_name
    """
    db_cursor.execute(sql_home)

    # Update away team stats
    sql_away = """
    UPDATE Clubs
    SET 
        games_played = games_played + 1,
        wins = wins + CASE
            WHEN Matches.away_team_goals > Matches.home_team_goals THEN 1
            ELSE 0
        END,
        draws = draws + CASE
            WHEN Matches.away_team_goals = Matches.home_team_goals THEN 1
            ELSE 0
        END,
        losses = losses + CASE
            WHEN Matches.away_team_goals < Matches.home_team_goals THEN 1
            ELSE 0
        END,
        points = points + CASE
            WHEN Matches.away_team_goals > Matches.home_team_goals THEN 3
            WHEN Matches.away_team_goals = Matches.home_team_goals THEN 1
            ELSE 0
        END,
        goals_scored = goals_scored + Matches.away_team_goals,
        goals_conceded = goals_conceded + Matches.home_team_goals,
        goal_difference = (goals_scored + Matches.away_team_goals) - (goals_conceded + Matches.home_team_goals)
    FROM Matches
    WHERE Clubs.club_name = Matches.away_team_name
    """
    db_cursor.execute(sql_away)

    # Commit the changes
    conn.commit()



def update_player_stats():
    # Reset goals to zero
    reset_sql = """
    UPDATE Players
    SET goals = 0
    """
    db_cursor.execute(reset_sql)

    # Increment goals based on match info
    update_sql = """
    UPDATE Players AS p
    SET goals = p.goals + m.goals_scored
    FROM MatchInfo AS m
    WHERE p.shirt_number = m.shirt_number AND p.club_name = m.club_name
    """
    db_cursor.execute(update_sql)

    conn.commit()





def insert_customer(customer: Customer):
    sql = """
    INSERT INTO Customers(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (customer.user_name, customer.full_name, customer.password))
    conn.commit()


def insert_produce(produce: Produce):
    sql = """
    INSERT INTO Produce(category, item, unit, variety, price)
    VALUES (%s, %s, %s, %s, %s) RETURNING pk
    """
    db_cursor.execute(sql, (
        produce.category,
        produce.item,
        produce.unit,
        produce.variety,
        produce.price
    ))
    conn.commit()
    return db_cursor.fetchone().get('pk') if db_cursor.rowcount > 0 else None


def insert_sell(sell: Sell):
    sql = """
    INSERT INTO Sell(manager_pk, produce_pk)
    VALUES (%s, %s)
    """
    db_cursor.execute(sql, (sell.manager_pk, sell.produce_pk,))
    conn.commit()


def insert_produce_order(order: ProduceOrder):
    sql = """
    INSERT INTO ProduceOrder(produce_pk, Manager_pk, customer_pk)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (
        order.produce_pk,
        order.manager_pk,
        order.customer_pk,
    ))
    conn.commit()


# SELECT QUERIES
def get_user_by_pk(pk):
    sql = """
    SELECT * FROM Users
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


def get_manager_by_pk(pk):
    sql = """
    SELECT * FROM Managers
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    manager = Manager(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return manager


def get_produce_by_filters(category=None, item=None, variety=None,
                           manager_pk=None, manager_name=None, price=None):
    sql = """
    SELECT * FROM vw_produce
    WHERE
    """
    conditionals = []
    if category:
        conditionals.append(f"category='{category}'")
    if item:
        conditionals.append(f"item='{item}'")
    if variety:
        conditionals.append(f"variety = '{variety}'")
    if manager_pk:
        conditionals.append(f"manager_pk = '{manager_pk}'")
    if manager_name:
        conditionals.append(f"manager_name LIKE '%{manager_name}%'")
    if price:
        conditionals.append(f"price <= {price}")

    args_str = ' AND '.join(conditionals)
    order = " ORDER BY price "
    db_cursor.execute(sql + args_str + order)
    produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return produce

def get_player_by_name(player_name=None):
    sql = """
    SELECT * FROM players
    WHERE LOWER(player_name) LIKE LOWER(%s)
    """
    name = f"%{player_name}%"

    db_cursor.execute(sql, (name,))
    players = [Players(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return players

def get_club_by_name(club_name=None):
    sql = """
    SELECT * FROM clubs
    WHERE LOWER(club_name) LIKE LOWER(%s)
    """
    name = f"%{club_name}%"

    db_cursor.execute(sql, (name,))
    clubs = [Clubs(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return clubs


def get_customer_by_pk(pk):
    sql = """
    SELECT * FROM Customers
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    customer = Customer(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return customer


def get_produce_by_pk(pk):
    sql = """
    SELECT produce_pk as pk, * FROM vw_produce
    WHERE produce_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    produce = Produce(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return produce


def get_all_produce_by_manager(pk):
    sql = """
    SELECT * FROM vw_produce
    WHERE manager_pk = %s
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql, (pk,))
    produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return produce


def get_user_by_user_name(user_name):
    sql = """
    SELECT * FROM Users
    WHERE user_name = %s
    """
    db_cursor.execute(sql, (user_name,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


def get_all_produce():
    sql = """
    SELECT produce_pk as pk, category, item, variety, unit, price, manager_name, available, manager_pk
    FROM vw_produce
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql)
    produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return produce


def get_available_produce():
    sql = """
    SELECT * FROM vw_produce
    WHERE available = true
    ORDER BY price  
    """
    db_cursor.execute(sql)
    produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return produce


def get_orders_by_customer_pk(pk):
    sql = """
    SELECT * FROM ProduceOrder po
    JOIN Produce p ON p.pk = po.produce_pk
    WHERE customer_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    orders = [ProduceOrder(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return orders


# UPDATE QUERIES
def update_sell(available, produce_pk, manager_pk):
    sql = """
    UPDATE Sell
    SET available = %s
    WHERE produce_pk = %s
    AND manager_pk = %s
    """
    db_cursor.execute(sql, (available, produce_pk, manager_pk))
    conn.commit()
