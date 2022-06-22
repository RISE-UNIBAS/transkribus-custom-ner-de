""" client.py

Client class ."""

from __future__ import annotations

import os.path

from custom_ner_de.extract import extract_entities
from custom_ner_de.predict import predict
from custom_ner_de.train import custom_ner_training
from datetime import datetime
from os import path
from pandas import DataFrame, read_csv, Series
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
                 model: Language = None,
                 input_text: DataFrame = None,
                 result=None,
                 ) -> None:
        self.entities = entities
        self.model_dir = model_dir
        self.model = model
        self.input_text = input_text
        self.result = result
        self.setup()

    def setup(self):
        """ Set up client. """

        self.model_dir = TemporaryDirectory()
        if os.path.isdir(PARENT_DIR + "/user_output/") is False:
            os.mkdir(PARENT_DIR + "/user_output/")

    def train_model(self,
                    zip_url: str,
                    word_remove: List[str] = None,
                    person_names: List[str] = None,
                    location_names: List[str] = None,
                    epochs: int = 100,
                    _local: bool = False) -> None:
        """ Train custom NER model.

        :param zip_url: URL to Zip file (PAGE XML) of annotated documents exported from Transkribus
        :param word_remove: list of words to remove, defaults to None
        :param person_names: person names to be included for entity ruler, defaults to None
        :param location_names: location names to be included for entity ruler, defaults to None
        :param epochs: number of training epochs, defaults to 100
        :param _local: toggle interpreting text_url as complete path to text instead of URL, defaults to False
        """

        filterwarnings('ignore')

        if _local is True:
            print(f"Extracting entities...", end=" ")
            self.entities = extract_entities(zip_path=zip_url,
                                             word_remove=word_remove)
            print(f"done.")
        else:
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

    def save_model(self,
                   save_dir: str = None) -> None:
        """ Save custom NER model.

        If no save directory is provided, the model is saved to /user_output/models/.

        :param save_dir: complete path to model directory, defaults to None
        """

        if save_dir is None:
            if os.path.exists(PARENT_DIR + "/user_output/models/") is False:
                os.mkdir(path=PARENT_DIR + "/user_output/models/")
            save_dir = PARENT_DIR + "/user_output/models/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        shutil.copytree(self.model_dir.name, save_dir)
        print(f"Saved model to {save_dir}.")

    def load_model(self,
                   model_path: str = None) -> None:
        """ Load custom NER model to self.model.

        If no model_path is provided, an attempt is made to load the model from self.model_directory.

        :param model_path: complete path to model directory, defaults to None
        """

        if model_path is None:
            self.model = spacy.load(name=self.model_dir.name)
        else:
            self.model = spacy.load(name=model_path)

    def apply_model(self,
                    text_url: str,
                    model_path: str = None,
                    _local: bool = False) -> None:
        """ Apply a custom NER model to a text.

        If no model is provided, an attempt is made to load the model from self.model_directory.

        :param text_url: URL to plain text file
        :param model_path: complete path to model directory, defaults to None
        :param _local: toggle interpreting text_url as complete path to text instead of URL, defaults to False
        """

        filterwarnings('ignore')

        if _local is True:
            self.input_text = self.load_text2csv(text_path=text_url)
        else:
            print(f"Downloading TXT file...", end=" ")
            download = TemporaryFile()
            try:
                download.write(Session().get(url=text_url).content)
            except exceptions.RequestException as e:
                raise SystemExit(e)
            self.input_text = self.load_text2csv(text_path=download)
            download.close()
            print(f"done.")

        print(f"Loading custom NER model...", end=" ")
        try:
            self.load_model(model_path=model_path)
        except Exception as e:
            raise SystemExit(e)
        print(f"done.")

        print(f"Applying custom NER model to TXT file...", end=" ")
        persons, locations = predict(model=self.model,
                                     dataframe=self.input_text)
        self.result = self.input_text.copy()
        self.result["persons"] = Series(persons)
        self.result["locations"] = Series(locations)
        print(f"done.")

    @staticmethod
    def load_text2csv(text_path: str) -> DataFrame:
        """ Load plain text as CSV.

        :param text_path: complete path to the plain text file including .txt extension
        """

        dataframe = read_csv(filepath_or_buffer=text_path,
                             engine="python",
                             delimiter="\n",
                             header=None,
                             names=["text"])

        return dataframe

    def save_result2csv(self,
                        save_path: str = None) -> None:
        """ Save result as CSV-file.

        If no save path is provided, the result is saved to /user_output/results/.

        :param save_path:
        """

        if save_path is None:
            if os.path.exists(PARENT_DIR + "/user_output/results/") is False:
                os.mkdir(path=PARENT_DIR + "/user_output/results/")
            save_path = PARENT_DIR + "/user_output/results/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
        self.result.to_csv(path_or_buf=save_path, index=False)
        print(f"Saved result to {save_path}.")
