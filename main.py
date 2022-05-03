import time
import shutil
import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')
url = f"https://saucenao.com/search.php?output_type=2&testmode=1&numres=8&db=999&hide=0&api_key={api_key}"
print(url)
