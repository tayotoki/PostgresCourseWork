from datetime import datetime

from dateutil import parser
from enum import Enum


class Currency(Enum):
    RUR = "RUR"
    USD = "USD"
    BYR = "BYR"
    EUR = "EUR"
    KZT = "KZT"
    UZS = "UZS"


class Snippet:
    def __init__(self,
                 requirement: str,
                 responsibility: str,
                 *args,
                 **kwargs):
        self.description = requirement
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
                 from_: int | None,
                 to: int | None,
                 currency: Currency,
                 gross: bool,
                 *args,
                 **kwargs):
        self.salary_from = from_
        self.salary_to = to
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
                 salary: Salary | None,
                 alternate_url: str,
                 published_at: str):
        self.id: str = id
        self.employer_id: str = employer.id
        self.name: str = name
        self.area: str = area.name
        self.description: str = snippet.description
        self.responsibility: str = snippet.responsibility
        self.salary: Salary | None = salary
        self.alternate_url = alternate_url
        self.published_at: datetime = parser.parse(published_at)
