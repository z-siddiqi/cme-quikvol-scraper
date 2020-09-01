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
    
    def test_no_date(self):
        """Tests the function using data with no date."""

        unparsed_data = 'date|~dte|4~atmStrike|1.1950~vol|9.43'
        result = parse_data(unparsed_data)
        expected_result = {'date': None, 'type': 'IV', 'vol': 9.43, 'dte': 4}
        
        self.assertEqual(result, expected_result)
    
    def test_no_vol(self):
        """Tests the function using data with no volatility."""

        unparsed_data = 'date|31/08/2020~dte|4~atmStrike|1.1950~vol|'
        result = parse_data(unparsed_data)
        expected_date = dt.date(2020, 8, 31)
        expected_result = {'date': expected_date, 'type': 'IV', 'vol': None, 'dte': 4}
        
        self.assertEqual(result, expected_result)
    
    def test_no_dte(self):
        """Tests the function using data with no days to expiry."""

        unparsed_data = 'date|31/08/2020~dte|~atmStrike|1.1950~vol|9.43'
        result = parse_data(unparsed_data)
        expected_date = dt.date(2020, 8, 31)
        expected_result = {'date': expected_date, 'type': 'IV', 'vol': 9.43, 'dte': None}
        
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()