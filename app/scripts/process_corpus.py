import spacy
import sys
import os

# Import your add_domain_patterns function
from ner import add_domain_patterns

# Load spaCy model and add domain patterns
nlp = spacy.load("en_core_web_lg")
nlp = add_domain_patterns(nlp)

def process_corpus(nlp, corpus_path):
    """
    Process each line in the corpus file with the provided nlp object.
    Returns a list of spaCy doc objects, one for each line.
    """
    docs = []
    with open(corpus_path, "r") as f:
        for line in f:
            doc = nlp(line.strip())
            docs.append(doc)
    return docs