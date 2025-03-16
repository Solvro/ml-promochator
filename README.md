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
This repository contains code of recommendation system, which is based on large language models. System should match supervisor for thesis title or description given by user

## Technologies
Project uses following languages and technologies
* Python 3
* LangChain
* LangGraph
* FastAPI
* WebUI

## Development
### Quick start
If you want to set up project locally

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

6. create `.env` file and fill it according to template below

   ```
   OPENAI_API_KEY="<yourkey>"
   SESSION_SECRET_KEY="<random_string>"
   DB_USERNAME=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   DB_DATABASE=
   ```

7. Download the `final_data_and_vectorstore.zip` archive from the [promochator dataset](https://drive.google.com/drive/folders/1odcaykO5uGtJXGugjCm8UioFT2XWWHNM). Unpack archive and place both folders `data` and `vectorstores` within project directory.

After these steps project scripts are ready to launch


### Launching

1. To launch in console
   ```
   python src/graph.py
   ```
2. To launch web server
   ```
   python main.py
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
   curl -X POST "http://localhost:8000/recommend/invoke" \
   -H "Content-Type: application/json" \
   -d '{"input": {"question": "Deep Generative Models", "faculty": "Faculty of Information and Communication Technology"}}'
   ```

response:

```
{"output":{"hello_message":"Here are some recommended thesis supervisors for your project on Deep Generative Models:","recommended_supervisors":[{"name":"dr inż. Marcin Michalski","faculty":"Faculty of Mechanical and Power Engineering","papers":[{"title":"Are gans created equal? a large-scale study","description":"sets random tuning empirical goodfellow2014generative scores hard finally despite results arise propose models optimization algorithms activity computed measures metrics improvements experimental based tested precision higher numerous conduct outperforms recall algorithm in\\cite rich limitations data restarts algorithmic overcome find assess subclass leading enough computational generative suggest introduced systematic evaluation reach multi-faceted current better study budget networks art research changes several consistently interesting perform large-scale adversarial procedures objective state-of-the evidence gan still similar powerful hyperparameter non-saturating future neutral suggests others fundamental also"},{"title":"Towards accurate generative models of video: A new metric & challenges","description":"new sets play images synthesizing e 2 high processing metric propose provide results models image visual presentation metrics synthetic purely samples capture success challenging requiring well representation scv deep objects custom initial remarkable lack coherence benchmark data successful complexity generated 1 scenarios videos challenge scene following generative starcraft capabilities current contribute fr\\ temporal real-world model correlates progress next study hampered important game distance attempts gap lead step confirms recent large-scale dynamics consider formulating chet wide advances human quality harder fvd task addition application much terms learning video diversity extent qualitative judgment"},{"title":"Google research football: A novel reinforcement learning environment","description":"new license open-source play permissive showcase physics-based three customize environments simpler trained ideas results provide propose algorithms manner dqn provides experiments challenging tested introduce academy safe diverse accelerated resulting available baseline games scenarios football advanced novel promising impala agents full-game environment 3d reinforcement multiplayer ape-x difficulty used progress research commonly several field simulator benchmarks recent reproducible multi-agent virtual use google ppo addition quickly easy varying set learning video support also directions report"}]},{"name":"dr inż. arch. Marcin Michalski","faculty":"Faculty of Architecture","papers":[{"title":"Are gans created equal? a large-scale study","description":"several objective algorithm outperforms computed suggest state-of-the arise random research art tested precision models reach similar also current improvements algorithms generative higher finally non-saturating numerous limitations changes despite find subclass overcome still hyperparameter propose study tuning empirical scores restarts evaluation evidence large-scale gan conduct hard systematic multi-faceted goodfellow2014generative consistently networks budget future neutral in\\cite measures data perform assess based rich fundamental sets metrics computational enough interesting results algorithmic introduced leading powerful better activity experimental optimization procedures adversarial recall others suggests"},{"title":"Towards accurate generative models of video: A new metric & challenges","description":"complexity objects application processing capture extent success custom gap chet model important presentation terms provide hampered deep image models current initial generative lead purely judgment synthetic scenarios starcraft step challenging scv play remarkable formulating following synthesizing much task propose visual human study images representation dynamics attempts 1 large-scale harder temporal benchmark metric confirms challenge correlates real-world advances videos data qualitative capabilities 2 e addition sets generated recent progress metrics diversity video distance contribute quality results learning fvd high well next fr\\ scene lack successful coherence game samples consider new requiring wide"},{"title":"Google research football: A novel reinforcement learning environment","description":"manner several 3d physics-based agents promising advanced customize full-game use trained multi-agent research provide tested also support google algorithms multiplayer baseline quickly environment dqn scenarios permissive simulator safe football ape-x challenging play simpler provides virtual introduce propose resulting difficulty novel showcase impala reinforcement diverse available ppo directions license addition recent academy progress set video ideas accelerated report results learning field games varying open-source environments used easy three benchmarks reproducible experiments new commonly"}]},{"name":"dr hab. inż. Maciej Zięba","faculty":"Faculty of Information and Communication Technology","papers":[{"title":"Adversarial autoencoders for compact representations of 3D point clouds","description":"extend capable meaningful accept simultaneously complex compact existing input ... conducted end-to-end 3d output aae train approach used representation challenging generate clouds deep separate images solution descriptors training space objects create goal provide method architectures present tasks novel thanks generation work including cloud point moreover adversarial achieve 3-dimensional way points first model contrary obtain latent learning models representations reconstruction learn generative compression clustering binary shape also allows methods decoupled autoencoder shapes"}]},{"name":"dr Marcin Michalski","faculty":"Faculty of Pure and Applied Mathematics","papers":[{"title":"Are gans created equal? a large-scale study","description":"several objective algorithm outperforms computed suggest state-of-the arise random research art tested precision models reach similar also current improvements algorithms generative higher finally non-saturating numerous limitations changes despite find subclass overcome still hyperparameter propose study tuning empirical scores restarts evaluation evidence large-scale gan conduct hard systematic multi-faceted goodfellow2014generative consistently networks budget future neutral in\\cite measures data perform assess based rich fundamental sets metrics computational enough interesting results algorithmic introduced leading powerful better activity experimental optimization procedures adversarial recall others suggests"},{"title":"Towards accurate generative models of video: A new metric & challenges","description":"complexity objects application processing capture extent success custom gap chet model important presentation terms provide hampered deep image models current initial generative lead purely judgment synthetic scenarios starcraft step challenging scv play remarkable formulating following synthesizing much task propose visual human study images representation dynamics attempts 1 large-scale harder temporal benchmark metric confirms challenge correlates real-world advances videos data qualitative capabilities 2 e addition sets generated recent progress metrics diversity video distance contribute quality results learning fvd high well next fr\\ scene lack successful coherence game samples consider new requiring wide"}]},{"name":"dr inż. Jan Kocoń","faculty":"Faculty of Information and Communication Technology","papers":[{"title":"Beyond the imitation game: Quantifying and extrapolating the capabilities of language models","description":"language poorly exhibit benefits commonly biology involve transformer expert scale billions breakthrough physics gpt evaluate addition ... challenge limitations calibration predictably improve demonstrate 132 prepare poor spanning harmful parameters disruptive address switch-style rater quantitative google-internal new remarkably impact potentially drawing dense research 204 near-future though strong focuses qualitative math openai sizes big-bench classes authors '' transformers millions beyond provide believed architectures reasoning benchmark whereas software component ameliorate present tasks current human memorization introduce absolute similar terms common-sense increasing future understand performance topics gradually currently team compared game sparsity `` bias 450 task despite improvement institutions effects baseline transformative characterized model childhood sparse imitation models across hundreds order social capabilities consists behavior findings socially development performed linguistics contributed large raters problems include 's knowledge yet diverse vital inform"}]}]},"metadata":{"run_id":"21cc36f5-542e-4d87-a520-7c826b4fa065","feedback_tokens":[]}}
```

### Data managment

Dataset should be kept in `data` and `vectorstores` folder. If you want to access solvro dataset, you could try to contact project manager or techlead

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
- [@avtorgenii](https://github.com/avtorgenii) - ML Engineer
- [@Barionetta](https://github.com/Barionetta) - Project Manager
- [@rychu777](https://github.com/rychu777) - ML Engineer