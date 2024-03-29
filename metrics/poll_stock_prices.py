#!/usr/bin/env python

import simplejson as json
import datetime
import urllib
import os
import os.path
import csv

#   Removed because these fields contain commas (doh!)
#   ('a5', 'Ask Size'), #WARNING THIS CONTAINS COMMAS FOR 1,000,000 markers
#   ('b6', 'Bid Size'),
#   ('k3', 'Last Trade Size'),
#   ('f6', 'Float Shares'),

#   Removed because this wastes too much space
#   ('t6', 'Trade Links'),

fields = [
   ('a', 'Ask'),
   ('a2', 'Average Daily Volume'),
   ('b', 'Bid'),
   ('b2', 'Ask (Real-time)'),
   ('b3', 'Bid (Real-time)'),
   ('b4', 'Book Value'),
   ('c', 'Change & Percent Change'),
   ('c1', 'Change'),
   ('c3', 'Commission'),
   ('c6', 'Change (Real-time)'),
   ('c8', 'After Hours Change (Real-time)'),
   ('d', 'Dividend/Share'),
   ('d1', 'Last Trade Date'),
   ('d2', 'Trade Date'),
   ('e', 'Earnings/Share'),
   ('e1', 'Error Indication (returned for symbol changed / invalid)'),
   ('e7', 'EPS Estimate Current Year'),
   ('e8', 'EPS Estimate Next Year'),
   ('e9', 'EPS Estimate Next Quarter'),
   ('g', "Day's Low"),
   ('h', "Day's High"),
   ('j', '52-week Low'),
   ('k', '52-week High'),
   ('g1', 'Holdings Gain Percent'),
   ('g3', 'Annualized Gain'),
   ('g4', 'Holdings Gain'),
   ('g5', 'Holdings Gain Percent (Real-time)'),
   ('g6', 'Holdings Gain (Real-time)'),
   ('i', 'More Info'),
   ('i5', 'Order Book (Real-time)'),
   ('j1', 'Market Capitalization'),
   ('j3', 'Market Cap (Real-time)'),
   ('j4', 'EBITDA'),
   ('j5', 'Change From 52-week Low'),
   ('j6', 'Percent Change From 52-week Low'),
   ('k1', 'Last Trade (Real-time) With Time'),
   ('k2', 'Change Percent (Real-time)'),
   ('k4', 'Change From 52-week High'),
   ('k5', 'Percent Change From 52-week High'),
   ('l', 'Last Trade (With Time)'),
   ('l1', 'Last Trade (Price Only)'),
   ('l2', 'High Limit'),
   ('l3', 'Low Limit'),
   ('m', "Day's Range"),
   ('m2', "Day's Range (Real-time)"),
   ('m3', '50-day Moving Average'),
   ('m4', '200-day Moving Average'),
   ('m5', 'Change From 200-day Moving Average'),
   ('m6', 'Percent Change From 200-day Moving Average'),
   ('m7', 'Change From 50-day Moving Average'),
   ('m8', 'Percent Change From 50-day Moving Average'),
   ('n', 'Name'),
   ('n4', 'Notes'),
   ('o', 'Open'),
   ('p', 'Previous Close'),
   ('p1', 'Price Paid'),
   ('p2', 'Change in Percent'),
   ('p5', 'Price/Sales'),
   ('p6', 'Price/Book'),
   ('q', 'Ex-Dividend Date'),
   ('r', 'P/E Ratio'),
   ('r1', 'Dividend Pay Date'),
   ('r2', 'P/E Ratio (Real-time)'),
   ('r5', 'PEG Ratio'),
   ('r6', 'Price/EPS Estimate Current Year'),
   ('r7', 'Price/EPS Estimate Next Year'),
   ('s', 'Symbol'),
   ('s1', 'Shares Owned'),
   ('s7', 'Short Ratio'),
   ('t1', 'Last Trade Time'),
   ('t7', 'Ticker Trend'),
   ('t8', '1 yr Target Price'),
   ('v', 'Volume'),
   ('v1', 'Holdings Value'),
   ('v7', 'Holdings Value (Real-time)'),
   ('w', '52-week Range'),
   ('w1', "Day's Value Change"),
   ('w4', "Day's Value Change (Real-time)"),
   ('x', 'Stock Exchange'),
   ('y', 'Dividend Yield'),
]
basedir = os.path.abspath(os.path.dirname(__file__))
all_securities = list(set([ urllib.quote(s) for s in open(basedir+"/securities.csv").read().split() if s.strip()!="" ]))
i = 0

now = datetime.datetime.now()

while len(all_securities)>0:
    i += 1
    securities,all_securities = all_securities[:200],all_securities[200:]

    url = "http://finance.yahoo.com/d/quotes.csv?f="\
      + "".join(k for (k,v) in fields)\
      + "&s=" + "+".join(securities)
    outdir = now.strftime(basedir+'/securities_db/%Y/%m/%d/%H/%M')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    file(basedir+"/securities_db/polling.log","w").write("%s Polled yahoo for stock prices.\n" % now)

    response = urllib.urlopen(url)
    if response.getcode()!=200:
        print "Error response: "+response.getcode()
        print response.read()
        print
        break
    outfile = open(now.strftime(basedir+'/securities_db/%Y/%m/%d/%H/%M/securities_%Y%m%d_%H%M%S.part'+str(i)+'.csv'),'w')
    for line in urllib.urlopen(url).readlines():
        if line.strip()=="": continue
        quote = dict(zip([k for (k,v) in fields], line.split(',')))
        if len(quote)!=len(fields):
            print "|values|=%d != |keys|=%d !!!\n%s" % (len(quote),len(fields),line)
            continue
        if quote['e1'] != '"N/A"':
            print "No such ticker symbol: %s" % [quote['s']]
        outfile.write( json.dumps(quote)+"\n" )
    outfile.close()

