"""
Author: Matt Nicholson
18 Jan 2020

A class to represent a FlightAware track log file
"""
import xml.etree.ElementTree as ET
import pandas as pd

from os.path import isfile

class TrackLog:
    """
    Class attributes
    -----------------
    f_path: str
        Absolute path of the track log KML file
    flight_num: str
        Flight number, including callsign
    date: str
        Date of the flight. Format: YYYY-MM-DD
    origin: str
        4-letter ICAO code of the origin airport
    dest: str
        4-letter ICAO code of the destination airport
    origin_coords: str
        Latitude, Longitude, and altitude of the origin airport.
        Format: lon, lat, alt. Lon & lat in decimal degrees, altitude in meters
    dest_coords: str
        Latitude, Longitude, and altitude of the destination airport.
        Format: lon, lat, alt. Lon & lat in decimal degrees, altitude in meters
    alt_mode: str
        Mode of the altitude measurements. 'Absolute' means above sea level
    time_stamps: list of str
        Time stamps related to the track points using zulu/GMT and a 24-hr clock.
        Format: YYYY-MM-DDTHH:MM:SSZ
    track_coords: list of str
        Flight track coordinates. Format: Lon, Lat, Alt.
        Lon & lat in decimal degrees, altitude in meters
    """
    def __init__(self, f_path):
        self.f_path =        f_path
        self.flight_num =    None
        self.date =          None
        self.origin =        None
        self.origin_coords = None
        self.dest =          None
        self.dest_coords =   None
        self.alt_mode =      None
        self.time_stamps =   None
        self.track_coords =  None
        self.parse_file()


    def parse_file(self):
        """
        Parse the KML track log file and extract the goodies
        """
        namespaces = {'default':"http://www.opengis.net/kml/2.2",
                      'google': "http://www.google.com/kml/ext/2.2"}

        if (not isfile(self.path)):
            raise FileNotFoundError('File does not exist {}'.format(self.path))

        track_tree = ET.parse(self.path)
        root = track_tree.getroot()

        for document in root.findall('default:Document', namespaces):

            # Get the three Placemark nodes
            placemarks = doc.findall('default:Placemark', namespaces)
            self._parse_apt_placemark(placemarks[0], namespaces, 'origin')
            self._parse_apt_placemark(placemarks[1], namespaces, 'dest')
            self._parse_data_placemark(placemarks[2], namespaces)


    def __repr__(self):
        return '<TrackLog object - {} {}-{} {}'.format(self.flight_num, self.origin,
                                                       self.dest, self.date)

#------------------------------ Helper Functions ------------------------------#

    def _parse_apt_placemark(self, placemark, namespaces, keyword):
        """
        Private helper function
        Get the airport data from the first/second placemark node

        Parameters
        ----------
        placemark : ElementTree Element
        namespaces: dict of xml namespaces
        keyword: str; either 'origin' or 'dest'
        """
        # Get the airport name
        for name in placemark.findall('default:name', namespaces):
            apt_name = name.text.split(' ')[0]

        # Get the coordinates of the airport
        for name in curr.findall('default:Point', namespaces):
            for p in name.findall('default:coordinates', namespaces):
                apt_coords = p.text

        if (keyword == 'origin'):
            self.origin = apt_name
            self.origin_coords = apt_coords
        elif (keyword == 'dest'):
            self.dest = apt_name
            self.dest_coords = apt_coords
        else:
            raise ValueError('Invalid placemark parse keyword')


    def _parse_data_placemark(self, placemark, namespaces):
        """
        Private helper function
        Get the flight data from the third placemark node

        Parameters
        ----------
        placemark : ElementTree Element
        namespaces: dict of xml namespaces
        """
        # Get flight num
        for name in placemark.findall('default:name', namespaces):
            self.flight_num = name.text

        # Get time stamps and track coords
        for track_node in curr.findall('google:Track', namespaces):
            for alt_mode in track_node.findall('default:altitudeMode', namespaces):
                self.alt_mode = alt_mode.text

            self.time_stamps = [x.text for x in track_node.findall('default:when', namespaces)]
            self.track_coords = [x.text for x in track_node.findall('google:coord', namespaces)]

            # Get the flight date from the first time stamp
            self.date = self.time_stamps[0].split('T')[0]
