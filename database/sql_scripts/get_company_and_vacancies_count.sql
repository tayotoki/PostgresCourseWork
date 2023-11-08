select e.name company, count(v.*) vacancy_count
from vacancies v join employers e using (employer_id)
group by e.name;