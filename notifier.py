#!/usr/bin/env python
import os
import sys
import datetime
import time
import urllib
from BeautifulSoup import BeautifulSoup
from gsendmail import GSendMail


class AbsolutePunkFeed(object):
    url = "http://www.absolutepunk.net/releasedates.php"
    def __init__(self):
        pass

    def _parse_date(self, date_str):
        #Release Date: Mon, 06 Apr 2009
        #10-01-12&c=3
        ds = date_str.split("&")[0].strip()
        d = time.strptime(ds, "%y-%m-%d")
        return datetime.date(d.tm_year, d.tm_mon, d.tm_mday)

    def get_events(self):
        entries = []
        html = urllib.urlopen(self.url).read()
        soup = BeautifulSoup(html)
        releases = soup.findAll("td", { "class": "big" })[2:]
        for entry in releases:
            date = self._parse_date(entry.find("div", { 'class': 'time' }).find("a")['href'].split("day=")[1])
            entries.append([entry.find("b").text, date])
        return entries

def main(args):
    ab = AbsolutePunkFeed()
    entries = ab.get_events()
    dates = {}
    for entry in entries:
        if not dates.has_key(entry[1]):
            dates[entry[1]] = []
        if entry[0] not in dates[entry[1]]:
            dates[entry[1]].append(entry[0])
    now = datetime.date.today()
    #now = datetime.date(2009, 12, 8)
    if now in dates:
        msg = []
        for entry in dates[now]:
            msg.append(entry)
        html = '<br/>'.join(msg)
        g = GSendMail(args[0], args[1]) #pass in
        g.send_html(args[0], 'Album Releases', 'Album Releases Today', html)

if __name__ == "__main__": main(sys.argv[1:])

