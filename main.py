import os
import json

import requests
from fastapi import FastAPI
from dotenv import load_dotenv
from graphene import ObjectType, List, String, Field, JSONString, Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

load_dotenv()


class Film(ObjectType):
    Title = String(required=True)
    Year = String()
    imdbID = String()
    Type = String()
    Poster = String()


class FilmResult(ObjectType):
    Search = List(Film)
    totalResults = String()


class Query(ObjectType):
    film_list = None
    get_films = Field(FilmResult, Title=String()) #List(Film)

    def resolve_get_films(self, info, Title):
        payload = {'apikey': os.getenv('OMDB_API_TOKEN'), 's': Title}
        result = requests.get('http://www.omdbapi.com/', params=payload)
        film_list = result.json()#['Search']

        return film_list


app = FastAPI()
schema = Schema(query=Query)

app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))
