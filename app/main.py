import os

import requests
from fastapi import FastAPI
from dotenv import load_dotenv
from graphene import ObjectType, String, Int, Connection, Schema, relay
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

load_dotenv()


def get_films(
    title: str, result_type: str = None, year: int = None, response_page: int = 1
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
    result = requests.get("http://www.omdbapi.com/", params=payload)

    if result.json().get("Response") == "False":
        film_list = []

    else:
        # OMDB api returns 10 results per page
        films_per_page = 10
        response_pages = int(result.json().get("totalResults")) // films_per_page + 1

        # Get full number of searched films in one list
        film_list = result.json().get("Search")
        for page in range(response_page, response_pages + 1):
            payload["page"] = page
            result = requests.get("http://www.omdbapi.com/", params=payload)

            film_list += result.json().get("Search")

    return film_list


class Film(ObjectType):
    """Represents film structure from OMBD API"""

    Title = String()
    Year = String()
    imdbID = String()
    Type = String()
    Poster = String()

    class Meta:
        interfaces = (relay.Node,)


class FilmConnection(Connection):
    total_count = Int()

    def resolve_total_count(root, info, **kwargs) -> int:
        """
        :descr: Return total amount of films in the response
        :param info: Meta information about the execution of the current GraphQL Query
        :return: Total amount of films
        """
        return len(root.iterable)

    class Meta:
        node = Film

    class Edge:
        other = String()

        def resolve_other(instance, info):
            return "This is other: " + instance.node.other


class Query(ObjectType):
    # Root field due Relay specification
    node = relay.Node.Field()

    film_list = None
    get_films = relay.ConnectionField(
        FilmConnection, title=String(), type=String(), year=Int()
    )

    def resolve_get_films(self, info, **kwargs) -> list:
        """
        :descr: Return full list of searched films
        :param info: Meta information about the execution of the current GraphQL Query
        :return: list of searched films
        """

        film_list = get_films(
            title=kwargs.get("title"),
            result_type=kwargs.get("type"),
            year=kwargs.get("year"),
        )
        return film_list


app = FastAPI()
schema = Schema(query=Query)

app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))
