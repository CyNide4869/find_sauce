import time
import shutil
import json
import os
from pathlib import Path
from typing import BinaryIO
from io import TextIOWrapper
from tqdm import tqdm
from dotenv import load_dotenv
from saucenao_api import SauceNao, errors

load_dotenv()
current_directory = Path.cwd()
# Images whose sauce are to be found are placed in the 'images' folder in the current directory
images_directory = current_directory / 'images'
found_directory = images_directory / 'found'

# Place the api_key inside the .env file with the variable name API_KEY
API_KEY = os.environ.get('API_KEY')
sauce = SauceNao(API_KEY)

def append_to_file(output: dict, name: str, urls: list, file: TextIOWrapper) -> None:

    sauce, data = {}, {}
    last = len(output['sauces'])

    data['name'] = name.strip()
    for i, url in enumerate(urls, 1):
        temp = url.strip()
        temp = temp.strip('][').split(', ')
        sauce[i] = temp
    data['sauce'] = sauce
    data['_id'] = last + 1

    output['sauces'].append(data)

    json.dump(output, file, indent=4, sort_keys=True, encoding='utf8')

def find_sauce(img_name: str, bin_img: BinaryIO, count: int, output: dict, file: TextIOWrapper) -> int:

    try:
        results = sauce.from_file(bin_img)       
    except errors.ShortLimitReachedError as e:
        print(e)
        print('Waiting for 30 seconds.....')
        # Progress bar
        for i in tqdm(range(30), ncols=75):
            time.sleep(1)
        # Trying to fetch the sauce again after reaching the 30 second limit
        try:
            results = sauce.from_file(bin_img)
        except Exception as e:
            print(e)
            print(f'Found sauce for {count} images')
            return -1
    except errors.LongLimitReachedError as e:
        print(e)
        print(f'Found sauce for {count} images')
        exit()
    except Exception as e:
        print(e)
        print(f'Found sauce for {count} images')
        return -1

    print(f'\n-----{results.long_remaining} requests remaining-----\n')
    urls = []
    
    for i in range(len(results)):
        print(results[i].urls)
        urls.append(str(results[i].urls))

    append_to_file(output, img_name, urls, file)

    return results.status

def main() -> None:

    if not found_directory.exists():
        found_directory.mkdir()

    images = [item for item in images_directory.iterdir() if not item.is_dir()]
    for count, img in enumerate(images):
        
        # Opening the image in binary, open json in r+, if opened in w+ it deletes all the content
        with open('results.json', 'r+', encoding='utf8') as f, open(img.relative_to(current_directory), 'rb') as bin_img:
            print('\n{}'.format(img.name))
            data = json.load(f)
            res = find_sauce(img.name, bin_img, count, data, f)

        if not res:
            # Move the images to the found folder after the search is complete
            shutil.move(img.as_posix(), found_directory.as_posix())

if __name__ == '__main__':
    main()
