from graphene import ObjectType, String, Int, Connection, relay

from .get_films import get_films


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

    @staticmethod
    def resolve_total_count(root, info, **kwargs) -> int:
        """
        :param root: Used to derive the values for most fields on an ObjectType
        :descr: Return total amount of films in the response

        :param info: Meta information about the execution of the current GraphQL Query
        :return: Total amount of films
        """
        return len(root.iterable)

    class Meta:
        node = Film

    class Edge:
        other = String()

        @staticmethod
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

    @staticmethod
    def resolve_get_films(root, info, **kwargs) -> list:
        """
        :descr: Return full list of searched films
        :param root: Used to derive the values for most fields on an ObjectType
        :param info: Meta information about the execution of the current GraphQL Query
        :return: list of searched films
        """

        film_list = get_films(
            title=kwargs.get("Title"),
            result_type=kwargs.get("Type"),
            year=kwargs.get("Year"),
        )
        return film_list
