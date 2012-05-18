#!/usr/bin/env python

import boto
import glob
import os
import os.path

c = boto.connect_s3("AKIAIJKXBJLHXT7HIPTQ","Kp86pC6CB2f0syp+Uyix7T5jjqjb4oMmMSefpT13")
b = c.get_bucket('karmafeeder',validate=False)

for key in b.list(prefix="securities_db"):
    filename = key.key
    if filename.count('/')!=6 or os.path.exists(filename):
        continue
    try:
        os.makedirs('/'.join(filename.split('/')[:-1]))
    except OSError:
        pass
    key.get_contents_to_filename(filename)
