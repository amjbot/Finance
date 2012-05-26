#!/usr/bin/env python

import os.path
import glob
import simplejson as json
import subprocess

blacklist = set()
for line in open(os.path.join(os.path.dirname(__file__),"blacklist.txt")):
    if line.strip()=="":
        continue
    blacklist.add(line.strip())

daily_observations = {}
for file in glob.glob(os.path.join(os.path.dirname(__file__),"securities_db/*/*/*/*/*/*.csv")):
    date = '/'.join(file.split('/')[-6:-3])
    for line in open(file):
        try:
            record = json.loads(line)
            if not (isinstance(record['s'],unicode) or isinstance(record['s'],str)) or\
               not record['s'].startswith('"') or record['s'][1:-1] in blacklist: 
                continue
            j1 = record['j1']
            if j1.endswith('K'):
                j1 = j1.split('.')[0] + '000'
            elif j1.endswith('M'):
                j1 = j1.split('.')[0] + '000000'
            elif j1.endswith('B'):
                j1 = j1.split('.')[0] + '000000000'
            daily_observations[record['s']] = daily_observations.get(record['s'],{})
            daily_observations[record['s']][date] = { 'e':record['e'], 'r':record['r'], 'j1':j1, 'y':record['y'] }
        except json.decoder.JSONDecodeError:
            pass

def average_stats( symbol, dates ):
    d_sigma = { 'e':0, 'r':0, 'j1':0, 'y':0 }
    d_count = 0
    for day in dates:
        d = daily_observations[symbol][day]
        dd_sigma = {}
        for key in d:
            try:
                dd_sigma[key] = float(d[key])
            except ValueError:
                dd_sigma[key] = 0.0
        if 'error' not in dd_sigma:
            for key in dd_sigma:
                d_sigma[key] += dd_sigma[key]
            d_count += 1
    if d_count == 0 or d_sigma['e']==0 or d_sigma['r']==0:
        return { 'e':-1, 'r':-1, 'j1':0, 'y':0 }
    for key in d_sigma:
        d_sigma[key] = d_sigma[key] / d_count
    return d_sigma

daily_report = open(os.path.join(os.path.dirname(__file__),"daily_report.txt"),"w")
for symbol in daily_observations:
    timeline = sorted(daily_observations[symbol].keys())
    current = average_stats(symbol,timeline[-1:])
    trailing_4 = average_stats(symbol,timeline[-(4*7+1):])
    trailing_52 = average_stats(symbol,timeline[-(52*7+1):])
    trailing_260 = average_stats(symbol,timeline[-(260*7+1):])
    if any(d['r']<0 for d in [current,trailing_4,trailing_52,trailing_260]) or\
       any(d['e']<0 for d in [current,trailing_4,trailing_52,trailing_260]):
        continue   
    deviance = (current['r']/trailing_4['r']) *\
               (current['r']/trailing_52['r']) *\
               (current['r']/trailing_260['r'])
    performance = (current['e']/trailing_4['e']) *\
               (current['e']/trailing_52['e']) *\
               (current['e']/trailing_260['e'])
    cap = current.get('j1',0)
    bubble = current.get('r',0)
    dividend = current.get('y',0)
    daily_report.write(
        "%.2f %s %.2f %s %.2f %s %.2f %s $%d %s %s\n" %
        (deviance, "undervalued" if deviance<1.0 else "overvalued",\
        dividend, "profitable" if dividend>0 else "speculative",\
        performance, "shrinking" if performance<1.0 else "growing",\
        bubble, "BUBBLICIOUS" if bubble>100 else "HYPED" if bubble>30 else "RATIONAL" if bubble>10 else "NEGLECTED",\
        cap, "LARGE" if cap>1000**3 else "MEDIUM" if cap>1000**2 else "SMALL",\
        symbol[1:-1]))

subprocess.Popen("sort -n daily_report.txt > .daily_report.txt",shell=True).wait()
subprocess.Popen("mv .daily_report.txt daily_report.txt",shell=True).wait()
