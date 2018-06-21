import unittest

import calendar

import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEqual(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # DATES

    # prove that if we look for dates in format YYYY-MM-DD
    # where there are none, we get no results.
    def test_no_dates(self):
        for extr in (library.dates_iso8601, library.dates_DDMonYYYY):
            self.assert_extract('I was born in middle ages.', extr)

    # DATES in YYYY-MM-DD format

    # prove that if we look for dates in format YYYY-MM-DD
    # where MM is in range [1, 12] and DD is in range [1, 31] we find one
    def test_iso8601_dates(self):
        # TODO split to several tests
        for mm in range(1, 13):
            self.assert_extract("I was born on 2015-{:02d}-25.".format(mm),
                    library.dates_iso8601, "2015-{:02d}-25".format(mm))
        for dd in range(1, 32):
            self.assert_extract("I was born on 2015-07-{:02d}.".format(dd),
                    library.dates_iso8601, "2015-07-{:02d}".format(dd))

    # prove that if we look for dates in format YYYY-MM-DD
    # where MM is not in range [1, 12], we get no results.
    def test_invalid_month_in_iso8601_dates(self):
        for mm in (0, 13):
            self.assert_extract("I was born on 2015-{:02d}-25.".format(mm), library.dates_iso8601)

    # prove that if we look for dates in format YYYY-MM-DD
    # where DD is not in range [1, 31], we get no results.
    def test_invalid_day_in_iso8601_dates(self):
        for dd in (0, 32):
            self.assert_extract("I was born on 2015-07-{:02d}.".format(dd), library.dates_iso8601)

    # DATES in DD Mon YYYY format
    # prove that if we look for dates in format DD Mon YYYY
    # where Mon is abbreviated UK/US month and DD is in range [1, 31] we find one
    def test_DDMonYYYY_dates(self):
        for mm in range(1, 13):
            _date = "25 {} 2015".format(calendar.month_abbr[mm])
            self.assert_extract("I was born on {}.".format(_date),
                    library.dates_DDMonYYYY, _date)
        # TODO split to several tests
        for dd in range(1, 32):
            _date = "{:02d} Jul 2015".format(dd)
            self.assert_extract("I was born on {}.".format(_date),
                    library.dates_DDMonYYYY, _date)


        # ISO 8601 with timestamps
    def test_more_test01(self):
        #   time precision of minutes
        self.assert_extract("The exact datetime is 2018-06-22 18:22.",
                library.dates_iso8601, "2018-06-22 18:22")

    def test_more_test02(self):
        #   time precision of seconds
        self.assert_extract("The exact datetime is 2018-06-22 18:22:19.",
                library.dates_iso8601, "2018-06-22 18:22:19")

    def test_more_test03(self):
        #   time precision of milliseconds
        self.assert_extract("The exact datetime is 2018-06-22 18:22:19.123.",
                library.dates_iso8601, "2018-06-22 18:22:19.123")

    def test_more_test04(self):
        #   date-time delimiter is 'T'
        self.assert_extract("The exact datetime is 2018-06-22T18:22:19.123.",
                library.dates_iso8601, "2018-06-22T18:22:19.123")

        # DDMonYYYY
    def test_more_test05(self):
        #   year is greater 0
        self.assert_extract("I was born on 25 Jul -2015.",
                library.dates_DDMonYYYY)

    def test_more_test06(self):
        #   day is in range [1, 31]
        self.assert_extract("I was born on 0 Jul 2015.",
                library.dates_DDMonYYYY)
        self.assert_extract("I was born on 32 Jul 2015.",
                library.dates_DDMonYYYY)

    def test_more_test07(self):
        #   no matches if Mon is wrong
        self.assert_extract("I was born on 25 Juf, 2015.",
                library.dates_DDMonYYYY)

    def test_more_test08(self):
        #   any number of spaces inside DDMonYYYY
        self.assert_extract("I was born on 25  Jul\t 2015.",
                library.dates_DDMonYYYY, "25  Jul\t 2015")

    def test_more_test09(self):
        #   comma after Mon in DDMonYYYY
        self.assert_extract("I was born on 25 Jul, 2015.",
                library.dates_DDMonYYYY, "25 Jul, 2015")

    def test_more_test10(self):
        # comma-separated grouping in numbers
        self.assert_extract("Total number was 123,456,789", library.integers, '123,456,789')

if __name__ == '__main__':
    unittest.main()
