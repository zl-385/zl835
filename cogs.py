from replit import db
from datetime import datetime
from math import floor
import os
import discord
import logging
from discord.ext import commands,tasks
from random import randint
from googletrans import Translator


def update(author_id, attr, val):
	context = db[author_id]
	context[attr] = val
	db[author_id] = context
