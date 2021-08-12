import asyncio
from typing import List
import discord
from discord.ext import commands as BotCmd

from engine.configurator import cfg
from engine.pokemeow import PokeRarities, PokeBalls


class Main(BotCmd.Cog):
    """
    Main cog for the bot.
    """

    def __init__(self, bot: BotCmd.Bot) -> None:
        self.bot = bot
        self.token = cfg.getToken()

    @BotCmd.command(aliases=["p"])
    async def ping(self, ctx: BotCmd.Context) -> None:
        """
        ping the bot
        """
        await ctx.message.delete()
        await ctx.send(f"pong! {self.bot.latency}")

    @BotCmd.command(aliases=["h"])
    async def help(self, ctx: BotCmd.Context) -> None:
        """
        show help
        """
        await ctx.message.delete()
        emb = discord.Embed(title="Welcome to PokeMeow Sniper Bot!", color=discord.Color(0))
        emb.description = txt_help_desc()
        emb.add_field(name="`$help`,  `$h`", value="Show you this window\n‎", inline=False)
        emb.add_field(name="`$ping`,  `$p`", value="Play Ping-Pong with you\n‎", inline=False)
        emb.add_field(name="`$config`,  `$stats`,  `$q`", value="Show config parameter\n‎", inline=False)
        emb.add_field(name="`$set`,  `$e`", value="Set config parameter\n‎", inline=False)
        emb.add_field(name="`$enable [nitro|pokemeow]`", value="Enable bot\n‎", inline=False)
        emb.add_field(name="`$disable [nitro|pokemeow]`", value="Disable bot\n‎", inline=False)
        emb.add_field(name="`$poke [start|stop] <p|f>`", value="start auto poke catch or fish\n‎", inline=False)
        emb.set_footer(text = txt_footl())
        await ctx.send(embed=emb)

    @BotCmd.command(aliases=["stats", "q"])
    async def config(self, ctx: BotCmd.Context) -> None:
        """
        show configuration
        """
        await ctx.message.delete()
        emb = discord.Embed(title="PokeMeow Sniper Configuration", color=discord.Color(0))
        emb.description = txt_config_desc()
        emb.add_field(name="**Bot Running**", value=txt_config_f_botrun(), inline=False)
        emb.add_field(name="**PokeMeow Delay Value**", value=txt_config_f_delay(), inline=False)
        emb.add_field(name="**PokeMeow Minimum Ball Stock**", value=txt_config_f_min(), inline=False)
        emb.add_field(name="**PokeMeow Ball Buying Lot**", value=txt_config_f_lot(), inline=False)
        emb.add_field(name="**PokeMeow Catch Ball Selection**", value=txt_config_f_rarity(), inline=False)
        emb.set_footer(text=txt_footl())
        msg = await ctx.send(embed=emb)
        await asyncio.sleep(5)
        await msg.delete()


    @BotCmd.command(aliases=["e"])
    async def set(self, ctx: BotCmd.Context, mode: str = "", variable: str = "", value: str = "") -> None:
        """
        set configuration
        """
        await ctx.message.delete()
        modesel = ["delay", "stock", "buy", "catch"]
        ballbuyable = [str(b).lower() for b in PokeBalls.getBalls()][0:4]
        ballsel = [str(b).lower() for b in PokeBalls.getBalls()]
        raritysel = [str(r).lower() for r in PokeRarities.getRarities()]
        pokecmd = ["catch", "fish"]


        if mode == "":
            emb = discord.Embed(title="PokeMeow Sniper Setting", color=discord.Color(0))
            emb.description = txt_headl()
            emb.add_field(name=f"`$set {modesel[0]} [{'|'.join(pokecmd)}] <num>`", value=f"change delay interval of catch and fishing\n‎", inline=False)
            emb.add_field(name=f"`$set {modesel[1]} [{'|'.join(ballbuyable)}] <num>`", value=f"change minimum amount of ball to stock\n‎", inline=False)
            emb.add_field(name=f"`$set {modesel[2]} [{'|'.join(ballbuyable)}] <num>`", value=f"change amount of ball to buy at once\n‎", inline=False)
            emb.add_field(name=f"`$set {modesel[3]} [rarity] <ball>`", value=txt_set_catch(ballsel, raritysel), inline=False)
            emb.set_footer(text=txt_footl())
            msg = await ctx.send(embed=emb)
            await asyncio.sleep(5)
            await msg.delete()

        elif mode == "delay":
            msg = await ctx.send(embed = self.handleDelay(variable, value, pokecmd))
            await asyncio.sleep(5)
            await msg.delete()

        elif mode == "stock":
            msg = await ctx.send(embed = self.handleStock(variable, value, ballbuyable))
            await asyncio.sleep(5)
            await msg.delete()

        elif mode == "buy":
            msg = await ctx.send(embed = self.handleBuy(variable, value, ballbuyable))
            await asyncio.sleep(5)
            await msg.delete()

        elif mode == "catch":
            msg = await ctx.send(embed = self.handleCatch(variable, value, ballsel, raritysel))
            await asyncio.sleep(5)
            await msg.delete()

        else:
            msg = await ctx.send(embed = emb_wrong_mode("set", mode, modesel))
            await asyncio.sleep(5)
            await msg.delete()

    @BotCmd.command()
    async def enable(self, ctx: BotCmd.Context, mode: str = "") -> None:
        """
        enable bot
        """
        bots = ["nitro", "pokemeow"]
        example = f"\nexample: `$enable {bots[0]}`"
        await ctx.message.delete()
        if mode == "":
            msg = await ctx.send(embed = emb_unspecified_mode("enable", bots, example))
            await asyncio.sleep(5)
            await msg.delete()
            return
        if mode.lower() == "nitro":
            cfg.setNitro(True)
        elif mode.lower() == "pokemeow":
            cfg.setPokeMeow(True)
        else:
            msg = await ctx.send(embed = emb_wrong_mode("enable", mode, bots))
            await asyncio.sleep(5)
            await msg.delete()
            return
        msg = await ctx.send(embed = emb_success("Success!", f"`{mode.capitalize()}` is `{toggleMaker(True)}`..."))
        await asyncio.sleep(5)
        await msg.delete()


    @BotCmd.command()
    async def disable(self, ctx: BotCmd.Context, mode: str = "") -> None:
        """
        stop bot
        """
        bots = ["nitro", "pokemeow"]
        example = f"\nexample: `$disable {bots[0]}`"
        await ctx.message.delete()
        if mode == "":
            msg = await ctx.send(embed = emb_unspecified_mode("disable", bots, example))
            await asyncio.sleep(5)
            await msg.delete()
            return
        if mode.lower() == "nitro":
            cfg.setNitro(False)
        elif mode.lower() == "pokemeow":
            cfg.setPokeMeow(False)
        else:
            msg = await ctx.send(embed = emb_wrong_mode("disable", mode, bots))
            await asyncio.sleep(5)
            await msg.delete()
            return
        msg = await ctx.send(embed = emb_success("Success!", f"`{mode.capitalize()}` is `{toggleMaker(False)}`..."))
        await asyncio.sleep(5)
        await msg.delete()



    def handleDelay(self, poke_bot_cmd: str, value_delay: str, var: List[str]) -> None:
        example = f"\nexample: `$set delay {var[0]} 11`"
        if poke_bot_cmd == "":
            return emb_unspecified_mode("delay", var, example)
        if poke_bot_cmd.lower() not in var:
            return emb_wrong_mode("delay", poke_bot_cmd, var, example)
        if value_delay == "":
            return emb_unspecified_value("delay", example, var)
        if not value_delay.isdigit():
            return emb_wrong_value("delay", value_delay, "number", example)
        if poke_bot_cmd.lower() == "catch":
            cfg.setPokeDelay(1, int(value_delay))
        if poke_bot_cmd.lower() == "fish":
            cfg.setPokeDelay(2, int(value_delay))
        return emb_success("Success!", f"Delay for `{poke_bot_cmd}` is set to `{value_delay}` seconds...")


    def handleStock(self, ball_type: str, value: str, mode_balls: List[str]) -> None:
        example = f"\nexample: `$set stock {mode_balls[0]} 10`"
        if ball_type == "":
            return emb_unspecified_mode("stock", mode_balls, example)
        if ball_type.lower() not in mode_balls:
            return emb_wrong_mode("stock", ball_type, mode_balls, example)
        if value == "":
            return emb_unspecified_value("stock", example)
        if not value.isdigit():
            return emb_wrong_value("stock", value, "number", example)
        if ball_type.lower() == str(PokeBalls.Reg):
            cfg.setPokeBuyAt(PokeBalls.Reg.type, int(value))
        if ball_type.lower() == str(PokeBalls.Great):
            cfg.setPokeBuyAt(PokeBalls.Great.type, int(value))
        if ball_type.lower() == str(PokeBalls.Ultra):
            cfg.setPokeBuyAt(PokeBalls.Ultra.type, int(value))
        if ball_type.lower() == str(PokeBalls.Master):
            cfg.setPokeBuyAt(PokeBalls.Master.type, int(value))
        return emb_success("Success!", f"Stock for `{ball_type}` is set to `{value}`")


    def handleBuy(self, variable: str, value: str, mode_balls: List[str]) -> None:
        example = f"\nexample: `$set buy {mode_balls[0]} 10`"
        if variable == "":
            return emb_unspecified_mode("buy", mode_balls, example)
        if variable.lower() not in mode_balls:
            return emb_wrong_mode("buy", variable, mode_balls, example)
        if value == "":
            return emb_unspecified_value("buy", example)
        if not value.isdigit():
            return emb_wrong_value("buy", value, "number", example)
        if variable.lower() == str(PokeBalls.Reg):
            cfg.setPokeBuyQty(PokeBalls.Reg.type, int(value))
        if variable.lower() == str(PokeBalls.Great):
            cfg.setPokeBuyQty(PokeBalls.Great.type, int(value))
        if variable.lower() == str(PokeBalls.Ultra):
            cfg.setPokeBuyQty(PokeBalls.Ultra.type, int(value))
        if variable.lower() == str(PokeBalls.Master):
            cfg.setPokeBuyQty(PokeBalls.Master.type, int(value))
        return emb_success("Success!", f"Buying quantity for `{variable}` is set to `{value}`")


    def handleCatch(self, poke_rarities: str, ball_used: str, val_balls: List[str], mode_rarities: List[str]) -> None:
        example = f"\nexample: `$set catch {mode_rarities[0]} {val_balls[0]}`"

        if poke_rarities == "":
            return emb_unspecified_mode("catch", mode_rarities, example)
        if poke_rarities.lower() not in mode_rarities:
            return emb_wrong_mode("catch", poke_rarities, mode_rarities, example)
        if ball_used == "":
            return emb_unspecified_value("catch", example, val_balls)
        if ball_used.lower() not in val_balls:
            return emb_wrong_value("catch", ball_used, "pokeball type", example)
        if poke_rarities.lower() == str(PokeRarities.COMMON).lower():
            cfg.setPokeThrow(PokeRarities.COMMON.type, ball_used)
        if poke_rarities.lower() == str(PokeRarities.UNCOMMON).lower():
            cfg.setPokeThrow(PokeRarities.UNCOMMON.type, ball_used)
        if poke_rarities.lower() == str(PokeRarities.RARE).lower():
            cfg.setPokeThrow(PokeRarities.RARE.type, ball_used)
        if poke_rarities.lower() == str(PokeRarities.SHINYF).lower():
            cfg.setPokeThrow(PokeRarities.SHINYF.type, ball_used)
        if poke_rarities.lower() == str(PokeRarities.SUPERRARE).lower():
            cfg.setPokeThrow(PokeRarities.SUPERRARE.type, ball_used)
        if poke_rarities.lower() == str(PokeRarities.LEGENDARY).lower():
            cfg.setPokeThrow(PokeRarities.LEGENDARY.type, ball_used)
        if poke_rarities.lower() == str(PokeRarities.SHINYA).lower():
            cfg.setPokeThrow(PokeRarities.SHINYA.type, ball_used)
        if poke_rarities.lower() == str(PokeRarities.SHINYE).lower():
            cfg.setPokeThrow(PokeRarities.SHINYE.type, ball_used)
        return emb_success("Success!", f"`{poke_rarities.capitalize()}` is now catched using `{ball_used}`")




def setup(bot) -> None:
    bot.add_cog(Main(bot))



# EVERYTHING AFTER THIS IS TRASH LOL
# ===========================================
# WELCOME TO TRASHLAND

def txt_headl(): return "=============================="
def txt_footl(): return "============ Farabot © 2021 ============"
def toggleMaker(toggle: bool): return "Enabled ✅" if toggle else "Disabled ❌"
def txt_help_desc(): return f"""
We help you to catch the best pokemon

**⚠ WARNING!**
Bot is under heavy developement
use at your own risk!

{txt_headl()}
**Available Command:**
"""
def txt_config_desc(): return f"""
to edit these configuration, use `$set`


{txt_headl()}
"""
def txt_config_f_botrun(): return f"""
NITRO Sniper : `{  toggleMaker(cfg.getNitro())}`
PokeMeow Farm : `{ toggleMaker(cfg.getPokeMeow())}`
‎
"""
def txt_config_f_delay(): return f"""
PokeCatch : `{  cfg.getPokeDelay(1)} sec`
PokeFish : `{   cfg.getPokeDelay(2)} sec`
‎
"""
def txt_config_f_min(): return f"""
PokeBall : `{   cfg.getPokeBuyAt(1)} pcs`
GreatBall : `{  cfg.getPokeBuyAt(2)} pcs`
UltraBall : `{  cfg.getPokeBuyAt(3)} pcs`
MasterBall : `{ cfg.getPokeBuyAt(4)} pcs`
‎
"""
def txt_config_f_lot(): return f"""
PokeBall : `{   cfg.getPokeBuyQty(1)} pcs`
GreatBall : `{  cfg.getPokeBuyQty(2)} pcs`
UltraBall : `{  cfg.getPokeBuyQty(3)} pcs`
MasterBall : `{ cfg.getPokeBuyQty(4)} pcs`
‎
"""
def txt_config_f_rarity(): return f"""
Common : `{      cfg.getPokeThrow(1)} ball`
Uncommon : `{    cfg.getPokeThrow(2)} ball`
Rare : `{        cfg.getPokeThrow(3)} ball`
Super Rare : `{  cfg.getPokeThrow(5)} ball`
Legendary : `{   cfg.getPokeThrow(6)} ball`
Shiny (Full) : `{cfg.getPokeThrow(4)} ball`
Shiny (Appr) : `{cfg.getPokeThrow(7)} ball`
Shiny (Exac) : `{cfg.getPokeThrow(8)} ball`
‎
"""
def txt_set_catch(ballsel: List[str], raritysel: List[str]): return f"""
change the ball used to catch pokemon

**rarity selection:**
{txt_listify(raritysel)}

**ball selection:**
{txt_listify(ballsel)}
‎
"""

def txt_listify(l: List[str]) -> str:
    return "\n".join([f"- `{e}`" for e in l])

def txt_enumify(l: List[str]) -> str:
    return "\n".join([f"{i}. `{e}`" for e,i in enumerate(l)])

def emb_fail(failtxt: str, desc: str, example: str = ""):
    emb = discord.Embed(color = discord.Color(0))
    emb.add_field(name="🔴 " + failtxt, value = (("‎\n"+desc+"\n") if desc else "‎") + example)
    return emb

def emb_success(successtxt: str, desc: str):
    emb = discord.Embed(color = discord.Color(0))
    emb.add_field(name="🟢 " + successtxt, value = "‎\n" + desc + "\n")
    return emb

def emb_unspecified_mode(cmd: str, modesel:List[str], example: str):
    return emb_fail(
        f"Please specify bot mode!",
        f"mode available in **${cmd}** :\n{txt_listify(modesel)}",
        example
    )

def emb_unspecified_value(cmd: str, example: str, limitedVal:List[str] = None):
    return emb_fail(
        f"Please specify value!",
        f"value available in **${cmd}** :\n{txt_listify(limitedVal)}" if limitedVal else "", 
        example
    )

def emb_wrong_mode(cmd: str, mode: str, modesel: List[str], example: str = ""):
    return emb_fail(
        f"invalid mode '{mode}'!",
        f"**${cmd}** can only be used with :\n{txt_listify(modesel)}",
        example,
    )

def emb_wrong_value(cmd: str, value: str, valueType: str, example: str = ""):
    return emb_fail(
        f"invalid value '{value}'!",
        f"value should be a {valueType}",
        example,
    )
        