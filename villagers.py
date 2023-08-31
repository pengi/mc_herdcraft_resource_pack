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

    def sale_nbt(self):
        return {
            "CustomModelData": self.sell[2] if len(self.sell) > 2 else None,
            "display": {
                "Name": nbt_text(self.sell[3])
            } if len(self.sell) > 3 else None
        }

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
                "tag": self.sale_nbt()
            }
        }

        return nbt

    def is_custom(self):
        return len(self.sell) > 2

    def give(self):
        return "give @p %s%s" % (self.sell[0], nbt_format(self.sale_nbt()))

# give @p chest{BlockEntityTag:{Items:[{Slot:0,id:totem_of_undying,Count:1},{Slot:1,id:totem_of_undying,Count:1},{Slot:2,id:totem_of_undying,Count:1},{Slot:3,id:totem_of_undying,Count:1},{Slot:4,id:totem_of_undying,Count:1},{Slot:5,id:totem_of_undying,Count:1},{Slot:6,id:totem_of_undying,Count:1},{Slot:7,id:totem_of_undying,Count:1},{Slot:8,id:totem_of_undying,Count:1},{Slot:9,id:totem_of_undying,Count:1},{Slot:10,id:totem_of_undying,Count:1},{Slot:11,id:totem_of_undying,Count:1},{Slot:12,id:totem_of_undying,Count:1},{Slot:13,id:totem_of_undying,Count:1},{Slot:14,id:totem_of_undying,Count:1},{Slot:15,id:totem_of_undying,Count:1},{Slot:16,id:totem_of_undying,Count:1},{Slot:17,id:totem_of_undying,Count:1},{Slot:18,id:totem_of_undying,Count:1},{Slot:19,id:totem_of_undying,Count:1},{Slot:20,id:totem_of_undying,Count:1},{Slot:21,id:totem_of_undying,Count:1},{Slot:22,id:totem_of_undying,Count:1},{Slot:23,id:totem_of_undying,Count:1},{Slot:24,id:totem_of_undying,Count:1},{Slot:25,id:totem_of_undying,Count:1},{Slot:26,id:totem_of_undying,Count:1}]}}


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

    def gives(self):
        return [offer.give() for offer in self.offers if offer.is_custom()]


villagers = [
    Villager("Cheese Master", "jungle", -90, [
        Sale(("emerald", 1), None, ("pumpkin_pie", 1, 14170001, "Cheese")),
        Sale(("emerald", 1), None, ("pumpkin_pie", 1, 14170002, "Pizza")),
        Sale(("emerald", 1), None, ("pumpkin_pie", 1, 14170003, "Cheese Wheel")),
        Sale(("emerald", 5), None, ("cooked_porkchop", 1, 14170004, "Grilled Cheese"))
    ]),
    Villager("Penguin King", "plains", 180, [
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 14180002, "Professor Hair")),
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
    Villager("Santa Claus", "plains", 0, [
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 14170005, "Santas hat"))
    ]),
    Villager("LandLand souvenirs", "plains", 0, [
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 14210001, "Antennas")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 14210002, "Gloria")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 14210003, "Green Hat")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 14210004, "Mooshroom Hat")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 14210005, "Rainbow Pig Hat")),
        Sale(("emerald", 1), None, ("beetroot_soup", 1, 14210006, "LandLand Ice Cream"))
    ]),
    Villager("sebxter hats", "plains", 0, [
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 10110015, "Hat 1")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 10110016, "Hat 2")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 10110017, "Hat 3")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 10110018, "Hat 4")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 10110019, "Hat 5")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 10110020, "Hat 6")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 10110021, "Hat 7")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 10110022, "Hat 8")),
        Sale(("emerald", 1), None, ("carved_pumpkin", 1, 10110023, "Hat 9")),
    ]),
    Villager("Everything else", "plains", 0, [
        Sale(("emerald", 1), None, ("shield", 1, 14170006, "Mobile Router"))
    ]),
]

for villager in villagers:
    print("")
    print("Villager: " + villager.name)
    print("")
    print(villager.summon())
    print("")
    for give_cmd in villager.gives():
        print(give_cmd)
