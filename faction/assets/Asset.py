class Asset:
    def __init__(self, name, type, max_hp, cost, tl, asset_class, attack, counterattack, special):
        self.name = name
        self.type = type
        self.max_hp = max_hp
        self.cost = cost
        self.tl = tl
        self.asset_class = asset_class
        self.attack = attack
        self.counterattack = counterattack
        self.special = special

    def get_name(self):
        return self.name
