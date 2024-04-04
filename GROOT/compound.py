from GROOT.postag import postag
from GROOT.util import read_json, save_json_list


def naive_caption(captions):
    for caption in captions:
        cap = ""
        for i, c in enumerate(caption[1][0]):
            if i == 0:
                cap = c
            else:
                cap = cap + " and " + c
        caption[1][0] = cap
    return captions

def naive_caption_postag(captions):
    for caption in captions:
        cap = ""
        for i, c in enumerate(caption[1][0]):
            if i == 0:
                cap = c
            else:
                tag = postag(c)
                first_noun = True
                for t in tag:
                    if "V" in t[1] and first_noun:
                        first_noun = False
                        cap = cap + " and"
                    if not first_noun:
                        cap = cap + " " + t[0]
                if first_noun:
                    cap = cap + " and " + c
        caption[1][0] = cap
    return captions

if __name__ == "__main__":
    path_to_json = '/Users/tanveerhannan/data/groot/custom/mot17_train_coco_captions.json'
    captions = read_json(path_to_json)
    captions = naive_caption_postag(captions)
    save_json_list(captions, path_to_json.replace('.json', '') + '_naive_compound_postag.json')
