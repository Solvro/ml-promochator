# PromoCHATor

## Installation

1. Create new virtual environment:
   If you use _conda_:

   ```
   conda create --name your-environment-name python=3.10
   ```

   Alternatively use any other virtual enviroment manager of your choice.

2. Activate environment
   ```
   conda activate your-environment-name
   ```
3. Make sure you use recent _pip_ version:
   ```
   python -m pip install --upgrade pip
   ```
4. Install packages:

   ```
   python -m pip install -e .
   ```

5. Enable pre-commit
   ```
   pre-commit install
   ```
6. create .env file and paste your Open Ai Api Key
   ```
   OPEN_AI_API_KEY = "your api key"
   ```

## Scrpits

1. scrape_scholarly.py

   ```
   python scripts/scrape_scholarly.py
   ```

Before running recomend.py, please ensure that you have downloaded the authors_with_papers.csv file from the (promochator dataset)[https://drive.google.com/drive/folders/1odcaykO5uGtJXGugjCm8UioFT2XWWHNM]. Place the file in the data folder within your project directory.

2. recomend.py

   ```
   python scripts/recomend.py --question="your's question"
   ```
