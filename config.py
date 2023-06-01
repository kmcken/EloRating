import datetime
import json
import numpy as np
import scipy as sp
import os
import pandas as pd
import requests
import sqlite3
import time
import uuid


version = 'v0.1'
root = os.path.dirname(os.path.abspath(__file__))

ratings_db = root + r'\Data\eloratings.db'
classifiers_db = root + r'\Data\classifiers.db'

noob_skill = 1000
noob_uncertainty = 350
noob_weight = 0.1
noob_placement = 5
rating_min = 100
rating_max = 3000
percent_factor = 0.05
stage_count_factor = 0.15
competitor_count_factor = 0.01
mmr_method = 'normal'
ignore_classifier = True
