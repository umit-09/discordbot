import json
import pickle
import os

# Read banner_template.json file
with open('banner-template.json', 'r') as f:
    banner_template = json.load(f)

# Write banner_template to banner.bin file
def write_banner_template():
    with open('banner.bin', 'wb') as fp:
        pickle.dump(banner_template, fp)
    os.system('cls')
    print('banner.bin:\n')
    print(json.dumps(banner_template, indent=4))

write_banner_template()
