<p align="center">
    <img src="./assets/solvro.png">
</p>

# Solvro ML - PromoCHATor
<p align="justify"> 
W tym repozytorium znajduje się kod systemu rekomendacyjnego opartego na dużych modelach językowych. System w postaci chatbota, na podstawie dorobku naukowego pracowników Politechniki Wrocławskiej, dopasowywuje odpowiedniego promotora do podanego przez studenta tematu pracy dyplomowej
</p>

## Table of contents

1. **[Description](#description)**
2. **[Technologies](#technologies)**
3. **[Development](#development)**
   1. [Quick start](#quick-start)
   2. [Launching](#launching)
   2. [Data managment](#data-managment)
   3. [Github workflow](#github-workflow)
4. **[Current team](#current-team)**

## Description
<p align="justify"> 
This repository contains code of recommendation system, which is based on large language models. System should match supervisor for thesis title or description given by user
</p>

## Technologies
Project uses following languages and technologies
* Python 3
* LangChain
* WebUI

## Development
### Quick start
If you want to setup project locally

1. Create new virtual environment:

   If you use _conda_

   ```
   conda create --name your-environment-name python=3.10
   ```

   Alternatively use any other virtual enviroment manager of your choice.

2. Activate environment

   ```
   conda activate your-environment-name
   ```

3. Make sure you use recent _pip_ version

   ```
   python -m pip install --upgrade pip
   ```

4. Install packages

   ```
   python -m pip install -e .[dev]
   ```

5. Enable pre-commit

   ```
   pre-commit install
   ```

6. create `.env` file and paste your OpenAI API Key

   ```
   OPEN_AI_API_KEY = "<yourkey>"
   ```

After these steps project scripts are ready to launch

### Launching
T.B.C

### Data managment

Dataset should be kept in `data` folder. If you want to access solvro dataset, you could try to contact project manager or techlead

> [!WARNING]
> Please do not push dataset to remote repository


### Github workflow

When you had assigned yourself to new task, you should stick to these steps
1. `git checkout main` Check out main branch
2. `git pull origin main` Pull current changes from main branch
3. `git fetch` Be up to date with remote branches
4. `git checkout -b type/task` Create new task branch
5. `git add .` Add all changes we have made
6. `git commit -m "My changes description"` Commit changes with proper description
7. `git push origin type/task` Pushing our changes to remote branch
8. On Github we are going to make Pull Request (PR) from our remote branch

> [!WARNING]
> Do not push changes directly to main branch

For further information read Solvro handbook

**Github Solvro Handbook 🔥** - https://docs.google.com/document/d/1Sb5lYqYLnYuecS1Essn3YwietsbuLPCTsTuW0EMpG5o/edit?usp

## Current team
This is our current team
- [@LukiLenkiewicz](https://github.com/LukiLenkiewicz) - Tech Lead
- [@Micz26](https://github.com/Micz26) - ML Engineer
- [@farqlia](https://github.com/farqlia) - ML Engineer
- [@AgataGro](https://github.com/AgataGro) - ML Engineer
- [@dekompot](https://github.com/dekompot) - ML Engineer
- [@b4rt4s](https://github.com/b4rt4s) - ML Engineer
- [@Woleek](https://github.com/Woleek) - ML Engineer
- [@WiktoriaFrost](https://github.com/WiktoriaFrost) - ML Engineer
- [@Barionetta](https://github.com/Barionetta) - Project Manager