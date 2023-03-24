README in `transkribus-custom-ner-de/sample`.

## Creator

This dataset was created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in 2022.

## License

This dataset is licensed under a Creative Commons Attribution 4.0 International License.

## File structure and overview

The input data stem from the digital collection "Stenographisches Protokoll der Verhandlungen des ... Zionisten-Kongresses ... in ..." (ZDB mark: 2176334-3, persistent link: https://sammlungen.ub.uni-frankfurt.de/cm/periodical/titleinfo/3476254) provided by the Goethe University Frankfurt. More specifically:


- [/sample/gold_standard.zip](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/sample/gold_standard.zip) is the protocol of 1897, automatically segmented and transcribed using PyLaya Transkribus Print M1 (model 39995) without manual corrections, manually annotated with `person` and `place` labels, exported as PAGE XML Zip file.
- [/sample/custom_ner_de_model](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/sample/custom_ner_de_model) is the custom model trained on the gold standard.
- [/sample/text_unanalyzed.txt](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/sample/text_unanalyzed.txt) is the protocol of 1899, automatically segmented and transcribed using PyLaya Transkribus Print M1 (model 39995) without manual corrections, exported as plain text file.
- [/sample/text_analyzed.txt](https://github.com/RISE-UNIBAS/transkribus-custom-ner-de/tree/main/sample/text_analyzed.txt) is the same protocol of 1899 but with `person` and `place` labels automatically extracted by the custom model.

