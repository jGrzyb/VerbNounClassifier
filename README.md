# Verb Noun Classifier

This project is a simple semantic analyzer of Esperanto. It groups nouns based on what verb they appear after, which creates sets of nouns with simmilar meanings.

In order to run this program, you first need to provide text in Esperanto, that will serve as the basis of the analysis. You can either put your own text in `text.txt`, or run `textGetter.py` which will download the Bible in Esperanto from [sacred-texts.com](https://sacred-texts.com) and put it in said file.

Afterwards, run `program.py`. Results of the analysis will appear in `results.json`.