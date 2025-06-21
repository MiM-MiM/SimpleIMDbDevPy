import requests
from functools import lru_cache
import re
from requests.exceptions import HTTPError

from SimpleIMDbDev.constants import BASE_HEADERS

BASE_URL = "https://rest.imdbapi.dev"

@lru_cache(maxsize=None)
def getMovie(id: int | str = "", subselection: str = "") -> dict:
    global BASE_HEADERS
    allowed_subselection = ['akas', 'credits', 'release_dates']
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
    if not re.fullmatch(r'tt\d{7}', title_id):
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
    # Do not cache, calls getMovie that will.
    if not isinstance(movie, dict):
        raise TypeError(f"The movie object must be a dict, {type(movie)} passed.")
    id = movie.get('id', '')
    title_id = "tt" + str(id).replace("tt", "").rjust(7, "0")
    if not id:
        raise ValueError("The ID of the movie was not found in the object.")
    if not re.fullmatch(r'tt\d{7}', title_id):
        raise ValueError("The format of the ID was incorrect, 'tt#######' expected, '{id}' recieved.")
    subeelection_json = getMovie(title_id, subselection)
    movie[subselection] = subeelection_json[subselection]
    return movie


@lru_cache(maxsize=None)
def getPerson(id: int | str = "", subselection: str = "") -> dict:
    global BASE_HEADERS
    allowed_subselection = ['known_for']
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
    if not re.fullmatch(r'nm\d{7}', person_id):
        raise ValueError("A valid ID must be provided, form nm#######.")
    if subselection:
        url = f"{BASE_URL}/v2/names/{person_id}/{subselection}"
    else:
        url = f"{BASE_URL}/v2/names/{person_id}"
    response = requests.get(url, headers=BASE_HEADERS)
    response.raise_for_status()
    response_json = response.json()
    if not response_json or response_json == {'id': person_id}:
        # As of now it returns a 200 response with only the ID passed back.
        # Subselections return an empty json
        response.status_code = 500 # Manually update status code.
        raise HTTPError('PersonID not found.', response=response)
    return response_json

def updatePerson(person: dict, subselection: str = "") -> dict:
    # Do not cache, calls getPerson that will.
    if not isinstance(person, dict):
        raise TypeError(f"The movie object must be a dict, {type(person)} passed.")
    id = person.get('id', '')
    person_id = "nm" + str(id).replace("nm", "").rjust(7, "0")
    if not id:
        raise ValueError("The ID of the person was not found in the object.")
    if not re.fullmatch(r'nm\d{7}', person_id):
        raise ValueError("The format of the ID was incorrect, 'tt#######' expected, '{id}' recieved.")
    subeelection_json = getPerson(person_id, subselection)
    person[subselection] = subeelection_json[subselection]
    return person
