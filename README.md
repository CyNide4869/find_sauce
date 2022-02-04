# Find Sauce

Script to find sauce (source) of images present locally, useful when images are to be searched in bulk.
Uses saucenao's api to perform the reverse image search.

To use this script, create an account on saucenao and get the api_key from the account settings and place it in the script.

## Folder Structure

The parent folder or the root folder has to consist of Find_Sauce.py and another folder named 'images' which consists the images whose sauce is to be searched / found.

## Run

To run the script, first install all the dependencies from requirements.txt
```
pip install -r requirements.txt
```
Open the terminal in the current folder and run
```
python Find_Sauce.py
```

# Links

[saucenao website](https://saucenao.com/)\
[saucenao api module](https://github.com/nomnoms12/saucenao_api)
