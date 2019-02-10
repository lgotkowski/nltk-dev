import nltk
import os


def check_nltk_data_packages():
    print "Checking nltk data packages..."
    nltk_data_path = os.path.join(os.getenv("APPDATA"), "nltk_data")
    data_dirs = {"corpora": "wordnet", "taggers": "averaged_perceptron_tagger", "tokenizers": "punkt", "help": "tagsets"}

    for dir, package_name in data_dirs.iteritems():
        if not os.path.exists(os.path.join(nltk_data_path, dir)):
            nltk.download(package_name)
        print "Package ready: '{}'".format(package_name)

    print "All packages ready!"