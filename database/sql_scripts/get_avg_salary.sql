select round(avg((salary).salary_from)) avg_from,
       round(avg((salary).salary_to)) avg_to
from vacancies
where (salary).currency = 'RUR' and salary is not null;