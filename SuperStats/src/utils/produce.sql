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
    farmer_pk int not null REFERENCES Farmers(pk) ON DELETE CASCADE,
    produce_pk int not null REFERENCES Produce(pk) ON DELETE CASCADE,
    available boolean default true,
    PRIMARY KEY (farmer_pk, produce_pk)
);

CREATE INDEX IF NOT EXISTS sell_index
ON Sell (farmer_pk, available);

DELETE FROM Sell;

DROP TABLE IF EXISTS ProduceOrder;

CREATE TABLE IF NOT EXISTS ProduceOrder(
    pk serial not null PRIMARY KEY,
    customer_pk int not null REFERENCES Customers(pk) ON DELETE CASCADE,
    farmer_pk int not null REFERENCES Farmers(pk) ON DELETE CASCADE,
    produce_pk int not null REFERENCES Produce(pk) ON DELETE CASCADE,
    created_at timestamp not null default current_timestamp
);

DELETE FROM ProduceOrder;

CREATE OR REPLACE VIEW vw_produce
AS
SELECT p.category, p.item, p.variety,
       p.unit, p.price, s.available,
       p.pk as produce_pk,
       f.full_name as farmer_name,
       f.pk as farmer_pk
FROM Produce p
JOIN Sell s ON s.produce_pk = p.pk
JOIN Farmers f ON s.farmer_pk = f.pk
ORDER BY available, p.pk;