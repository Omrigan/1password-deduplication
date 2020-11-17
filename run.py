import os
import subprocess
import json
subp = subprocess.run("op list items".split(" "), capture_output=True)
objs = json.loads(subp.stdout)
print(objs[0])
import tqdm

result_objs = []
for obj in tqdm.tqdm(objs):
    uuid = obj['uuid']
    subp = subprocess.run("op get item".split(" ") + [uuid], capture_output=True)
    obj2 = json.loads(subp.stdout)
    fs = obj2['details'].get('fields')
    if not fs:
        continue
    name = obj['overview']['title']

    obj1 = (uuid, name, fs)

    for obj2 in result_objs:
        if (obj1[1] in obj2[1] or obj2[1] in obj1[1]) and obj1[2] == obj2[2]:
            print("Duplicate found!")
            print(obj1)
            print(obj2)
            print()
            if obj1[1] in obj2[1]:
                uuid = obj2[0]
            else:
                uuid = obj1[0]
            cmd = "op delete item".split(" ") + [uuid]
            print(cmd)
            print(subprocess.run(cmd))

    result_objs.append(obj1)
