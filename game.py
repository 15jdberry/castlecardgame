import random
from time import sleep
from utility import Utility, ColorClass
from participants import Player, Opponent


class Game:
    deck = [i for i in range(1, 53)]
    burnt = []
    stack = []
    active_card = int()
    keep_record = False

    def __init__(self) -> None:
        """Class containing the Castle / Palace card game."""
        print(f"""\
{ColorClass.BOLD}{ColorClass.OKCYAN}{ColorClass.CBLACKBG}\
{"~" * 22} WELCOME TO THE CASTLE CARD GAME {"~" * 22}\
{ColorClass.ENDC}\
""")
        self.player = Player()
        self.opp = Opponent()

    def reset_game(self):
        Game.deck = [i for i in range(1, 53)]
        Game.burnt = []
        Game.stack = []
        Game.active_card = int()
        self.player = Player()
        self.opp = Opponent()

    def player_turn(self) -> classmethod:
        """
        Starting point for Player's Turn
        :return: Player or Opponent's Turn, depending on game logic
        """
        turn = 'player'
        self.show_table()
        if len(self.player.hand) == 0 and len(self.player.face_up) > 0:
            # ! Play from Face Up Cards
            player_selection = self.ask_player_selection(cardset='face_up')
            candidate_card = self.player.face_up[player_selection - 1]
            Game.active_card = Game.stack[-1] if len(Game.stack) > 0 else int(0)
            if (Utility.get_card_val(candidate_card) >= Utility.get_card_val(Game.active_card)
                    or Utility.get_card_val(candidate_card) == 14
                    or Utility.get_card_val(candidate_card) == 2
                    or Utility.get_card_val(candidate_card) == 8):
                # ! Proceed, card value sufficient
                Game.active_card = self.player.face_up[player_selection - 1]
                Game.stack.append(Game.active_card)
                self.player.face_up.remove(Game.active_card)
                print(f'\t{self.player.text_color}You played the{ColorClass.ENDC}'
                      f'\t{ColorClass.CBLACKBG}{ColorClass.BOLD} {self.id_active_card()} {ColorClass.ENDC}')
            elif Utility.get_card_val(candidate_card) < Utility.get_card_val(Game.active_card):
                # ! Card value too low
                print(f'\t{ColorClass.CRED}Card value too low, Try again...{ColorClass.ENDC}')
                return self.player_turn()
            if Utility.get_card_val(Game.active_card) == 8:
                self.burn_stack(turn)
                return self.player_turn()
            self.test_top_4(turn)
        elif len(self.player.hand) == 0 and len(self.player.face_up) == 0:
            # ! Play from Hidden Cards
            player_selection = self.ask_player_selection(cardset='hidden')
            candidate_card = self.player.hidden[player_selection - 1]
            Game.stack.append(candidate_card)
            self.player.hidden.remove(candidate_card)
            # ! Play card, then evaluate
            print(f"\t{self.player.text_color}You turned over the{ColorClass.ENDC}"
                  f"\t{ColorClass.CBLACKBG}{ColorClass.BOLD} {self.id_active_card()} {ColorClass.ENDC}")
            if Utility.get_card_val(candidate_card) == 8:
                self.burn_stack(turn)
                self.question_victory(turn)
                return self.player_turn()
            below_card_value = Utility.get_card_val(Game.stack[-2]) if len(Game.stack) >= 2 else int(0)
            if Utility.get_card_val(candidate_card) < below_card_value \
                    and Utility.get_card_val(candidate_card) != 2 \
                    and Utility.get_card_val(candidate_card) != 8:
                # ! Card value too low
                print(f"\t{ColorClass.CRED}Card value was too low{ColorClass.ENDC}")
                self.pickup_stack(turn)
            else:
                self.test_top_4(turn)
                self.question_victory(turn)
        else:
            # ! Play from Hand
            player_selection = self.ask_player_selection(cardset='hand')
            candidate_card = self.player.hand[player_selection - 1]
            Game.active_card = Game.stack[-1] if len(Game.stack) > 0 else int(0)
            if Utility.get_card_val(candidate_card) < Utility.get_card_val(Game.active_card) \
                    and Utility.get_card_val(candidate_card) != 2 \
                    and Utility.get_card_val(candidate_card) != 8:
                print(f'\t\t{ColorClass.CRED}Card value too low, Try again...{ColorClass.ENDC}')
                return self.player_turn()
            # ! Proceed, card value sufficient
            Game.active_card = self.player.hand[player_selection - 1]
            Game.stack.append(Game.active_card)
            self.player.hand.remove(self.player.hand[player_selection - 1])
            print(f"\t{self.player.text_color}You played the{ColorClass.ENDC}"
                  f"\t{ColorClass.CBLACKBG}{ColorClass.BOLD} {self.id_active_card()} {ColorClass.ENDC}")
            self.lay_all_same(turn)
            if Utility.get_card_val(Game.active_card) == 8:
                self.burn_stack(turn)
                self.fill_hand(turn)
                self.question_victory(turn)
                return self.player_turn()
            self.test_top_4(turn)
            self.fill_hand(turn)
            self.question_victory(turn)
        return self.opponent_turn()

    def opponent_turn(self) -> classmethod:
        """
        Starting point for Opponent's Turn
        :return: Player or Opponent's Turn, depending on game logic
        """
        turn = 'opponent'
        sleep_time = float(0.2)
        print(f"\n{ColorClass.BOLD}{self.opp.text_color}OPPONENT'S TURN ...{ColorClass.ENDC}")
        sleep(0.5)
        Game.active_card = Game.stack[-1] if len(Game.stack) > 0 else int(0)
        if len(self.opp.hand) == 0 and len(self.opp.face_up) > 0:
            # ! Play from Face Up Cards
            opponent_choice = self.id_opponent_playable(cardset='face_up')
            Game.stack.append(opponent_choice)
            self.opp.face_up.remove(opponent_choice)
            print(f'\t{self.opp.text_color}Opponent played the{ColorClass.ENDC}'
                  f'\t{ColorClass.BOLD}{ColorClass.CBLACKBG}',
                  self.id_active_card(), f'{ColorClass.ENDC}')
            sleep(sleep_time)
            if Utility.get_card_val(Game.active_card) == 8:
                self.burn_stack(turn)
                return self.opponent_turn()
            self.test_top_4(turn)
        elif len(self.opp.hand) == 0 and len(self.opp.face_up) == 0:
            # ! Play from Hidden Cards
            opponent_choice = self.id_opponent_playable(cardset='hidden')
            Game.stack.append(opponent_choice)
            self.opp.hidden.remove(opponent_choice)
            print(f'\t{self.opp.text_color}Opponent turned over the{ColorClass.ENDC}'
                  f'\t{ColorClass.CBLACKBG}{ColorClass.BOLD}',
                  self.id_active_card(), f'{ColorClass.ENDC}')
            sleep(sleep_time)
            if Utility.get_card_val(opponent_choice) == 8:
                self.burn_stack(turn)
                self.question_victory(turn)
                return self.opponent_turn()
            below_card_value = Utility.get_card_val(Game.stack[-2]) if len(Game.stack) >= 2 else int(0)
            if Utility.get_card_val(opponent_choice) < below_card_value \
                    and (Utility.get_card_val(opponent_choice) != 2):
                # ! Card value too low
                self.pickup_stack(turn)
                return self.player_turn()
            self.test_top_4(turn)
            self.question_victory(turn)
        else:
            # ! Play from Hand
            opponent_choice = self.id_opponent_playable(cardset='hand')
            Game.stack.append(opponent_choice)
            self.opp.hand.remove(opponent_choice)
            print(f'\t{self.opp.text_color}Opponent played the{ColorClass.ENDC}'
                  f'\t{ColorClass.BOLD}{ColorClass.CBLACKBG}',
                  self.id_active_card(), f'{ColorClass.ENDC}')
            sleep(sleep_time)
            self.lay_all_same(turn)
            if Utility.get_card_val(Game.active_card) == 8:
                self.burn_stack(turn)
                self.fill_hand(turn)
                return self.opponent_turn()
            self.test_top_4(turn)
            self.fill_hand(turn)
            self.question_victory(turn)
        return self.player_turn()

    def id_opponent_playable(self, cardset: str) -> int or classmethod:
        """
        Identify playable cards throughout all phases of Opponent's Turn.
        :param cardset: Which set of cards is the opponent playing from? 'hand', 'face_up', or 'hidden'
        :return: Opponent's choice within specified cardset.
        --- Single selection the opponent will play (candidate_card)
        --- If no playable options, opponent will pick up stack and end turn
        """
        _cardset = list()
        _candidate_card = int()
        _opponentOptions = []
        _opponentOptionsSame = []
        _opponentOptionsNext = []
        _opponentOptionsN2 = []
        _opponentOptionsN3 = []  # N+3 card search
        Game.active_card = Game.stack[-1] if len(Game.stack) > 0 else int(0)
        if cardset == 'hidden':
            # ! Last phase of game, when opponent plays cards from Hidden Cards
            _candidate_card = random.choice(self.opp.hidden)
            return _candidate_card
        elif cardset == 'face_up':
            # ! Next phase of game, when opponent plays cards from Face Up Cards
            _cardset = self.opp.face_up
        elif cardset == 'hand':
            # ! Beginning of game, when opponent plays cards from Hand
            _cardset = self.opp.hand

        for j in range(0, len(_cardset)):
            # ! Identify playable options from 'face_up' and 'hand' options
            if ((Utility.get_card_val(_cardset[j]) >= Utility.get_card_val(Game.active_card))
                    or (Utility.get_card_val(_cardset[j]) == 1)
                    or (Utility.get_card_val(_cardset[j]) == 2)
                    or (Utility.get_card_val(_cardset[j]) == 8)):
                # ! Add playable options to `_opponentOptions` array
                _opponentOptions.append(_cardset[j])
        if len(_opponentOptions) == 0:
            # ! Pick up stack and end turn if no playable cards
            self.pickup_stack(turn='opponent')
            return self.player_turn()
        elif len(_opponentOptions) == 1:
            # ! Play the only option
            # print(f'\t{self.opp.text_color}Opponent only has one option...{ColorClass.ENDC}')  # TOGGLE
            _candidate_card = _opponentOptions[0]
            return _candidate_card
        else:
            # ! Opponent has more than 1 option to play
            for j in range(0, len(_opponentOptions)):
                # ! Identify cards of same, N+2, N+3 value as active card
                if Utility.get_card_val(_opponentOptions[j]) == Utility.get_card_val(Game.active_card):
                    _opponentOptionsSame.append(_opponentOptions[j])
                elif Utility.get_card_val(_opponentOptions[j]) == (Utility.get_card_val(Game.active_card) + 1):
                    _opponentOptionsNext.append(_opponentOptions[j])
                elif Utility.get_card_val(_opponentOptions[j]) == (Utility.get_card_val(Game.active_card) + 2):
                    _opponentOptionsN2.append(_opponentOptions[j])
                elif Utility.get_card_val(_opponentOptions[j]) == (Utility.get_card_val(Game.active_card) + 3):
                    _opponentOptionsN3.append(_opponentOptions[j])
            # ! Choose a card from Options
            if len(_opponentOptionsSame) > 0:
                print(f'\t{self.opp.text_color}Opponent has the same value card...{ColorClass.ENDC}')
                _candidate_card = _opponentOptionsSame[0]
            elif len(_opponentOptionsNext) > 0:
                print(f'\t{self.opp.text_color}Opponent has the next value card...{ColorClass.ENDC}')
                _candidate_card = _opponentOptionsNext[0]
            elif len(_opponentOptionsN2) > 0:
                # print(f'\t{self.opp.text_color}Opponent has the n+2 card...{ColorClass.ENDC}')  # TOGGLE
                _candidate_card = _opponentOptionsN2[0]
            elif len(_opponentOptionsN3) > 0:
                # print(f'\t{self.opp.text_color}Opponent has the n+3 card...{ColorClass.ENDC}')  # TOGGLE
                _candidate_card = _opponentOptionsN3[0]
            # Keep adding for more refined logic
            else:
                _candidate_card = _opponentOptions[0]
            return _candidate_card

    def ask_player_selection(self, cardset: str) -> int or classmethod:
        """
        Ask player selection from a specified card list. Eliminate options of picking up stack and when index
        is not in card list.
        :param str cardset: Which set of cards is the player playing from? 'hand', 'face_up', or 'hidden'
        :return: Player's choice of card in specified cardset. (1 to length of cardset).
        --- 99 will pick up the current stack
        --- If there is a typo, player will be asked again
        """
        print(f"""\
{ColorClass.BOLD}{self.player.text_color}YOUR TURN!\
{f"(Type 99 to pick up stack){ColorClass.ENDC}": >70}\
""")
        if cardset == 'hand':
            _cardset = self.player.hand
        elif cardset == 'face_up':
            _cardset = self.player.face_up
            cardset = 'face-up cards'
        elif cardset == 'hidden':
            _cardset = self.player.hidden
            cardset = 'hidden cards'
        try:
            player_selection = int(input(f"""\tWhich card in your {cardset} will you play (1-{len(_cardset)})?: """))
        except KeyboardInterrupt:
            quit()
        except (SyntaxError, NameError, IndexError, ValueError):
            print(f"\t{ColorClass.CRED}Please enter an integer of a card in your {cardset}.{ColorClass.ENDC}")
            return self.player_turn()
        if player_selection == 99:
            if len(Game.stack) != 0:
                # ! 99 To pick up stack and end turn
                self.pickup_stack(turn='player')
                return self.opponent_turn()
            elif len(Game.stack) == 0:
                print(f"""\t{ColorClass.CRED}You must play a card.
\tPlease try again or type 99 to pick up the stack.{ColorClass.ENDC}""")
                return self.player_turn()
        elif player_selection not in range(1, len(_cardset) + 1):
            print(f"\t{ColorClass.CRED}Index not in {cardset}. Please Try Again.{ColorClass.ENDC}")
            return self.player_turn()
        return player_selection

    def fill_hand(self, turn: str) -> None:
        """
        Draw cards to keep at least 3 cards in hand while there is still a deck.
        :param turn: Whose turn was it when the last card was played? 'player' or 'opponent'
        """
        sleep(0.2)
        if turn == 'player':
            if len(self.player.hand) < 3 and len(Game.deck) > 0:
                print(f"\t{self.player.text_color}Drawing card ...{ColorClass.ENDC}")
                self.player.hand.append(Game.deck.pop())
                print(f"\t{self.player.text_color}Hand:{ColorClass.ENDC} {Utility.id_card_list(self.player.hand)}")
                self.fill_hand(turn)
        elif turn == 'opponent':
            if len(self.opp.hand) < 3 and len(Game.deck) > 0:
                print(f"\t{self.opp.text_color}Drawing card ...{ColorClass.ENDC}")
                self.opp.hand.append(Game.deck.pop())
                self.fill_hand(turn)

    def lay_all_same(self, turn: str) -> None:
        """
        Lay all same value cards ###IN A CARD SET?### WIP
        :param str turn: Whose turn was it when the last card was played? 'player' or 'opponent'
        :return: None
        """
        _all_same = []
        Game.active_card = Game.stack[-1]  # Top card of stack
        sleep_time = float(0.1)
        if turn == 'player':
            for i in range(0, len(self.player.hand)):
                if Utility.get_card_val(self.player.hand[i]) == Utility.get_card_val(Game.active_card):
                    _all_same.append(self.player.hand[i])
                    sleep(sleep_time)
            while len(_all_same) > 0:
                card = _all_same.pop()
                Game.stack.append(card)
                self.player.hand.remove(card)
                print(f"\t{self.player.text_color}You played the{ColorClass.ENDC}"
                      f"\t{ColorClass.CBLACKBG}{ColorClass.BOLD} {self.id_active_card()} {ColorClass.ENDC}")
        elif turn == 'opponent':
            for i in range(0, len(self.opp.hand)):
                if Utility.get_card_val(self.opp.hand[i]) == Utility.get_card_val(Game.active_card):
                    _all_same.append(self.opp.hand[i])
                    sleep(sleep_time)
            while len(_all_same) > 0:
                card = _all_same.pop()
                Game.stack.append(card)
                self.opp.hand.remove(card)
                print(f'\t{self.opp.text_color}Opponent played the{ColorClass.ENDC}'
                      f'\t{ColorClass.CBLACKBG}{ColorClass.BOLD}',
                      self.id_active_card(), f'{ColorClass.ENDC}')
        sleep(0.3)

    def burn_stack(self, turn: str) -> None:
        """
        Moves the currentStack to the burntStack.
        :param str turn: Whose turn was it when the last card was played? 'player' or 'opponent'
        """
        while len(Game.stack) > 0:
            Game.burnt.append(Game.stack.pop())
            sleep(0.1)
        self.fill_hand(turn)
        print(f"\t{ColorClass.CRED}The stack was burned...\t🔥{ColorClass.ENDC}")
        self.question_victory(turn)

    def pickup_stack(self, turn: str) -> None:
        """
        Pick up current stack if no available options in card set.
        :param str turn: Who has to pick up the stack? 'player' or 'opponent'
        """
        if turn == 'player':
            while len(Game.stack) > 0:
                self.player.hand.insert(len(self.player.hand), Game.stack.pop(0))
            print(f'\t{self.player.text_color}Picked up stack, New Hand:{ColorClass.ENDC}\n   ',
                  Utility.id_card_list(self.player.hand))
        elif turn == 'opponent':
            print(f'\t{self.opp.text_color}Opponent had to pick up the stack{ColorClass.ENDC}')
            while len(Game.stack) > 0:
                self.opp.hand.insert(len(self.opp.hand), Game.stack.pop(0))

    def test_top_4(self, turn: str) -> classmethod or None:
        """
        If the stack is >= 4, burn the stack if top 4 cards have the same value.
        :param str turn: Whose turn was it when the last card was played? 'player' or 'opponent'
        :return: If the top 4 cards are equal, the stack will be burned and respective turn will restart
        """
        if len(Game.stack) >= 4:
            _top_4_card_vals = list(map(Utility.get_card_val, Game.stack[-4:]))
            print(f"\tTop 4 card values: {ColorClass.CYELLOW}{' '.join(map(str, _top_4_card_vals))}{ColorClass.ENDC}")
            # print(f"\tTop 4 cards are: {_top_4_card_vals}")  # ALTERNATE DISPLAY
            if Utility.check_all_same(_top_4_card_vals):
                # ! Top 4 card values are the same
                print(f"\t{ColorClass.CRED}All Four {Utility.get_card_val(Game.active_card)}'s ",
                      f"were played together...{ColorClass.ENDC}")
                self.burn_stack(turn)
                sleep(0.2)
                if turn == 'player':
                    return self.player_turn()
                elif turn == 'opponent':
                    return self.opponent_turn()

    @staticmethod
    def id_active_card() -> str:
        """
        Prints the active card as a string.
        :return: String of card number and suit
        """
        _card_suit = str()
        _card_no = str()
        _active_card_og = int(Game.stack[-1])  # Top card of stack
        # ! Assign suits
        if _active_card_og in range(1, 14):
            _card_suit = "\u2663 Clubs \u2663"
        elif _active_card_og in range(14, 27):
            _card_suit = "\u2660 Spades \u2660"
        elif _active_card_og in range(27, 40):
            _card_suit = "\u2661 Hearts \u2661"
        elif _active_card_og in range(40, 53):
            _card_suit = "\u2662 Diamonds \u2662"
        elif _active_card_og == 0:
            _card_suit = None
        # ! Assign values
        if _active_card_og in [1, 14, 27, 40]:
            _card_no = "A"
        elif _active_card_og in [2, 15, 28, 41]:
            _card_no = "2"
        elif _active_card_og in [3, 16, 29, 42]:
            _card_no = "3"
        elif _active_card_og in [4, 17, 30, 43]:
            _card_no = "4"
        elif _active_card_og in [5, 18, 31, 44]:
            _card_no = "5"
        elif _active_card_og in [6, 19, 32, 45]:
            _card_no = "6"
        elif _active_card_og in [7, 20, 33, 46]:
            _card_no = "7"
        elif _active_card_og in [8, 21, 34, 47]:
            _card_no = "8"
        elif _active_card_og in [9, 22, 35, 48]:
            _card_no = "9"
        elif _active_card_og in [10, 23, 36, 49]:
            _card_no = "10"
        elif _active_card_og in [11, 24, 37, 50]:
            _card_no = "J"
        elif _active_card_og in [12, 25, 38, 51]:
            _card_no = "Q"
        elif _active_card_og in [13, 26, 39, 52]:
            _card_no = "K"
        _active_id = str(_card_no + ' ' + _card_suit)
        return _active_id

    def shuffle_deal(self) -> None:
        """
        Shuffle and deal cards to player and opponent.
        Players are not given a choice to pick their own Face-Up Cards. They are dealt randomly
        """
        serve_range = int(3)
        print(f"\tShuffling Deck ...")
        random.shuffle(Game.deck)
        print(f"\tDealing Cards ...")
        for j in range(serve_range):
            # ! Deal 9 cards to each player
            self.player.hidden.append(Game.deck.pop())
            self.opp.hidden.append(Game.deck.pop())
            self.player.face_up.append(Game.deck.pop())
            self.opp.face_up.append(Game.deck.pop())
            self.player.hand.append(Game.deck.pop())
            self.opp.hand.append(Game.deck.pop())
        # ! Flip over first card of stack
        Game.stack.append(Game.deck.pop())
        Game.active_card = Game.stack[-1]

    def show_table(self) -> None:
        """Print the active Game Table"""
        _msg = self.id_active_card() if len(Game.stack) > 0 else "[none]"
        print(f"""
{ColorClass.BOLD}{ColorClass.OKCYAN}{ColorClass.CBLACKBG}\
┌{' GAME TABLE ' + '─' * 52} burnt: {len(Game.burnt)} ┐{ColorClass.ENDC}""")
        print(f"""\
{self.opp.text_color}│{'Opponent Hidden Cards: ': >25}{ColorClass.ENDC}{len(self.opp.hidden)}
{self.opp.text_color}│{'Face-Up: ': >25}{ColorClass.ENDC}{" ".join(Utility.id_card_list(self.opp.face_up))}
{self.opp.text_color}│{'Hand: ': >25}{ColorClass.ENDC} {len(self.opp.hand)}""")
        print(f"""{ColorClass.CYELLOW}│{'ACTIVE CARD: ': >25}{ColorClass.ENDC}\
{f"{ColorClass.CBLACKBG}{ColorClass.BOLD}-> {_msg} <-{ColorClass.ENDC}": ^{56 - len(_msg)}}\
{f"stack: {len(Game.stack)} ": >{6 + len(_msg)}}""")
        print(f"""\
{self.player.text_color}│{'Your Hidden Cards: ': >25}{ColorClass.ENDC}{len(self.player.hidden)}
{self.player.text_color}│{'Face-Up: ': >25}{ColorClass.ENDC}{' '.join(Utility.id_card_list(self.player.face_up))}
{self.player.text_color}│{f'Hand ({len(self.player.hand)}): ': >25}{ColorClass.ENDC}\
{' '.join(Utility.id_card_list(self.player.hand))}""")
        print(f"""\
{ColorClass.BOLD}{ColorClass.OKCYAN}{ColorClass.CBLACKBG}└{'─' * 64} deck: {len(Game.deck)} ┘{ColorClass.ENDC}""")

    def question_victory(self, turn: str):
        """
        Endgame Logic. Display Victory message if victory conditions are met.
        If the game ends, it will ask player if they want to play again.
        :param str turn: Whose victory are we questioning? 'player' or 'opponent'
        :return: Starts a new game or quits program
        """
        victory = False
        sleep(0.1)
        if turn == 'player':
            if len(self.player.hand) == 0 and len(self.player.face_up) == 0 and len(self.player.hidden) == 0:
                print(f"\t{ColorClass.BOLD}{self.player.text_color}*{'~' * 40}*")
                for message in ["VICTORY!", "YOU WON!"]:
                    print(f"\t*{' ' * 16}{message}{' ' * 16}*")
                    sleep(1.5)
                print(f"\t*{'~' * 40}*{ColorClass.ENDC}")
                victory = True
        elif turn == 'opponent':
            if len(self.opp.hand) == 0 and len(self.opp.face_up) == 0 and len(
                    self.opp.hidden) == 0:
                print(f"\n\t{self.opp.text_color}OPPONENT VICTORY{ColorClass.ENDC}\n")
                victory = True
        if victory:
            sleep(1)
            if Game.keep_record:
                Utility.update_win_loss_records(victor=turn)
            _play_again = str(input("Would you like to play again (y or n)? "))
            if _play_again == 'y':
                self.reset_game()
                self.run_game_loop(ask_rules=False, keep_record=Game.keep_record)
            else:
                return quit()

    def run_game_loop(self, ask_rules: bool = True, keep_record: bool = True) -> classmethod:
        """
        Main method to run the Castle card game
        :param str ask_rules: set to True for player to be asked if they want the rules read
        :param str keep_record: set to True for records.json file to be shown and updated with gameplay
        :return: Player or Opponent Turn
        """
        Game.keep_record = keep_record
        if ask_rules:
            Utility.ask_rules()
        if Game.keep_record:
            Utility.read_win_loss_records()
        self.shuffle_deal()
        if Utility.get_card_val(Game.active_card) == 8:
            # ! If first card is an 8, burn the stack and pass turn to opponent
            self.burn_stack(turn='player')
            return self.opponent_turn()
        return self.player_turn()
