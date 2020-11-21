import unittest
import covid_main
import os


class MyTestCase(unittest.TestCase):
    def test_get_covid_data(self):
        cd = covid_main.get_covid_data()
        self.assertEqual(len(cd) > 0, True)

    def test_list_counties(self):
        cd = covid_main.get_covid_data()
        c = covid_main.list_counties(cd)
        self.assertEqual("United States" in c, True)

    def test_create_cases_death_plots(self):
        cd = covid_main.get_covid_data()
        covid_main.create_cases_death_plots(cd, "United States", 11, 2020)
        self.assertEqual(os.path.exists("United States new_cases.png"), True)
        self.assertEqual(os.path.exists("United States new_deaths.png"), True)

    def test_line_plot(self):
        cd = covid_main.get_covid_data()
        covid_main.line_plot("TEST", cd, "date", "new_cases", country="United States")
        self.assertEqual(os.path.exists("United States TEST.png"), True)

    def test_create_pie_plot(self):
        cd = covid_main.get_covid_data()
        covid_main.create_pie_plot(cd, 11, 2020)
        self.assertEqual(os.path.exists("Top 10 new cases pie for 11-2020.png"), True)

    def test_write_csv(self):
        cd = covid_main.get_covid_data()
        covid_main.write_csv(cd, "covid_data.csv", "covid")
        number_of_lines = len(open("covid_data.csv").readlines())
        self.assertEqual(number_of_lines > 10, True)


if __name__ == '__main__':
    unittest.main()
