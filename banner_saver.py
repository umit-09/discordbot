import json
import os

# Read banner_template.json file
with open('banner-template.json', 'r') as f:
    banner_template = json.load(f)

# Write banner_template to banner.json file
def write_banner_template():
    with open('banner.json', 'w') as fp:
        json.dump(banner_template, fp, indent=4)
    os.system('cls')
    print('banner.json:\n')
    print(json.dumps(banner_template, indent=4))

write_banner_template()
