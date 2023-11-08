DO
$$
BEGIN
  IF NOT EXISTS (SELECT *
                        FROM pg_type typ
                             INNER JOIN pg_namespace nsp
                                        ON nsp.oid = typ.typnamespace
                        WHERE nsp.nspname = current_schema()
                              AND typ.typname IN ('currency', 'salary_type')) THEN
    CREATE TYPE currency
                AS ENUM ('RUR',
                         'USD',
                         'BYR',
                         'EUR',
                         'KZT',
                         'UZS');

    CREATE TYPE salary_type
                AS (salary_from INT,
                    salary_to INT,
                    currency CURRENCY,
                    gross BOOLEAN);
  END IF;
END;
$$;


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
    alternate_url VARCHAR,
    area VARCHAR,
    description TEXT,
    responsibility TEXT,
    salary salary_type,
    published_at TIMESTAMP,

    PRIMARY KEY (vacancy_id)
);