import json
import random

version = "1.4.0"

with open ('settings.json') as file:
    data = json.load(file)

def getDivider():
    divider = ""
    for i in range(56):
        divider += data["DIVIDER"]
    return divider

def rangeRNG(lowest: int, highest: int):
    return random.randint(lowest, highest)

class Player:
    name: str
    health = 100
    max_health: int
    healingPotions: int
    HealingPotionsName: str
    minionActive: bool
    minions: int
    minionTurns: int
    minionMaxTurns: int
    shieldActive: bool
    shields: int
    shieldTurns: int
    shieldDamage: int
    shieldName: str
    minionName: str
    def __init__(self, name: str, health: int, max_health: int, healingPotions: int, HealingPotionsName: str, minionActive: int, minions: int, minionTurns: int, minionMaxTurns: int, shieldActive: int, shields: int, shieldTurns: int, shieldMaxTurns: int, shieldDamage: int, shieldName: str, minionName: str):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.healingPotions = healingPotions
        self.HealingPotionsName = HealingPotionsName
        self.minionActive = minionActive
        self.minions = minions
        self.minionTurns = minionTurns
        self.minionMaxTurns = minionMaxTurns
        self.shieldActive = shieldActive
        self.shields = shields
        self.shieldTurns = shieldTurns
        self.shieldMaxTurns = shieldMaxTurns
        self.shieldDamage = shieldDamage
        self.shieldName = shieldName
        self.minionName = minionName
        
    def attack(self, opposingPlayer: object, lowest: int, highest: int, testlowest: int, testhighest: int, missPercent: int):
        if self.shieldActive:
            self.shieldTurns -= 1
            if self.shieldTurns <= 0:
                self.shieldActive = False
                print(f"{self.name}'s {self.shieldName} has worn off!")
        minionDamage = 0
        if self.minionActive:
            if self.minionTurns == 1:
                print(f"{self.name}'s {self.minionName} will be deactivated next turn!")
            self.minionTurns -= 1
            minionDamage = rangeRNG(lowest, highest)
            testhighest += 25
        testRng = rangeRNG(testlowest, testhighest)
        if testRng > missPercent:
            hitRng = rangeRNG(lowest, highest)
            damage = hitRng + minionDamage
            finalDamage = damage - opposingPlayer.shieldDamage
            if opposingPlayer.shieldActive:
                finalDamage = damage / self.shieldDamage
            opposingPlayer.health -= finalDamage
            print(f"\nThat's a hit! {hitRng} damage.\n")
            if self.minionActive:
                print(f"Active {self.minionName} added {minionDamage} damage.")
                if self.minionTurns <= 0:
                    self.minionActive = False
            if opposingPlayer.shieldActive:
                print(f"{opposingPlayer.name}'s {opposingPlayer.shieldName} blocked {damage - finalDamage} damage.")
            print("\n")
            print("\nThat's a miss!\n\n")
            return 1
    
    def heal(self):
        if self.health >= self.max_health:
            return 2
        if self.healingPotions <= 0:
            return 3
        self.healingPotions -= 1
        healedHealth = rangeRNG(7, 20)
        self.health += healedHealth
        if self.health > self.max_health:
            total = 0
            while self.health > self.max_health:
                total += 1
                self.health -= 1
            healedHealth -= total
        print(f"{self.name} healed {healedHealth} health!\n")
        return 0

    def shield(self):
        if self.shields <= 0:
            return 6
        elif self.shieldActive:
            return 7
        else:
            print(f"{self.shieldName} enabled and active!")
            self.shieldActive = True
            self.shieldTurns = self.shieldMaxTurns
            self.shields -= 1
            return 0
    
    def summonMinion(self):
        if self.minions <= 0:
            return 4
        if(self.minionActive):
            return 5
        self.minions -= 1
        self.minionActive = True
        self.minionTurns = data["PLAYER1"]["ATTACKS"]["MINIONS"]["TURNS"]
        print(f"{self.minionName} summoned and active!\n")
        return 0

    def getList(self, opposingPlayer: object):
        attacks = {}
        attacks["Small Attack"] = lambda: self.attack(opposingPlayer, 1, 15, 1, 100, 25)
        attacks["Large Attack"] = lambda: self.attack(opposingPlayer, 15, 30, 1, 100, 50)
        attacks[self.HealingPotionsName] = self.heal
        attacks[f"Summon {self.minionName}"] = self.summonMinion
        attacks[f"Use {self.shieldName}"] = self.shield
        return attacks

def finish(winningPlayer: Player):
    print(f"\n{winningPlayer.name} has won the battle with {winningPlayer.health} health!\n")

def turn(player1: Player, player2: Player):
    print(f"\n{getDivider()}\n")
    print(f"Current Turn: {player1.name}\n{player1.name}'s Health: {player1.health}\n{player2.name}'s Health: {player2.health}\n")
    attacks = player1.getList(player2)
    print("\nAttacks:\n")
    index = 0
    for i in attacks:
        print(f"{index + 1}. {i}\n")
        index += 1
    print(f"\nHealing Potions left: {player1.healingPotions}\n")
    print(f"{player1.shieldName}s left: {player1.shields}")
    print(f"\nShields divide damage by {player1.shieldDamage}. They last for 2 of your turns.\n")
    print(f"Available {player1.minionName}s: {player1.minions}\n{player1.minionName}s add a random damage boost (potentially double) but lower your chances of hitting. They last for {player1.minionMaxTurns} of your turns.\n")
    print(f"{player1.minionName} Active?: ")

    if player1.minionActive:
        print("Yes\n")
    else:
        print("No\n")
    
    print("Shield Active?: ")

    if player1.shieldActive:
        print("Yes")
    else:
        print("No")

    print(f"\n{getDivider()}\n")
    print("Type the name of your attack.\n")
    x = ""
    print("> ")
    while True:
        input(x)
        try:
            attak = attacks[x]()
            if attak == 2:
                print("Your health is already at max!\n")
                print("> ")
            elif attak == 3:
                print(f"You don't have any {player1.HealingPotionsName}s!\n")
                print("> ")
            elif attak == 4:
                print(f"You don't have any {player1.minionName}s left!")
                print("> ")
            elif attak == 5:
                print(f"You already have a {player1.minionName} active!")
                print("> ")
            elif attak == 6:
                print(f"You don't have any {player1.shieldName}s left!")
                print("> ")
            elif attak == 7:
                print(f"You already have a {player1.shieldName} active!")
                print("> ")
            else:
                break
        except:
            print(f"Attack \"{x}\" not found!\n")
            print("> ")

def start(player1: Player, player2: Player):
    print(f"Made with BattleEngine v{version} by CombineSoldier14\n")
    print(f"{getDivider()}\n")
    print(f"The battle has begun!\n {player1.name} vs {player2.name}\n\n")
    while player1.health > 0 and player2.health > 0:
        turn(player1, player2)
        if player2.health <= 0:
            finish(player1)
            break
        turn(player2, player1)
        if player1.health <= 0:
            finish(player2)
            break


p1 = Player(
    name = data["PLAYER1"]["NAME"],
    health = data["PLAYER1"]["STARTING_HEALTH"],
    max_health = data["PLAYER1"]["STARTING_HEALTH"],
    healingPotions = data["PLAYER1"]["ATTACKS"]["HEALING_POTIONS"]["AMOUNT"],
    HealingPotionsName = data["PLAYER1"]["ATTACKS"]["HEALING_POTIONS"]["NAME"],
    minions = data["PLAYER1"]["ATTACKS"]["MINIONS"]["AMOUNT"],
    minionActive = False,
    minionTurns =  data["PLAYER1"]["ATTACKS"]["MINIONS"]["TURNS"],
    minionMaxTurns = data["PLAYER1"]["ATTACKS"]["MINIONS"]["TURNS"],
    minionName = data["PLAYER1"]["ATTACKS"]["MINIONS"]["NAME"],
    shieldTurns = 0,
    shieldMaxTurns = data["PLAYER1"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
    shieldActive = False,
    shieldDamage = data["PLAYER1"]["ATTACKS"]["SHIELDS"]["DIVIDE_DAMAGE"],
    shields = data["PLAYER1"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
    shieldName = data["PLAYER1"]["ATTACKS"]["SHIELDS"]["NAME"]
)

p2 = Player(
    name = data["PLAYER2"]["NAME"],
    health = data["PLAYER2"]["STARTING_HEALTH"],
    max_health = data["PLAYER2"]["STARTING_HEALTH"],
    healingPotions = data["PLAYER2"]["ATTACKS"]["HEALING_POTIONS"]["AMOUNT"],
    HealingPotionsName = data["PLAYER2"]["ATTACKS"]["HEALING_POTIONS"]["NAME"],
    minions = data["PLAYER2"]["ATTACKS"]["MINIONS"]["AMOUNT"],
    minionActive = False,
    minionTurns =  data["PLAYER2"]["ATTACKS"]["MINIONS"]["TURNS"],
    minionMaxTurns = data["PLAYER2"]["ATTACKS"]["MINIONS"]["TURNS"],
    minionName = data["PLAYER2"]["ATTACKS"]["MINIONS"]["NAME"],
    shieldTurns = 0,
    shieldMaxTurns = data["PLAYER2"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
    shieldActive = False,
    shieldDamage = data["PLAYER2"]["ATTACKS"]["SHIELDS"]["DIVIDE_DAMAGE"],
    shields = data["PLAYER2"]["ATTACKS"]["SHIELDS"]["AMOUNT"],
    shieldName = data["PLAYER2"]["ATTACKS"]["SHIELDS"]["NAME"]
)

start(p1, p2)
