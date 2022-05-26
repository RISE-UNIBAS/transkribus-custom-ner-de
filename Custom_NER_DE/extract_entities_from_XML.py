"""
filename : extract_entities_from_XML.py

This script is responsible for reading XML files from specified folder and extracts Person and Places available.

It will print all the extracted entites and will also the store results in a text file.

Execution time : 4 seconds for given 202 XML files.
"""

import os
import xml.etree.ElementTree as ET


### below function is the algorithm to extract entities from all the XML files from given folder
def extract_entities(folder_path):
    """
    function to extract entites from XML files

    input ::
        - folder_path : folder which contains all the XML files

    output ::
        - All the extracted entities will be printed on terminal
        - All the extracted entities will be stored in a txt file
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
                
                            ent_tuple = [a, a+b, ent] #v2 update as per spacy 3.3.0 single list as per the format defined by spacy
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
                    print(final_tuple)
                    final_all_ents_tuple.append(final_tuple)  #this variable holds all the tuples from all the files
                    print("=="*50)

    # storing all the labels in txt file 
    with open("extracted_entities.txt", "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(str(item) for item in final_all_ents_tuple))


## change below path with directory path where all the XML files stored
folder_path = "C:/Users/User/kaushal/Protokoll-Zionistenkongress-Basel_1897-0200/"

# function call to extract entities
extract_entities(folder_path)

print("All the extracted entities stored in a file...")