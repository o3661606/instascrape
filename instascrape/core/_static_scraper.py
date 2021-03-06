from __future__ import annotations
#pylint: disable=no-member

import json
import datetime
from typing import Dict, Any, List
from abc import ABC, abstractmethod
import csv
import json

import requests
from bs4 import BeautifulSoup

from instascrape.scrapers.json_scraper import JsonScraper

class _StaticHtmlScraper(ABC):
    _METADATA_KEYS = ['json_dict', 'url', '_json_scraper', 'scrape_timestamp', 'map_dict', 'json_data']

    def __init__(self, url, name=None):
        """
        Parameters
        ----------
        url : str
            Full URL to an Instagram page
        """
        self.url = url
        self._json_scraper = JsonScraper()

    def load(self, keys: List[str] = [], exclude: List[str] = []):
        if type(keys) == str:
            keys = [keys]
        if type(exclude) == str:
            exclude = [exclude]
        self.json_dict = self._json_scraper.json_from_url(self.url)
        scraped_dict = self._json_scraper.parse_json(
                                json_dict=self.json_dict,
                                map_dict=self._Mapping.return_mapping(keys=keys, exclude=exclude)
                            )
        self._load_into_namespace(scraped_dict=scraped_dict)
        self.scrape_timestamp = datetime.datetime.now()

    def to_dict(self, metadata: bool = False) -> Dict[str, Any]:
        data_dict = {
            key: val
            for key, val in self.__dict__.items()
                if key not in self._METADATA_KEYS
        } if not metadata else self.__dict__
        return data_dict

    def to_csv(self, fp: str, metadata: bool = False):
        with open(fp, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.to_dict(metadata=metadata).items():
                writer.writerow([key, value])

    def to_json(self, fp: str, metadata: bool = False):
        with open(fp, 'w') as outjson:
            json.dump(self.to_dict(metadata=metadata), outjson)

    def __getitem__(self, key):
        return getattr(self, key)

    def _load_into_namespace(self, scraped_dict):
        for key, val in scraped_dict.items():
            setattr(self, key, val)



