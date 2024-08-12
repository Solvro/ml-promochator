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
   python -m pip install -e .[dev]
   ```

5. Enable pre-commit
   ```
   pre-commit install
   ```

## Scrpits

1. scrape_scholarly.py

    ```
    python scripts/scrape_scholarly.py
    ```

2. recomend.py

    ```
    python scripts/recomend.py --question="your question"
    ```
