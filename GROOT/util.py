import json

def read_json(path_to_json):
    captions = []
    with open(path_to_json, 'r') as file:
        for line in file:
            captions.append(json.loads(line))
    return captions

def save_json_list(captions, path_to_json):
    with open(path_to_json, 'w') as outfile:
        for c in captions:
            json.dump(c, outfile)
            outfile.write('\n')