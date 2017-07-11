# Relationship Finder

Temporal Index for finding relationships between entities based on a temporal constraint

## Installation

- install python 2.7 and pip
- `pip install -r requirements.txt`

## Running

 - Download Yelp Challenge Dataset (https://www.yelp.com/dataset_challenge) and unzip to the project root in the folder, yelp_dataset_challenge_round9/
 - `python Approach1.py`
 - Follow the onscreen instructions

### Optional
 - **Create Index:** In Approach1.py, `create_index` function creates the index and saves it to a local file called index.json. It is sufficient to do it once.
 - **Load Index:** If the index already exists as `index.json` the line in `__main__` creating the index can be commented and the process starts from loading the index from index.json
 
## Contribute
 - Feel free to submit issues using the issues tab if any
 - Pull requests will be greatfully accepted
