from time import sleep
import json


class ColorClass:
    """Class for colored text output"""
    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CYELLOW = '\33[33m'
    CBLACKBG = '\33[40m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


class Utility:
    """Class of static methods used in the card game"""
    @staticmethod
    def ask_rules() -> None:
        """Ask player if they would like the rules described."""
        print(f"{ColorClass.OKCYAN}Would you like the Castle/Palace Card Game to be explained?{ColorClass.ENDC}")
        try:
            _rule_var = str(input(f"\ty for yes: "))
        except KeyboardInterrupt:
            quit()
        if _rule_var == 'y':
            print(f"""
GAME RULES:
    THE FIRST PLAYER TO RUN OUT OF CARDS WINS!
    1.  3 cards are dealt to each player face-down (Hidden Cards).
    2.  3 cards are dealt to each player face-up (Face-Up Cards).
    3.  3 cards are dealt to each player's Hand.
    4.  The first card is turned over from the shuffled deck and becomes the
        Active Card.
    5.  During their turn, each player will play a card that is equal to
        or of higher value than the active card.
        --- 2's, 8's, and A's play on top of any card
        --- 2's reset the stack
        --- 8's burn the stack and remove it from play
        --- A's have the highest card value
    6.  You must play a card during your turn. If you cannot play a card,
        type 99 to pick up the current stack. The next player can play any
        card from their choices.
    7.  Burn the stack if:
        --- The top 4 cards are of the same value, and/or
        --- An 8 is played
        The player who played the last card will restart their turn.
    8.  Once your turn is finished, if there is still a deck,
        you will draw cards from the draw pile (deck) to maintain 3 cards in your hand.
    9. Once the deck is depleted, players rely solely on the cards
        in their hand.
        --- If you pick up the stack, you must play all of those cards before
            playing from your cards on the table (Hidden and Face-Up Cards).
        --- Once your Hand is depleted, you will play from your Face-Up Cards.
        --- Once your Face-Up Cards are depleted, you will play from your
            Hidden Cards.
        --- You win the game if you deplete your Hand, Face-Up, and Hidden Cards
            before your opponent\n
NOTES ABOUT THIS VERSION:
    [A] Players CANNOT choose their 3 Face-Up Cards.
    [B] 10's are NOT special cards. They will NOT add the burnt stack back
        to the game.
    [C] By default, you will play all cards of the same value from your hand.
    [D] You will NOT be able to play a 4-of-a-kind from your hand unless
        those cards are of equal or higher value than the active card.
    [E] KeyboardInterrupt is supported.
""")
            sleep(2.4)

    @staticmethod
    def check_all_same(lst: object) -> bool:
        """
        Check if all elements in a list are identical
        Used in test_top_4 function.
        :param list lst: Top 4 cards of active stack
        :return: True (Boolean) if all elements in list are equal
        """
        return len(set(lst)) == 1

    @staticmethod
    def id_card_list(card_list: list) -> list[str]:
        """
        Convert any list of 1-52 card numbers into a list of number+suit for human-readable format
        :param list card_list: List of cards numbered 1-52
        :return: List of card names
        """
        card_list_names = []
        _card_no = str()
        _card_suit = str()
        for _card in range(len(card_list)):
            # ! Assign suits
            if card_list[_card] in range(1, 14):
                _card_suit = "\u2663"  # clubs
            elif card_list[_card] in range(14, 27):
                _card_suit = "\u2660"  # spades
            elif card_list[_card] in range(27, 40):
                _card_suit = "\u2661"  # hearts
            elif card_list[_card] in range(40, 53):
                _card_suit = "\u2662"  # diamonds
            # ! Assign values
            if card_list[_card] in [1, 14, 27, 40]:
                _card_no = "A"
            elif card_list[_card] in [2, 15, 28, 41]:
                _card_no = "2"
            elif card_list[_card] in [3, 16, 29, 42]:
                _card_no = "3"
            elif card_list[_card] in [4, 17, 30, 43]:
                _card_no = "4"
            elif card_list[_card] in [5, 18, 31, 44]:
                _card_no = "5"
            elif card_list[_card] in [6, 19, 32, 45]:
                _card_no = "6"
            elif card_list[_card] in [7, 20, 33, 46]:
                _card_no = "7"
            elif card_list[_card] in [8, 21, 34, 47]:
                _card_no = "8"
            elif card_list[_card] in [9, 22, 35, 48]:
                _card_no = "9"
            elif card_list[_card] in [10, 23, 36, 49]:
                _card_no = "10"
            elif card_list[_card] in [11, 24, 37, 50]:
                _card_no = "J"
            elif card_list[_card] in [12, 25, 38, 51]:
                _card_no = "Q"
            elif card_list[_card] in [13, 26, 39, 52]:
                _card_no = "K"
            card_list_names.append(_card_no + " " + _card_suit)
        return card_list_names

    @staticmethod
    def get_card_val(card_q: int) -> int:
        """
        Return the card value (2-14), of any single card (1-52). 0 is an empty currentStack.
        :param int card_q: Card integer (1-52)
        :return: Card value (2-14)
        """
        _card_val = int()
        if card_q in [1, 14, 27, 40]:
            _card_val = 14  # Aces
        elif card_q in [2, 15, 28, 41]:
            _card_val = 2
        elif card_q in [3, 16, 29, 42]:
            _card_val = 3
        elif card_q in [4, 17, 30, 43]:
            _card_val = 4
        elif card_q in [5, 18, 31, 44]:
            _card_val = 5
        elif card_q in [6, 19, 32, 45]:
            _card_val = 6
        elif card_q in [7, 20, 33, 46]:
            _card_val = 7
        elif card_q in [8, 21, 34, 47]:
            _card_val = 8
        elif card_q in [9, 22, 35, 48]:
            _card_val = 9
        elif card_q in [10, 23, 36, 49]:
            _card_val = 10
        elif card_q in [11, 24, 37, 50]:
            _card_val = 11
        elif card_q in [11, 24, 37, 50]:
            _card_val = 12
        elif card_q in [12, 25, 38, 51]:
            _card_val = 12
        elif card_q in [13, 26, 39, 52]:
            _card_val = 13  # Kings
        return _card_val

    @staticmethod
    def read_win_loss_records() -> None:
        """Display Win/Loss records from json file"""
        with open('records.json', mode='r', encoding='utf-8') as records:
            file_contents = records.read()
            file_dict = json.loads(file_contents)
            print(f"{ColorClass.OKCYAN}Records: {file_dict}{ColorClass.ENDC}")

    @staticmethod
    def update_win_loss_records(victor) -> None:
        """Update and display records in json file"""
        print("\tUpdating records...")
        with open('records.json', mode='r+', encoding='utf-8') as records:
            file_contents = records.read()
            file_dict = json.loads(file_contents)
            file_dict['totalGamesPlayed'] += 1
            if victor == 'player':
                file_dict['playerWins'] += 1
            elif victor == 'opponent':
                file_dict['opponentWins'] += 1
            print(f"{ColorClass.CBLACKBG}{ColorClass.OKCYAN}Records: {file_dict}{ColorClass.ENDC}")
            records.seek(0)
            json.dump(file_dict, records, indent=4)
