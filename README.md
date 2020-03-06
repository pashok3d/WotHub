# WotHub
 Data mining system for [World of Tanks](https://en.wikipedia.org/wiki/World_of_Tanks) game.
# About
 WotHub is a data mining project which parses data packets from game replays, preprocesses data and makes predictions based on statistical approach. 
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
