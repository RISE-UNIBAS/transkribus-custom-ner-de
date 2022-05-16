# Spacy_Model_Zionistenkongress
Named Entity Recognition for Persons and Locations - Pre-Trained Spacy Model &amp; Own Model



# Creator
This dataset was created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in May 2022. It is based on the digital collection of the Zionistenkongress in Basel 1897 xxxx

# File structure and data overview
Documentation of work in /docs 

Data in /files with

- text file as .txt of training and testing dataset
- code as Python file (.py) and as Jupyternotebook (.ipynb) with comments as description
- extracted entities from the .xml files to train the model as extensible markup language file (.xml)
- the model 
- extracted entities from the .xml files to train the model as text file (.txt)
- requirements file with the required packages and dependencies to run the code
- result of trained model based on training dataset as CSV file (.csv)
- result of already pre-trained model of the spacy german large package as CSV file (.csv)



# Data processing
- .xml files were extracted from the collection by importing the collection into Transkribus and then marking the PERSON (PER) and LOCATION (LOC) labels. Then the .xml files got exported (202) in an output file.
This output file was then inserted into the python script, which then parses the XML files and extracts the labels to convert them into the spacy format.

- Based on that the spacy format, a pipeline will be built on which the natural langauge processor (nlp) of the spacy package will be trained on. Therefore a "blank" model will be created within the python code where the trained information will be stored in.

- After that the spacy model will be trained using the annotation and the entities 
(Takes up to 3 hours depending on machine and on epochs/batches set)

- Saving the trained model in the output directory for the analysis later on and testing the sample inference using the trained model



# Data analysis



# Data presentation



