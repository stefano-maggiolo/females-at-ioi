#!/usr/bin/env python


from bs4 import BeautifulSoup

delegations = []
for y in range(1989, 2015):
    page = BeautifulSoup(open('data/%s' % y).read())
    rows = page.table.find_all('tr')
    for row in rows:
        if row.td is not None:
            parts = row.td.a.get('href').split('/')
            delegations.append((parts[1], parts[2]))

with open("data/delegations", "w") as f:
    for d in delegations:
        f.write("%s,%s\n" % d)
