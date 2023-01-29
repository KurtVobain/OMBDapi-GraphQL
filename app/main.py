from fastapi import FastAPI
from dotenv import load_dotenv
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from .schema import Query

load_dotenv()

app = FastAPI()
schema = Schema(query=Query)

app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))
