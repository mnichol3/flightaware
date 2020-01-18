import unittest
from os.path import join

from tracklog import TrackLog

class TestTrackLog(unittest.TestCase):
    def setUp(self):
        f_path = '/media/Poseidon/data/flightaware/track-logs'
        f_name = 'FlightAware_UAL5316_KMRY_KSFO_20200114.kml'
        f_in = join(f_path, f_name)

        self.test_file = TrackLog(f_in)


    # Test basic functionality of the TrackLog classs
    def test_tracklog_1(self):
        origin = self.test_file.origin
        dest = self.test_file.dest
        date = self.test_file.date

        self.assertEquals(origin, 'KMRY')
        self.assertEquals(dest, 'KSFO')

        self.assertEquals(date, '2020-01-14')


if __name__ == '__main__':
    unittest.main()
