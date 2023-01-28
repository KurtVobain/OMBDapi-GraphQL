import os

import requests
from fastapi import FastAPI
from dotenv import load_dotenv
from graphene import ObjectType, String, Int, Connection, Schema, relay
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

load_dotenv()


def get_films(
    title: str, result_type: str = None, year: int = None, response_page: int = 1
) -> list[dict]:
    """
    :descr: Make a request to OMDBAPI
    :param title: Film title to search for
    :param result_type: Type of result to return. Could be movie, series or episode
    :param year: Year of release
    :param response_page: Page number to return.

    :return: List of request results and amount of elements in the list
    """
    payload = {
        "apikey": os.getenv("OMDB_API_TOKEN"),
        "s": title,
        "page": response_page,
        "type": result_type,
        "y": year,
    }
    result = requests.get("http://www.omdbapi.com/", params=payload)
    # TODO:
    # Error Handler
    response_pages = int(result.json().get("totalResults")) // 10 + 1

    film_list = result.json().get("Search")
    # status = dict()
    if response_pages > 1:
        for page in range(response_page, response_pages + 1):
            payload["page"] = page
            result = requests.get("http://www.omdbapi.com/", params=payload)

            # status[page] = result.status_code
            film_list += result.json().get("Search")

    return film_list  # , status


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

    def resolve_total_count(root, info, **kwargs):
        return len(root.iterable)

    class Meta:
        node = Film

    class Edge:
        other = String()

        def resolve_other(instance, info):
            print(instance)
            print(info)
            return "This is other: " + instance.node.other


class Query(ObjectType):
    # Root field due Relay specification
    node = relay.Node.Field()

    film_list = None
    get_films = relay.ConnectionField(
        FilmConnection, Title=String(), Type=String(), Year=Int()
    )

    def resolve_get_films(self, info, **kwargs):

        film_list = get_films(
            title=kwargs.get("Title"),
            result_type=kwargs.get("Type"),
            year=kwargs.get("Year"),
        )
        return film_list


app = FastAPI()
schema = Schema(query=Query)

app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))
