CREATE TABLE IF NOT EXISTS RespondentsData (
    id SERIAL PRIMARY KEY,
    Date DATE,
    respondent INTEGER,
    Sex SMALLINT,
    Age INTEGER,
    Weight NUMERIC
);

COPY RespondentsData(id, Date, respondent, Sex, Age, Weight)
FROM '/docker-entrypoint-initdb.d/data_1.csv'
DELIMITER ';'
CSV HEADER;
