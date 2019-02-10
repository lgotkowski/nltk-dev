from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn


def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = max([synset.path_similarity(ss) for ss in synsets2])

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    # Average the values
    score /= count
    return score


def symmetric_sentence_similarity(sentence1, sentence2):
    """ compute the symmetric sentence similarity using Wordnet """
    return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) / 2


def find_item(scentence):
    items = ["box", "sphere", "pen", "ship", "glass", "table", "coffee", "bottle"]
    for item in items:
        if item in scentence:
            return item


def find_name(scentence):
    names = ["Fussel", "Phine", "Peter", "Justin"]
    for name in names:
        if name in scentence:
            return name


def adjust_scentences(sentences, data):
    for key, value in data.iteritems():
        print key, value
        adjusted = []
        for sentence in sentences:
            print "Before: " + sentence
            if key in sentence:
                adjusted_scentence = sentence.replace(key, value)
                adjusted.append(adjusted_scentence)
            print "After: " + adjusted_scentence
        sentences = adjusted

    return sentences


if __name__ == "__main__":
    import prepare
    print "Start"

    prepare.check_nltk_data_packages()

    sentences = [
        "PERSON be MOOD.",
        "PERSON follow the ITEM.",
        "Can you smile PERSON?",
        "PERSON please walk to the LOCATION.",
        "PERSON look at me.",
        "PERSON can you bring me the ITEM?",
        "PERSON bring me the ITEM."
    ]

    focus_sentence = "Take the pen and bring it to me immediately, Fussel."

    print "Orig Scentence: {}".format(focus_sentence)

    item = find_item(focus_sentence)
    name = find_name(focus_sentence)

    data = {"PERSON": name, "ITEM": item}

    sentences = adjust_scentences(sentences, data)

    print "Adjust Scentence: {}".format(focus_sentence)

    print ""
    for sentence in sentences:
        score = symmetric_sentence_similarity(focus_sentence, sentence)
        print "Score: '{}' : {}".format(sentence, score)
        print ""
    print "End"