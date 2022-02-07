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

def find_sauce(img_name: str, bin_img: BinaryIO, count: int, output: TextIOWrapper) -> int:

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
    output.write(f'\n{img_name}\n')
    
    for i in range(len(results)):
        print(results[i].urls)
        output.write(f'{results[i].urls}\n')

    return results.status

def main() -> None:

    if not found_directory.exists():
        found_directory.mkdir()

    images = [item for item in images_directory.iterdir() if not item.is_dir()]
    for count, img in enumerate(images):
        
        # Opening the image in binary
        with open('results.txt', 'a') as output, open(img.relative_to(current_directory), 'rb') as bin_img:
            print('\n{}'.format(img.name))
            res = find_sauce(img.name, bin_img, count, output)

        if not res:
            # Move the images to the found folder after the search is complete
            shutil.move(img.as_posix(), found_directory.as_posix())

        # 30s limits 6 images, hence 6 * 5s = 30s, results in maximum of 6 requests in 30s 
        time.sleep(5)

if __name__ == '__main__':
    main()
