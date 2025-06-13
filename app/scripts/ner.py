import spacy
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts')))
from tech import objects, params, instances, layers, purposes

def add_domain_patterns(nlp):
    """Add domain-specific NER patterns to a spaCy pipeline."""
    ruler = nlp.add_pipe(
        "entity_ruler",
        before="ner",
        config={"phrase_matcher_attr": "LOWER"}  # <-- add this line
    )
    patterns = []
    patterns += [{"label": "OBJECT", "pattern": obj} for obj in objects]
    patterns += [{"label": "PARAM", "pattern": param} for param in params]
    patterns += [{"label": "INSTANCE", "pattern": inst} for inst in instances]
    patterns += [{"label": "LAYER", "pattern": layer} for layer in layers]
    patterns += [{"label": "PURPOSE", "pattern": purpose} for purpose in purposes]
    ruler.add_patterns(patterns)
    return nlp