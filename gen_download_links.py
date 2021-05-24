# -*- coding: utf8 -*-
from __future__ import print_function

from datetime import datetime

import argparse, os, io
import pandas
import urllib.request
import database

def generate_links(stock_number, since_years=5):
  links = []
  csv_link = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={}&stockNo={}'
  today = datetime.today()
  current_year = int(today.year)
  start_year = current_year - since_years
  for year in range(start_year, current_year):
    for month in range(1, 13):
      date_str = '{}{:02}01'.format(year, month)
      links.append(csv_link.format(date_str, stock_number))
  for month in range(1, int(today.month) + 1):
    date_str = '{}{:02}01'.format(current_year, month)
    links.append(csv_link.format(date_str, stock_number))
  return links

def run(dir_path, years):
  cnt = 0
  csv_link = 'https://quality.data.gov.tw/dq_download_csv.php?nid=18419&md5_url=9791ec942cbcb925635aa5612ae95588'
  # Download the last updated CSV.
  response = urllib.request.urlopen(csv_link)
  csv = pandas.read_csv(io.StringIO(response.read().decode('utf-8')))
  company_list = csv.loc[:, ['公司名稱', '公司簡稱', '公司代號', '產業別']]
  # Write all of links to a file.
  with open(os.path.join(dir_path, 'links.txt'), 'w') as txt:
    for _, info in company_list.iterrows():
      stock_name = info['公司簡稱']
      stock_number = info['公司代號']
      links = generate_links(stock_number, years)
      txt.write('\n'.join(links))
      cnt += len(links)
      print('{:5}: {}.'.format(stock_number, stock_name))
  print('Total {} links.'.format(cnt))
  company_list.to_csv(os.path.join(dir_path, 'company_list.csv'), index=False)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--directory',
    type=str,
    default='.',
    help='Directory to store the downloaded CSV files.')
  parser.add_argument('-y', '--years',
    type=int,
    default=1,
    help='How many years of historical data to download.')
  args = parser.parse_args()
  run(args.directory, args.years)
