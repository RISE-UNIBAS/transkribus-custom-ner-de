# Tutorial

## Introduction

This document serves as a step-by-step guide to running a Named Entitiy Recogniticon algorithm
with Natural Language Processing via the Python script in [!todo add specific path].
This is important so that the user can train his/her own machine learning model by marking people and
places in the text of Transkribus.
This allows the user not only to use the already pre-trained Spacy model to recognize named entities,
but also to train his own text to better match the document model to be analyzed.
A mixture of the already existing Large Package from the spacy library and the own trained model
can lead to significantly better results.
Thus, a whole text can be taken to train the labels and then other texts to analyze, or if only one text
is available, split it to train the algorithm based on it and apply it to the remaining text.
As a rule, the model should be trained with about 70%-80% of the text base and applied to 20%-30%
to test this.
Afterwards, this trained model can be used to analyze texts that have not been seen before.
Ultimately, the more data these NLP algorithms are fed, the more accurate the text analysis models
will be.



![image](https://user-images.githubusercontent.com/62709221/171058157-3471e2d2-7e34-4c56-bb52-8e91446d9a5b.png)

## Step 1: Prepare document for training using Transkribus Expert Client

In order to prepare a collection of documents with [Transkribus Expert Client](https://readcoop.eu/transkribus/download/) (version 1.19 or above) so that it can be used to train a spaCy model for named entity recognition, take the following sub-steps (tutorials on how to use the Transkribus Expert Client are provided by [READ-COOP](https://readcoop.eu/transkribus/resources/how-to-guides/)):

1. Create a collection in Transkribus and upload all relevant documents. Automatically or manually segment and transcribe the documents, and carry out corrections if necessary. Be sure that you are happy with the result since there is no going back.
2. Choose a representative sample of all documents. Think about the required sample size and make sure to include as much variety as possible.
3. Define which entities you want to annotate and specify annotation guidelines. [!todo add link to annotation best practices]
4. Annotate the representative sample. Try to ensure that annotations across all documents are consistent. Of course, annotation guidelines will likely be amended during the annotation process; simply try to be explicit in recording all decisions you are taking.
5. If you are happy with the result, export the annotated representative sample (again, there is no going back from here).

---

This is the Transkribus Expert Client interface that is displayed when opening a document in a collection. Here we see the title page of [!todo link to specific file].
Here you can navigate (as marked in yellow) to the "Overview".

![image](https://user-images.githubusercontent.com/62709221/171058207-23dd404c-dc9c-4780-90a1-3c566b424bd1.png)

In the "Overview" it is then possible for the user to navigate to the individual scanned pages of the
text.
Here, the next step is to select a page and then navigate to "Metadata" after the selection.

![image](https://user-images.githubusercontent.com/62709221/171058248-20ad346b-8613-400d-84d8-faabf936c912.png)

After navigating to "Metadata", the user is able to select via "Textual" and then under "Customize"
the respective colors and tags with which to mark the respective persons and places within the text.

![image](https://user-images.githubusercontent.com/62709221/171058284-b2fe7496-dd34-4d92-b869-7e41f5385d84.png)

If the user wants to annotate a place or a person (as in Step 4), he has to mark the respective word in
the window (bottom right) and then click on the button marked in red.
In this example, we can see that the word Egypt has been marked and should be annotated as
"place".

![image](https://user-images.githubusercontent.com/62709221/171058299-412a0ec9-8824-43cb-b734-d5e2d512a2a5.png)

The next step is to save your changes (Step 5 - highlighted in green) before navigating to the next
page via Overview.

![image](https://user-images.githubusercontent.com/62709221/171058321-c2add96a-26c6-469f-a0b1-2f8a07c47220.png)

As soon as you are done with a page, you can mark it as "Done" (see green marker in Figure 6).
Once the user has finished labeling the people and places, he can view the results (see blue marker in

![image](https://user-images.githubusercontent.com/62709221/171058367-9c62de01-541a-4688-ad12-6574f038b4cb.png)

In this figure you can see which window opens for the user afterwards. Here the user can specify the
location of his export ("client export" ) and how the data should be named ("File/Folder name").

To export the text as .txt the user has to mark "Export text files" and to export the .xml files with the
labels he has set before "Export page".
The .xml pages are then used for the python script, as well as the text file.

![image](https://user-images.githubusercontent.com/62709221/171058409-b25aef4e-ac79-4777-ae40-3d669431b502.png)

## STEP 2)
In order to use the Python script or the JupyterNotebook, the following interfaces must be adapted
for the user.
The adjusting spots for the script will also be visible as comments in the code to be able to run the
code.
Adjustments are marked in yellow!
In the third cell it is important to specify the path where the zip file with the XML files of the
individual pages is located (see screenshot – yellow marked).
The XML files should contain the labels with the entities like the persons and the places/locations.
Furthermore, it would be important to upload the zip file to the JupyterNotebook.
All results will be stored in the following path "/content/de_spacy_custom"
In addition, the test text and the training text should also be loaded into the Jupyternotebook or
placed in the directory accessed by the code.
The code can take between 2-3 hours to run depending on the machine and the dataset.

![image](https://user-images.githubusercontent.com/62709221/171058445-37dd04e7-7017-4950-992e-3311a0d90ccc.png)
![image](https://user-images.githubusercontent.com/62709221/171058453-86f50f89-0ba5-4a6e-91ed-fdb784f79a0d.png)
![image](https://user-images.githubusercontent.com/62709221/171058459-8c7b3775-fcc1-4a5c-ab53-534de24d2480.png)

In the next figure you can see the next interface that has to be adapted in order to run the code.
Here the text file must be uploaded and the text file must be adapted which should be used to test
the model!

![image](https://user-images.githubusercontent.com/62709221/171058539-696f4e47-82cc-4da4-b8e2-7f22d6a10999.png)

![image](https://user-images.githubusercontent.com/62709221/171058563-ef067b89-afca-4ba2-b65c-3ec884719909.png)
![image](https://user-images.githubusercontent.com/62709221/171058569-3b5b0c14-2fd8-44bd-b30c-814c007bd2c5.png)

In the next screenshot it is necessary to adjust the name of the CSV file, if you want to give the file a
different name.
The file contains the results of the text dataset, which is examined with the own train model.

![image](https://user-images.githubusercontent.com/62709221/171058579-33d02a52-9035-4b39-90be-28099f2898f2.png)
![image](https://user-images.githubusercontent.com/62709221/171058589-5946a7ec-5f29-4288-a377-96c38aefddae.png)

In the yellow marked cell (see figure below) you have to read the csv dataset that was generated to
test the self-trained model on the test text.
(If the name has been adjusted in the previous step, it must be adjusted here in exactly the same
way).

![image](https://user-images.githubusercontent.com/62709221/171058603-92a8b56e-2557-430e-826a-13efaef33f5a.png)

In the next figure, the user can rename the file that shows the results of the self-trained model + the
already existing model from spacy.

![image](https://user-images.githubusercontent.com/62709221/171058612-593847d1-2659-4ffb-a674-d04d1ce4df6a.png)

If the user does not want to have certain names/persons or places/locations included in the analysis,
the following part can be used:

![image](https://user-images.githubusercontent.com/62709221/171058627-a9a010af-985b-42dd-904b-c4c390a0e4ff.png)

Word just need to be inserted here in this list, separated by a comma. These terms will be removed
for the analysis and for training the model.
Another functionality of the script is that words (persons/names) and/or (locations/places) can be
added to a list which will be added to an entity ruler.
These terms and words will be included in the model if not detected by the model itself or if they
were forgotten in the first step of identifying persons or locations.

![image](https://user-images.githubusercontent.com/62709221/171058651-b76a6fe0-a5ee-46b4-9cd7-5e5af1275766.png)

This can be done after the analysis if the results in the .csv file did not include a certain name of a
person or a place.
The user just needs to add those names into the “person_names” list for persons or in the
“location_names” list for the places. If multiple words needs to be included and added manually to
the pipeline, then the user needs to separate those words within the list with a comma (“,”).


## STEP 3)
In order to evaluate the custom trained model and the pre-trained spacy model, the
“accuracy_calculation.py” can be used (or respectively the Notebook version of it).

This guideline explains how to use it in order to get the precision, the recall and the F1-score of the
models.
- It is important to have the text file with the already pre-defined entities of the persons and
the locations in the same directory path as the code
- This file is called “extracted_entities.txt” but may differ if renamed before
The first function included in the script loads the entity data and process it in order to be able to
calculate the accuracy with it.
The second function “def load_custom_spacy_model” loads the custom trained spacy model done in
STEP 2.
- It is important to set the folder_path with the model the same way as the working directory
of the “accuracy_calculation.py” (or the Notebook version) is.
- This function returns a model which will be used for calculations of the scores.

The third function “def calculate_custom_model_accuracy” takes the data with the entities as an
input and generates the accuracy metrics
- Set the path for the “nlp” object to the path where your saved model is stored.
The fourth function “def calculate_pre_trained_model_score” loads the de_core_news_lg package
from spacy, which is the large already pre-trained model and calculates the scores based on that.

![image](https://user-images.githubusercontent.com/62709221/171058681-acd633bf-883d-4291-8652-3b054c010287.png)

![image](https://user-images.githubusercontent.com/62709221/171058688-95b21078-8afb-4db8-a78a-6008ab26a4ad.png)

![image](https://user-images.githubusercontent.com/62709221/171058696-02759234-3822-450b-9828-14ba026d3b2e.png)

The functions for the evaluation will be added to the jupyter notebook, enabling the user to only use
this.
The pathways still needs to be adapted to the files/folders of the working directory.


