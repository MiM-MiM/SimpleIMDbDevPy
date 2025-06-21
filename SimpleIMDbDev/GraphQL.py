__all__ = ["getMovie", "getPerson"]

import requests
from functools import lru_cache

from SimpleIMDbDev.constants import BASE_HEADERS

"""This is a work in progress GraohQL implementation provided by data from https://imdbapi.dev/docs/graphql/quickstart
It does not currently work with TV episodes.
Can fetch movie by ID and person by ID.
"""

API_ENDPOINT = "https://graph.imdbapi.dev/v1"
REQUIRED = True
MAIN_ATTRIBUTE = True


class IMDbGraphQL:
    """Base class for IMDb GraphQL objects.
    Any tuple types must have the first one iterable.
    https://imdbapi.dev/docs/graphql/quickstart

    SCHEMA = {
        "name": (type, Required, MainAttribute)
    }
    Type can be a tuple, type, or string.
    Tuple indicates a list, contains list and type.
    If the type is a string it references an internal type found in `IMDbGraphQLTypes`.
    """

    class Title:
        """Represents a title in the IMDb GraphQL schema."""

        SCHEMA = {
            "id": (str, REQUIRED, MAIN_ATTRIBUTE),
            "type": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "is_adult": (bool, not REQUIRED, not MAIN_ATTRIBUTE),
            "primary_title": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "original_title": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "start_year": (int, not REQUIRED, MAIN_ATTRIBUTE),
            "end_year": (int, not REQUIRED, not MAIN_ATTRIBUTE),
            "runtime_minutes": (int, not REQUIRED, MAIN_ATTRIBUTE),
            "plot": (str, not REQUIRED, not MAIN_ATTRIBUTE),
            "rating": ("IMDbGraphQL.Rating", not REQUIRED, not MAIN_ATTRIBUTE),
            "certificates": ((list, "IMDbGraphQL.Certificate"), not REQUIRED, MAIN_ATTRIBUTE),
            "critic_review": ("IMDbGraphQL.CriticReview", not REQUIRED, MAIN_ATTRIBUTE),
            "genres": ((list, str), not REQUIRED, MAIN_ATTRIBUTE),
            "spoken_languages": ((list, "IMDbGraphQL.Language"), not REQUIRED, MAIN_ATTRIBUTE),
            "origin_countries": ((list, "IMDbGraphQL.Country"), not REQUIRED, MAIN_ATTRIBUTE),
            "posters": ((list, "IMDbGraphQL.Poster"), not REQUIRED, MAIN_ATTRIBUTE),
            # Credits must be false for main to avoid circular query generation
            "credits": ((list, "IMDbGraphQL.Credit"), not REQUIRED, not MAIN_ATTRIBUTE), # fmt: skip
        }

        __name__ = "IMDbGraphQL.Title"

        def __init__(self, **kwargs: dict):
            id = kwargs.get("id", "")
            if isinstance(id, int):
                id = "tt" + str(id).ljust(7, "0")
            kwargs["id"] = id  # type: ignore
            check_kwargs(self, self.SCHEMA, kwargs)
            self.__dict__ = todict(self)  # type: ignore

        def as_dict(self) -> dict:
            return self.__dict__

        def get(self, key):
            return self.__getitem__(key)

        def __getitem__(self, key):
            if key not in self.SCHEMA:
                return None
            try:
                return self.__dict__[key]
            except AttributeError:
                return None

        def __setitem__(self, key, value):
            check_kwargs(self, self.SCHEMA, dict(key=value), ignore_required=True)
            self.__dict__[key] = value

    class Name:
        """Represents a name in the IMDb GraphQL schema."""

        SCHEMA = {
            "id": (str, REQUIRED, MAIN_ATTRIBUTE),
            "display_name": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "alternate_names": ((list, str), not REQUIRED, MAIN_ATTRIBUTE),
            "birth_year": (int, not REQUIRED, MAIN_ATTRIBUTE),
            "birth_location": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "death_year": (int, not REQUIRED, MAIN_ATTRIBUTE),
            "death_location": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "dead_reason": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "avatars": ((list, "IMDbGraphQL.Avatar", True), not REQUIRED, MAIN_ATTRIBUTE),
            # Known for is not the main to avoid slow queries.
            "known_for": ((list, "IMDbGraphQL.Title", True), not REQUIRED, not MAIN_ATTRIBUTE), # fmt: skip
        }

        __name__ = "IMDbGraphQL.Name"

        def __init__(self, **kwargs: dict):
            id = kwargs.get("id", "")
            if isinstance(id, int):
                id = "nm" + str(id).ljust(7, "0")
            kwargs["id"] = id  # type: ignore
            check_kwargs(self, self.SCHEMA, kwargs)
            self.__dict__ = todict(self)  # type: ignore

        def as_dict(self) -> dict:
            return self.__dict__

        def get(self, key):
            return self.__getitem__(key)

        def __getitem__(self, key):
            if key not in self.SCHEMA:
                return None
            try:
                return self.__dict__[key]
            except AttributeError:
                return None

        def __setitem__(self, key, value):
            check_kwargs(self, self.SCHEMA, dict(key=value), ignore_required=True)
            self.__dict__[key] = value

    class Rating:
        """Represents a rating in the IMDb GraphQL schema."""

        SCHEMA = {
            "aggregate_rating": (float, not REQUIRED, MAIN_ATTRIBUTE),
            "votes_count": (int, not REQUIRED, MAIN_ATTRIBUTE),
        }

        __name__ = "IMDbGraphQL.Rating"

        def __init__(self, **kwargs: dict):
            check_kwargs(self, self.SCHEMA, kwargs)
            self.__dict__ = todict(self)  # type: ignore

        def as_dict(self) -> dict:
            return self.__dict__

        def get(self, key):
            return self.__getitem__(key)

        def __getitem__(self, key):
            if key not in self.SCHEMA:
                return None
            try:
                return self.__dict__[key]
            except AttributeError:
                return None

        def __setitem__(self, key, value):
            check_kwargs(self, self.SCHEMA, dict(key=value), ignore_required=True)
            self.__dict__[key] = value

    class Certificate:
        """Represents a certificate in the IMDb GraphQL schema."""

        SCHEMA = {
            "country": ("IMDbGraphQL.Country", not REQUIRED, MAIN_ATTRIBUTE),
            "rating": (str, not REQUIRED, MAIN_ATTRIBUTE),
        }

        __name__ = "IMDbGraphQL.Certificate"

        def __init__(self, **kwargs: dict):
            check_kwargs(self, self.SCHEMA, kwargs)
            self.__dict__ = todict(self)  # type: ignore

        def as_dict(self) -> dict:
            return self.__dict__

        def get(self, key):
            return self.__getitem__(key)

        def __getitem__(self, key):
            if key not in self.SCHEMA:
                return None
            try:
                return self.__dict__[key]
            except AttributeError:
                return None

        def __setitem__(self, key, value):
            check_kwargs(self, self.SCHEMA, dict(key=value), ignore_required=True)
            self.__dict__[key] = value

    class Language:
        """Represents a language in the IMDb GraphQL schema."""

        SCHEMA = {
            "code": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "name": (str, not REQUIRED, MAIN_ATTRIBUTE),
        }

        __name__ = "IMDbGraphQL.Language"

        def __init__(self, **kwargs: dict):
            check_kwargs(self, self.SCHEMA, kwargs)
            self.__dict__ = todict(self)  # type: ignore

        def as_dict(self) -> dict:
            return self.__dict__

        def get(self, key):
            return self.__getitem__(key)

        def __getitem__(self, key):
            if key not in self.SCHEMA:
                return None
            try:
                return self.__dict__[key]
            except AttributeError:
                return None

        def __setitem__(self, key, value):
            check_kwargs(self, self.SCHEMA, dict(key=value), ignore_required=True)
            self.__dict__[key] = value

    class Country:
        """Represents a country in the IMDb GraphQL schema."""

        SCHEMA = {
            "code": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "name": (str, not REQUIRED, MAIN_ATTRIBUTE),
        }

        __name__ = "IMDbGraphQL.Country"

        def __init__(self, **kwargs: dict):
            check_kwargs(self, self.SCHEMA, kwargs)
            self.__dict__ = todict(self)  # type: ignore

        def as_dict(self) -> dict:
            return self.__dict__

        def get(self, key):
            return self.__getitem__(key)

        def __getitem__(self, key):
            if key not in self.SCHEMA:
                return None
            try:
                return self.__dict__[key]
            except AttributeError:
                return None

        def __setitem__(self, key, value):
            check_kwargs(self, self.SCHEMA, dict(key=value), ignore_required=True)
            self.__dict__[key] = value

    class CriticReview:
        """Represents a critic review in the IMDb GraphQL schema."""

        SCHEMA = {
            "score": (int, not REQUIRED, MAIN_ATTRIBUTE),
            "review_count": (int, not REQUIRED, MAIN_ATTRIBUTE),
        }

        __name__ = "IMDbGraphQL.CriticReview"

        def __init__(self, **kwargs: dict):
            check_kwargs(self, self.SCHEMA, kwargs)
            self.__dict__ = todict(self)  # type: ignore

        def as_dict(self) -> dict:
            return self.__dict__

        def get(self, key):
            return self.__getitem__(key)

        def __getitem__(self, key):
            if key not in self.SCHEMA:
                return None
            try:
                return self.__dict__[key]
            except AttributeError:
                return None

        def __setitem__(self, key, value):
            check_kwargs(self, self.SCHEMA, dict(key=value), ignore_required=True)
            self.__dict__[key] = value

    class Credit:
        """Represents a credit in the IMDb GraphQL schema."""

        SCHEMA = {
            "name": ("IMDbGraphQL.Name", not REQUIRED, MAIN_ATTRIBUTE),
            "category": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "characters": ((list, str), not REQUIRED, MAIN_ATTRIBUTE),
            "episodes_count": (int, not REQUIRED, MAIN_ATTRIBUTE),
        }

        __name__ = "IMDbGraphQL.Credit"

        def __init__(self, **kwargs: dict):
            check_kwargs(self, self.SCHEMA, kwargs)
            self.__dict__ = todict(self)  # type: ignore

        def as_dict(self) -> dict:
            return self.__dict__

        def get(self, key):
            return self.__getitem__(key)

        def __getitem__(self, key):
            if key not in self.SCHEMA:
                return None
            try:
                return self.__dict__[key]
            except AttributeError:
                return None

        def __setitem__(self, key, value):
            check_kwargs(self, self.SCHEMA, dict(key=value), ignore_required=True)
            self.__dict__[key] = value

    class Poster:
        """Represents a poster in the IMDb GraphQL schema."""

        SCHEMA = {
            "url": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "width": (int, not REQUIRED, MAIN_ATTRIBUTE),
            "height": (int, not REQUIRED, MAIN_ATTRIBUTE),
            "language_code": (str, not REQUIRED, MAIN_ATTRIBUTE),
        }

        __name__ = "IMDbGraphQL.Poster"

        def __init__(self, **kwargs: dict):
            check_kwargs(self, self.SCHEMA, kwargs)
            self.__dict__ = todict(self)  # type: ignore

        def as_dict(self) -> dict:
            return self.__dict__

        def get(self, key):
            return self.__getitem__(key)

        def __getitem__(self, key):
            if key not in self.SCHEMA:
                return None
            try:
                return self.__dict__[key]
            except AttributeError:
                return None

        def __setitem__(self, key, value):
            check_kwargs(self, self.SCHEMA, dict(key=value), ignore_required=True)
            self.__dict__[key] = value

    class Avatar:
        """Represents an avatar in the IMDb GraphQL schema."""

        SCHEMA = {
            "url": (str, not REQUIRED, MAIN_ATTRIBUTE),
            "width": (int, not REQUIRED, MAIN_ATTRIBUTE),
            "height": (int, not REQUIRED, MAIN_ATTRIBUTE),
        }

        __name__ = "IMDbGraphQL.Avatar"

        def __init__(self, **kwargs: dict):
            check_kwargs(self, self.SCHEMA, kwargs)
            self.__dict__ = todict(self)  # type: ignore

        def as_dict(self) -> dict:
            return self.__dict__

        def get(self, key):
            return self.__getitem__(key)

        def __getitem__(self, key):
            if key not in self.SCHEMA:
                return None
            try:
                return self.__dict__[key]
            except AttributeError:
                return None

        def __setitem__(self, key, value):
            check_kwargs(self, self.SCHEMA, dict(key=value), ignore_required=True)
            self.__dict__[key] = value


IMDbGraphQLTypes = {
    "IMDbGraphQL.Title": IMDbGraphQL.Title,
    "IMDbGraphQL.Name": IMDbGraphQL.Name,
    "IMDbGraphQL.Rating": IMDbGraphQL.Rating,
    "IMDbGraphQL.Certificate": IMDbGraphQL.Certificate,
    "IMDbGraphQL.Language": IMDbGraphQL.Language,
    "IMDbGraphQL.Country": IMDbGraphQL.Country,
    "IMDbGraphQL.CriticReview": IMDbGraphQL.CriticReview,
    "IMDbGraphQL.Credit": IMDbGraphQL.Credit,
    "IMDbGraphQL.Poster": IMDbGraphQL.Poster,
    "IMDbGraphQL.Avatar": IMDbGraphQL.Avatar,
}


def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for k, v in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict(
            [
                (key, todict(value, classkey))
                for key, value in obj.__dict__.items()
                if not callable(value) and not key.startswith("_")
            ]
        )
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


def check_kwargs(
    obj: object, schema: dict, kwargs: dict, ignore_required: bool = False
):
    for key in kwargs:
        if key not in schema:
            raise AttributeError(f"{key} is not a valid attribute for {obj.__name__}")  # type: ignore
    for field, (field_type, required, main) in schema.items():
        if required and field not in kwargs and not ignore_required:
            raise ValueError(f"Missing required field: {field}")
        value = kwargs.get(field)
        if value is None:
            continue
        if isinstance(field_type, str):
            field_type = IMDbGraphQLTypes.get(field_type)
            if not field_type:
                raise TypeError(
                    f"Field '{field}' was given an invalid type, {field_type}."
                )
            setattr(obj, field, field_type(**value))
            continue
        if not isinstance(value, field_type):
            raise TypeError(f"Field '{field}' must be of type {field_type.__name__}.")
        if isinstance(field_type, tuple):
            if not hasattr(value, "__iter__"):
                raise TypeError(f"Field '{field}' must be itterable.")
            list_type = field_type[1]
            if isinstance(list_type, str) and isinstance(value, list):
                setattr(obj, field, [IMDbGraphQLTypes[list_type](**v) for v in value])
            elif isinstance(list_type, str):
                setattr(obj, field, IMDbGraphQLTypes[list_type](**value))
            elif value and any(not isinstance(v, list_type) for v in value):
                raise TypeError(
                    f"Field '{field}' must be of type {field_type[1].__name__}."
                )
        setattr(obj, field, value)


def get_attribute_main_query(schema: dict, all: bool = True) -> str:
    query = ""
    for field_name in schema:
        field_type, required, main = schema[field_name]
        if not (all or main):
            continue
        if isinstance(field_type, tuple) and not IMDbGraphQLTypes.get(field_type[1]):
            query = f"{query}\n{field_name}"
        elif isinstance(field_type, tuple) and IMDbGraphQLTypes.get(field_type[1]):
            field_schema = IMDbGraphQLTypes.get(field_type[1]).SCHEMA  # type: ignore
            query = f"{query}\n{field_name} {{{get_attribute_main_query(field_schema, False)}\n}}\n"
        elif isinstance(field_type, str):
            field_schema = IMDbGraphQLTypes.get(field_type).SCHEMA  # type: ignore
            query = f"{query}\n{field_name} {{{get_attribute_main_query(field_schema, False)}\n}}\n"
        else:
            query = f"{query}\n{field_name}"
    return query


@lru_cache(maxsize=None)
def getMovie(id: int | str = "") -> IMDbGraphQL.Title:
    # Does not work with TV Episodes
    if not id:
        raise ValueError("A valid ID must be provided.")
    if not isinstance(id, str) and not isinstance(id, int):
        raise TypeError(f"ID must be of type str or int, {type(id)} given.")
    if not str(id).replace("tt", "").isnumeric():
        raise ValueError(
            f"The format of the ID is incorrect, should be tt### or ####. Given: {id}"
        )
    query_id = "tt" + str(id).replace("tt", "").ljust(7, "0")
    attributes = get_attribute_main_query(IMDbGraphQL.Title.SCHEMA)
    query = """query titleById
    {{
        title(id: "{query_id}") {{
            {attributes}
        }}
    }}
    """.format(
        query_id=query_id, attributes=attributes
    )
    response = requests.post(API_ENDPOINT, json={"query": query}, headers=BASE_HEADERS)
    response.raise_for_status()
    response_json = response.json()
    if errors := response_json.get("errors", []):
        raise ValueError(errors)
    response_json = response_json["data"]["title"]
    movie = IMDbGraphQL.Title(**response_json)
    return movie


@lru_cache(maxsize=None)
def getPerson(id: str | int) -> IMDbGraphQL.Name:
    global BASE_HEADERS
    if not id:
        raise ValueError("A valid ID must be provided.")
    if not isinstance(id, str) and not isinstance(id, int):
        raise TypeError(f"ID must be of type str or int, {type(id)} given.")
    if not str(id).replace("nm", "").isnumeric():
        raise ValueError(
            f"The format of the ID is incorrect, should be nm### or ####. Given: {id}"
        )
    query_id = "nm" + str(id).replace("nm", "").ljust(7, "0")
    attributes = get_attribute_main_query(IMDbGraphQL.Name.SCHEMA)
    query = """query personById
    {{
        name(id: "{query_id}") {{
            {attributes}
        }}
    }}
    """.format(
        query_id=query_id, attributes=attributes
    )
    response = requests.post(API_ENDPOINT, json={"query": query}, headers=BASE_HEADERS)
    response.raise_for_status()
    response_json = response.json()
    if errors := response_json.get("errors", []):
        raise ValueError(errors)
    response_json = response.json()["data"]["name"]
    person = IMDbGraphQL.Name(**response_json)
    return person
