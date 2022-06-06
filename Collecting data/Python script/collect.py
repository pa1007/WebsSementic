import json

import wikipedia
from SPARQLWrapper import SPARQLWrapper, JSON

if __name__ == '__main__':
    removed_images = ['https://upload.wikimedia.org/wikipedia/commons/4/49/Star_empty.svg',
                      'https://upload.wikimedia.org/wikipedia/commons/5/51/Star_full.svg',
                      'https://upload.wikimedia.org/wikipedia/commons/8/81/Star_half.svg']
    sparql_dbpedia = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql_dbpedia.setReturnFormat(JSON)

    SPARQL_GET_LISTS = '''
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbp: <http://dbpedia.org/property/>

    SELECT * WHERE {
    ?a a dbo:VideoGame  ; foaf:name ?page ; foaf:isPrimaryTopicOf ?c ;
     dbo:computingPlatform ?cp ;
     dbo:developer ?dev;
     dbo:genre ?genre;
     dbo:publisher ?pub;
     dbp:modes ?mode;
     dbo:wikiPageID ?id.
    FILTER (lang(?page) = 'en')
    }limit 100000
    '''
    sparql_dbpedia.setQuery(SPARQL_GET_LISTS)
    obj = {}
    try:
        res = sparql_dbpedia.queryAndConvert()
        for r in res["results"]["bindings"]:
            dbobj = r["a"]['value']
            pagename = r["page"]['value']
            wikiurl = r["c"]['value']
            platform = r["cp"]['value']
            dev = r["dev"]['value']
            genre = r["genre"]['value']
            publisher = r["pub"]['value']
            if dbobj in obj:
                temp = obj.get(dbobj)
                if platform not in temp['platform']:
                    temp['platform'] += [platform]
                if dev not in temp['dev']:
                    temp['dev'] += [dev]
                if genre not in temp['genre']:
                    temp['genre'] += [genre]
            else:
                page = wikipedia.page(pageid=r["id"]['value'])
                for x in range(len(page.images)):
                    image = page.images[x]
                    if image not in removed_images:
                        break
                obj.update({dbobj: {"url": dbobj, "name": pagename, "wikipedia": wikiurl,
                                    "platform": [platform], "dev": [dev], "pub": publisher, "genre": [genre],
                                    "image": image}})
        with open("data.json", "w") as f:
            json.dump(obj, f)
    except Exception as e:
        print(e)
