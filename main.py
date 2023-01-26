import os
import json

import requests
from fastapi import FastAPI
from dotenv import load_dotenv
from graphene import (
    ObjectType, List, String, Int, Connection, Schema, relay
)
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

load_dotenv()


def get_films(title: str) -> list[dict] and int:
    """
    :descr: Make a request to OMDBAPI
    :param title: Film title to search for

    :return: List of request results and amount of elements in the list
    """
    payload = {'apikey': os.getenv('OMDB_API_TOKEN'), 's': title}
    result = requests.get('http://www.omdbapi.com/', params=payload)
    film_list = result.json().get('Search')

    return film_list


class Film(ObjectType):
    """Represents film structure from OMBD API """
    class Meta:
        interfaces = (relay.Node, )

    Title = String()
    Year = String()
    imdbID = String()
    Type = String()
    Poster = String()


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
    get_films = relay.ConnectionField(FilmConnection, Title=String())

    def resolve_get_films(self, info, **kwargs):
        film_list = get_films(kwargs.get('Title'))
        return film_list


app = FastAPI()
schema = Schema(query=Query)

app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))
