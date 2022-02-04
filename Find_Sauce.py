import time
from pathlib import Path
from saucenao_api import SauceNao

current_directory = Path.cwd()
# Images whose sauce are to be found are placed in the 'images' folder
images_directory = current_directory / 'images'

# Enter the api_key from saucenao by creating an account
sauce = SauceNao('<Replace this with the api key>')

def find_sauce(bin_img):
    try:
        results = sauce.from_file(bin_img)
    except Exception as e:
        print(e)
        exit()

    for i in range(len(results)):
        print(results[i].urls)

    return [results.long_limit, results.long_remaining, results.short_limit, results.short_remaining]

def main():

    for img in images_directory.iterdir():
        bin_img = open(img.relative_to(current_directory), 'rb')
        print('\n{}'.format(img.name))
        ll, lr, sl, sr = find_sauce(bin_img)
        bin_img.close()

        if lr == 0:
            print('\nLimit reached for today, run again in 24h\n')
            break

        if sr == 0:
            print('\nShort limit reached, waiting for 30 seconds .....\n')
            time.sleep(30)

if __name__ == '__main__':
    main()
