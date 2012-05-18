#!/usr/bin/env python

import boto
import glob
import os
import os.path

c = boto.connect_s3("AKIAIJKXBJLHXT7HIPTQ","Kp86pC6CB2f0syp+Uyix7T5jjqjb4oMmMSefpT13")
b = c.get_bucket('karmafeeder',validate=False)
from boto.s3.key import Key
k = Key(b)

for s in glob.glob(os.path.join(os.path.dirname(__file__),"securities_db/*/*/*/*/*/*")):
    k.key = '/'.join(s.split('/')[-7:])
    k.set_contents_from_filename(s)
    os.remove(s)
