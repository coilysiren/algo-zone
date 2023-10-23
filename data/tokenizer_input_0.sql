CREATE TABLE town ();

CREATE TABLE city (
    name VARCHAR,
    population INT,
    timezone INT
);

INSERT INTO city (name, population, timezone)
VALUES ('San Francisco', 852469, -8);

INSERT INTO city (name, population)
VALUES ('New York', 8405837);

SELECT (
    name,
    population,
    timezone
)
FROM city;

SELECT name FROM city;
