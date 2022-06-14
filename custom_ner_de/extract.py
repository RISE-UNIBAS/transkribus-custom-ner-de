""" extract.py

This script is responsible for reading XML files from specified folder and extracts Person and Places available.

It will print all the extracted entites and will also the store results in a text file.

Execution time : 4 seconds for given 202 XML files.
"""

from custom_ner_de.utility import Utility
from typing import List
import os
import tempfile
import xml.etree.ElementTree as ET


def extract_entities(zip_path: str,
                     save_path: str = None,
                     word_remove: List[str] = None,
                     verbose: bool = False) -> List[tuple]:
    """ Extract entities from Zip file.

    Zip file must be created by exporting from Transkribus as PAGE XML.

    :param zip_path: complete path to zip file including filename and .zip extension
    :param save_path: complete path to save file including filename and .txt extension, defaults to None
    :param word_remove: list of words to remove, defaults to None
    :param verbose: flag for verbose output, defaults to False
    """

    if word_remove is None:
        word_remove = []

    # unzip Zip file to memory:
    with tempfile.TemporaryDirectory() as tmpdir:
        Utility.unzip(zip_path=zip_path,
                      unzip_path=tmpdir)
        xml_files = os.listdir(tmpdir)
        xml_files = sorted(xml_files)

        if verbose is True:
            print("Total number of files available in this folder :: {0}".format(len(xml_files)))

        final_all_ents_tuple = []
        all_sentences_present = []

        # looping over all the files:
        for j in range(len(xml_files)):

            if verbose is True:
                print("processing file=================================== ", xml_files[j])

            mytree = ET.parse(tmpdir + "/" + xml_files[j])
            myroot = mytree.getroot()

            for x in myroot[1][1]:  # looping over each TextLine in the particular XML file
                if x.tag.endswith('TextLine'):
                    if "person" in x.attrib['custom'] or "place" in x.attrib['custom']:

                        ents = x.attrib['custom'].split(" ")[2:]
                        if verbose is True:
                            print(ents)
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

                                # some labels have "continued:true" meaning there are more words belonging to current word:
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
                        if verbose is True:
                            print(final_tuple)
                        final_all_ents_tuple.append(final_tuple)  # this variable holds all the tuples from all the files
                        if verbose is True:
                            print("=="*50)

        # saving all the labels in .txt file:
        if save_path is not None:
            with open(save_path, "w", encoding="utf-8") as outfile:
                outfile.write("\n".join(str(item) for item in final_all_ents_tuple))

    return final_all_ents_tuple
