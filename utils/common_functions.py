import datetime
import urllib.parse
import random
import requests
import binascii
import json
import calendar
import re
from django.contrib.auth.models import User, Group
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags, format_html
from django.db.models.functions import Lower
from django.db.models import Q
from django.shortcuts import render




"""
While Creating a user username is spliting form email and
if username is already exist a random number is appending to username
due to username is unique so we are making making the username is unique"""
def make_unique_username(email):
    user_name = email.split('@', 1)[0]
    if User.objects.filter(username=user_name).exists():
        postfix = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3))
        return str(user_name+postfix)
    else:
        return user_name


