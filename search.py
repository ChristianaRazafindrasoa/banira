from collections import deque
import requests

def search(startingPage, maxLevel, maxPagesVisited):
    pageQueue = deque()
    visitedPages = set()

    pageQueue.append(startingPage)
    visitedPages.add(startingPage)

    while(pageQueue and maxLevel > 0):
        nodesInLevel = len(pageQueue)
        for i in range(nodesInLevel):
            currentPage = pageQueue.popleft()
            maxPagesVisited -= 1
            links, lat, lon = getLinks(currentPage)
            print(lat, lon)
            for link in links:
                if link not in visitedPages and not filter(link):
                    pageQueue.append(link)
                    visitedPages.add(link)
            if (maxPagesVisited == 0):
                return
        maxLevel -= 1
        

     
def filter(title):
    return len(title) < 5

def buildGetPageInfoUrl(title):
    title = title.replace(" ", "_")
    return f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&generator=links&prop=coordinates&gpllimit=50&format=json"


def getLinks(title):
    link = buildGetPageInfoUrl(title)
    response = requests.get(link)
    print("executed api request")
    if not response.ok:
        print(response)
        return []
    json = response.json()
    pages = json['query']['pages']
    titles = []
    for pageId in pages.keys():
        if pageId == '-1':
            continue
        for link in pages[pageId]['links']:
            titles.append(link['title'])
        lat = -1
        lon = -1
        if 'coordinates' not in pages[pageId]:
            continue
        for coordinate in pages[pageId]['coordinates']:
            lat = coordinate['lat']
            lon = coordinate['lon']
    return titles, lat, lon