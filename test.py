import unittest
import datetime as dt

from scraper import get_prev_weekday, parse_data


class TestGetPrevWeekday(unittest.TestCase):
    """Includes tests for the get_prev_weekday function."""

    def test_monday(self):
        """Tests the function using a random monday."""

        random_monday_date = dt.datetime(2020, 8, 3)
        result = get_prev_weekday(random_monday_date)
        expected_result = dt.datetime(2020, 7, 31)

        self.assertEqual(result, expected_result)

    def test_friday(self):
        """Tests the function using a random friday."""

        random_friday_date = dt.datetime(2020, 7, 24)
        result = get_prev_weekday(random_friday_date)
        expected_result = dt.datetime(2020, 7, 23)

        self.assertEqual(result, expected_result)


class TestParseData(unittest.TestCase):
    """Includes tests for the parse_data function."""
    
    def test_incorrect_data(self):
        """Tests the function using incorrect data."""

        unparsed_data = 'this is a test'
        result = parse_data(unparsed_data)
        expected_result = {'date': None, 'type': None, 'vol': None, 'dte': None}
        
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()