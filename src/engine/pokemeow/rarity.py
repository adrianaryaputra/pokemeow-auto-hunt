import re
from typing import List

from .ball import PokeBall, PokeBalls
from engine.configurator import cfg



class ErrorUndefinedRarities(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Undefined rarity: {name}")



class PokeRarity:
    def __init__(self, regex, name: str, type: int) -> None:
        self.regex = regex
        self.name: str = name
        self.type: int = type
        self.balls = PokeBalls.findball(
            cfg.getPokeThrow(type)
        )

    def __str__(self) -> str:
        return self.name

    def re(self) -> str:
        return self.regex

    def ball(self) -> str:
        return str(self.balls)

    def getBall(self) -> PokeBall:
        return self.balls

    def setBall(self, ball: PokeBall) -> None:
        self.balls = ball
        cfg.setPokeThrow(self.type, str(ball))




class PokeRarities:
    COMMON: PokeRarity = PokeRarity(r"Common", "Common", 1)
    UNCOMMON: PokeRarity = PokeRarity(r"Uncommon", "Uncommon", 2)
    RARE: PokeRarity = PokeRarity(r"Rare", "Rare", 3)
    SHINYF: PokeRarity = PokeRarity(r"Shiny \(F", "ShinyFull", 4)
    SUPERRARE: PokeRarity = PokeRarity(r"Super Rare", "SuperRare", 5)
    LEGENDARY: PokeRarity = PokeRarity(r"Legendary", "Legendary", 6)
    SHINYA: PokeRarity = PokeRarity(r"Shiny \(A", "ShinyApprox", 7)
    SHINYE: PokeRarity = PokeRarity(r"Shiny \(E", "ShinyEvent", 8)
    SHINY: PokeRarity = PokeRarity(r"Shiny \([0-9]", "Shiny", 9)
    FISH_NORMAL: PokeRarity = PokeRarity(r"fished out", "FishNormal", 10)
    FISH_KYOGRE: PokeRarity = PokeRarity(r"fished out", "FishKyogre", 11)
    FISH_SUICUNE: PokeRarity = PokeRarity(r"fished out", "FishSuicune", 12)
    FISH_SHINY: PokeRarity = PokeRarity(r"fished out", "FishShiny", 13)
    FISH_GOLDEN: PokeRarity = PokeRarity(r"fished out", "FishGolden", 14)

    @classmethod
    def compiledRe(self) -> str:
        return r"({})".format("|".join(r.re() for r in [
                self.COMMON,
                self.UNCOMMON,
                self.RARE,
                self.SHINYF,
                self.SUPERRARE,
                self.LEGENDARY,
                self.SHINYA,
                self.SHINYE,
                self.SHINY
            ]))

    @classmethod
    def reg2type(self, reg: str) -> str:
        for r in [
            self.COMMON, 
            self.UNCOMMON, 
            self.RARE, 
            self.SHINYF, 
            self.SUPERRARE, 
            self.LEGENDARY, 
            self.SHINYA, 
            self.SHINYE,
            self.SHINY
        ]:
            if re.match(r.re(), reg):
                return r
        return None


    @classmethod
    def changeBall(self, rarity: str, ball: str) -> None:
        r: PokeRarity = self.findRarity(rarity)
        if r is not None: r.setBall(PokeBalls.findball(ball))

    @classmethod
    def findRarity(self, rarity_name: str) -> PokeRarity:
        for rarity in self.__dict__.items():
            if str(rarity[1]).lower() == rarity_name.lower():
                return getattr(PokeRarities, rarity[0])
        
        raise ErrorUndefinedRarities(rarity_name)

    @classmethod
    def getRarities(self) -> List[PokeRarity]:
        return [
            self.COMMON,
            self.UNCOMMON,
            self.RARE,
            self.SHINYF,
            self.SUPERRARE,
            self.LEGENDARY,
            self.SHINYA,
            self.SHINYE,
            self.SHINY,
            self.FISH_NORMAL,
            self.FISH_KYOGRE,
            self.FISH_SUICUNE,
            self.FISH_SHINY,
            self.FISH_GOLDEN,
        ]