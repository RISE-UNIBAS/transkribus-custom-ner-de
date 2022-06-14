"""
filename : train_custom_spacy_ner.py

This script is responsible for reading XML files from specified folder and extracting all entites and training the model.

It will store all the extracted entities in txt file for reference and will use it for model training.

Execution time : 25 minutes on Google Colab CPU instance.
"""
import warnings
warnings.filterwarnings('ignore')

import os
import xml.etree.ElementTree as ET
from __future__ import unicode_literals, print_function
import plac
import random
from pathlib import Path
import spacy
from tqdm import tqdm
from spacy.util import minibatch, compounding
from spacy.training import Example
from spacy.pipeline import EntityRuler


### below function is the algorithm to extract entities from all the XML files from given folder
def extract_entities(folder_path, word_remove):
    """
    function to extract entites from XML files

    input ::
        - folder_path : folder which contains all the XML files
        - word_remove : list of words that needs to be ignored

    output ::
        - All the extracted entities will be stored in a txt file
        - returns an array containing labels to use it further in training.
    """

    xml_files = os.listdir(folder_path)
    xml_files = sorted(xml_files)

    print("Totla number of files available in this folder :: {0}".format(len(xml_files)))

    final_all_ents_tuple = []
    all_sentences_present = []

    #looping over all the files
    for j in range(len(xml_files)):

        print("processing file=================================== ", xml_files[j])
        
        mytree = ET.parse(folder_path+xml_files[j])
        myroot = mytree.getroot()

        for x in myroot[1][1]:  ## looping over each Textline in the particular XML file
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

                            ## following if-else condition is written as there are some labels which has 'continued:true' means there are more word belong to current word
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
                
                            # checking if word is part of words to remove
                            if not list(set(sentence[a:a+b].split(" ")) & set(word_remove)):
                                ent_tuple = [a, a+b, ent] #single list as per the format defined by spacy3.3
                                all_ents.append(ent_tuple)

                    # following loop is written because in there are some samples which has overlapping range, this loop handles those overlapping words as they are already covered.
                    all_ents_copy = all_ents.copy()
                    for k in range(len(all_ents)-1):
                        if all_ents[k][0] <= all_ents[k+1][0] <= all_ents[k][1] or all_ents[k][0] <= all_ents[k+1][1] <= all_ents[k][1]:
                            try:
                                del all_ents_copy[k+1]
                            except:
                                del all_ents_copy[k]

                    final_tuple = (sentence, {'entities' : all_ents_copy})
                    final_all_ents_tuple.append(final_tuple)  #this variable holds all the tuples from all the files

    # storing all the labels in txt file 
    with open("../sample/extracted_entities.txt", "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(str(item) for item in final_all_ents_tuple))

    return final_all_ents_tuple


# below function is for training custom spacy model
def custom_ner_training(final_all_ents_tuple, output_dir, person_names, location_names):
    """
    function to train the spacy NER model on extracted entities

    input ::
        - final_all_ents_tuple : a list containig tuples of extracted entities in format defined by Spacy
        - output_dir : directory path to store the trained model
        - person_name : names to be included for Entity ruler
        - location_names : names to be included for entity ruler

    output ::
        - Trained model will be exported in specified folder
    """

    model = None
    output_dir=Path(output_dir) #output folder in which trained model will be stored
    n_iter=100 #number of training epochs

    ## load the blank model
    if model is not None:
        nlp = spacy.load(model)  
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('de')  
        print("Created blank 'de' model")

    #set up the pipeline
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe('ner')

    person_patterns = []

    for i in range(len(person_names)):
        person_patterns.append({"label": "PERSON", "pattern": person_names[i]})

    location_patterns = []

    for i in range(len(location_names)):
        location_patterns.append({"label": "LOC", "pattern": location_names[i]})

    patterns = person_patterns + location_patterns

    # Creating Entity Ruler with custom patterns
    cfg = {"overwrite_ents": True}
    nlp.add_pipe('entity_ruler', before='ner', config=cfg).add_patterns(patterns)
    nlp.to_disk(output_dir)
    
    # adding data
    for _, annotations in final_all_ents_tuple:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    print("Starting training for {0} epochs.....".format(n_iter))

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

    # training code
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(final_all_ents_tuple)
        losses = {}
        # batch up the examples using spaCy's minibatch
        batches = minibatch(final_all_ents_tuple, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            example = []
            # Update the model with iterating each text
            for i in range(len(texts)):
                doc = nlp.make_doc(texts[i])
                example.append(Example.from_dict(doc, annotations[i]))
            
            # Update the model
            nlp.update(example, drop=0.5, losses=losses)
            print("Losses", losses)

    print("Training completed.....")
    #saving trained model in directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)



## change below path with directory path where all the XML files stored
folder_path = "C:/Users/User/kaushal/Protokoll-Zionistenkongress-Basel_1897-0200/"

# add words in the list to remove
word_remove = ["BASEL", "HÃ¤ndeklatschen"]

# function call to extract entities
final_all_ents_tuple = extract_entities(folder_path, word_remove)

# list of words to be added as person in training using entity ruler
person_names = ['Gustav Gottheil', 'Juden']

# list of words to be added as location in training using entity ruler
location_names = ['Boston', 'Roman']

# function call to start NER training
output_dir = "C:/Users/User/NER/de_spacy_custom_v2"
custom_ner_training(final_all_ents_tuple, output_dir, person_names, location_names)

print("All the extracted entities stored in a file...")