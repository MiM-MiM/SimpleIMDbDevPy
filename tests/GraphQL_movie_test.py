import responses, unittest
from responses import matchers
from SimpleIMDbDev import GraphQL
from SimpleIMDbDev import flatten


class TestMovieMethods(unittest.TestCase):
    """Test cases for GraphQL Methods
    Fake the responses to avoid API call issues if a server is down."""

    def test_invalid_types(self):
        """Test for incorrect types."""
        with self.assertRaises(TypeError):
            GraphQL.getMovie(["a"])  # type: ignore
        with self.assertRaises(TypeError):
            GraphQL.getMovie({"a": 0})  # type: ignore
        with self.assertRaises(TypeError):
            GraphQL.getMovie(None)  # type: ignore
        with self.assertRaises(TypeError):
            GraphQL.getMovie(6.4)  # type: ignore
        with self.assertRaises(TypeError):
            GraphQL.getMovie(set(1, 2))  # type: ignore

    def test_invalid_value(self):
        """Test for correct types with invalid values for arguments."""
        with self.assertRaises(ValueError):
            GraphQL.getMovie("a")
        with self.assertRaises(ValueError):
            GraphQL.getMovie(-1)
        with self.assertRaises(ValueError):
            GraphQL.getMovie("tt04770510")

    @responses.activate
    def test_valid(self):
        # fmt: off
        tt0477051 = {'data': {'title':
                              {'id': 'tt0477051', 'type': 'movie', 'is_adult': False,
                               'primary_title': 'Norbit', 'original_title': None,
                               'start_year': 2007, 'end_year': None, 'runtime_minutes': 102,
                               'plot': 'A mild-mannered guy, who is married to a monstrous woman, meets the woman of his dreams, and schemes to find a way to be with her.',
                               'rating': {'aggregate_rating': 4.2, 'votes_count': 79169},
                               'certificates': [{'country': {'code': 'US', 'name': 'United States'}, 'rating': 'PG-13'}],
                               'critic_review': {'score': 27, 'review_count': 26}, 'genres': ['Comedy', 'Romance'],
                               'spoken_languages': [{'code': 'eng', 'name': 'English'}],
                               'origin_countries': [{'code': 'US', 'name': 'United States'}],
                               'posters': [{'url': 'https://m.media-amazon.com/images/M/MV5BMTI4NDE4MjgyNV5BMl5BanBnXkFtZTcwMTQwODc0MQ@@._V1_.jpg', 'width': 300, 'height': 444, 'language_code': None}],
                               'credits': [{'name': {'id': 'nm0005367', 'display_name': 'Brian Robbins', 'alternate_names': None,
                                                     'birth_year': 1963, 'birth_location': 'Marine Park, Brooklyn, New York, USA',
                                                     'death_year': None, 'death_location': None, 'dead_reason': None,
                                                     'avatars': [{'url': 'https://m.media-amazon.com/images/M/MV5BMjA0MjczNjc0OV5BMl5BanBnXkFtZTYwODY3MTY2._V1_.jpg',
                                                                  'width': 450, 'height': 675}]}, 'category': 'director', 'characters': None, 'episodes_count': None},
                                            {'name': {'id': 'nm0000552', 'display_name': 'Eddie Murphy',
                                                      'alternate_names': ['Fred Braughton', "Edward 'Eddie' Regan Murphy"],
                                                      'birth_year': 1961, 'birth_location': 'Brooklyn, New York City, New York, USA',
                                                      'death_year': None, 'death_location': None, 'dead_reason': None,
                                                      'avatars': [{'url': 'https://m.media-amazon.com/images/M/MV5BMTc0NDQzODAwNF5BMl5BanBnXkFtZTYwMzUzNTk3._V1_.jpg', 'width': 285, 'height': 400}]},
                                                      'category': 'actor', 'characters': ['Norbit', 'Rasputia', 'Mr. Wong'], 'episodes_count': None},
                                            {'name': {'id': 'nm0000552', 'display_name': 'Eddie Murphy',
                                                      'alternate_names': ['Fred Braughton', "Edward 'Eddie' Regan Murphy"],
                                                      'birth_year': 1961, 'birth_location': 'Brooklyn, New York City, New York, USA',
                                                      'death_year': None, 'death_location': None, 'dead_reason': None,
                                                      'avatars': [{'url': 'https://m.media-amazon.com/images/M/MV5BMTc0NDQzODAwNF5BMl5BanBnXkFtZTYwMzUzNTk3._V1_.jpg', 'width': 285, 'height': 400}]},
                                                      'category': 'writer', 'characters': None, 'episodes_count': None},
                                            {'name': {'id': 'nm0628601', 'display_name': 'Thandiwe Newton',
                                                      'alternate_names': ['Thandie Newton'],
                                                      'birth_year': 1972, 'birth_location': 'Westminster, London, England, UK',
                                                      'death_year': None, 'death_location': None, 'dead_reason': None,
                                                      'avatars': [{'url': 'https://m.media-amazon.com/images/M/MV5BNjMzNTAxNDUwNV5BMl5BanBnXkFtZTcwMjMyNjI5MQ@@._V1_.jpg', 'width': 308, 'height': 400}]},
                                                      'category': 'actress', 'characters': ['Kate Thomas'], 'episodes_count': None}]}}}
        tt0477051_query_string = 'query titleById { title(id: "tt0477051") { id type is_adult primary_title original_title start_year end_year runtime_minutes plot rating { aggregate_rating votes_count } certificates { country { code name } rating } critic_review { score review_count } genres spoken_languages { code name } origin_countries { code name } posters { url width height language_code } credits { name { id display_name alternate_names birth_year birth_location death_year death_location dead_reason avatars { url width height } } category characters episodes_count } } }'
        tt0477051_expected_response = {'id': 'tt0477051', 'type': 'movie', 'is_adult': False,
                                       'primary_title': 'Norbit', 'start_year': 2007, 'runtime_minutes': 102,
                                       'plot': 'A mild-mannered guy, who is married to a monstrous woman, meets the woman of his dreams, and schemes to find a way to be with her.',
                                       'rating': {'aggregate_rating': 4.2, 'votes_count': 79169},
                                       'certificates': [{'country': {'code': 'US', 'name': 'United States'}, 'rating': 'PG-13'}],
                                       'critic_review': {'score': 27, 'review_count': 26}, 'genres': ['Comedy', 'Romance'],
                                       'spoken_languages': [{'code': 'eng', 'name': 'English'}], 'origin_countries': [{'code': 'US', 'name': 'United States'}],
                                       'posters': [{'url': 'https://m.media-amazon.com/images/M/MV5BMTI4NDE4MjgyNV5BMl5BanBnXkFtZTcwMTQwODc0MQ@@._V1_.jpg', 'width': 300, 'height': 444, 'language_code': None}],
                                       'credits': [{'name': {'id': 'nm0005367', 'display_name': 'Brian Robbins', 'alternate_names': None,
                                                             'birth_year': 1963, 'birth_location': 'Marine Park, Brooklyn, New York, USA',
                                                             'death_year': None, 'death_location': None, 'dead_reason': None,
                                                             'avatars': [{'url': 'https://m.media-amazon.com/images/M/MV5BMjA0MjczNjc0OV5BMl5BanBnXkFtZTYwODY3MTY2._V1_.jpg', 'width': 450, 'height': 675}]},
                                                             'category': 'director', 'characters': None, 'episodes_count': None},
                                                    {'name': {'id': 'nm0000552', 'display_name': 'Eddie Murphy',
                                                              'alternate_names': ['Fred Braughton', "Edward 'Eddie' Regan Murphy"],
                                                              'birth_year': 1961, 'birth_location': 'Brooklyn, New York City, New York, USA',
                                                              'death_year': None, 'death_location': None, 'dead_reason': None,
                                                              'avatars': [{'url': 'https://m.media-amazon.com/images/M/MV5BMTc0NDQzODAwNF5BMl5BanBnXkFtZTYwMzUzNTk3._V1_.jpg', 'width': 285, 'height': 400}]},
                                                              'category': 'actor', 'characters': ['Norbit', 'Rasputia', 'Mr. Wong'], 'episodes_count': None},
                                                    {'name': {'id': 'nm0000552', 'display_name': 'Eddie Murphy',
                                                              'alternate_names': ['Fred Braughton', "Edward 'Eddie' Regan Murphy"],
                                                              'birth_year': 1961, 'birth_location': 'Brooklyn, New York City, New York, USA',
                                                              'death_year': None, 'death_location': None, 'dead_reason': None,
                                                              'avatars': [{'url': 'https://m.media-amazon.com/images/M/MV5BMTc0NDQzODAwNF5BMl5BanBnXkFtZTYwMzUzNTk3._V1_.jpg', 'width': 285, 'height': 400}]},
                                                              'category': 'writer', 'characters': None, 'episodes_count': None},
                                                    {'name': {'id': 'nm0628601', 'display_name': 'Thandiwe Newton', 'alternate_names': ['Thandie Newton'],
                                                              'birth_year': 1972, 'birth_location': 'Westminster, London, England, UK',
                                                              'death_year': None, 'death_location': None, 'dead_reason': None,
                                                              'avatars': [{'url': 'https://m.media-amazon.com/images/M/MV5BNjMzNTAxNDUwNV5BMl5BanBnXkFtZTcwMjMyNjI5MQ@@._V1_.jpg', 'width': 308, 'height': 400}]},
                                                              'category': 'actress', 'characters': ['Kate Thomas'], 'episodes_count': None}]}
        # fmt: on
        responses.add(
            responses.POST,
            "https://graph.imdbapi.dev/v1",
            json=tt0477051,
            status=200,
            match=[matchers.json_params_matcher({"query": tt0477051_query_string})],
        )
        tt0477051_response = GraphQL.getMovie("tt0477051")
        tt0477051_response_dict = flatten(tt0477051_response.as_dict())
        self.assertEqual(tt0477051_response_dict, tt0477051_expected_response)

    @responses.activate
    def test_invalid_ID(self):
        tt0000000 = {
            "errors": [{"message": "UNSUPPORT_TYPE ", "path": ["title"]}],
            "data": {"title": None},
        }
        tt0000000_query_string = 'query titleById { title(id: "tt0000000") { id type is_adult primary_title original_title start_year end_year runtime_minutes plot rating { aggregate_rating votes_count } certificates { country { code name } rating } critic_review { score review_count } genres spoken_languages { code name } origin_countries { code name } posters { url width height language_code } credits { name { id display_name alternate_names birth_year birth_location death_year death_location dead_reason avatars { url width height } } category characters episodes_count } } }'
        responses.add(
            responses.POST,
            "https://graph.imdbapi.dev/v1",
            json=tt0000000,
            status=200,
            match=[matchers.json_params_matcher({"query": tt0000000_query_string})],
        )
        with self.assertRaises(ValueError):
            tt0000000_response = GraphQL.getMovie("tt0000000")
