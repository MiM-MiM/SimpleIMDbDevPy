__all__ = ["IMDbAPI"]

from SimpleIMDbDev import GraphQL, Rest


def flatten(obj: dict) -> dict:
    """Flatten a dict containing other objects.
    Each object that has a `as_dict` method gets called with recursion.

    Args:
        obj(dict): The dict to be flattened.

    Returns:
        dict: The flattened dict."""
    if not isinstance(obj, dict):
        raise ValueError("flatten must be called with a dict.")
    final_obj = dict()
    for key, val in obj.items():
        try:
            val_as_dict = val.as_dict()
            final_obj[key] = flatten(val_as_dict)
        except AttributeError:
            final_obj[key] = val
    return final_obj


class IMDbAPI:
    """Base class for IMDbAPI, using standardized dicts.
    Default is `Rest` interface.

    Note: Underlying API calls are cached using their respective modules.

    Notes:
        - Episodes do not work under the `GraphQL` interface.
        - GraphQL has a list of images where Rest has a primary image.

    Functions:
        getMovie (int | str): Returns dict of the MovieID
        getPerson (int | str): Returns dict of the PersonID
        search (str): Searches for the given title.
            *Only works under `Rest` interface.*"""

    _parsers = {
        "graphql": "GraphQL",
        "rest": "Rest",
    }

    def __init__(self, parser: str = "Rest"):
        if not isinstance(parser, str):
            raise TypeError(
                f"The 'parser' must be of type str, '{type(parser)}' given."
            )
        self._parser = self._parsers.get(parser.lower(), "GraphQL")

    def getMovie(self, id: int | str = "", subsection: str = "") -> dict:
        """Gets the movie information, subselection is for additional data.
        To get both you must make two calls, one for the main moviee dict and another via update.

        Note: Updating objects is only possible via REST.

        Args:
            self (IMDbAPI): The object that defined the parser to use.
            id (int | str): The ID of the movie, tt### or ###.
            subselection (str, optional): Typically called via update, the additional data to grab.

        Returns:
            dict: The information gathered from the query.

        Raises:
            NotImplementedError: When the requested API call is not implemented for that type.
            TypeError: When an agrument is not of the correct type.
            ValueError: When an argument was of the correct type, but invalid values.
            HTTPError: Any lookup errors or connection issues.
        """
        if subsection != "" and self._parser != "Rest":
            raise NotImplementedError("Subselection only possible via rest API.")
        match self._parser:
            case "GraphQL":
                response = GraphQL.getMovie(id).as_dict()
            case "Rest":
                response = Rest.getMovie(id, subsection)
            case _:
                response = GraphQL.getMovie(id).as_dict()
        return flatten(response)

    def getPerson(self, id: str | int, subsection: str = "") -> dict:
        """Gets the person information, subselection is for additional data.
        To get both you must make two calls, one for the main person dict and another via update.

        Note: Updating objects is only possible via REST.

        Args:
            self (IMDbAPI): The object that defined the parser to use.
            id (int | str): The ID of the person, nm### or ###.
            subselection (str, optional): Typically called via update, the additional data to grab.

        Returns:
            dict: The information gathered from the query.

        Raises:
            NotImplementedError: When the requested API call is not implemented for that type.
            TypeError: When an agrument is not of the correct type.
            ValueError: When an argument was of the correct type, but invalid values.
            HTTPError: Any lookup errors or connection issues.
        """
        if subsection != "" and self._parser != "Rest":
            raise NotImplementedError("Subselection only possible via rest API.")
        match self._parser:
            case "GraphQL":
                response = GraphQL.getPerson(id).as_dict()
            case "Rest":
                response = Rest.getPerson(id, subsection)
            case _:
                response = GraphQL.getPerson(id).as_dict()
        return flatten(response)

    def updateMovie(self, movie: dict, subselection: str = "") -> dict:
        """Updates a movie object (dict).
        The dict is required to have a valid ID, the rest are optional.
        The subselection is only allowed to be one of `akas`, `credits`, or `release_dates`.

        Args:
            self (IMDbAPI): The object that defined the parser to use.
            movie (dict): The movie object, typically obtained by `getMovie(id)`
            subselction (str): The data to update.

        Returns:
            dict: The updated movie.

        Raises:
            NotImplementedError: When the requested API call is not implemented for that type.
            TypeError: When an agrument is not of the correct type.
            ValueError: When an argument was of the correct type, but invalid values.
            HTTPError: raised from the `getMovie` call on any lookup errors or connection issues.
        """
        if subselection != "" and self._parser != "Rest":
            raise NotImplementedError(
                "Updating movie subselection only possible via rest API."
            )
        movie = Rest.updateMovie(movie, subselection)
        return flatten(movie)

    def updatePerson(self, person: dict, subselection: str = "") -> dict:
        """Updates a person object (dict).
        The dict is required to have a valid ID, the rest are optional.
        The subselection is only allowed to be `known_for`.

        Args:
            self (IMDbAPI): The object that defined the parser to use.
            person (dict): The person object, typically obtained by `getPerson(id)`
            subselction (str): The data to update.

        Returns:
            dict: The updated person.

        Raises:
            NotImplementedError: When the requested API call is not implemented for that type.
            TypeError: When an agrument is not of the correct type.
            ValueError: When an argument was of the correct type, but invalid values.
            HTTPError: raised from the `getPerson` call on any lookup errors or connection issues.
        """
        if subselection != "" and self._parser != "Rest":
            raise NotImplementedError(
                "Updating person subselection only possible via rest API."
            )
        person = Rest.updatePerson(person, subselection)
        return flatten(person)

    def search(self, title: str, year: int, country: str):
        if self._parser != "Rest":
            raise NotImplementedError("Only the 'Rest' API supports searching.")
        raise NotImplementedError("To come.")
