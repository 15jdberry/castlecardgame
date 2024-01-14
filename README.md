# Castle Card Game
A Python script to run a derivative of the card game [Palace](https://bicyclecards.com/how-to-play/palace/).

## Table of Contents
* [Features](#features)
* [Installation](#installation)
* [Playing](#playing)
* [Pictures](#pictures)
* [Game Rules](#rules)
* [Palace Deviations](#palace-deviations)
* [Testing](#testing)
* [Contributing](#contributing)
* [License](#license)

## Features
* Play a 1-on-1 card game in your terminal (bash or Python)
* Your Win-Loss record is stored in the `records.json` file automatically.

## Installation
The only Python libraries used are from the standard library (random, time, and json).

> ### In terminal with Git
~~~
git clone https://github.com/15jdberry/castlecardgame.git
cd castlecardgame/
./play_castle
~~~

> ### Download the zip file from GitHub
* Unzip and play the game.


## Playing

> ### With Python
~~~
python3 main.py
~~~

> ### With executable (bash script for Mac and Linux)
~~~
./play_castle
~~~

> ### In Finder  
Double click the `play_castle` executable to start the game.  
You may have to use `sudo chmod +x play_castle` in case permissions are not sufficient or you find it not executable. Alternatively, you may have to right-click and "Open with" Terminal.

* Manually edit the `records.json` file to reset the win/loss records.
* See [Rules](#rules) for gameplay.


## Pictures
<img width="634" alt="castle_gameplay_screenshot01" src="https://github.com/15jdberry/castlecardgame/assets/148604533/67c9c31f-e541-47d2-97ce-40afd3af82af">


## Rules
The first player to run out of their cards wins the game!
1.  3 cards are dealt to each player face-down (Hidden Cards).
2.  3 cards are dealt to each player face-up (Face-Up Cards).
3.  3 cards are dealt to each player's Hand.
4.  The first card is turned over from the shuffled deck and becomes the
    Active Card.
5.  During their turn, each player will play a card that is equal to
    or of higher value than the active card.
    * 2's, 8's, and A's play on top of any card
    * 2's reset the stack
    * 8's burn the stack and remove it from play
    * A's have the highest card value
6.  You must play a card during your turn. If you cannot play a card,
    type 99 to pick up the current stack. The next player can play any
    card from their choices.
7.  Burn the stack if:
    * The top 4 cards are of the same value, and/or
    * An 8 is played
    The player who played the last card will restart their turn.
8.  Once your turn is finished, if there is still a deck,
    you will draw cards from the draw pile (deck) to maintain 3 cards in your hand.
9. Once the deck is depleted, players rely solely on the cards
    in their hand.
    * If you pick up the stack, you must play all of those cards before
        playing from your cards on the table (Hidden and Face-Up Cards).
    * Once your Hand is depleted, you will play from your Face-Up Cards.
    * Once your Face-Up Cards are depleted, you will play from your
        Hidden Cards.
    * You win the game if you deplete your Hand, Face-Up, and Hidden Cards
        before your opponent


## Palace Deviations
- Players CANNOT choose their 3 Face-Up Cards.
- 10's are NOT special cards. They will NOT add the burnt stack back
    to the game.
- By default, you will play all cards of the same value from your hand.
- You will NOT be able to play a 4-of-a-kind from your hand unless
    those cards are of equal or higher value than the active card.


## Testing
Visual checking of console logs was performed to ensure the game and logic operates as intended. Test results are stored in the `tests/` directory with `game_tests.py` (Test comments were omitted from the working `game.py` file).


## Contributing
Contributions are welcome. Please refer to [contribution]() guidelines.
Feel free to improve your own version of the game through different logic, colors, and ways to increase the number of players in the game.

## License
This project is licensed under the terms of the MIT license.
