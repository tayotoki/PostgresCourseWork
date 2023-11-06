import json
from typing import Any

import requests
from requests import HTTPError

from DTO.dto import (
    Snippet,
    Area,
    Salary,
    Employer,
    Vacancy
)


class HeadHunterAPI:
    API_URI = "https://api.hh.ru"

    def get_employer(self, search_text: str) -> Employer:
        params = {
            "only_with_vacancies": True,
            "per_page": 1,
            "text": search_text,
        }

        employers: list[dict] = self.http_get(
            url="/employers",
            params=params
        ).get("items")

        if employers:
            print(employers[0])
            return Employer(**employers[0])

    def get_vacancies_by_employer(self, employer: Employer) -> list[Vacancy]:
        vacancies_url: str = employer.vacancies_url

        if vacancies_url:
            vacancies_url = vacancies_url.split("/")[-1]  # .../vacancies?employer_id=*

        params = {"per_page": 100}

        vacancies: list[dict] = self.http_get(
            url=vacancies_url,
            params=params
        ).get("items")

        vacancies_objects = [
            Vacancy(
                id=vacancy.get("id"),
                employer=vacancy.get("employer"),
                name=vacancy.get("name"),
                area=Area(**vacancy.get("area")),
                snippet=Snippet(**vacancy.get("snippet")),
                salary=Salary(**vacancy.get("salary")),
                published_at=vacancy.get("published_at")
            ) for vacancy in vacancies
        ]

        return vacancies_objects

    def http_get(self,
                 url: str,
                 headers: dict[str, Any] | None = None,
                 params: dict[str, Any] | None = None) -> dict[str | dict, Any]:

        with requests.Session() as session:
            response: requests.Response = session.get(
                url=self.API_URI + url,
                headers=headers,
                params=params
            )

            if response.status_code == 200:
                data = response.json()

                return data

            raise HTTPError(f"Ошибка во время запроса на {self.API_URI + url}")
