from datetime import datetime

from dateutil import parser
from enum import Enum


class Currency(Enum):
    RUR = "RUR"
    USD = "USD"
    BYR = "BYR"
    EUR = "EUR"
    KZT = "KZT"


class Snippet:
    def __init__(self,
                 description: str,
                 responsibility: str,
                 *args,
                 **kwargs):
        self.description = description
        self.responsibility = responsibility


class Area:
    def __init__(self,
                 id: str,
                 name: str,
                 url: str):
        self.id = id
        self.name = name
        self.url = url


class Salary:
    def __init__(self,
                 salary_from: int,
                 salary_to: int | None,
                 currency: Currency,
                 gross: bool,
                 *args,
                 **kwargs):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.gross = gross


class Employer:
    def __init__(self,
                 id: str,
                 name: str,
                 vacancies_url: str,
                 description: str | None = None,
                 *args,
                 **kwargs):
        self.id = id
        self.name = name
        self.description = description
        self.vacancies_url = vacancies_url


class Vacancy:
    def __init__(self,
                 id: str,
                 employer: Employer,
                 name: str,
                 area: Area,
                 snippet: Snippet,
                 salary: Salary,
                 published_at: str):
        self.id: str = id
        self.employer: str = employer.id
        self.name: str = name
        self.area: str = area.name
        self.description: str = snippet.description
        self.responsibility: str = snippet.responsibility
        self.salary: Salary = salary
        self.published_at: datetime = parser.parse(published_at)
