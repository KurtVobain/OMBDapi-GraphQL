import pytest
import graphene
from graphene.test import Client

from app.schema import Query


@pytest.fixture(scope="module")
def client():
    client = Client(schema=graphene.Schema(query=Query))
    return client
