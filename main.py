from config import ConfigD
from exeptions import IncorrectSeedURLError, IncorrectHeadersError, \
    IncorrectEncodingError, IncorrectTimeoutError, IncorrectVerifyError
from get_cities import get_cities

import sqlite3
from bs4 import BeautifulSoup
import json
from pathlib import Path
import re
import time
import requests
import random

conn = sqlite3.connect("vacancies_final.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Vacancies
(ORGANIZATION, VACANCY_NAME, GENERAL_NAME, EXPERIENCE, REQUIREMENTS, CITY, WORK_SCHEDULE)""")


class Config:
    """
    Unpacks and validates configurations
    """

    def __init__(self, path_to_config: Path) -> None:
        """
        Initializes an instance of the Config class
        """
        self.path_to_config = path_to_config
        self._validate_config_content()
        config = self._extract_config_content()
        self._seed_urls = config.seed_urls
        self._headers = config.headers
        self._encoding = config.encoding
        self._timeout = config.timeout
        self._should_verify_certificate = config.should_verify_certificate
        self._headless_mode = config.headless_mode

    def _extract_config_content(self) -> ConfigD:
        """
        Returns config values
        """
        with open(self.path_to_config, "r", encoding="utf-8") as f:
            config = json.load(f)
        return ConfigD(**config)

    def _validate_config_content(self) -> None:
        """
        Ensure configuration parameters are not corrupt
        """
        config = self._extract_config_content()

        if not isinstance(config.seed_urls, list):
            raise IncorrectSeedURLError("seed URL is not a list")

        for url in config.seed_urls:
            if not re.match(r"^https?://.*", url):
                raise IncorrectSeedURLError

        if not isinstance(config.headers, dict):
            raise IncorrectHeadersError

        if not isinstance(config.encoding, str):
            raise IncorrectEncodingError

        if not isinstance(config.timeout, int) or \
                not 0 <= config.timeout <= 60:
            raise IncorrectTimeoutError

        if not isinstance(config.should_verify_certificate, bool):
            raise IncorrectVerifyError

        if not isinstance(config.headless_mode, bool):
            raise IncorrectVerifyError()

    def get_seed_urls(self) -> list[str]:
        """
        Retrieve seed urls
        """
        return self._seed_urls

    def get_headers(self) -> dict[str, str]:
        """
        Retrieve headers to use during requesting
        """
        return self._headers

    def get_encoding(self) -> str:
        """
        Retrieve encoding to use during parsing
        """
        return self._encoding

    def get_timeout(self) -> int:
        """
        Retrieve number of seconds to wait for response
        """
        return self._timeout

    def get_verify_certificate(self) -> bool:
        """
        Retrieve whether to verify certificate
        """
        return self._should_verify_certificate

    def get_headless_mode(self) -> bool:
        """
        Retrieve whether to use headless mode
        """
        return self._headless_mode


def make_request(url: str, config: Config) -> requests.models.Response:
    """
    Delivers a response from a request
    with given configuration
    """
    time.sleep(random.randint(1, 10))
    timeout = config.get_timeout()
    headers = config.get_headers()

    response = requests.get(url, timeout=timeout, headers=headers)
    response.encoding = config.get_encoding()
    return response


class HTMLParser:
    """
    ArticleParser implementation
    """

    def __init__(self, url: str, config: Config) -> None:
        """
        Initializes an instance of the HTMLParser class
        """
        self._seed_url = config.get_seed_urls()
        self.url = url
        self.config = config
        self.names_cities = get_cities()
        self.org_names = []
        self.vacancy_names = []
        self.general_name = []
        self.experience_name = []
        self.requirements = []
        self.cities = []
        self.work_schedule = []

    def _get_company_name(self, article_soup: BeautifulSoup) -> None:
        """
        Finds company name
        """
        company_names = article_soup.find_all("div", {"class": "vacancy-card__company-title"})
        self.org_names.extend([name.text for name in company_names])
        # print(self.org_names)

    def _get_vacancy_name(self, article_soup: BeautifulSoup) -> None:
        """
        Finds vacancy name
        """
        vacancy = article_soup.find_all("div", {"class": "vacancy-card__title"})
        self.vacancy_names.extend([name.text for name in vacancy])

    def _get_city_and_work_schedule(self, article_soup: BeautifulSoup) -> None:
        """
        Finds city name and work schedule
        """
        self.meta = article_soup.find_all("div", {"class": "vacancy-card__meta"})
        for elem in self.meta:
            cities = []
            extra = []
            info = elem.text.split(" • ")
            for piece in info:
                if piece in self.names_cities:
                    cities.append(piece)
                else:
                    extra.append(piece)
            self.cities.append(", ".join(cities) if cities else "no info")
            self.work_schedule.append(", ".join(extra) if extra else "no info")

    def _get_requirements_general_name_experience(self, article_soup: BeautifulSoup) -> None:
        """
        Finds requirements, general name and experience
        """
        requirements = article_soup.find_all("div", {"class": "vacancy-card__skills"})
        for elem in requirements:
            information = elem.text.split("•")
            self.requirements.append(", ".join(information[1:]))

            self.general_name.append(information[0].split(", ")[0])
            self.experience_name.append(information[0].split(", ")[1] if len(information[0].split(", ")) > 1
                                        else "no info")

    def parse(self) -> None:
        """
        Parses each page
        """
        response = make_request(self.url, self.config)
        info = BeautifulSoup(response.text, "lxml")
        self._get_company_name(info)
        self._get_vacancy_name(info)
        self._get_city_and_work_schedule(info)
        self._get_requirements_general_name_experience(info)

    def append_database(self) -> None:
        """
        Appends db
        """
        for elem in range(len(self.org_names)):
            cur.execute("INSERT INTO Vacancies VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (self.org_names[elem], self.vacancy_names[elem], self.general_name[elem],
                         self.experience_name[elem], self.requirements[elem], self.cities[elem],
                         self.work_schedule[elem]))
            conn.commit()


def main() -> None:
    """
    Entrypoint for scrapper module
    """
    config = Config(path_to_config=Path(__file__).parent.parent / "pythonProject1" / "data.json")
    for url in config.get_seed_urls():
        parser = HTMLParser(url=url, config=config)
        parser.parse()
        parser.append_database()

    conn.close()


if __name__ == "__main__":
    main()
