import os
from pathlib2 import Path

import nltk
from nltk.tag import StanfordPOSTagger, StanfordNERTagger
from nltk import word_tokenize


def get_resource_dir():
    current_path = os.getcwd()
    res_path = os.path.abspath(os.path.join(current_path, "./res/"))
    return Path(res_path)


def default_pos_tag(text):
    text_tokenized = word_tokenize(text)
    return nltk.pos_tag(text_tokenized)


def _setup_java_home(java_path=None):
    os.environ['JAVAHOME'] = java_path or "C:/Program Files/Java/jdk1.8.0_201/bin/java.exe"


def stanford_pos_tag(text, java_path=None):
    _setup_java_home(java_path)
    model_name = "english-caseless-left3words-distsim.tagger"
    res_dir = get_resource_dir()
    stanfort_dir = res_dir.joinpath("stanford-postagger-full-2018-10-16")
    jar = str(stanfort_dir.joinpath("stanford-postagger-3.9.2.jar"))
    model = str(stanfort_dir.joinpath("models/{}".format(model_name)))

    st = StanfordPOSTagger(model, jar, encoding="utf8")

    text_tokenized = word_tokenize(text)
    return st.tag(text_tokenized)


def stanford_named_entity_tag(text, java_path=None):
    _setup_java_home(java_path)
    classifier_name = "english.all.3class.distsim.crf.ser.gz"
    res_dir = get_resource_dir()
    stanfort_dir = res_dir.joinpath("stanford-ner-2018-10-16")
    jar = str(stanfort_dir.joinpath("stanford-ner.jar"))
    model = str(stanfort_dir.joinpath("classifiers/{}".format(classifier_name)))

    st = StanfordNERTagger(model, jar, encoding="utf8")

    text_tokenized = word_tokenize(text)
    return st.tag(text_tokenized)