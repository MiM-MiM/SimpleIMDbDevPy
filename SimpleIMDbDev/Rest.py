__all__ = ["getMovie", "getPerson"]

import requests
from functools import lru_cache
import re
from requests.exceptions import HTTPError

from SimpleIMDbDev.constants import BASE_HEADERS

BASE_URL = "https://rest.imdbapi.dev"


@lru_cache(maxsize=None)
def getMovie(id: int | str = "", subselection: str = "") -> dict:
    """Gets the movie information, subselection is for additional data.
    To get both you must make two calls, one for the main movie dict and another via update.

    Args:
        id (int | str): The ID of the movie, tt### or ###.
        subselection (str, optional): Typically called via update, the additional data to grab.

    Returns:
        dict: The information gathered from the query.

    Raises:
        TypeError: When an agrument is not of the correct type.
        ValueError: When an argument was of the correct type, but invalid values.
        HTTPError: Any lookup errors or connection issues.
    """
    allowed_subselection = ["akas", "credits", "release_dates"]
    if not isinstance(id, str) and not isinstance(id, int):
        raise TypeError(f"ID must be of type str or int, {type(id)} given.")
    if not id:
        raise ValueError("A valid ID must be provided.")
    if not isinstance(subselection, str):
        raise TypeError("The subselection must be a string.")
    subselection = subselection.lower()
    if subselection and subselection not in allowed_subselection:
        raise ValueError(f"The subselection must be one of {allowed_subselection}")
    title_id = "tt" + str(id).replace("tt", "").rjust(7, "0")
    if not re.fullmatch(r"tt\d{7}", title_id):
        raise ValueError("A valid ID must be provided, form tt#######.")
    if subselection:
        url = f"{BASE_URL}/v2/titles/{title_id}/{subselection}"
    else:
        url = f"{BASE_URL}/v2/titles/{title_id}"
    response = requests.get(url, headers=BASE_HEADERS)
    response.raise_for_status()
    response_json = response.json()
    return response_json


def updateMovie(movie: dict, subselection: str = "") -> dict:
    """Updates a movie object (dict).
    The dict is required to have a valid ID, the rest are optional.
    The subselection is only allowed to be one of `akas`, `credits`, or `release_dates`.
    This is not directly cached, `getMovie` is cached and will be called for the new data.

    Args:
        movie (dict): The movie object, typically obtained by `getMovie(id)`
        subselction (str): The data to update.

    Returns:
        dict: The updated movie.

    Raises:
        TypeError: When an agrument is not of the correct type.
        ValueError: When an argument was of the correct type, but invalid values.
        HTTPError: raised from the `getMovie` call on any lookup errors or connection issues.
    """
    if not isinstance(movie, dict):
        raise TypeError(f"The movie object must be a dict, {type(movie)} passed.")
    id = movie.get("id", "")
    title_id = "tt" + str(id).replace("tt", "").rjust(7, "0")
    if not id:
        raise ValueError("The ID of the movie was not found in the object.")
    if not re.fullmatch(r"tt\d{7}", title_id):
        raise ValueError(
            f"The format of the ID was incorrect, 'tt#######' expected, '{id}' recieved."
        )
    subeelection_json = getMovie(title_id, subselection)
    movie[subselection] = subeelection_json[subselection]
    return movie


@lru_cache(maxsize=None)
def getPerson(id: int | str = "", subselection: str = "") -> dict:
    """Gets the person information, subselection is for additional data.
    To get both you must make two calls, one for the main person dict and another via update.

    Args:
        id (int | str): The ID of the person, nm### or ###.
        subselection (str, optional): Typically called via update, the additional data to grab.

    Returns:
        dict: The information gathered from the query.

    Raises:
        TypeError: When an agrument is not of the correct type.
        ValueError: When an argument was of the correct type, but invalid values.
        HTTPError: Any lookup errors or connection issues.
    """
    allowed_subselection = ["known_for"]
    if not isinstance(id, str) and not isinstance(id, int):
        raise TypeError(f"ID must be of type str or int, {type(id)} given.")
    if not id:
        raise ValueError("A valid ID must be provided.")
    if not isinstance(subselection, str):
        raise TypeError("The subselection must be a string.")
    subselection = subselection.lower()
    if subselection and subselection not in allowed_subselection:
        raise ValueError(f"The subselection must be one of {allowed_subselection}")
    person_id = "nm" + str(id).replace("nm", "").rjust(7, "0")
    if not re.fullmatch(r"nm\d{7}", person_id):
        raise ValueError("A valid ID must be provided, form nm#######.")
    if subselection:
        url = f"{BASE_URL}/v2/names/{person_id}/{subselection}"
    else:
        url = f"{BASE_URL}/v2/names/{person_id}"
    response = requests.get(url, headers=BASE_HEADERS)
    response.raise_for_status()
    response_json = response.json()
    if not response_json or response_json == {"id": person_id}:
        # As of now it returns a 200 response with only the ID passed back.
        # Subselections return an empty json
        response.status_code = 500  # Manually update status code.
        raise HTTPError("PersonID not found.", response=response)
    return response_json


def updatePerson(person: dict, subselection: str = "") -> dict:
    """Updates a person object (dict).
    The dict is required to have a valid ID, the rest are optional.
    The subselection is only allowed to be `known_for`.
    This is not directly cached, `getPerson` is cached and will be called for the new data.

    Args:
        person (dict): The person object, typically obtained by `getPerson(id)`
        subselction (str): The data to update.

    Returns:
        dict: The updated person.

    Raises:
        TypeError: When an agrument is not of the correct type.
        ValueError: When an argument was of the correct type, but invalid values.
        HTTPError: raised from the `getPerson` call on any lookup errors or connection issues.
    """
    if not isinstance(person, dict):
        raise TypeError(f"The movie object must be a dict, {type(person)} passed.")
    id = person.get("id", "")
    person_id = "nm" + str(id).replace("nm", "").rjust(7, "0")
    if not id:
        raise ValueError("The ID of the person was not found in the object.")
    if not subselection:
        raise ValueError("A subselection is required.")
    if not re.fullmatch(r"nm\d{7}", person_id):
        raise ValueError(
            f"The format of the ID was incorrect, 'tt#######' expected, '{id}' recieved."
        )
    subeelection_json = getPerson(person_id, subselection)
    person[subselection] = subeelection_json[subselection]
    return person


@lru_cache(maxsize=None)
def searchMovie(query: str, year: int = 0, max_year_difference: int = 2) -> list[dict]:
    """Search for a movie.
    Allows for passing a year to filter and search.

    Args:
        query (str): Any query to search, typically the title.
        year (int, optional): A year to help filter the results, also passed to the search via `(year)`
            Cannot be negative.
        max_year_difference (int, optional): To filter the results, a difference of 0 passed means exact.
            Negative means no filtering is being done.
            Default of 2.

    Returns:
        list[dict]: The list of the results, not all data is returned, a call to `getMovie()` may be needed.

    Raises:
        TypeError: When an argument is of the incorrec type.
        ValueError: When the value of an argument is invalid.
        HTTPError: Any API call or connection issues may cause this, none raised manually.
    """
    if not isinstance(query, str):
        raise TypeError(f"The query must be a string, {type(query)} passed.")
    if not isinstance(year, int):
        raise TypeError(f"The year must be an int, {type(year)} passed.")
    if not isinstance(max_year_difference, int):
        raise TypeError(
            f"The country must be an int, {type(max_year_difference)} passed."
        )
    if not query:
        raise ValueError("The query cannot be blank.")
    if year < 0:
        raise ValueError(f"The year cannot be less than 0, {year} given.")
    search_query = f"{query} ({year})" if year else query
    url = f"{BASE_URL}/v2/search/titles"
    params = {"query": search_query}
    response = requests.get(url, headers=BASE_HEADERS, params=params)
    response.raise_for_status()
    response_json = response.json()
    titles = response_json.get("titles", [])
    if year and max_year_difference >= 0:
        # Negative max_difference is no filter, year only used for search query.
        filtered = [
            title
            for title in titles
            if title.get("start_year") is not None
            and abs(title.get("start_year") - year) <= max_year_difference
        ]
    else:
        filtered = titles
    return filtered
