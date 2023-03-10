import os
import requests


def get_films(
    title: str,
    result_type: str | None = None,
    year: int | None = None,
    response_page: int = 1,
) -> list:
    """
    :descr: Make a request to OMDBAPI
    :param title: Film title to search for
    :param result_type: Type of result to return. Could be movie, series or episode
    :param year: Year of release
    :param response_page: Page number to return.

    :return: List of request results
    """
    payload = {
        "apikey": os.getenv("OMDB_API_TOKEN"),
        "s": title,
        "page": response_page,
        "type": result_type,
        "y": year,
    }
    film_list = []

    try:
        result = requests.get("http://www.omdbapi.com/", params=payload, timeout=10)
    except requests.exceptions.Timeout:
        return film_list
    except requests.exceptions.ConnectionError:
        return film_list

    if result.json().get("Response") == "False":
        return film_list


    # OMDB api returns 10 results per page
    films_per_page = 10
    response_pages = int(result.json().get("totalResults")) // films_per_page + 1

    # Get full number of searched films in one list
    film_list = result.json().get("Search")
    for page in range(response_page + 1, response_pages + 1):
        payload["page"] = page
        result = requests.get("http://www.omdbapi.com/", params=payload, timeout=10)
        if result.json().get("Response") == "True":
            film_list += result.json().get("Search")

    return film_list
