import unittest
from dataAnalyzer.weather import checkTemperature, get_temperatures_for_colorado, calculatePoints
from dataAnalyzer.mockJsonData import getJsonData

class WeatherTestCase(unittest.TestCase):
    def test_checkTemperature_within_range(self):
        self.assertTrue(checkTemperature(75, 65, 85))

    def test_checkTemperature_below_range(self):
        self.assertFalse(checkTemperature(64, 65, 85))

    def test_checkTemperature_above_range(self):
        self.assertFalse(checkTemperature(86, 65, 85))
    
    def test_checkTemperature_at_lower_limit(self):
        self.assertTrue(checkTemperature(65,65,85))

    def test_checkTemperature_at_upper_limit(self):
        self.assertTrue(checkTemperature(85,65,85))

    def test_get_temperatures_for_colorado(self):
        json_data = getJsonData()
        result = get_temperatures_for_colorado(40, 2, -105, 2, 0, 2, 65, 85, json_data)
        expected = [
            {'lat': 40, 'lon': -105, 'withinRange': True},
            {'lat': 40, 'lon': -104, 'withinRange': True},
            {'lat': 39, 'lon': -105, 'withinRange': True},
            {'lat': 39, 'lon': -104, 'withinRange': False}
        ]
        self.assertEqual(result, expected)
        print(result, expected)

    def test_calculatePoints(self):
        json_data = getJsonData()
        result = calculatePoints(40, 2, -105, 2, 65, 85, 15, 18, json_data)
        expected = [
            {'lat': 40, 'lon': -105, 'withinRange': True},
            {'lat': 40, 'lon': -104, 'withinRange': False},
            {'lat': 39, 'lon': -105, 'withinRange': False},
            {'lat': 39, 'lon': -104, 'withinRange': False}
        ]
        self.assertEqual(result, expected)
if __name__ == '__main__':
    unittest.main()