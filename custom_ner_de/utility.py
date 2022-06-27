""" utility.py

Utility class ."""

from __future__ import annotations

from pandas import DataFrame, read_csv
from zipfile import ZipFile
import os


class Utility:

    @staticmethod
    def load_text2csv(text_path: str) -> DataFrame:
        """ Load plain text as CSV.

        :param text_path: complete path to the plain text file including .txt extension
        """

        dataframe = read_csv(filepath_or_buffer=text_path,
                             engine="python",
                             delimiter="\n",
                             #sep=None,
                             #delim_whitespace=True,
                             header=None,
                             names=["text"])

        return dataframe

    @staticmethod
    def unzip(zip_path: str,
              unzip_path: str,
              verbose: bool = False) -> None:
        """

        :param zip_path: complete path to zip file including filename and extension
        :param unzip_path: complete path to folder
        :param verbose: flag for verbose output, defaults to False
        """

        with ZipFile(file=zip_path, mode="r") as zip_object:
            zip_object.extractall(path=unzip_path)
            if verbose is True:
                print(f"{len(os.listdir(unzip_path))} files unzipped to {unzip_path}.")
