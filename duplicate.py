#!/usr/bin/python
import os
import sys

print "input the university code (e.g. 8-PU)\n>>>",
sys.stdout.flush()
univ_name = raw_input()

os.system("cp -r src/8-PU/ src/" + univ_name + "/")
os.system('sed -n "s/8-PU/'\
 + univ_name + '/g" src/' + univ_name + '/faculty/faculty/spiders/faculty_spider.py')
os.system("mkdir -p data/" + univ_name)

print "Don't forget to change (1) allowed_domains (2) start_urls (3) xpath"
