from graphene import ObjectType, String, Int, Connection, relay

from app import get_films


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
    def resolve_total_count(root, _, **kwargs) -> int:
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
        def resolve_other(instance, _):
            return "This is other: " + instance.node.get("other", "Nothings")


class Query(ObjectType):
    get_films = relay.ConnectionField(
        FilmConnection, Title=String(), Type=String(), Year=Int()
    )

    @staticmethod
    def resolve_get_films(_, __, **kwargs) -> list:
        """
        :descr: Return full list of searched films
        :param root: Used to derive the values for most fields on an ObjectType
        :param info: Meta information about the execution of the current GraphQL Query
        :return: list of searched films
        """

        film_list = get_films.get_films(
            title=kwargs.get("Title"),
            result_type=kwargs.get("Type"),
            year=kwargs.get("Year"),
        )
        return film_list
