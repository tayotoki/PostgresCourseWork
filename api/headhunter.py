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
            return Employer(**employers[0])

    def get_vacancies_by_employer(self, employer: Employer) -> list[Vacancy]:
        vacancies_url: str = employer.vacancies_url

        params = {"per_page": 100}

        vacancies: list[dict] = self.http_get(
            url=vacancies_url.replace(self.API_URI, ""),
            params=params
        ).get("items")

        vacancies_objects = [
            Vacancy(
                id=vacancy.get("id"),
                employer=Employer(**vacancy.get("employer")),
                name=vacancy.get("name"),
                area=Area(**vacancy.get("area")),
                snippet=Snippet(**vacancy.get("snippet")),
                salary=Salary(**{
                    k if k != "from" else "from_": v
                    for k, v in vacancy.get("salary").items()
                }) if vacancy.get("salary") is not None else None,
                alternate_url=vacancy.get("alternate_url"),
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
