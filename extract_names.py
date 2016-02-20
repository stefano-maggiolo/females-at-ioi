#!/usr/bin/env python

import io
from glob import glob
from bs4 import BeautifulSoup

delegations = [x.strip().split(',') for x in open("data/delegations")]
names = []
for d in delegations:
    print d
    page = BeautifulSoup(open("data/%s.%s" % (d[0], d[1])).read())
    sections = page.find_all(class_='basicname')
    for s in sections:
        s_name = s.string
        for name in s.next_sibling.find_all(class_="name"):
            img = name.previous_sibling
            img_src = ''
            if img is not None and img.name == 'img':
                img_src = img.attrs['src']
            id_ = name.parent.attrs['href'].replace('people/', '')
            names.append((d[0], d[1], s_name, name.string, img_src, id_))

with io.open("data/names", "w", encoding="utf-8") as f:
    for n in names:
        f.write("%s,%s,%s,%s,%s,%s\n" % n)

