# -*- coding: utf8 -*-
from __future__ import print_function

import sqlite3

def connect_database(db_name = 'tw-stock.db'):
  return sqlite3.connect(db_name)
