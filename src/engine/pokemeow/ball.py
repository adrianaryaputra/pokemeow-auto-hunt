from typing import List
from engine.configurator import cfg



class ErrorUndefinedBalls(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Undefined balls: {name}")



class PokeBall:
    def __init__(self, ball_name: str, ball_type: int):
        self.name = ball_name
        self.type = ball_type
        self.count = 0
        self.minimal = cfg.getPokeBuyAt(ball_type)
        self.buyqty = cfg.getPokeBuyQty(ball_type)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def setMinimal(self, minimal: int):
        self.minimal = minimal
        cfg.setPokeBuyAt(self.type, minimal)

    def setCount(self, count: int):
        self.count = count

    def setBuyQty(self, buy_quantity: int):
        self.buyqty = buy_quantity
        cfg.setPokeBuyQty(self.type, buy_quantity)

    def shouldbuy(self) -> bool:
        return self.count < self.minimal

    def buy(self) -> str:
        return f';s b {str(self.type)} {str(self.buyqty)}'



class PokeBalls:
    Reg = PokeBall("pb", 1)
    Great = PokeBall("gb", 2)
    Ultra = PokeBall("ub", 3)
    Master = PokeBall("mb", 4)
    Premier = PokeBall("prb", 5)
    Dive = PokeBall("db", 6)

    @classmethod
    def print(self):
        print(f"{self.Reg} {self.Great} {self.Ultra} {self.Master} {self.Premier}")


    @classmethod
    def findball(self, ball_name: str) -> PokeBall:
        for balls in self.__dict__.items():
            if str(balls[1]).lower() == ball_name.lower():
                return getattr(PokeBalls, balls[0])

        raise ErrorUndefinedBalls(ball_name)

    @classmethod
    def getBalls(self) -> List[PokeBall]:
        return [
            self.Reg,
            self.Great,
            self.Ultra,
            self.Master,
            self.Premier,
            self.Dive
        ]
