def nbt_text(text):
    return "{\"text\":\""+text+"\"}"


def nbt_format(nbt):
    if type(nbt) == dict:
        return "{" + ",".join([
            key + ":" + nbt_format(value) for key, value in nbt.items() if value != None
        ]) + "}"
    if type(nbt) == list:
        return "[" + ",".join([nbt_format(el) for el in nbt if el != None]) + "]"
    if type(nbt) == str:
        return "\"" + nbt.replace("\"", "\\\"") + "\""
    if type(nbt) == int:
        return str(nbt)
    if type(nbt) == float:
        return str(nbt) + "f"
    else:
        return str(type(nbt))


class Sale:
    def __init__(self, buy, buyB, sell):
        self.buy = buy
        self.buyB = buyB
        self.sell = sell

    def outp(self):
        nbt = {
            "rewardExp": 0,
            "maxUses": 2147483647,
            "buy": {
                "id": self.buy[0],
                "Count": self.buy[1]
            },
            "sell": {
                "id": self.sell[0],
                "Count": self.sell[1],
                "tag": {
                    "CustomModelData": self.sell[2] if len(self.sell) > 2 else None,
                    "display": {
                        "Name": nbt_text(self.sell[3])
                    } if len(self.sell) > 3 else None
                }
            }
        }

        return nbt


class Villager:
    def __init__(self, name, biome, rotation, offers):
        self.name = name
        self.biome = biome
        self.rotation = rotation
        self.offers = offers

    def outp(self):
        nbt = {
            "CustomName": nbt_text(self.name),
            "CustomNameVisible": 1,
            "Rotation": [float(self.rotation), float(0)],
            "NoAI": 1,
            "Invulnerable": 1,
            "VillagerData": {
                "type": self.biome,
                "profession": "mason",
                "level": 6
            },
            "Offers": {
                "Recipes": [offer.outp() for offer in self.offers]
            }
        }
        return nbt

    def summon(self):
        return "summon minecraft:villager ~ ~1.5 ~ " + nbt_format(self.outp())


villagers = [
    Villager("Cheese Master", "jungle", -90, [
        Sale(("emerald", 1), None, ("pumpkin_pie", 1, 14170001, "Cheese")),
        Sale(("emerald", 1), None, ("pumpkin_pie", 1, 14170002, "Pizza")),
        Sale(("emerald", 1), None, ("pumpkin_pie", 1, 14170003, "Cheese Wheel")),
        Sale(("emerald", 5), None, ("cooked_porkchop", 1, 14170004, "Grilled Cheese"))
    ]),
    Villager("Penguin King", "plains", 180, [
        Sale(("totem_of_undying", 1), None,
             ("totem_of_undying", 1, 14180001, "Penguin of Undying")),
        Sale(("totem_of_undying", 1), None, ("totem_of_undying", 1))
    ]),
    Villager("Bobo Brime Bames", "plains", 0, [
        Sale(("totem_of_undying", 1), None,
             ("totem_of_undying", 1, 14190001, "Totem of Bobo")),
        Sale(("totem_of_undying", 1), None, ("totem_of_undying", 1))
    ]),
    Villager("Kingmooshelper", "plains", 0, [
        Sale(("totem_of_undying", 1), None,
             ("totem_of_undying", 1, 14200001, "Moo's Extra Life")),
        Sale(("totem_of_undying", 1), None, ("totem_of_undying", 1))
    ]),
]

for villager in villagers:
    print("")
    print("Villager: " + villager.name)
    print("")
    print(villager.summon())
