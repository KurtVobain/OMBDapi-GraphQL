import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from app import schema

load_dotenv()

app = FastAPI()
schema = Schema(query=schema.Query)

app.add_route("/", GraphQLApp(schema, on_get=make_graphiql_handler()))


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
