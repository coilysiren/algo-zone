-- https://cratedb.com/docs/sql-99/en/latest/chapters/01.html
-- https://www.postgresql.org/docs/16/sql-createtable.html
-- https://www.postgresql.org/docs/16/sql-insert.html
-- https://www.postgresql.org/docs/16/sql-select.html
CREATE TABLE city (
    name VARCHAR,
    population INT,
    timezone INT
);

INSERT INTO city (name, population, timezone)
VALUES ('San Francisco', 852469, -8);

INSERT INTO city (name, population, timezone)
VALUES ('New York', 8405837, -5);

SELECT
    name,
    population,
    timezone
FROM city;
