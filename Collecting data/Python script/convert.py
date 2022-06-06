import json
import re


def process_item(item):
    id = re.findall("([^/]+$)", item['url'])[0]

    return f'''
dat:{id}
    a pro:Game;
    rdfs:label "{item["name"]}"@en;
    pro:wiki "{item["wikipedia"]}";
    pro:publisher {item["pub"]};
    pro:dev {",".join(item['dev'])};
    pro:genre {",".join(item['genre'])};
    pro:platforms {",".join(item['platform'])};
    pro:image "{item["image"]}".
'''.replace("http://dbpedia.org/resource/", "dbr:").replace('(', '').replace(')', '')


if __name__ == '__main__':
    with open("data.json") as f:
        data = json.load(f)
    prefixs = '''
@prefix pro: <http://api.pa1007.dev/ontology/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dat: <http://api.pa1007.dev/data/> .  
@prefix dbr: <http://dbpedia.org/resource/> .
'''
    for x in data:
        prefixs += "\n" + process_item(data[x])

    print(prefixs)
