import time
from pathlib import Path
import shutil
from typing import BinaryIO
from io import TextIOWrapper
from tqdm import tqdm
from saucenao_api import SauceNao, errors

current_directory = Path.cwd()
# Images whose sauce are to be found are placed in the 'images' folder in the current directory
images_directory = current_directory / 'images'
found_directory = images_directory / 'found'

# Enter the api_key from saucenao by creating an account
sauce = SauceNao('<Replace this with the api key>')

def find_sauce(img_name: str, bin_img: BinaryIO, count: int, output: TextIOWrapper) -> None:

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
            exit()
    except Exception as e:
        print(e)
        print(f'Found sauce for {count} images')
        exit()

    print(f'\n-----{results.long_remaining} requests remaining-----\n')
    output.write(f'\n{img_name}\n')
    
    for i in range(len(results)):
        print(results[i].urls)
        output.write(f'{results[i].urls}\n')

def main() -> None:

    if not found_directory.exists():
        found_directory.mkdir()

    images = [item for item in images_directory.iterdir() if not item.is_dir()]
    for count, img in enumerate(images):
        # Opening the image in binary
        bin_img = open(img.relative_to(current_directory), 'rb')
        output = open('results.txt', 'a')

        print('\n{}'.format(img.name))
        find_sauce(img.name, bin_img, count, output)

        bin_img.close()
        output.close()

        # Move the images to the found folder after the search is complete
        shutil.move(img.as_posix(), found_directory.as_posix())

if __name__ == '__main__':
    main()
