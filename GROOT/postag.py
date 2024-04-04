from GROOT.util import read_json, save_json_list

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('all-nltk')

def postag(txt):
    tokenized = sent_tokenize(txt)
    for i in tokenized:
        # Word tokenizers is used to find the words
        # and punctuation in a string
        wordsList = nltk.word_tokenize(i)

        # removing stop words from wordList
        #wordsList = [w for w in wordsList if not w in stop_words]

        #  Using a Tagger. Which is part-of-speech
        # tagger or POS-tagger.
        tagged = nltk.pos_tag(wordsList)

        return tagged


if __name__ == "__main__":
    stop_words = set(stopwords.words('english'))
    path_to_json = '/Users/tanveerhannan/data/groot/custom/mot17_train_coco_captions_naive_compound.json'
    captions = read_json(path_to_json)

    tags = []
    for cap in captions:
        tags.append(postag(cap[1][0]))
    save_json_list(tags, path_to_json.replace('.json', '') + '_postag.json')

    verbs = {}
    for tag in tags:
        if tag is not None:
            for t in tag:
                if 'VB' in t[1]:
                    if t[0] in verbs:
                        verbs[t[0]] += 1
                    else:
                        verbs[t[0]] = 1

    print()