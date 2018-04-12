__author__ = 'cmgiler'

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import datetime as dt

def GetMongoCollection(db_name, collection_name):
    from pymongo import MongoClient
    client = MongoClient()
    db = client[db_name]
    return db[collection_name]

def GetCollectionNames(db_name):
    from pymongo import MongoClient
    client = MongoClient()
    db = client[db_name]
    return db.collection_names()

def GetFields(collection):
    field_names = set()
    for item in collection.find():
        [field_names.add(x) for x in item.keys()]
    return field_names