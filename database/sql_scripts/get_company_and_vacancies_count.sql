select v.name vacancy, e.name company, salary, alternate_url link
from vacancies v join employers e using (employer_id);