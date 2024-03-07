class Player:
    def __init__(self):
        self.position = 0
        self.money = 500
        self.jailed = False
        self.components = {"Keyboard": 0, "Mouse": 0, "Monitor": 0, "Printer": 0, "CPU": 0, "GPU": 0, "Motherboard": 0, "Mini Tower": 0, "Harddrive": 0}
        self.has_done_query_this_turn = False
        self.has_done_event_this_turn = False
        self.has_done_famous_this_turn = False
        self.has_sold_computer_this_turn = False
        self.has_traded_this_turn = False
        self.items_bought_this_turn = 0
        self.guesses_done_this_turn = 0
        self.can_sell_computer = False
