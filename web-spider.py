from pyquery import PyQuery as pq
from graphviz import Digraph
 
import hashlib
import queue

dot = Digraph(comment='Sitemap')

_domain = "http://www.umass.edu"

url_pool = []
graph = {}

def dive(target_url):
    try:
        url_hash = hashlib.md5(target_url.encode('utf-8')).hexdigest()
    
        if not _domain in target_url:
            target_url = _domain + target_url
        if url_hash in url_pool:
            return
        if not url_hash in graph:
            graph[url_hash] = []

        result = []
        d = pq(url=target_url)
        d('a').each(lambda i, item: result.append({"url": pq(item).attr('href'), "title": d('title').text()}))
        result = list(filter(lambda node: (node['url'] != None) and (len(node['url']) > 1) and (_domain in node['url'] or node['url'][0] == "/"), result))
        

        for i in result:
            if not _domain in i['url']:
                item_url = _domain + i['url'] 
            
            print('Adding Url Releation between ' + target_url + " and " + item_url)
            graph[url_hash].append(i)
            dot.node(hashlib.md5(item_url.encode('utf-8')).hexdigest(), item_url)
            dot.edge(hashlib.md5(target_url.encode('utf-8')).hexdigest(), hashlib.md5(item_url.encode('utf-8')).hexdigest())
        
        url_pool.append(url_hash)

    except Exception as e:
        print(e)

dive(_domain)

dot.view()
