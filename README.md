# Seek Scraper
Scrapes data from Seek

## Requirements
Any python 3.x installation will work for this app

## Installation
1. Clone this repo on your PC
2. Create a virtual environment to be used for this app. In the project directory, run: python -m venv venv
3. Activate virtual environment: venv/Scripts/activate
4. pip install -r requirements.txt

## Using the scripts
1. Run python SeekScraperPh1.py to collect job posting links
2. Run python SeekScraperPh2.py to collect details for each job posting collecting in Ph1
3. This will produce database file seek.db in the root directory which can be seen in grafana/tableau or similar dashboarding tools.
