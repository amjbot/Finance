#!/usr/bin/env python

import boto
import glob

c = boto.connect_s3("AKIAIJKXBJLHXT7HIPTQ","Kp86pC6CB2f0syp+Uyix7T5jjqjb4oMmMSefpT13")
b = c.create_bucket('karmafeeder')
from boto.s3.key import Key
k = Key(b)

for s in glob.glob("securities_db/*/*/*/*/*/*"):
    k.key = s
    k.set_contents_from_filename(s)
    os.remove(s)
