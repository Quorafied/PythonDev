from _ownLibrary import *
from database._database import *
from main import function
from imageRecgonition import *
from discord import app_commands
from discord.app_commands import Choice
import discord
from typing import Optional
from discord.ext import commands, tasks
import traceback

class foxcraftSlashCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.minecraftScript.start()
        self.autoupdate.start()

        self.auction_items = foxDB.show_auctionHouse()
        self.auction_items_DICT = {}
        self.inaccuracy = {}
    
        self.price_mobspawners = {"Allay Spawner": 750000.00,
                "Axolotl Spawner": 1500000.00,
                "Bat Spawner": 0.00,
                "Camel Spawner": 800000.00,
                "Cat Spawner": 200000.00,
                "Chicken Spawner": 150000.00,
                "Cow Spawner": 150000.00,
                "Cod Spawner": 3100000.00,
                "Fox Spawner": 150000.00,
                "Frog Spawner": 1500000.00,
                "Horse Spawner": 100000.00,
                "Mushroom Cow Spawner": 150000.00,
                "Ocelot Spawner": 150000.00,
                "Parrot Spawner": 180000.00,
                "Pig Spawner": 300000.00,
                "Pufferfish Spawner": 1000000.00,
                "Rabbit Spawner": 100000.00,
                "Salmon Spawner": 3100000.00,
                "Sheep Spawner": 450000.00,
                "Sniffer Spawner": 780000.00,
                "Squid Spawner": 1600000.00,
                "Strider Spawner": 160000.00,
                "Tropical Fish Spawner": 0.00,
                "Turtle Spawner": 100000.00,
                "Villager Spawner": 1000000.00,

                "Bee Spawner": 200000.00,
                "Cave Spider Spawner": 35000.00,
                "Spider Spawner": 35000.00,
                "Dolphin Spawner": 1000000.00,
                "Enderman Spawner": 120000.00,
                "Goat Spawner": 100000.00,
                "Iron Golem Spawner": 5000000.00,
                "Piglin Spawner": 420000.00,
                "Wolf Spawner": 0.00,

                "Blaze Spawner": 30000.00,
                "Creeper Spawner": 300000.00,
                "Drowned Spawner": 600000.00,
                "Elder Guardian Spawner": 2000000.00,
                "Endermite Spawner": 100000.00,
                "Evoker Spawner": 1000000.00,
                "Ghast Spawner": 200000.00,
                "Guardian Spawner": 500000.00,
                "Hoglin Spawner": 0.00,
                "Husk Spawner": 50000.00,
                "Magma Cube Spawner": 125000.00,
                "Phantom Spawner": 150000.00,
                "Piglin Brute Spawner": 0.00,
                "Pillager Spawner": 1000000.00,
                "Ravager Spawner": 5000000.00,
                "Shulker Spawner": 2000000.00,
                "Silverfish Spawner": 1000000.00,
                "Skeleton Spawner": 425000.00,
                "Slime Spawner": 130000.00,
                "Stray Spawner": 250000.00,
                "Vindicator Spawner": 2000000.00,
                "Witch Spawner": 1000000.00,
                "Zombie Spawner": 20000.00,
        }
            
        self.price_minions = {
            "Seller Minion": {
                "T1": 5000000.00,
                "T2": 5500000.00,
                "T3": 7000000.00
            },
            "Farmer Minion": {
                "T1": 8000000.00,
                "T2": 8700000.00,
                "T3": 9500000.00
            },
            "Miner Minion": {
                "T1": 4000000.00,
                "T2": 5000000.00,
                "T3": 6000000.00
            },
            "Slayer Minion": {
                "T1": 500000.00,
                "T2": 800000.00,
                "T3": 1200000.00
            },
            "Lumberjack Minion": {
                "T1": 500000.00,
                "T2": 800000.00,
                "T3": 1200000.00
            },
            "Collector Minion": {
                "T1": 1000000.00,
                "T2": 1500000.00,
                "T3": 2200000.00
            },
            "Sorter Minion": {
                "T1": 800000.00,
                "T2": 1200000.00,
                "T3": 2000000.00
            },
            "Fishing Minion": {
                "T1": 300000.00,
                "T2": 500000.00,
                "T3": 900000.00
            }
        }

        self.price_spawneggs = {
            "Axolotl Spawn Egg": 0.00,
            "Bat Spawn Egg": 0.00,
            "Camel Spawn Egg": 0.00,
            "Cat Spawn Egg": 0.00,
            "Chicken Spawn Egg": 0.00,
            "Cow Spawn Egg": 0.00,
            "Fox Spawn Egg": 0.00,
            "Frog Spawn Egg": 0.00,
            "Glow Squid Spawn Egg": 0.00,
            "Goat Spawn Egg": 0.00,
            "Horse Spawn Egg": 0.00,
            "Mushroom Cow Spawn Egg": 0.00,
            "Ocelot Spawn Egg": 0.00,
            "Parrot Spawn Egg": 0.00,
            "Pig Spawn Egg": 0.00,
            "Rabbit Spawn Egg": 0.00,
            "Sheep Spawn Egg": 0.00,
            "Squid Spawn Egg": 0.00,
            "Tropical Fish Spawn Egg": 0.00,
            "Turtle Spawn Egg": 0.00,
            "Villager Spawn Egg": 0.00,
            "Bee Spawn Egg": 0.00,
            "Goat Spawn Egg": 0.00,
            "Llama Spawn Egg": 0.00,
            "Panda Spawn Egg": 0.00,
            "Wolf Spawn Egg": 0.00,
            "Endermite Spawn Egg": 0.00,
            "Silverfish Spawn Egg": 0.00,
            "Slime Spawn Egg": 0.00
        }

        self.price_vouchers = {
            "7 days Rabbit Rank": 0.00,
            "Rabbit Rank Voucher": 0.00,
            "Wolf Rank Voucher": 0.00,
            "Fox Rank Voucher": 0.00,
            "Skyfox Rank Voucher": 0.00,
            "Shadowfox Rank Voucher": 0.00,
            "Mysticfox Rank Voucher": 0.00,
            "FoxQueen Rank Voucher": 0.00,
            "FoxKing Rank Voucher": 0.00
        }

        self.price_normalItems = {}

        self.whitelist_items = ["Classic Crate Key", "Rank Crate Key", "Fortune Crate Key", "January Crate Key", "February Crate Key", "March Crate Key", "April Crate Key",
                                "May Crate Key", "June Crate Key", "July Crate Key", "August Crate Key", "September Crate Key", "October Crate Key", "November Crate Key", "December Crate Key"
                                "Squid Tentacle", "Crab Scale", "Crab Claw", "Dolphin Tail", "Solar Rage",
                                "Small Backpack", "Medium Backpack", "Large Backpack", "End Backpack", "Nether Sack (small)", "Nether Sack (medium)", "Nether Sack (large)",
                                "Garden Bag", "Colorful Bag", "First Aid Kit Bag", "Magic Bag", "Ancient Bag", "Red Striped Bag", "Medieval Cloth bag", "Orange Shopping Bag",
                                "Money Bag", "Cloth Bag", "Grocery bag", "Cloth Seeds Bag",
                                "Bundle", "Totem of Undying", "Portable Trash Bin", "Netherite Ingot", "Reinforced Deepslate", "Torchflower", "Beacon", "Sniffer Egg"]

    @tasks.loop(seconds=180)
    async def autoupdate(self):
        try:
            await self.bot.wait_until_ready()
            self.auction_items = foxDB.show_auctionHouse()
            self.auction_items_DICT = {}
            if self.auction_items:
                for auction_item in self.auction_items:
                    if auction_item[0] in self.auction_items_DICT:
                        self.auction_items_DICT[auction_item[0]].append([auction_item[1], auction_item[2]])
                    else:
                        self.auction_items_DICT[auction_item[0].strip()] = [[auction_item[1], auction_item[2]]]

            def calc_round(integer):
                integer = int(integer)
                lenx = len(str(integer))

                if lenx == 1: integer = round(integer, 0)
                elif lenx == 2: integer = round(integer, -1)
                elif lenx == 3: integer = round(integer, -1)
                elif lenx == 4: integer = round(integer, -2)
                elif lenx == 5: integer = round(integer, -3)
                elif lenx == 6: integer = round(integer, -4)
                elif lenx == 7: integer = round(integer, -4)
                elif lenx == 8: integer = round(integer, -4)

                return integer
            
            for spawner in self.price_mobspawners:
                try:
                    prices = []

                    while len(self.auction_items_DICT[spawner]) > 3:
                        self.auction_items_DICT[spawner].pop(0)

                    for price in self.auction_items_DICT[spawner]:
                        prices.append(price[0])

                    lengthPrices = 1 if len(prices) == 0 else len(prices)
                    summedPrice = calc_round(sum(prices) / lengthPrices)
                    self.price_mobspawners[spawner] = summedPrice

                    if len(self.auction_items_DICT[spawner]) < 3:
                        self.inaccuracy[spawner] = True

                except Exception as e:
                    pass
                    # print(traceback.format_exc())

            for minion in self.price_minions:
                minion_for_dict = minion.replace(" Minion", "")
                self.inaccuracy[minion] = {}
                for tier in self.price_minions[minion]:
                    prices = []

                    try:
                        while len(self.auction_items_DICT[str(minion_for_dict + tier)]) > 3:
                            self.auction_items_DICT[str(minion_for_dict + tier)].pop(0)

                        for price in self.auction_items_DICT[str(minion_for_dict + tier)]:
                            prices.append(price[0])
                        
                        lengthPrices = 1 if len(prices) == 0 else len(prices)
                        summedPrice = calc_round(sum(prices) / lengthPrices)
                        self.price_minions[minion][tier] = summedPrice


                        if len(self.auction_items_DICT[str(minion_for_dict + tier)]) < 3:
                            self.inaccuracy[minion][tier] = True


                    except Exception as e:
                        self.inaccuracy[minion][tier] = True


                        # print(traceback.format_exc())

            for spawnegg in self.price_spawneggs:
                try:
                    prices = []

                    while len(self.auction_items_DICT[spawnegg]) > 3:
                        self.auction_items_DICT[spawnegg].pop(0)

                    for price in self.auction_items_DICT[spawnegg]:
                        prices.append(price[0])

                    lengthPrices = 1 if len(prices) == 0 else len(prices)
                    summedPrice = calc_round(sum(prices) / lengthPrices)
                    self.price_spawneggs[spawnegg] = summedPrice

                    if len(self.auction_items_DICT[spawnegg]) < 3:
                        self.inaccuracy[spawnegg] = True

                except Exception as e:
                    pass
                    # print(traceback.format_exc())

            for voucher in self.price_vouchers:
                try:
                    prices = []
                    
                    while len(self.auction_items_DICT[voucher]) > 3:
                        self.auction_items_DICT[voucher].pop(0)

                    for price in self.auction_items_DICT[voucher]:
                        prices.append(price[0])

                    lengthPrices = 1 if len(prices) == 0 else len(prices)
                    summedPrice = calc_round(sum(prices) / lengthPrices)
                    self.price_vouchers[voucher] = summedPrice

                    if len(self.auction_items_DICT[voucher]) < 3:
                        self.inaccuracy[voucher] = True
                
                except Exception as e:
                    pass
                    # print(traceback.format_exc())

            for key in self.auction_items_DICT:
                try:
                    prices = []

                    if key in self.whitelist_items:
                        while len(self.auction_items_DICT[key]) > 3:
                            self.auction_items_DICT[key].pop(0)

                        for price in self.auction_items_DICT[key]:
                            prices.append(price[0])

                        lengthPrices = 1 if len(prices) == 0 else len(prices)
                        summedPrice = calc_round(sum(prices) / lengthPrices)
                        self.price_normalItems[key] = summedPrice

                        if len(self.auction_items_DICT[key]) < 3:
                            self.inaccuracy[key]

                except Exception as e:
                    pass
                    # print(traceback.format_exc())

                
        except Exception as e:
            pass 
            # print(traceback.format_exc())

        channel = self.bot.get_channel(1137094380906348646)
        current_time = time.time()
        async for last_message in channel.history(limit=300):
            created_at = last_message.created_at
            time_difference = current_time - created_at.timestamp()

            if time_difference > 86400:
                await last_message.delete()

        print("Updated")
                
            

    @tasks.loop(seconds=15.0)
    async def minecraftScript(self):
        await self.bot.wait_until_ready()

        def calc_round(integer):
            integer = int(integer)
            lenx = len(str(integer))

            if lenx == 1: integer = round(integer, 0)
            elif lenx == 2: integer = round(integer, -1)
            elif lenx == 3: integer = round(integer, -1)
            elif lenx == 4: integer = round(integer, -2)
            elif lenx == 5: integer = round(integer, -3)
            elif lenx == 6: integer = round(integer, -4)
            elif lenx == 7: integer = round(integer, -4)
            elif lenx == 8: integer = round(integer, -4)

            return integer
        
        try:
            channel = self.bot.get_channel(1137094380906348646)

            conn = sqlite3.connect("C:/Users/Cosmin/Documents/Code/minecraft/data.db")
            c = conn.cursor()

            c.execute("""SELECT * FROM update_table""")
            rows = c.fetchall()
            if len(rows) != 0:
                for listing in rows:

                    listing_item, listing_items, listing_price, listing_id = listing[0], listing[1], listing[2], listing[3]

                    embed = Embed(color = Color.from_rgb(243, 205, 140))
                    embed.set_author(name = "New Listing")
                    embed.add_field(name="Item", value = f"x{listing_items} {listing_item}")
                    embed.add_field(name="Price", value = f"${listing_price:,.2f}")
                    embed.add_field(name="Price per item", value = f"${calc_round(float(listing_price) / int(listing_items)):,.2f}", inline = False)

                    embed.set_footer(text="Visible for 24 hours or until purchased.")

                    if "T1" in listing_item or "T2" in listing_item or "T3" in listing_item:
                        embed.set_thumbnail(url=("https://static.wikia.nocookie.net/minecraft_gamepedia/images/4/44/Dragon_Egg_BE1.png/revision/latest/scale-to-width/360?cb=20211218053444"))
                    
                    elif "Spawner" in listing_item:
                        embed.set_thumbnail(url=("https://static.wikia.nocookie.net/minecraft/images/f/f8/MobSpawnerNew.png/revision/latest?cb=201909102330231" if "Spawner" in listing_item else None))

                    elif "Spawn Egg" in listing_item:
                        embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b1/Axolotl_Spawn_Egg_JE1_BE1.png/revision/latest?cb=20201216173708")
                    
                    else:
                        continue

                    foxDB.c.execute("""DELETE FROM update_table WHERE id=?""", (listing_id,))
                    foxDB.commitChanges()
                    
                    await channel.send(embed=embed)

        except Exception as e:
            newchannel = self.bot.get_channel(1131297521935859813)
            await newchannel.send("Caught an error: \n- " + str(traceback.format_exc()))


        # if not channel:
        # await self.bot.fetch_channel(1131290602902913096).send("hello")



    @app_commands.command(name="startup")
    async def startup(self, interaction: discord.Interaction):
        pass





    @app_commands.command(name="poll", description="Prepare a build poll!")
    @app_commands.describe(question= "Question to enter", option1 = "Option 1", option2 = "Option 2", option3 = "Option 3", option4 = "Option 4", option5 = "Option 5")
    async def poll(self, interaction: discord.Interaction, question: str, option1: Optional[str] = None, option2: Optional[str] = None, option3: Optional[str] = None, option4: Optional[str] = None, option5: Optional[str] = None):
        # await interaction.response.send_message(f"You have chosen {builds.name}\nSlash command invokez    d by: {interaction.user.mention} & {interaction.user.display_name}")
        channel_id = interaction.channel.id
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
        options = [option1, option2, option3, option4, option5]
        result_options = []
        for i in options:
            if i != None:
                result_options.append(i)

        if len(result_options) != 0:
            embed = Embed(
                title="Question:",
                description=f"{question}\n",
                color=Color.from_rgb(243, 205, 140)
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)
            
            for index, i in enumerate(result_options):
                embed.add_field(name = f"Option {index+1}", value=i, inline=False)

            # await interaction.response.send_message(f"Question: {question}, builds: {result_options}")
            await interaction.response.send_message(embed=embed)
            
            channel = self.bot.get_channel(channel_id)
            async for last_message in channel.history(limit=1):
                for i in range(len(result_options)):
                    await last_message.add_reaction(emojis[i])

            return False
                
        await interaction.response.send_message(f"Question: {question}, no builds.")





    @app_commands.command(name="price", description="Return average transaction for an item.")
    @app_commands.describe(item = "Search item i.e: 'Rabbit Spawner'")
    async def getPrice(self, interaction: discord.Interaction, item: str):
        channel_id = interaction.channel.id

        searchitem = item
        print(f"GetPrice was called with item: {item}")

        # Spawners section.
        if "spawner" in searchitem.lower():
            for _item in self.price_mobspawners:
                if  _item.lower() == searchitem.lower():

                    price = self.price_mobspawners[_item]
                    

                    embed = Embed(color = Color.from_rgb(243, 205, 140))
                    embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/f8/MobSpawnerNew.png/revision/latest?cb=201909102330231")
                    embed.set_author(name = _item)
                    embed.set_footer(text = "Up to date average transaction price")

                    if _item in self.inaccuracy:
                        embed.add_field(name="Price:", value=f"${(price):,.2f} (**Inaccurate**)")
                    else:
                        embed.add_field(name="Price:", value=f"${(price):,.2f}")

                    await interaction.response.send_message(embed=embed)
                    return False
            
        # Minions section
        if "minion" in searchitem.lower():
            for _item in self.price_minions:
                if _item.lower() == searchitem.lower():
                    price1 = self.price_minions[_item]["T1"]
                    price2 = self.price_minions[_item]["T2"]
                    price3 = self.price_minions[_item]["T3"]
                    
                    embed = Embed(color = Color.from_rgb(243, 205, 140))

                    embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/4/44/Dragon_Egg_BE1.png/revision/latest/scale-to-width/360?cb=20211218053444")
                    embed.set_author(name = _item)
                    embed.set_footer( text = "Up to date average transaction price")



                    if _item in self.inaccuracy:
                        embed.add_field(name="T1 Price:", value=f"${(price1):,.2f}")
                        embed.add_field(name="T2 Price:", value=f"${(price2):,.2f}")
                        embed.add_field(name="T3 Price:", value=f"${(price3):,.2f}")

                        for tier in self.inaccuracy[_item]:
                            if "T1" in tier:
                                embed.set_field_at(0, name = "T1 Price:", value = f"${(price1):,.2f} (**Inaccurate**)")
                            elif "T2" in tier:
                                embed.set_field_at(1, name = "T2 Price:", value = f"${(price2):,.2f} (**Inaccurate**)")
                            elif "T3" in tier:
                                embed.set_field_at(2, name = "T3 Price:", value = f"${(price3):,.2f} (**Inaccurate**)")

                    await interaction.response.send_message(embed=embed)
                    return False
        
        # Spawn Egg section
        if "egg" in searchitem.lower():
            for _item in self.price_spawneggs:
                if _item.lower() == searchitem.lower():
                    price = self.price_spawneggs[_item]

                    embed = Embed(color = Color.from_rgb(243, 205, 140))

                    embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b1/Axolotl_Spawn_Egg_JE1_BE1.png/revision/latest?cb=20201216173708")
                    embed.set_author(name = _item)
                    embed.set_footer(text = "Up to date average transaction price")

                    if _item in self.inaccuracy:
                        embed.add_field(name="Price:", value=f"${(price):,.2f} (**Inaccurate**)")
                    else:
                        embed.add_field(name="Price:", value=f"${(price):,.2f}")

                    await interaction.response.send_message(embed=embed)
                    return False
                
        if "rank" in searchitem.lower() or "voucher" in searchitem.lower():
            if "7 days rabbit rank" in searchitem.lower():
                searchitem = "7 days rabbit rank"
            elif "voucher" in searchitem.lower() and "rank" not in searchitem.lower():
                searchitem = searchitem.split()
                if len(searchitem) == 2:
                    searchitem = f"{searchitem[0]} Rank {searchitem[1]}"
                else:
                    await interaction.response.send_message("Item not found!")
                    return False
                               
            elif "voucher" not in searchitem.lower() and "rank" in searchitem.lower():
                print("found rank")
                searchitem = searchitem.split()

                if len(searchitem) == 2:
                    searchitem = f"{searchitem[0]} {searchitem[1]} Voucher"
                else:
                    await interaction.response.send_message("Item not found!")
                    return False
            else:
                await interaction.response.send_message("Item not found!")
                return False
                
            
            for _item in self.price_vouchers:
                if _item.lower() == searchitem.lower():
                    price = self.price_vouchers[_item]

                    embed = Embed(color = Color.from_rgb(243, 205, 140))

                    embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f2/Paper_JE2_BE2.png/revision/latest?cb=20230611043112")
                    embed.set_author(name = _item)
                    embed.set_footer(text = "Up to date average transaction price")

                    if _item in self.inaccuracy:
                        embed.add_field(name="Price:", value=f"${(price):,.2f} (**Inaccurate**)")
                    else:
                        embed.add_field(name="Price:", value=f"${(price):,.2f}")
                    
                    await interaction.response.send_message(embed=embed)
                    return False
                
        #if searchitem in self.whitelist_items:
        #    price = self.price_normalItems[searchitem]
#
        #    embed = Embed(color = Color.from_rgb(243, 205, 140))
#
        #    embed.set_author(name = searchitem)
        #    embed.set_footer(text = "Up to date average transaction price")
#
        #    if searchitem in self.inaccuracy:
        #        embed.add_field(name="Price:", value=f"${(price):,.2f} (***Inaccurate*)")
        #    else:
        #        embed.add_field(name="Price:", value=f"${(price):,.2f}")
#
        #    await interaction.response.send_message(embed=embed)
        #    return False
          
        await interaction.response.send_message("Item not found!")




    @app_commands.command(name="listprices", description="Return prices for each item of the type given.")
    @app_commands.describe(itemtypes = "Type of item, i.e. 'Minion' or 'Mob Spawner'")
    @app_commands.choices(itemtypes = [
        Choice(name="Minion", value=1),
        Choice(name="Neutral Mob Spawner", value=2),
        Choice(name="Passive Mob Spawner", value=3),
        Choice(name="Hostile Mob Spawner", value=4)
    ])
    async def priceType(self, interaction: discord.Interaction, itemtypes: Choice[int]):
        channel = self.bot.get_channel(interaction.channel.id)
        
        embed = Embed(
                    color = Color.from_rgb(243, 205, 140)
                    )
        embed.set_footer(text = "Up to date average transaction prices")

        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
        minion_emojis = ["1️⃣", "2️⃣", "3️⃣"]

        page1 = Embed(
                    color = Color.from_rgb(243, 205, 140)
                    )
        page1.set_footer(text = "Up to date average transaction prices") # Passive

        page2 = Embed(
                    color = Color.from_rgb(243, 205, 140)
                    )
        page2.set_footer(text = "Up to date average transaction prices") # Neutral

        page3 = Embed(
                    color = Color.from_rgb(243, 205, 140)
                    )
        page3.set_footer(text = "Up to date average transaction prices") # Hostile

        if "Mob Spawner" in itemtypes.name:
            if itemtypes.name == "Passive Mob Spawner":
                limit = 24
            elif itemtypes.name == "Neutral Mob Spawner":
                lower_limit = 25
                limit = 33
            elif itemtypes.name == "Hostile Mob Spawner":
                lower_limit = 34

            for index, mobspawner in enumerate(self.price_mobspawners):
                print(mobspawner + str(index))

                if itemtypes.name == "Passive Mob Spawner":
                    if index <= limit: # index 24 is villager (last passive mob)
                        if mobspawner in self.inaccuracy:
                            page1.add_field(name=mobspawner, value= f"${self.price_mobspawners[mobspawner]:,.2f} (**Inaccurate**)", inline=True)
                        else:
                            page1.add_field(name=mobspawner, value= f"${self.price_mobspawners[mobspawner]:,.2f}", inline=True)

                        page1.set_author(name = "Passive Spawners")
                        page1.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/f8/MobSpawnerNew.png/revision/latest?cb=201909102330231")

                if itemtypes.name == "Neutral Mob Spawner":
                    if index >= lower_limit and index <= limit: # index 33 is Wolf (last neutral mob)
                        if mobspawner in self.inaccuracy:
                            page2.add_field(name=mobspawner, value= f"${self.price_mobspawners[mobspawner]:,.2f} (**Inaccurate**)", inline=True)
                        else:
                            page2.add_field(name=mobspawner, value= f"${self.price_mobspawners[mobspawner]:,.2f}", inline=True)

                        page2.set_author(name = "Neutral Spawners")
                        page2.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/f8/MobSpawnerNew.png/revision/latest?cb=201909102330231")

                if itemtypes.name == "Hostile Mob Spawner":
                    if index >= lower_limit:
                        if mobspawner in self.inaccuracy:
                            page3.add_field(name=mobspawner, value= f"${self.price_mobspawners[mobspawner]:,.2f} (**Inaccurate**)", inline=True)
                        else:
                            page3.add_field(name=mobspawner, value= f"${self.price_mobspawners[mobspawner]:,.2f}", inline=True)

                        page3.set_author(name = "Hostile Spawners")
                        page3.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/f8/MobSpawnerNew.png/revision/latest?cb=201909102330231")
                
            if itemtypes.name == "Passive Mob Spawner":
                message = await interaction.response.send_message(embed=page1)
            if itemtypes.name == "Neutral Mob Spawner":
                message2 = await interaction.response.send_message(embed=page2)
            if itemtypes.name == "Hostile Mob Spawner":
                message3 = await interaction.response.send_message(embed=page3)
                
        elif itemtypes.name == "Minion":
            for minion in self.price_minions:
                embed.add_field(name=minion, value = f"- T1: ${self.price_minions[minion]['T1']:,.2f}\n- T2: ${self.price_minions[minion]['T2']:,.2f}\n- T3: ${self.price_minions[minion]['T3']:,.2f}\n", inline=False)


            embed.set_author(name = "Minions sell for")
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/4/44/Dragon_Egg_BE1.png/revision/latest/scale-to-width/360?cb=20211218053444")
        
            #await interaction.response.send_message(embed=embed)
            #async for last_message in channel.history(limit=4):
            #    if last_message.author.id == 861370829253509133:
            #        for emoji in minion_emojis:
            #            await last_message.add_reaction(emoji)
#
            #    message = await interaction.original_response()
            #    
            #while True:
            #    newMessage = await channel.fetch_message(message.id)
            #    time.sleep(0.5)
#
            #    chosen = False
            #    print(newMessage.reactions)
            #
            #    if len(newMessage.reactions) != 0:
            #        counts = [newMessage.reactions[0], newMessage.reactions[1], newMessage.reactions[2]]
#
            #        for index, reaction in enumerate(counts):
            #            if reaction.count != 1:
            #                if index == 0:
            #                    await interaction.edit_original_response(content=f"You reacted with: {reaction.emoji}\nI should display first 1-3 Minions")
            #                    chosen = True
            #                    break
            #                elif index == 1:
            #                    await interaction.edit_original_response(content=f"You reacted with: {reaction.emoji}\nI should display 4-6th Minions")
            #                    chosen = True
            #                    break
            #                elif index == 2:
            #                    await interaction.edit_original_response(content=f"You reacted with: {reaction.emoji}\nI should display 7-9th Minions")
            #                    chosen = True
            #                    break
#
            #    if chosen == True: 
            #        break
        

            


class foxcraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
    @commands.command(name="info")
    async def showStatus(self, ctx):
        embed = Embed(
            title="This server is the basis of communication for the smurfs.",
            description="Here you can chat, ask questions and help the team in various ways.\n",
            color=Color.from_rgb(243, 205, 140)
        )

        embed.add_field(name="I like feedback", value = "Please give feedback to build on what we have.")
        embed.set_author(name = "Information", icon_url = "https://static.wikia.nocookie.net/smurfs/images/0/03/Papa_Smurf_2021_TV_Series_%282%29.png/revision/latest?cb=20210531184911")

        # embed.set_thumbnail(url = "https://media.discordapp.net/attachments/1131290602902913096/1131306134502899742/IMG_8761.PNG?width=910&height=910")
        embed.set_footer(text = "Provided by Quorizza.")
        
        await ctx.send(embed=embed)

    @commands.command(name="poll")
    async def createPoll(self, ctx):
        Target_Channel_ID = ctx.channel.id
        command_substring = "q.poll"
        content = ctx.message.content.strip()
        content = content.replace(command_substring, "")

        args = content.split()
        question = args[0] + args[1]
        options = [args[2], args[3], args[4]]

        
        await self.bot.get_channel(Target_Channel_ID).send(f"Question: {question}\nOptions:\n1. {options[0]}\n2. {options[1]}\n3. {options[2]}")
