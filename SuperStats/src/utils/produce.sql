DROP TABLE IF EXISTS Players CASCADE;

CREATE TABLE IF NOT EXISTS  Players(
    shirt_number int not null,
    club_name varchar(100),
    player_name varchar(100),
    nationality varchar(100),
    goals float,
    PRIMARY KEY (shirt_number, club_name)
);

DELETE FROM Players;

CREATE INDEX IF NOT EXISTS players_index
ON Players (shirt_number, club_name);

DROP TABLE IF EXISTS Produce CASCADE;

CREATE TABLE IF NOT EXISTS Produce(
    pk serial unique not null PRIMARY KEY,
    category varchar(30),
    item varchar(30),
    variety varchar(30),
    unit varchar(10),
    price float
);

DELETE FROM Produce;

CREATE INDEX IF NOT EXISTS produce_index
ON Produce (category, item, variety);

DROP TABLE IF EXISTS Sell;

CREATE TABLE IF NOT EXISTS Sell(
    manager_pk int not null REFERENCES Managers(pk) ON DELETE CASCADE,
    produce_pk int not null REFERENCES Produce(pk) ON DELETE CASCADE,
    available boolean default true,
    PRIMARY KEY (manager_pk, produce_pk)
);

CREATE INDEX IF NOT EXISTS sell_index
ON Sell (manager_pk, available);

DELETE FROM Sell;

DROP TABLE IF EXISTS ProduceOrder;

CREATE TABLE IF NOT EXISTS ProduceOrder(
    pk serial not null PRIMARY KEY,
    customer_pk int not null REFERENCES Customers(pk) ON DELETE CASCADE,
    manager_pk int not null REFERENCES Managers(pk) ON DELETE CASCADE,
    produce_pk int not null REFERENCES Produce(pk) ON DELETE CASCADE,
    created_at timestamp not null default current_timestamp
);

DELETE FROM ProduceOrder;

CREATE OR REPLACE VIEW vw_produce
AS
SELECT p.category, p.item, p.variety,
       p.unit, p.price, s.available,
       p.pk as produce_pk,
       m.full_name as manager_name,
       m.pk as manager_pk
FROM Produce p
JOIN Sell s ON s.produce_pk = p.pk
JOIN Managers m ON s.manager_pk = m.pk
ORDER BY available, p.pk;