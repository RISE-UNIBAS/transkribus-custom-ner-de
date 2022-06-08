"""
filename : accuracy_calculation.py

This script is responsible for calculating accuracy of the data using custom trained model and pre-trained model.

Execution time : 
"""
import warnings
warnings.filterwarnings('ignore')
from spacy.training import Example
import spacy


def load_data():
    """
    function to load entity data

    input ::
        
    output ::
        - Entity data to use for accuracy calculation
    """

    print("loading data...")
    file1=open('../sample/extracted_entities.txt') #put the "extracted_entities.txt" file into the working directory -> change name here if you renamed the file which contains the entities of persons and locations

    lines = file1.readlines()

    for i in range(len(lines)):
        lines[i] = eval(lines[i])

    return lines


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

def calculate_custom_model_accuracy(data):
    """
    function to calculate accuracy of custom trained entity model

    input ::
        - list containing entity data
        
    output ::
        - accuracy metrics 
    """

    nlp = load_custom_spacy_model("path/to/your/filesde_spacy_custom_v2") #change directory here to your path for the custom trained model

    print("Calculating score...")
    new_test_data = []

    for text, annots in data:
        new_test_data.append(Example.from_dict(nlp.make_doc(text), annots))

    scores_model = nlp.evaluate(new_test_data)

    #print scores that you want
    precision_model = scores_model["ents_p"]
    recall_model = scores_model["ents_r"]
    f_score_model = scores_model["ents_f"]
    scores_entities = scores_model["ents_per_type"]

    print("================ Accuracy scores using custom trained model =================\n")
   
    print("================= Overall scores =================\n")
    print("Precision : ",precision_model)
    print("Recall : ",recall_model)
    print("F1 Score : ",f_score_model)
   
    print("\n================= Entity wise score =================\n")
   
    print("============= Person Entity score =================\n")
    print("Precision : ",scores_entities['PERSON']['p'])
    print("Recall : ",scores_entities['PERSON']['r'])
    print("F1 Score : ",scores_entities['PERSON']['r'])

    print("\n============= Location Entity score =================\n")
    print("Precision : ",scores_entities['LOC']['p'])
    print("Recall : ",scores_entities['LOC']['r'])
    print("F1 Score : ",scores_entities['LOC']['r'])


def calculate_pre_trained_model_score(data):
    """
    function to calculate accuracy of custom trained entity model

    input ::
        - list containing entity data
        
    output ::
        - accuracy metrics 
    """

    # using spact large german model
    nlp = spacy.load("de_core_news_lg")

    print("\n\nCalculating score...")
    new_test_data = []

    for text, annots in data:
        new_test_data.append(Example.from_dict(nlp.make_doc(text), annots))

    scores_model = nlp.evaluate(new_test_data)

    #print scores that you want
    precision_model = scores_model["ents_p"]
    recall_model = scores_model["ents_r"]
    f_score_model = scores_model["ents_f"]
    scores_entities = scores_model["ents_per_type"]

    print("\n================ Accuracy scores using Pre-trained large model =================\n")
   
    print("================= Overall scores =================\n")
    print("Precision : ",precision_model)
    print("Recall : ",recall_model)
    print("F1 Score : ",f_score_model)
   
    print("\n================= Entity wise score =================\n")
   
    print("============= Person Entity score =================\n")
    print("Precision : ",scores_entities['PERSON']['p'])
    print("Recall : ",scores_entities['PERSON']['r'])
    print("F1 Score : ",scores_entities['PERSON']['r'])

    print("\n============= Location Entity score =================\n")
    print("Precision : ",scores_entities['LOC']['p'])
    print("Recall : ",scores_entities['LOC']['r'])
    print("F1 Score : ",scores_entities['LOC']['r'])



data = load_data()

calculate_custom_model_accuracy(data)

calculate_pre_trained_model_score(data)