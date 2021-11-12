import requests

from tools.loadConfig import ConfigLoader
from tools.observable import BasicPublisher
from tools.formatcmd import dateprint, dateinput



class ErrorInvalidToken(Exception):
    def __init__(self, token) -> None:
        self.token = token
        super().__init__(f"Invalid token: {token}")



class Config(BasicPublisher):
    """
    configurator.Config is the class that contains all the configuration
    information for the application.
    """

    _cfg: ConfigLoader = ConfigLoader()
    value = None
    

    def __init__(self) -> None:
        """
        Initializes the Config class.
        """
        super().__init__()
        self.__initValue()
        
    
    def __initValue(self) -> None:
        """
        Initializes the options for the Config class.
        """
        class BotValue:
            token = self._cfg.getConfigOption("Discord", "token")
            prefix = self._cfg.getConfigOption("Opt", "prefix")
            nickname = self._cfg.getConfigOption("PokeMeow", "nickname")
            captchatoken = self._cfg.getConfigOption("2captcha", "token")
            
            nitro = self._cfg.yn2bool(self._cfg.getConfigOption("Bot", "nitro"))
            giveaway = self._cfg.yn2bool(self._cfg.getConfigOption("Bot", "giveaway"))
            pokemeow = self._cfg.yn2bool(self._cfg.getConfigOption("Bot", "pokemeow"))

            poke_delay = self._cfg.str2intarr(self._cfg.getConfigOption("PokeMeow", "delay"))
            poke_buyat = self._cfg.str2intarr(self._cfg.getConfigOption("PokeMeow", "buyat"))
            poke_buyqty = self._cfg.str2intarr(self._cfg.getConfigOption("PokeMeow", "buyqty"))
            poke_throw = self._cfg.str2strarr(self._cfg.getConfigOption("PokeMeow", "throw"))

        self.value = BotValue()


    def handleInvalidToken(self, token: str) -> None:
        """
        Handles an invalid token.
        """
        dateprint("Invalid token: " + token)
        print("")
        t = dateinput("Please enter your bot token: ")
        vt = self.checkToken(t)
        if vt is None:
            return self.handleInvalidToken(t)
        self.setToken(t)
        
    
    def setToken(self, token: str) -> None:
        """
        Sets the value for the token option.
        """
        self.value.token = self.checkToken(token)
        self.notifySub({"token": token})
        self._cfg.setConfigOption("Discord", "token", token)

    
    def getToken(self) -> str:
        """
        Returns the value for the token option.
        """
        return self.value.token


    def checkToken(self, auth: str = None) -> bool:
        """
        Checks if the token is valid.
        """
        if auth is None:
            auth = self.getToken()
        headers = {'Content-Type': 'application/json', 'authorization': auth}
        url = "https://discordapp.com/api/v6/users/@me/library"
        req = requests.get(url, headers=headers)
        if req.status_code != 200:
            self.notifySub({"InvalidToken": auth})
            return None
        return auth


    def getCaptchaToken(self) -> str:
        """
        Returns the value for the 2captcha token option.
        """
        return self.value.captchatoken

    
    def setNitro(self, nitro: bool) -> None:
        """
        Sets the value for the nitro option.
        """
        self.value.nitro = nitro
        self.notifySub({"nitro": nitro})
        self._cfg.setConfigOption("Bot", "nitro", self._cfg.bool2yn(nitro))

    
    def getNitro(self) -> bool:
        """
        Returns the value for the nitro option.
        """
        return self.value.nitro

    
    def setGiveaway(self, giveaway: bool) -> None:
        """
        Sets the value for the giveaway option.
        """
        self.value.giveaway = giveaway
        self.notifySub({"giveaway": giveaway})
        self._cfg.setConfigOption("Bot", "giveaway", self._cfg.bool2yn(giveaway))


    def getGiveaway(self) -> bool:
        """
        Returns the value for the giveaway option.
        """
        return self.value.giveaway


    def setPokeMeow(self, pokemeow: bool) -> None:
        """
        Sets the value for the pokemeow option.
        """
        self.value.pokemeow = pokemeow
        self.notifySub({"pokemeow": pokemeow})
        self._cfg.setConfigOption("Bot", "pokemeow", self._cfg.bool2yn(pokemeow))


    def getPokeMeow(self) -> bool:
        """
        Returns the value for the pokemeow option.
        """
        return self.value.pokemeow


    def setPrefix(self, prefix: str) -> None:
        """
        Sets the value for the prefix option.
        """
        self.value.prefix = prefix
        self.notifySub({"prefix": prefix})
        self._cfg.setConfigOption("Opt", "prefix", prefix)


    def getPrefix(self) -> str:
        """
        Returns the value for the prefix option.
        """
        return self.value.prefix


    def setPokeDelay(self, poke: int, delay: int) -> None:
        """
        Sets the value for the poke delay option.
        """
        self.value.poke_delay[poke-1] = delay
        self.notifySub({"delay": self.value.poke_delay})
        self._cfg.setConfigOption("PokeMeow", "delay", self._cfg.intarr2str(self.value.poke_delay))

    
    def getPokeDelay(self, command: int = None) -> int:
        """
        Returns the value for the poke delay option.
        """
        if command is None: return self.value.poke_delay
        return self.value.poke_delay[command-1]


    def setPokeBuyAt(self, ball: int, buyAt: int) -> None:
        """
        Sets the value for the poke buy at option.
        """
        self.value.poke_buyat[ball-1] = buyAt
        self.notifySub({"buyat": self.value.poke_buyat})
        self._cfg.setConfigOption("PokeMeow", "buyat", self._cfg.intarr2str(self.value.poke_buyat))


    def getPokeBuyAt(self, ball: int = None) -> int:
        """
        Returns the value for the poke buy at option.
        """
        if ball is None: return self.value.poke_buyat
        return self.value.poke_buyat[ball-1]


    def setPokeBuyQty(self, ball: int, buyQty: int) -> None:
        """
        Sets the value for the poke buy qty option.
        """
        self.value.poke_buyqty[ball-1] = buyQty
        self.notifySub({"buyqty": self.value.poke_buyqty})
        self._cfg.setConfigOption("PokeMeow", "buyqty", self._cfg.intarr2str(self.value.poke_buyqty))

    
    def getPokeBuyQty(self, ball: int = None) -> int:
        """
        Returns the value for the poke buy qty option.
        """
        if ball is None: return self.value.poke_buyqty
        return self.value.poke_buyqty[ball-1]


    def setPokeThrow(self, poke: int, ball: str) -> None:
        """
        Sets the value for the poke throw option.
        """
        self.value.poke_throw[poke-1] = ball
        self.notifySub({"throw": self.value.poke_throw})
        self._cfg.setConfigOption("PokeMeow", "throw", self._cfg.strarr2str(self.value.poke_throw))


    def getPokeThrow(self, poke: int = None) -> str:
        """
        Returns the value for the poke throw option.
        """
        if poke is None: return self.value.poke_throw
        return self.value.poke_throw[poke-1]

    
    def setNickname(self, nickname: str) -> None:
        """
        Sets the value for the nickname option. 
        """
        self.value.nickname = nickname
        self.notifySub({"nickname": nickname})
        self._cfg.setConfigOption("PokeMeow", "nickname", nickname)

    
    def getNickname(self) -> str:
        """
        Returns the value for the nickname option.
        """
        return self.value.nickname


cfg: Config = Config()