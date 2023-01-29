import os

import requests
from dotenv import load_dotenv

from app.get_films import get_films

load_dotenv()


class TestApiRequest:
    def test_correct_amount(self):
        payload = {
            "apikey": os.getenv("OMDB_API_TOKEN"),
            "s": "mirror",
            "type": "series",
            "y": 2021,
        }

        example_result = requests.get("http://www.omdbapi.com/", params=payload)

        assert int(example_result.json()["totalResults"]) == len(
            get_films("mirror", "series", 2021)
        )

    def test_incorrect_request_parameter(self):
        payload = {
            "apikey": os.getenv("OMDB_API_TOKEN"),
            "s": "mirror",
            "type": "series",
            "y": 20212313,
        }

        example_result = requests.get("http://www.omdbapi.com/", params=payload)

        assert example_result.json().get("Error") is not None
        assert 0 == len(get_films("mirror", "series", 202120212313))
