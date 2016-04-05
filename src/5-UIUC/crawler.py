
import re
import time
import requests
import os
from os import system

def main():
    L = len('<a href="')
    with open("./data/5-UIUC/entrance.html", "r") as f:
        html = f.read()
    poses = re.findall('<a href="profile/[^"]*">[^<]*<', html)
    links = []
    names = []
    for pos in poses:
        head = L
        tail = head
        while pos[tail] != '"':
            tail += 1
        links.append("https://cs.illinois.edu/directory/" + pos[head:tail])
        head = tail + 2
        tail = len(pos) - 1
        names.append(pos[head:tail].replace(' ', '_').replace('(', '').replace(')', '').replace(',', ''))

    user_agent = {'User-agent': 'Mozilla/5.0'}
    L = len(links)
    for i in range(L):
        link = links[i]
        name = names[i]
        print link + " (" + str(i) + "/" + str(L) + ")...",
        if L % 10 == 0:
            time.sleep(5)
        if os.path.isfile("./data/5-UIUC/" + name + "/index.html"):
            print " (skip)"
            continue
        else:
            print ""
        try:
            response = requests.get(link, headers=user_agent)
            page = response.text
            system("mkdir \"./data/5-UIUC/" + name + "\"")
            with open("./data/5-UIUC/" + name + "/index.html", "w") as f:
                f.write(page.encode('utf-8'))
        except:
            pass


if __name__ == "__main__":
    main()
