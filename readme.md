# Superhero simulator

Superhero Simulator takes 2 teams of 5 superheroes each and makes them battle with each other.

To execute run
```
python main.py
# OR 
python3 main.py
```
or if you want to receive an email with the fight, run:
```
python main.py --email example@email.com
# OR 
python3 main.py --email example@email.com
```

## Requirements

### Python

#### Virtual env (optional)
To start a virtual environment run
```
python3 -m venv env
```
#### pip
To install python requirements run
```
pip install -r requirements.txt
```

### dotenv
To run it yourself, you'll need a `.env` file that conatins the following
```
MY_API_KEY=<your superhero API key, e.g.2183127771827858>
MAILGUN_API_KEY=<your mailgun API key>
MAILGUN_DOMAIN=<your mailgun domain>
```


## Assumptions

- Damage is done as an int
- Each Superhero has one (AS) Actual Stamina and one random element of FB chosen that's static
- To make it so one team does not always have an advantage, the superhero attacking between Team 1 and Team 2 is randomized

## Configurations
There are 2 global variables to tweak the simulator's experience
- MAX_FB = 9  Adjust number to adjust max of FB (Filiation Coefficient) and thus variance
    - If fights are too short, lowering this number helps
- SLEEP_TIME = 0.4
    - Adjust to set the time spent between actions, so the simulations runs slower the higher the number is (it's in seconds)

## Notes
- https://superheroapi.com is slower than https://akabab.github.io/superhero-api/api/, development was done with the latter, but am async solution enabled using the former