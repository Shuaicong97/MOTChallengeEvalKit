import json

from GROOT.util import read_json

if __name__ == "__main__":
    splits = ['mot17_test_coco', 'mot17_train_coco']
    for split in splits:
        path_to_json = f'/Users/tanveerhannan/data/groot/custom/{split}_captions.json'
        path_to_meta = f'/Users/tanveerhannan/data/groot/{split}.json'
        captions = read_json(path_to_json)
        meta = read_json(path_to_meta)
        videos = [m['name'][:-6] for m in meta[0]['videos']]

        video_dict = {}
        for video in videos:
            caption2ids = {}
            for cap in captions:
                if video in cap[0]:
                    for c in cap[1][0]:
                        if c in caption2ids:
                            caption2ids[c] += ", " +str(cap[0][-3:])
                        else:
                            caption2ids[c] = str(cap[0][-3:])
            sort_keys = sorted(caption2ids, key=lambda key: len(caption2ids[key]))
            caption2ids = {i: caption2ids[i] for i in sort_keys[::-1]}
            video_dict[video] = caption2ids

        with open(f"/Users/tanveerhannan/data/groot/custom/{split}_captions2ids.json", "w") as outfile:
            json.dump(video_dict, outfile, indent=1)
    print()