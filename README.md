# Simulatore di sistemi elettorali

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![CodeFactor](https://www.codefactor.io/repository/github/alessandrozito98/simulatoresistemielettorali-2/badge)](https://www.codefactor.io/repository/github/alessandrozito98/simulatoresistemielettorali-2)
<!--- 
[![wakatime](https://wakatime.com/badge/github/alessandrozito98/SimulatoreSistemiElettorali-2.svg)](https://wakatime.com/badge/github/alessandrozito98/SimulatoreSistemiElettorali-2) 
-->
<a href="https://github.com/alessandrozito98/SimulatoreSistemiElettorali-2/pulls">
      <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/alessandrozito98/SimulatoreSistemiElettorali-2?color=0088ff" />
</a>
<a href="https://github.com/alessandrozito98/SimulatoreSistemiElettorali-2/issues">
    <img alt="GitHub issuess" src="https://img.shields.io/github/issues/alessandrozito98/SimulatoreSistemiElettorali-2?color=0088ff" />
</a>

## Description

Simulations of different electoral laws with the same dataset to see if there would be any changes in the composition of the parliament.

## Installation

Needs python3.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the librabries.

```bash
pip3 install -r requirements.txt
```

## Configuration

### Usage

Two ways of starting the simulation:

1) Using the bash console:

```bash
python3 -m src LeggiElettorali/LawName
``` 

2) Using the python console:

```python
import src
src.run_simulation('LeggiElettorali/LawName')
 ```

### Setup
Create a folder in LeggiElettorali/*name_of_new_law* with this structure:
+ Classes
+ Data
+ Instances

for more information on which files to put in the folder, see the [documentation](https://github.com/alessandrozito98/SimulatoreSistemiElettorali-2/tree/master/docs).

## Credits

+ First release of the framework and Europee electoral law: Lorenzo Ruffati ([@LRuffati](https://github.com/LRuffati)) 
+ Porcellum electoral law: Laura Amabili ([@LauraAmabili](https://github.com/LauraAmabili))
+ Mattarellum electoral law: Davide Maioli ([@davidemaioli](https://github.com/davidemaioli)) 
+ Binomiale Electoral law: 
    + Alessandro Zito ([@alessandrozito98](https://github.com/alessandrozito98))
    + Mirko Li Veli ([@mirkoliveli](https://github.com/mirkoliveli))
+ Rosatellum Electoral law:
  + Furkan Gumus ([@FurkanGumus](https://github.com/gfurkan00))


### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
Licensed under [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/) license.
