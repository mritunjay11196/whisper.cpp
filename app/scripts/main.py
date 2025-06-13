import spacy
import os
from analyze_output import process_corpus, nlp

corpus_path = os.path.join(os.path.dirname(__file__), "corpus.txt")
docs = process_corpus(nlp, corpus_path)

# Example statement
example_statement = "change layer to metal 1 drawing"
doc = nlp(example_statement)

# Print entities for the example statement
for ent in doc.ents:
    print(ent.text, ent.label_)