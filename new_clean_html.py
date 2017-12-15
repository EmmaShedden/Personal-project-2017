import os
from library import np2t


with open("fakenews.txt") as fid:

    for count, url in enumerate(fid):
        
        url = url.rstrip()

        if os.path.exists(os.path.join("raw_text", str(count + 1))):
            continue
        text = np2t(url)
        if text is None:
            continue
        gid = open(os.path.join("raw_text", str(count + 1)), "w")
        gid.write(text)
        gid.close()

with open("realnews.txt") as fid:

    for count, url in enumerate(fid):
        
        url = url.rstrip()

        if os.path.exists(os.path.join("real_text", str(count + 1))):
            continue
        text = np2t(url)
        if text is None:
            continue
        gid = open(os.path.join("real_text", str(count + 1)), "w")
        gid.write(text)
        gid.close()
