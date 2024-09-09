# PromoCHATor

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
   3. [Docker](#docker)
   3. [Example docker usage](#docker-usage)
   4. [Data managment](#data-managment)
   5. [Github workflow](#github-workflow)
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
1. scrape_scholarly.py

   ```
   python scripts/scrape_scholarly.py
   ```

Before running recomend.py, please ensure that you have downloaded the authors_with_papers.csv file from the [promochator dataset](https://drive.google.com/drive/folders/1odcaykO5uGtJXGugjCm8UioFT2XWWHNM). Place the file in the data folder within your project directory.

2. recomend.py

   ```
   python scripts/recomend.py --question="your's question"
   ```

### Docker

It is also possible to use PromoCHATor's API. To do it go to project's directory and run

   ```
   docker build -t <app name> .
   ```

Then run

   ```
   docker run  -p 8000:8000 <app name>
   ```

### Example docker usage

   ```
   curl -X POST "http://localhost:8000/recommend" \
      -H "Content-Type: application/json" \
      -d '{"data": "Deep Generative Models"}'
   ```

response:

```
{"response":"\n1. Supervisor's name: dr hab. inż. Maciej Zięba\nFaculty: Faculty of Information and Communication Technology\nResearch papers:\n- Ensemble boosted trees with synthetic features generation in application to bankruptcy prediction\n- Boosted SVM for extracting rules from imbalanced data in application to prediction of the post-operative life expectancy in the lung cancer patients\n- Classification restricted Boltzmann machine for comprehensible credit scoring model\n- Adversarial autoencoders for compact representations of 3D point clouds\n- Bingan: Learning compact binary descriptors with a regularized gan\n\n2. Supervisor's name: prof. dr hab. inż. Jerzy Świątek\nFaculty: Faculty of Information and Communication Technology\nResearch papers:\n- Boosted SVM for extracting rules from imbalanced data in application to prediction of the post-operative life expectancy in the lung cancer patients\n- Generative adversarial networks: recent developments\n- System analysis techniques in ehealth systems: A case study\n- Ensemble classifier for solving credit scoring problems\n- Accelerated learning for restricted Boltzmann machine with momentum term\n\n3. Supervisor's name: dr inż. Dariusz Więcek\nFaculty: Faculty of Information and Communication Technology\nResearch papers:\n- Smart connected logistics\n"}
```

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
