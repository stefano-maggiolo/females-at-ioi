#!/usr/bin/env python

import os

from bs4 import BeautifulSoup

delegations = [x.strip().split(',') for x in open("delegations")]
for d in delegations:
    os.system("wget http://stats.ioinformatics.org/delegations/%s/%s -O %s.%s" %
              (d[0], d[1], d[0], d[1]))
