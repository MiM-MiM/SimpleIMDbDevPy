import responses, unittest
from responses import matchers
from SimpleIMDbDev import GraphQL
from SimpleIMDbDev import flatten


class TestPersonMethods(unittest.TestCase):
    """Test cases for GraphQL Methods
    Fake the responses to avoid API call issues if a server is down."""

    def test_invalid_types(self):
        """Test for incorrect types."""
        with self.assertRaises(TypeError):
            GraphQL.getPerson(["a"])  # type: ignore
        with self.assertRaises(TypeError):
            GraphQL.getPerson({"a": 0})  # type: ignore
        with self.assertRaises(TypeError):
            GraphQL.getPerson(None)  # type: ignore
        with self.assertRaises(TypeError):
            GraphQL.getPerson(6.4)  # type: ignore
        with self.assertRaises(TypeError):
            GraphQL.getPerson(set(1, 2))  # type: ignore

    def test_invalid_value(self):
        """Test for correct types with invalid values for arguments."""
        with self.assertRaises(ValueError):
            GraphQL.getPerson("a")
        with self.assertRaises(ValueError):
            GraphQL.getPerson(-1)
        with self.assertRaises(ValueError):
            GraphQL.getPerson("nm12345678")

    @responses.activate
    def test_valid(self):
        # fmt: off
        nm0000115 = {
            "data": {
                "name": {
                    "id": "nm0000115", "display_name": "Nicolas Cage",
                    "alternate_names": ["Nicholas Cage", "Nicolas Kim Coppola", "Nicolas Coppola",],
                    "birth_year": 1964, "birth_location": "Long Beach, California, USA",
                    "death_year": None, "death_location": None, "dead_reason": None,
                    "avatars": [
                        {
                            "url": "https://m.media-amazon.com/images/M/MV5BMjUxMjE4MTQxMF5BMl5BanBnXkFtZTcwNzc2MDM1NA@@._V1_.jpg",
                            "width": 1503, "height": 2048,
                        }
                    ],
                    "known_for": [
                        {
                            "id": "tt16360004", "type": "movie", "primary_title": "Spider-Man: Beyond the Spider-Verse",
                            "original_title": None, "start_year": None, "runtime_minutes": None, "certificates": None,
                            "critic_review": None, "genres": ["Action", "Adventure", "Animation", "...",],
                            "spoken_languages": [{"code": "eng", "name": "English"}], "origin_countries": [{"code": "US", "name": "United States"}],
                            "posters": [{
                                "url": "https://m.media-amazon.com/images/M/MV5BNWZjYTgzZmItMGEwZS00NTgwLThhOWItMzM2MTY0ODZjZGVhXkEyXkFqcGc@._V1_.jpg",
                                "width": 840, "height": 1240, "language_code": None,
                            }]}]}}}
        nm0000115_query_string = 'query personById { name(id: "nm0000115") { id display_name alternate_names birth_year birth_location death_year death_location dead_reason avatars { url width height } known_for { id type primary_title original_title start_year runtime_minutes certificates { country { code name } rating } critic_review { score review_count } genres spoken_languages { code name } origin_countries { code name } posters { url width height language_code } } } }'
        nm0000115_dict_expected = {'id': 'nm0000115', 'display_name': 'Nicolas Cage', 'alternate_names': ['Nicholas Cage', 'Nicolas Kim Coppola', 'Nicolas Coppola'], 'birth_year': 1964, 'birth_location': 'Long Beach, California, USA', 'avatars': [{'url': 'https://m.media-amazon.com/images/M/MV5BMjUxMjE4MTQxMF5BMl5BanBnXkFtZTcwNzc2MDM1NA@@._V1_.jpg', 'width': 1503, 'height': 2048}], 'known_for': [{'id': 'tt16360004', 'type': 'movie', 'primary_title': 'Spider-Man: Beyond the Spider-Verse', 'original_title': None, 'start_year': None, 'runtime_minutes': None, 'certificates': None, 'critic_review': None, 'genres': ['Action', 'Adventure', 'Animation', '...'], 'spoken_languages': [{'code': 'eng', 'name': 'English'}], 'origin_countries': [{'code': 'US', 'name': 'United States'}], 'posters': [{'url': 'https://m.media-amazon.com/images/M/MV5BNWZjYTgzZmItMGEwZS00NTgwLThhOWItMzM2MTY0ODZjZGVhXkEyXkFqcGc@._V1_.jpg', 'width': 840, 'height': 1240, 'language_code': None}]}]}
        # fmt: on
        responses.add(
            responses.POST,
            "https://graph.imdbapi.dev/v1",
            json=nm0000115,
            status=200,
            match=[matchers.json_params_matcher({"query": nm0000115_query_string})],
        )
        nm0000115_response = GraphQL.getPerson("nm0000115")
        nm0000115_dict = flatten(nm0000115_response.as_dict())
        self.assertEqual(nm0000115_dict, nm0000115_dict_expected)

    @responses.activate
    def test_invalid_ID(self):
        nm0000000 = {
            "errors": [{"message": "DISPLAY_NAME_REQURIRED", "path": ["name"]}],
            "data": {"name": None},
        }
        nm0000000_query_string = 'query personById { name(id: "nm0000000") { id display_name alternate_names birth_year birth_location death_year death_location dead_reason avatars { url width height } known_for { id type primary_title original_title start_year runtime_minutes certificates { country { code name } rating } critic_review { score review_count } genres spoken_languages { code name } origin_countries { code name } posters { url width height language_code } } } }'
        responses.add(
            responses.POST,
            "https://graph.imdbapi.dev/v1",
            json=nm0000000,
            status=200,
            match=[matchers.json_params_matcher({"query": nm0000000_query_string})],
        )
        with self.assertRaises(ValueError):
            nm0000000_response = GraphQL.getPerson("nm0000000")


if __name__ == "__main__":
    unittest.main()
