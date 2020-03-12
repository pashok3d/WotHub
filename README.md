# WotHub
 Data mining system for [World of Tanks](https://en.wikipedia.org/wiki/World_of_Tanks) game replays.
# About
 WotHub is a data mining project in which we parse data packets from game replays, preprocess data and make predictions based on statistical approach. 
# How to use
### Preparing
* Download [replays](http://wotreplays.ru/) and place them in `/replays` folder. 
### Parsing 
For a parsing part we use [wotreplay-parser](https://github.com/evido/wotreplay-parser) created by [Jan Temmerman](https://github.com/evido).
* run `parser.py`

Parsed data will appear in `/raw_data` folder in .json format.
### Preprocessing
* run `preprocessor.py`

Preprocessed data will appear in `/pro_data` folder in .csv format.

### Visualization
Visualization consists in creating position density plot where high values represent most frequent positions.
We use streamlit for convenient manipulation and further project deployment. 

* `streamlit run .\web_visual.py`


Example:

![](output.png)

### To-do
- [ ] Replays scraper
- [ ] Project deployment
