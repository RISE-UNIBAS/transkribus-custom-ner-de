""" client.py

Session class ."""

from __future__ import annotations

from custom_ner_de.extract import extract_entities
from custom_ner_de.train import custom_ner_training
from datetime import datetime
from os import path
from requests import exceptions, Session
from tempfile import TemporaryDirectory, TemporaryFile
from typing import List
from warnings import filterwarnings
import shutil


DIR = path.dirname(__file__)
PARENT_DIR = path.dirname(path.dirname(__file__))


class Client:
    """ Standalone client for Binder.

    :param entities: the extracted entities, defaults to None
    :param model_dir: the directory of the custom model, defaults to None

    """

    def __init__(self,
                 entities: List[tuple] = None,
                 model_dir: TemporaryDirectory = None,
                 ) -> None:
        self.entities = entities
        self.model_dir = model_dir
        self.setup()

    def setup(self):
        """ Set up client. """

        self.model_dir = TemporaryDirectory()

    def run(self,
            zip_url: str,
            word_remove: List[str],
            person_names: List[str],
            location_names: List[str]) -> None:
        """ Run client.

        :param zip_url: URL to Zip file (PAGE XML) of annotated documents exported from Transkribus
        :param word_remove: list of words to remove, defaults to None
        :param person_names: person names to be included for entity ruler, defaults to None
        :param location_names: location names to be included for entity ruler, defaults to None
        """

        filterwarnings('ignore')

        print(f"Downloading Zip file...", end=" ")
        download = TemporaryFile()
        try:
            download.write(Session().get(url=zip_url).content)
        except exceptions.RequestException as e:
            raise SystemExit(e)
        print(f"done.")

        print(f"Extracting entities...", end=" ")
        self.entities = extract_entities(zip_path=download,
                                         word_remove=word_remove)
        download.close()
        print(f"done.")

        custom_ner_training(entities=self.entities,
                            save_dir=self.model_dir.name,
                            person_names=person_names,
                            location_names=location_names,
                            epochs=1  # debug
                            )

    def save(self) -> None:
        """ Save model to /models/datetime. """

        save_dir = PARENT_DIR + "/models/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        shutil.copytree(self.model_dir.name, save_dir)
        print(f"Saved model to {save_dir}.")





