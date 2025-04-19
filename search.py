from collections import deque
import requests

# Modify this function to return a map (pageTitle -> []Page)
def search(startingTitle, maxLevel, maxPagesVisited):
    pageQueue = deque()
    visitedPages = set()
    graph = dict()

    startingPage = Page(startingTitle, -1, -1)
    pageQueue.append(startingPage)
    visitedPages.add(startingPage)

    while(pageQueue and maxLevel > 0):
        nodesInLevel = len(pageQueue)
        for i in range(nodesInLevel):
            currentPage = pageQueue.popleft()
            maxPagesVisited -= 1
            pages = getLinks(currentPage)
            graph[currentPage] = pages
            for page in pages:
                if page not in visitedPages and not filter(page.title):
                    pageQueue.append(page)
                    visitedPages.add(page)
            if (maxPagesVisited == 0):
                return format_graph(graph)
        maxLevel -= 1

    return format_graph(graph)

def format_graph(graph):
    formatted_graph = {
        "graph": {},
        "nodes": {}
    }
    for page in graph:
        titles = [p.title for p in graph.get(page)]
        formatted_graph['graph'][page.title] = titles
        formatted_graph['nodes'][page.title] = {}
        formatted_graph['nodes'][page.title]['lat'] = page.lat
        formatted_graph['nodes'][page.title]['lon'] = page.lon
    return formatted_graph

def filter(title):
    return len(title) < 5 or title.startswith("Wikipedia:") or title.startswith("Template:") 

def buildGetPageInfoUrl(title):
    title = title.replace(" ", "_")
    return f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&generator=links&prop=coordinates&gpllimit=50&format=json"


class Page():
    def __init__(self, title, lat, lon):
        self.title = title
        self.lat = lat
        self.lon = lon

    def __eq__(self, other):
        if not isinstance(other, Page):
            return False
        titles_equal =  self.title == other.title
        lats_equal = self.lat == other.lat
        lons_equal = self.lon == other.lon
        return titles_equal and lats_equal and lons_equal

    def __hash__(self):
            return hash((self.title, self.lat, self.lon))
    
    def containsCoordinates(self):
        return self.lat != -1 and self.lon != -1

def getLinks(page):
    link = buildGetPageInfoUrl(page.title)
    response = requests.get(link)
    print("executed api request")
    if not response.ok:
        print(response)
        return []
    json = response.json()
    pages = json['query']['pages']
    pageList = []
    for pageId in pages.keys():
        if pageId == '-1':
            continue
        if 'coordinates' in pages[pageId] and len(pages[pageId]['coordinates']) > 0:
            page = Page(pages[pageId]['title'], -1, -1)
            page.lat = pages[pageId]['coordinates'][0]['lat']
            page.lon = pages[pageId]['coordinates'][0]['lon']
            pageList.append(page)


    return pageList