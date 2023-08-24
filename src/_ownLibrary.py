import discord                               # Import the discord module for the bot
from discord.ext import commands             # Import the commands extension from the discord module
from discord.utils import get                # Import the get function from the discord.utils module
from discord import Embed, Color

import asyncio 
from PIL import Image, ImageDraw             # Import the Image and ImageDraw classes from the PIL module
import sqlite3

import time                                  # Import the time module
import random                                # Import the random module

# Import bot token and quotes
from apikeys import *                         # Import the bot token from the apikeys.py file
from quotes import *                          # Import quotes from the quotes.py file

from osu import *
# from database._database import *