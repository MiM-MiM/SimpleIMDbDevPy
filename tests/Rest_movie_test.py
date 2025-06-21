import responses, unittest
from SimpleIMDbDev import Rest
from requests.exceptions import HTTPError

"""Test cases for GraphQL Methods
Fake the responses to avoid API call issues if a server is down."""


class TestGraphQLMethodsMovie(unittest.TestCase):

    def test_Rest_invalid_types(self):
        """Test for incorrect types."""
        with self.assertRaises(TypeError):
            Rest.getMovie(["a"])  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getMovie({"a": 0})  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getMovie(None)  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getMovie(6.4)  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getMovie(set(1, 2))  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getMovie("tt0477052", 0)  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getMovie("tt0477052", {"a": 1})  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getMovie("tt0477052", set(1, 0))  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getMovie("tt0477052", 3.14)  # type: ignore

    def test_Rest_invalid_value(self):
        """Test for correct types with invalid values for arguments."""
        with self.assertRaises(ValueError):
            Rest.getMovie("a")
        with self.assertRaises(ValueError):
            Rest.getMovie(-1)
        with self.assertRaises(ValueError):
            Rest.getMovie("tt04770510")
        with self.assertRaises(ValueError):
            Rest.updateMovie({}, "credits")
        with self.assertRaises(ValueError):
            Rest.updateMovie({"id": 1}, "invalid choice")
        with self.assertRaises(ValueError):
            Rest.getMovie("tt0477052", "invalid choice")

    @responses.activate
    def test_Rest_valid(self):
        """Test GetMovie along with all possible updates.
        Some sample responses have been shortened for ease of view."""
        tt0477051 = {
            "id": "tt0477051",
            "type": "movie",
            "primary_title": "Norbit",
            "primary_image": {
                "url": "https://m.media-amazon.com/images/M/MV5BMTI4NDE4MjgyNV5BMl5BanBnXkFtZTcwMTQwODc0MQ@@._V1_.jpg",
                "width": 300,
                "height": 444,
            },
            "genres": ["Comedy", "Romance"],
            "rating": {"aggregate_rating": 4.2, "votes_count": 84384},
            "start_year": 2007,
            "runtime_minutes": 102,
            "plot": "A mild-mannered guy, who is married to a monstrous woman, meets the woman of his dreams, and schemes to find a way to be with her.",
        }
        responses.add(
            responses.GET,
            "https://rest.imdbapi.dev/v2/titles/tt0477051",
            json=tt0477051,
            status=200,
        )
        tt0477051_response = Rest.getMovie("tt0477051")
        self.assertEqual(tt0477051_response, tt0477051)

        tt0477051_akas = {
            "akas": [
                {"country_code": "AR", "text": "Norbit"},
                {"country_code": "AU", "text": "Norbit"},
                {"country_code": "BG", "language_code": "bul", "text": "Норбит"},
                {"country_code": "BR", "text": "Norbit", "attributes": ["new title"]},
                {"country_code": "CA", "language_code": "fra", "text": "Norbit"},
                {"country_code": "CO", "text": "Norbit"},
                {"country_code": "DE", "text": "Norbit"},
            ]
        }
        responses.add(
            responses.GET,
            "https://rest.imdbapi.dev/v2/titles/tt0477051/akas",
            json=tt0477051_akas,
            status=200,
        )
        tt0477051["akas"] = tt0477051_akas.get("akas")
        Rest.updateMovie(tt0477051_response, "akas")
        self.assertEqual(tt0477051_response, tt0477051)

        tt0477051_credits = {
            "credits": [
                {
                    "name": {
                        "id": "nm0000552",
                        "display_name": "Eddie Murphy",
                        "primary_image": {
                            "url": "https://m.media-amazon.com/images/M/MV5BMTc0NDQzODAwNF5BMl5BanBnXkFtZTYwMzUzNTk3._V1_.jpg",
                            "width": 285,
                            "height": 400,
                        },
                    },
                    "category": "ACTOR",
                    "characters": ["Norbit", "Rasputia", "Mr. Wong"],
                },
                {
                    "name": {
                        "id": "nm0000552",
                        "display_name": "Eddie Murphy",
                        "primary_image": {
                            "url": "https://m.media-amazon.com/images/M/MV5BMTc0NDQzODAwNF5BMl5BanBnXkFtZTYwMzUzNTk3._V1_.jpg",
                            "width": 285,
                            "height": 400,
                        },
                    },
                    "category": "WRITER",
                },
            ],
            "next_page_token": "token_b64_string=",
        }
        responses.add(
            responses.GET,
            "https://rest.imdbapi.dev/v2/titles/tt0477051/credits",
            json=tt0477051_credits,
            status=200,
        )
        tt0477051["credits"] = tt0477051_credits.get("credits")
        Rest.updateMovie(tt0477051_response, "credits")
        self.assertEqual(tt0477051_response, tt0477051)

        tt0477051_release_dates = {
            "release_dates": [
                {
                    "country_code": "US",
                    "release_date": {"year": 2007, "month": 2, "day": 9},
                },
                {
                    "country_code": "CA",
                    "release_date": {"year": 2007, "month": 2, "day": 9},
                },
            ]
        }
        responses.add(
            responses.GET,
            "https://rest.imdbapi.dev/v2/titles/tt0477051/release_dates",
            json=tt0477051_release_dates,
            status=200,
        )
        tt0477051["release_dates"] = tt0477051_release_dates.get("release_dates")
        Rest.updateMovie(tt0477051_response, "release_dates")
        self.assertEqual(tt0477051_response, tt0477051)

    @responses.activate
    def test_Rest_invalid_ID(self):
        tt0477052 = {
            "code": 13,
            "message": "GetTitleFromFetcher: failed fetch: imdb:FetchTitle parseTitleObject: missing type titleID:tt04770510",
        }
        responses.add(
            responses.GET,
            "https://rest.imdbapi.dev/v2/titles/tt0477052",
            json=tt0477052,
            status=500,
        )
        with self.assertRaises(HTTPError):
            Rest.getMovie("tt0477052")


if __name__ == "__main__":
    unittest.main()
