"""
filename : train_custom_spacy_ner.py

This script is responsible for reading XML files from specified folder and extracting all entites and training the model.

It will store all the extracted entities in txt file for reference and will use it for model training.

Execution time : 2 hours 10 minutes on Google Colab CPU instance.
"""

from __future__ import unicode_literals, print_function
import os
import xml.etree.ElementTree as ET
import plac
import random
from pathlib import Path
import spacy
from tqdm import tqdm


### below function is the algorithm to extract entities from all the XML files from given folder
def extract_entities(folder_path):
    """
    function to extract entites from XML files

    input ::
        - folder_path : folder which contains all the XML files

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
                
                            ent_tuple = (a, a+b, ent) #single tuple as per the format defined by spacy
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
    with open("extracted_entities.txt", "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(str(item) for item in final_all_ents_tuple))

    return final_all_ents_tuple


# below function is for training custom spacy model
def custom_ner_training(final_all_ents_tuple, output_dir):
    """
    function to train the spacy NER model on extracted entities

    input ::
        - final_all_ents_tuple : a list containig tuples of extracted entities in format defined by Spacy
        - output_dir : directory path to store the trained model

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

    # adding data
    for _, annotations in final_all_ents_tuple:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    print("Starting training for {0} epochs.....".format(n_iter))

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(final_all_ents_tuple)
            losses = {}
            for text, annotations in tqdm(final_all_ents_tuple):
                nlp.update(
                    [text],  
                    [annotations],  
                    drop=0.5,  
                    sgd=optimizer,
                    losses=losses)
            print(losses)

    print("Training completed.....")
    #saving trained model in directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)



## change below path with directory path where all the XML files stored
folder_path = "C:/Users/User/NER/Protokoll-Zionistenkongress-Basel_1897-0200/"

# function call to extract entities
final_all_ents_tuple = extract_entities(folder_path)

# function call to start NER training
output_dir = "C:/Users/User/NER/de_spacy_custom"
custom_ner_training(final_all_ents_tuple, output_dir)

print("All the extracted entities stored in a file...")