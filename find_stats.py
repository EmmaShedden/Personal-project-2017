import os
import json
import nltk
from library import find_stats

stats = []

for file in os.listdir("raw_text"):
    fname = os.path.join("raw_text", file)
    fid = open(fname)
    text = fid.read()
    fid.close()

    if len(text) == 0:
        continue

    stats_dict = {"file_id" : file}

    stats_dict.update(find_stats(text))

    stats.append(stats_dict)

gid = open("stats.json", "w")
gid.write(json.dumps(stats))
gid.close()

#real news

real_stats = []

for file in os.listdir("real_text"):
    fname = os.path.join("real_text", file)
    fid = open(fname)
    text = fid.read()
    fid.close()

    if len(text) == 0:
        continue

    real_stats_dict = {"file_id" : file}

    real_stats_dict.update(find_stats(text))

    real_stats.append(real_stats_dict)

gid = open("real_stats.json", "w")
gid.write(json.dumps(real_stats))
gid.close()
