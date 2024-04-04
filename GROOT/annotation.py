import os, json


def create_captions():
    max_track_id = 0
    for k in json_dict.keys():
        if 'categories' not in k:
            cap_dict = {}
            for c in json_dict[k]['annotations']:
                if c['track_id'] > max_track_id:
                    max_track_id = c['track_id']
                key = c['seq'][:-5] + '%03d' % c['track_id'] if 'mot' in k else str(c['video_id']) + "-" + '%05d' % c[
                    'track_id']
                if key in cap_dict:
                    cap_dict[key][1].append(c['image_id'])
                    cap_dict[key] = (cap_dict[key][0], [min(cap_dict[key][1]), max(cap_dict[key][1])])
                else:
                    cap_dict[key] = (c['captions'], [c['image_id']])

            myKeys = list(cap_dict.keys())
            myKeys.sort()
            cap_dict = {i: cap_dict[i] for i in myKeys}

            with open(path_to_json + '/custom/' + k.replace('.json', '') + '_captions.json', 'w') as outfile:
                for k, v in cap_dict.items():
                    json.dump((k, v), outfile)
                    outfile.write('\n')


if __name__ == "__main__":
    json_dict = []
    path_to_json = '/Users/tanveerhannan/data/groot'
    for pos_json in os.listdir(path_to_json):
        if pos_json.endswith('.json'):
            json_dict.append(pos_json)
        #     f = open(path_to_json+"/"+pos_json)
        #     json_dict[pos_json] = json.load(f)

    create_captions()


