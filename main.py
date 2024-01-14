from game import Game


if __name__ == '__main__':
    game = Game()
    game.run_game_loop(ask_rules=False, keep_record=True)
