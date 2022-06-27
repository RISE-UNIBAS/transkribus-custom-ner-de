""" gold_standard.py

GoldStandard class.
"""

from custom_ner_de.utility import Utility
from dataclasses import dataclass
from random import randint
from typing import List
import os
import tempfile
import xml.etree.ElementTree as ET


@dataclass
class GoldStandard:
    full: List[tuple] = None
    training: List[tuple] = None
    validation: List[tuple] = None

    def make(self,
             zip_path: str,
             save_path: str = None,
             word_remove: List[str] = None) -> None:
        """ Make full gold standard from Zip file.

        Zip file must be created by exporting annotated document from Transkribus as PAGE XML.

        :param zip_path: complete path to zip file including filename and .zip extension
        :param save_path: complete path to save file including filename and .txt extension, defaults to None
        :param word_remove: list of words to remove, defaults to None
        """

        if word_remove is None:
            word_remove = []

        # unzip Zip file to memory:
        with tempfile.TemporaryDirectory() as tmpdir:
            Utility.unzip(zip_path=zip_path,
                          unzip_path=tmpdir)
            xml_files = os.listdir(tmpdir)
            xml_files = sorted(xml_files)

            final_all_ents_tuple = []
            all_sentences_present = []

            # looping over all the files:
            for j in range(len(xml_files)):

                mytree = ET.parse(tmpdir + "/" + xml_files[j])
                myroot = mytree.getroot()

                for x in myroot[1][1]:  # looping over each TextLine in the particular XML file
                    if x.tag.endswith('TextLine'):
                        if "person" in x.attrib['custom'] or "place" in x.attrib['custom']:

                            ents = x.attrib['custom'].split(" ")[2:]
                            sentence = x[-1][0].text
                            all_sentences_present.append(sentence)

                            all_ents = []

                            for i in range(0, len(ents)):
                                if ents[i] in ['person', 'place']:
                                    if ents[i] == 'person':
                                        ent = 'PERSON'
                                    else:
                                        ent = 'LOC'

                                    a = int(ents[i+1].split(":")[1][:-1])

                                    # labels with "continued:true" are such that more words belong to current word:
                                    if ents[i+2].endswith("}"):
                                        b = int(ents[i+2].split(":")[1][:-2])
                                    else:
                                        try:
                                            i += 4
                                            b1 = int(a[i+1].split(":")[1][:-1])
                                            if ents[i+2].endswith("}"):
                                                b2 = int(ents[i+2].split(":")[1][:-2])
                                            else:
                                                b2 = int(ents[i+2].split(":")[1][:-1])
                                                b = b1 + b2
                                        except:
                                            i -= 4
                                            b = int(ents[i+2].split(":")[1][:-1])

                                    # checking if word is part of words to remove:
                                    if not list(set(sentence[a:a + b].split(" ")) & set(word_remove)):
                                        ent_tuple = [a, a + b, ent]  # single tuple as per the format defined by spacy
                                        all_ents.append(ent_tuple)
                                    else:
                                        continue

                            # in case of overlapping range exclude words that already covered:
                            all_ents_copy = all_ents.copy()
                            for k in range(len(all_ents)-1):
                                if all_ents[k][0] <= all_ents[k+1][0] <= all_ents[k][1] or all_ents[k][0] <= all_ents[k+1][1] <= all_ents[k][1]:
                                    try:
                                        del all_ents_copy[k+1]
                                    except:
                                        del all_ents_copy[k]

                            final_tuple = (sentence, {'entities' : all_ents_copy})
                            final_all_ents_tuple.append(final_tuple)

            # saving all the labels in .txt file:
            if save_path is not None:
                with open(save_path, "w", encoding="utf-8") as outfile:
                    outfile.write("\n".join(str(item) for item in final_all_ents_tuple))

        self.full = final_all_ents_tuple

    def split(self,
              training_size: int = 90) -> None:
        """ Split full gold standard into training and validation sets.

        :param training_size: size of validation set in percent, defaults to 10
        """

        try:
            assert self.full is not None
        except AssertionError:
            raise "Error: Gold standard not defined! Exiting."
        full_copy = self.full.copy()
        threshold = int((len(full_copy) / 100) * training_size)
        self.validation = []
        while len(full_copy) > threshold:
            line = randint(0, len(full_copy) - 1)
            self.validation.append(full_copy[line])
            del full_copy[line]
        self.training = full_copy
        print(f"done (training: {len(self.training)}, validation: {len(self.validation)}).")
