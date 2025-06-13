import os
from process_corpus import process_corpus, nlp

if __name__ == "__main__":
    corpus_path = os.path.join(os.path.dirname(__file__), "corpus.txt")
    docs = process_corpus(nlp, corpus_path)

    # Example: process a single statement
    example_statement = "change layer to poly drawing"
    doc = nlp(example_statement)
    for ent in doc.ents:
        print(ent.text, ent.label_)