# PromoCHATor

<p align="center">
    <img src="./assets/solvro.png">
</p>

# Solvro ML - PromoCHATor
<p align="justify"> 
W tym repozytorium znajduje się kod systemu rekomendacyjnego opartego na dużych modelach językowych. System w postaci chatbota, na podstawie dorobku naukowego pracowników Politechniki Wrocławskiej, dopasowywuje odpowiedniego promotora do podanego przez studenta tematu pracy dyplomowej
</p>

## Table of contents

1. **[Opis](#opis)**
2. **[Technologie](#technologie)**
3. **[Rozwój projektu](#rozwoj)**
   1. [Szybki start](#szybki-start)
   2. [Deployment](#deployment)
   3. [URL](#url)
   3. [Przykład użycia](#przyklad-uzycia)
   4. [Zbiór danych](#zbior-danych)
   5. [Github workflow](#github-workflow)
4. **[Nasz zespół](#nasz-zespol)**

## Opis
<p align="justify"> 
W tym repozytorium znajduje się kod systemu rekomendacyjnego opartego na dużych modelach językowych. System w postaci chatbota, na podstawie dorobku naukowego pracowników Politechniki Wrocławskiej, dopasowywuje odpowiedniego promotora do podanego przez studenta tematu pracy dyplomowej
</p>

## Technologie
Projekt został stworzony z wykorzystaniem następujących technologii:
* Python 3
* LangChain
* Ollama

## Rozwój projektu
### Szybki start
Jeśli chcesz lokalnie postawić projekt

1. Sklonuj repozytorium:

   ```
   git clone https://github.com/Solvro/ml-promochator.git && cd ml-promochator
   ```

3. Uzupełnij `.env` na podstawie `.env.example`

3. Uruchom [Dockera](https://docs.docker.com/compose/)
   ```
   docker compose watch
   ```

### Deployment
Jeśli chcesz postawić projekt na serwerze

1. Sklonuj repozytorium:

   ```
   git clone https://github.com/Solvro/ml-promochator.git && cd ml-promochator
   ```

3. Uzupełnij `.env` na podstawie `.env.example`

3. Uruchom [Dockera](https://docs.docker.com/compose/)
   ```
   docker compose up -d
   ```

Jeżeli chcesz zainicjalizować bazę danych, upewnij się, że pobrałeś plik `authors_with_papers.csv` z [projektowego datasetu](https://drive.google.com/drive/folders/1odcaykO5uGtJXGugjCm8UioFT2XWWHNM). Umieść plik w folderze `data` w katalogu z projektem.

### URL

Bazowy url: `http://localhost:8000`

Dokumentacja: `http://localhost:8000/docs`


### Przykład użycia

Zapytanie
   ```
   curl -X POST "http://localhost:8000/recommend" \
      -H "Content-Type: application/json" \
      -d '{"data": "Deep Generative Models"}'
   ```

Odpowiedź

```
{"response":"\n1. Supervisor's name: dr hab. inż. Maciej Zięba\nFaculty: Faculty of Information and Communication Technology\nResearch papers:\n- Ensemble boosted trees with synthetic features generation in application to bankruptcy prediction\n- Boosted SVM for extracting rules from imbalanced data in application to prediction of the post-operative life expectancy in the lung cancer patients\n- Classification restricted Boltzmann machine for comprehensible credit scoring model\n- Adversarial autoencoders for compact representations of 3D point clouds\n- Bingan: Learning compact binary descriptors with a regularized gan\n\n2. Supervisor's name: prof. dr hab. inż. Jerzy Świątek\nFaculty: Faculty of Information and Communication Technology\nResearch papers:\n- Boosted SVM for extracting rules from imbalanced data in application to prediction of the post-operative life expectancy in the lung cancer patients\n- Generative adversarial networks: recent developments\n- System analysis techniques in ehealth systems: A case study\n- Ensemble classifier for solving credit scoring problems\n- Accelerated learning for restricted Boltzmann machine with momentum term\n\n3. Supervisor's name: dr inż. Dariusz Więcek\nFaculty: Faculty of Information and Communication Technology\nResearch papers:\n- Smart connected logistics\n"}
```

### Zbiór danych

Dane powinny być przechowywane w katalogu `data`. Jeżeli potrzebujesz dostępu do zbioru danych Solvro, zgłoś się do Project Managera albo Tech Leada projektu.

> [!WARNING]
> Proszę nie pushować zbioru danych na zdalne repozytorium!


### Github workflow

Gdy przypiszesz się do nowego zadania, powinieneś przestrzegać tych zasad
1. `git checkout main` Wróć na główną gałąź
2. `git pull origin main` Zaaktualizuj główną gałąź
3. `git fetch` Zaaktualizuj pozostałe gałęzie
4. `git checkout -b type/task` Stwórz gałąź z nowym zadaniem
5. `git add .` Dodaj wszystkie zmiany, jakie wykonałaś/wykonałeś
6. `git commit -m "My changes description"` Zcommituj zmiany, odpowiednio je opisując
7. `git push origin type/task` Zpushuj zmiany na zdalne repozytorium
8. Na Githubie powinnaś/powinieneś zrobić Pull Request (PR), ze swojej zdalnej gałęzi

> [!WARNING]
> Nie pushuj zmian bezpośrednio na maina!

Aby dowiedzieć się więcej szczegółów na temat pracy w projekcie,
przeczytaj handbook Solvro

**Github Solvro Handbook 🔥** - https://docs.google.com/document/d/1Sb5lYqYLnYuecS1Essn3YwietsbuLPCTsTuW0EMpG5o/edit?usp

## Nasz zespół
To nasz obecny zespół

|             |             |               |
| :---        |    :----:   |          ---: |
| <img src="https://avatars.githubusercontent.com/u/87516463?v=4" style="width:200px;"> <br>[@LukiLenkiewicz](https://github.com/LukiLenkiewicz) - Tech Lead     | <img src="https://avatars.githubusercontent.com/u/122210130?v=4" style="width:200px;"> <br>[@Micz26](https://github.com/Micz26) - ML Engineer| <img src="https://avatars.githubusercontent.com/u/68340482?v=4" style="width:200px;"> <br>[@farqlia](https://github.com/farqlia) - ML Engineer |
| <img src="https://avatars.githubusercontent.com/u/115902377?v=4" style="width:200px;"> <br>[@AgataGro](https://github.com/AgataGro) - ML Engineer | <img src="https://avatars.githubusercontent.com/u/99985667?v=4" style="width:200px;"> <br>[@dekompot](https://github.com/dekompot) - ML Engineer| <img src="https://avatars.githubusercontent.com/u/109885481?v=4" style="width:200px;"> <br>[@b4rt4s](https://github.com/b4rt4s) - ML Engineer |
| <img src="https://avatars.githubusercontent.com/u/84938240?v=4" style="width:200px;"> <br>[@Woleek](https://github.com/Woleek) - ML Engineer | <img src="https://avatars.githubusercontent.com/u/169385041?v=4" style="width:200px;"> <br>[@WiktoriaFrost](https://github.com/WiktoriaFrost) - ML Engineer | <img src="https://avatars.githubusercontent.com/u/93910163?v=4" style="width:200px;"> <br>[@Barionetta](https://github.com/Barionetta) - Project Manager |
