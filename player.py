class Player:
    def __init__(self):
        self.position = 0
        self.money = 500
        self.jailed = False
        self.components = {"Keyboard": 0, "Mouse": 0, "Monitor": 0, "Printer": 0, "CPU": 0, "GPU": 0, "Motherboard": 0, "Mini Tower": 0}
        self.has_done_query_this_turn = False
