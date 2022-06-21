""" client.py

Client class ."""

from __future__ import annotations

from custom_ner_de.extract import extract_entities
from custom_ner_de.train import custom_ner_training
from datetime import datetime
from os import path
from requests import exceptions, Session
from spacy import Language
from tempfile import TemporaryDirectory, TemporaryFile
from typing import List
from warnings import filterwarnings
import shutil
import spacy

DIR = path.dirname(__file__)
PARENT_DIR = path.dirname(path.dirname(__file__))


class Client:
    """ Standalone client.

    :param entities: the extracted entities, defaults to None
    :param model_dir: the directory of the custom NER model, defaults to None
    :param model: the loaded custom NER model, defaults to None

    """

    def __init__(self,
                 entities: List[tuple] = None,
                 model_dir: TemporaryDirectory = None,
                 model: Language = None
                 ) -> None:
        self.entities = entities
        self.model_dir = model_dir
        self.model = model
        self.setup()

    def setup(self):
        """ Set up client. """

        self.model_dir = TemporaryDirectory()

    def train_model(self,
                    zip_url: str,
                    word_remove: List[str] = None,
                    person_names: List[str] = None,
                    location_names: List[str] = None,
                    epochs: int = 100) -> None:
        """ Train custom NER model.

        :param zip_url: URL to Zip file (PAGE XML) of annotated documents exported from Transkribus
        :param word_remove: list of words to remove, defaults to None
        :param person_names: person names to be included for entity ruler, defaults to None
        :param location_names: location names to be included for entity ruler, defaults to None
        :param epochs: number of training epochs, defaults to 100
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
                            epochs=epochs
                            )

    def save_model(self) -> None:
        """ Save custom NER model to /models/datetime. """

        save_dir = PARENT_DIR + "/models/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        shutil.copytree(self.model_dir.name, save_dir)
        print(f"Saved model to {save_dir}.")

    def load_model(self,
                   model_path: str = None) -> None:
        """ Load custom NER model to self.model.

        If no model_path is provided, an attempt is made to load the model from self.model_directory.

        :param model_path: complete path to model directory, defaults to None
        """

        if model_path is None:
            spacy.load(name=self.model_dir.name)
        else:
            spacy.load(name=model_path)


