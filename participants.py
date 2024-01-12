from utility import ColorClass


class Participant:
    def __init__(self):
        """Base class containing properties of card lists"""
        self.hidden = []
        self.face_up = []
        self.hand = []


class Player(Participant):
    def __init__(self):
        """Human participant"""
        super().__init__()
        self.text_color = ColorClass.OKGREEN


class Opponent(Participant):
    def __init__(self):
        """Computer opponent participant"""
        super().__init__()
        self.text_color = ColorClass.OKBLUE
