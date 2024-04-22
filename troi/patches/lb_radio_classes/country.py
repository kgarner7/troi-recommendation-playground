import logging
from time import sleep

import requests

import troi.patch
from troi import TARGET_NUMBER_OF_RECORDINGS
from troi.plist import plist
from troi import Element, ArtistCredit, Recording, PipelineError, DEVELOPMENT_SERVER_URL

logger = logging.getLogger(__name__)


class LBRadioCountryRecordingElement(Element):
    '''
        Given a country, return recordings for that country.

        Arguments:
            area_name: the name of the area to make a playlist for
    '''

    def __init__(self, area_name, mode):
        super().__init__()
        self.area_name = area_name
        self.mode = mode

    @staticmethod
    def inputs():
        return []

    @staticmethod
    def outputs():
        return [Recording]

    def lookup_area(self, area_name):

        while True:
            r = requests.get("http://musicbrainz.org/ws/2/area?query=%s&fmt=json" % area_name)
            if r.status_code == 503:
                sleep(1)
                continue

            if r.status_code != 200:
                raise PipelineError("Cannot fetch country code from MusicBrainz. HTTP code %s" % r.status_code)

            return r.json()['areas'][0]['id']

    def recording_from_row(self, row):
        if row['recording_mbid'] is None:
            return None

        r = Recording(mbid=row['recording_mbid'])
        if 'artist_credit_name' in row:
            r.artist = ArtistCredit(name=row['artist_credit_name'])

        if 'recording_name' in row:
            r.name = row['recording_name']

        if 'year' in row:
            r.year = row['year']

        if 'listen_count' in row:
            r.listenbrainz = {"listen_count": row["listen_count"]}

        return r

    def read(self, inputs):

        start, stop = {"easy": (66, 100), "medium": (33, 66), "hard": (0, 33)}[self.mode]
        area_mbid = self.lookup_area(self.area_name)
        args = [{"[area_mbid]": area_mbid}]
        r = requests.post(DEVELOPMENT_SERVER_URL + "/popular-recordings-by-country/json", json=args)
        if r.status_code != 200:
            raise PipelineError("Cannot fetch first dataset recordings from ListenBrainz. HTTP code %s (%s)" %
                                (r.status_code, r.text))

        self.data_cache = self.local_storage["data_cache"]
        self.data_cache["element-descriptions"].append("country %s" % self.area_name)

        recordings = plist()
        for row in r.json():
            recordings.append(self.recording_from_row(row))

        return recordings.random_item(start, stop, TARGET_NUMBER_OF_RECORDINGS)
