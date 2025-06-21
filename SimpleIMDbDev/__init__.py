from SimpleIMDbDev import GraphQL, Rest


def flatten(obj: dict) -> dict:
    """Flatten a dict containing other objects.
    Each object that has a `as_dict` method gets called with recursion.

    Input:
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

    def getMovie(self, id: int | str = "") -> dict:
        match self._parser:
            case "GraphQL":
                response = GraphQL.getMovie(id).as_dict()
            case "Rest":
                response = Rest.getMovie(id)
            case _:
                response = GraphQL.getMovie(id).as_dict()
        return flatten(response)
    
    def updateMovie(self, movie: dict, subselection: str = "") -> dict:
        if self._parser != "Rest":
            raise NotImplementedError("Only the 'Rest' API supports updating.")
        return Rest.updateMovie(movie, subselection)


    def getPerson(self, id: str | int) -> dict:
        match self._parser:
            case "GraphQL":
                response = GraphQL.getPerson(id).as_dict()
            case "Rest":
                response = Rest.getPerson(id)
            case _:
                response = GraphQL.getPerson(id).as_dict()
        return flatten(response)

    def search(self, title: str, year: int, country: str):
        if self._parser != "Rest":
            raise NotImplementedError("Only the 'Rest' API supports searching.")
