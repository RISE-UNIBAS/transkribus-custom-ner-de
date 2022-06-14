"""
filename : inference_custom_model_test_data.py

This script is responsible for using custom trained model and generate results on input data.

This script has 2 entity detection functions, first for single text and second for entire dataframe or list.

It will print the results on terminal and save it in csv file.

Execution time : <1 second for single text i/p, 20 seconds on test data provided.
"""

import warnings
warnings.filterwarnings('ignore')

import spacy
import pandas as pd

def load_custom_spacy_model(model_path):
    """
    function to load the custom trained spacy model

    input ::
        - folder_path : folder which contains model

    output ::
        - model
    """

    print("Loading model from {0}\n".format(model_path))
    nlp = spacy.load(model_path)

    return nlp

def generate_prediction_single_text(nlp, text, word_remove):
    """
    function to extract the entities of single text

    input ::
        - nlp : custom trained spacy model
        - text : input text for which entites needs to be extracted
        - word_remove : list of words that needs to be ignored

    output ::
        - extracted entites
    """

    doc = nlp(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON' and ent.text not in word_remove]
    locations = [ent.text for ent in doc.ents if ent.label_ == 'LOC' and ent.text not in word_remove]

    print("Input text : {0}".format(text))
    print("All the Person present in input text : {0}".format(persons))
    print("All the Location present in input text : {0}".format(locations))

def generate_prediction_list(nlp, data, word_remove):
    """
    function to extract the entities from input list

    input ::
        - nlp : custom trained spacy model
        - data : input list for which entites needs to be extracted
         - word_remove : list of words that needs to be ignored

    output ::
        - all_persons : list containg extracted entites for persons
        - all_locations : list containg extracted entites for locations
    """

    all_persons = []
    all_locations = []

    for i in range(len(data)):
        doc = nlp(data[i])
        persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON' and ent.text not in word_remove]
        locations = [ent.text for ent in doc.ents if ent.label_ == 'LOC' and ent.text not in word_remove]
        all_persons.append(persons)
        all_locations.append(locations)

    return all_persons, all_locations


#loading custom trained spacy model
model_path = ".../de_spacy_custom" # todo: change path
nlp = load_custom_spacy_model(model_path)

# add words in the list to remove
word_remove = ["BASEL", "HÃ¤ndeklatschen"]

print("Running single input extraction...\n")

#extracting entites from single text
single_input = "Dr. Friedemann aus Berlin,"
generate_prediction_single_text(nlp, single_input)

print("\nRunning list input extraction...\n")

#extracting entities from list
df = pd.read_csv('C:/Users/User/kaushal/03_Protokoll-Zionistenkongress-Basel_1899.txt', delimiter = "\n", header=None, names=["text"])
data = list(df['text'])

all_persons, all_locations = generate_prediction_list(nlp, data)

df['Custom-trained_Spacy_Person'] = pd.Series(all_persons)
df['Custom-trained_Spacy_Location'] = pd.Series(all_locations)

# storing results in csv file
df.to_csv('Custom_NER_inference_results.csv',index=False)

print("results stored in csv file....")