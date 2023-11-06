DROP TYPE SALARY, CURRENCY CASCADE;

CREATE TYPE CURRENCY AS ENUM (
    'RUR',
    'USD',
    'BYR',
    'EUR',
    'KZT'
);

CREATE TYPE SALARY AS (
    salary_from INT,
    salary_to INT,
    currency CURRENCY,
    gross BOOLEAN
);

CREATE TABLE IF NOT EXISTS employers (
    employer_id VARCHAR
                CONSTRAINT numeric_id CHECK ( employer_id ~ '^\d+$' ),
    name VARCHAR NOT NULL,
    description TEXT,
    vacancies_url TEXT,

    PRIMARY KEY (employer_id)
);

CREATE TABLE IF NOT EXISTS vacancies (
    vacancy_id VARCHAR
               CONSTRAINT id_check CHECK ( vacancy_id ~ '^\d+$' ),
    employer_id VARCHAR REFERENCES employers (employer_id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
    name VARCHAR NOT NULL,
    area VARCHAR,
    description TEXT,
    responsibility TEXT,
    salary SALARY,
    published_at DATE,

    PRIMARY KEY (vacancy_id)
);