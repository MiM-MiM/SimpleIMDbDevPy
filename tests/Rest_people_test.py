import responses, unittest
from SimpleIMDbDev import Rest
from requests.exceptions import HTTPError


class TestPersonMethods(unittest.TestCase):
    """Test cases for Rest Methods
    Fake the responses to avoid API call issues if a server is down."""

    def test_invalid_types(self):
        """Test for incorrect types."""
        with self.assertRaises(TypeError):
            Rest.getPerson(["a"])  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getPerson({"a": 0})  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getPerson(None)  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getPerson(6.4)  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getPerson(set(1, 2))  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getPerson("nm0477052", 0)  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getPerson("nm0477052", {"a": 1})  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getPerson("nm0477052", set(1, 0))  # type: ignore
        with self.assertRaises(TypeError):
            Rest.getPerson("nm0477052", 3.14)  # type: ignore

    def test_invalid_value(self):
        """Test for correct types with invalid values for arguments."""
        with self.assertRaises(ValueError):
            Rest.getPerson("a")
        with self.assertRaises(ValueError):
            Rest.getPerson(-1)
        with self.assertRaises(ValueError):
            Rest.getPerson("nm12345678")
        with self.assertRaises(ValueError):
            Rest.updatePerson({}, "known_for")
        with self.assertRaises(ValueError):
            Rest.updatePerson({"id": 1}, "invalid choice")
        with self.assertRaises(ValueError):
            Rest.getPerson("nm0477052", "invalid choice")

    @responses.activate
    def test_valid(self):
        """Test getPerson along with all possible updates.
        Some sample responses have been shortened for ease of view."""
        nm0000115 = {
            "id": "nm0000115",
            "display_name": "Nicolas Cage",
            "primary_image": {
                "url": "https://m.media-amazon.com/images/M/MV5BMjUxMjE4MTQxMF5BMl5BanBnXkFtZTcwNzc2MDM1NA@@._V1_.jpg",
                "width": 1503,
                "height": 2048,
            },
            "alternative_names": [
                "Nicholas Cage",
                "Nicolas Kim Coppola",
                "Nicolas Coppola",
            ],
            "primary_professions": ["actor", "producer", "director"],
            "biography": "Nicolas Cage was born Nicolas Kim Coppola in Long Beach, California, the son of comparative literature professor August Coppola (whose brother is director Francis Ford Coppola) and dancer/choreographer Joy Vogelsang. He is of Italian (father) and Polish and German (mother) descent. Cage changed his name early in his career to make his own reputation, succeeding brilliantly with a host of classic, quirky roles by the late 1980s.\n\nInitially studying theatre at Beverly Hills High School (though he dropped out at seventeen), he secured a bit part in Fast Times at Ridgemont High (1982) - most of which was cut, dashing his hopes and leading to a job selling popcorn at the Fairfax Theater, thinking that would be the only route to a movie career, but a job reading lines with actors auditioning for uncle Francis's Rumble Fish (1983) landed him a role in that film, followed by the romantic lead in Valley Girl (1983), which was released first and truly launched his career.\n\nHis one-time passion for method acting reached a personal limit when he smashed a street-vendor's remote-control car to achieve the sense of rage needed for his gangster character in The Cotton Club (1984).\n\nIn his early 20s, he dated Jenny Wright for two years and later linked to Uma Thurman. After a relationship of several years with Christina Fulton, a model, they split amicably and share custody of a son, Weston Cage (b. 1990). He also has a son with his ex-wife, Alice Kim Cage.",
            "birth_name": "Nicholas Kim Coppola",
            "birth_date": {"year": 1964, "month": 1, "day": 7},
            "birth_location": "Long Beach, California, USA",
        }
        responses.add(
            responses.GET,
            "https://rest.imdbapi.dev/v2/names/nm0000115",
            json=nm0000115,
            status=200,
        )
        nm0000115_response = Rest.getPerson("nm0000115")
        self.assertEqual(nm0000115_response, nm0000115)
        nm0000115_response = Rest.getPerson(115)
        self.assertEqual(nm0000115_response, nm0000115)

        nm0000115_known_for = {
            "known_for": [
                {
                    "title": {
                        "id": "tt0119094",
                        "type": "movie",
                        "primary_title": "Face/Off",
                        "primary_image": {
                            "url": "https://m.media-amazon.com/images/M/MV5BOGQyOWNmYTgtZWY0NS00NzhjLTg3NmMtMzcwYzQ2OTA2OTJkXkEyXkFqcGc@._V1_.jpg",
                            "width": 520,
                            "height": 777,
                        },
                        "rating": {"aggregate_rating": 7.3, "votes_count": 415671},
                        "start_year": 1997,
                    },
                    "category": "ACTOR",
                    "characters": ["Castor Troy"],
                },
            ]
        }
        responses.add(
            responses.GET,
            "https://rest.imdbapi.dev/v2/names/nm0000115/known_for",
            json=nm0000115_known_for,
            status=200,
        )
        nm0000115["known_for"] = nm0000115_known_for["known_for"]
        nm0000115_response = Rest.updatePerson(nm0000115_response, "known_for")
        self.assertEqual(nm0000115_response, nm0000115)

    @responses.activate
    def test_invalid_ID(self):
        nm0000000 = {"id": "nm0000000"}
        responses.add(
            responses.GET,
            "https://rest.imdbapi.dev/v2/names/nm0000000",
            json=nm0000000,
            status=200,
        )
        with self.assertRaises(HTTPError):
            Rest.getPerson("nm0000000")
        responses.add(
            responses.GET,
            "https://rest.imdbapi.dev/v2/names/nm0000000/known_for",
            json={},
            status=200,
        )
        with self.assertRaises(HTTPError):
            Rest.getPerson("nm0000000")


if __name__ == "__main__":
    unittest.main()
