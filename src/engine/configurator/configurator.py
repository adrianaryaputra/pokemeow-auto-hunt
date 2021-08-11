import requests

from tools.loadConfig import ConfigLoader
from tools.observable import BasicPublisher



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

            nitro = self._cfg.yn2bool(self._cfg.getConfigOption("Bot", "nitro"))
            giveaway = self._cfg.yn2bool(self._cfg.getConfigOption("Bot", "giveaway"))
            pokemeow = self._cfg.yn2bool(self._cfg.getConfigOption("Bot", "pokemeow"))

        self.value = BotValue()

    
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
        return auth

    
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


cfg: Config = Config()