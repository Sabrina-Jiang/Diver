# from pyquery import PyQuery as pq


# link_tree = []
# org_tree = []

# # d = pq(url=_domain)
# # d('a').each(lambda i, item: link_tree.append({"url": pq(item).attr('href'), "title": d('title').text(), "next": []}) )

# # link_tree = list(filter(lambda node: (node['url'] != None and (_domain in node['url'] or node['url'][0] == "/")), link_tree))

# # _domain in pq(item) or pq(item)[0] == "/"
# # pq(item) != None

# def dive(target_node, target_url):
#     global target_node
#     if not target_url in link_tree:
#         link_tree.append(target_url)
#     tree_node = []
    
#     if not _domain in target_url:
#         target_url = _domain + target_url

#     d = pq(url=target_url)
#     d('a').each(lambda i, item: tree_node.append({"url": pq(item).attr('href'), "title": d('title').text(), "next": []}))
#     tree_node = list(filter(lambda node: (node['url'] != None) and (_domain in node['url'] or node['url'][0] == "/"), tree_node))
    
#     for i in tree_node:
#         dive(i['next'], i['url'])
#         print(tree_node)
    

# dive(org_tree, _domain)



from pyquery import PyQuery as pq 
import hashlib
import queue

_domain = "http://www.umass.edu"
q = queue.Queue()

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
            print('Adding Url Releation between ' + target_url + " and " + i['url'])
            graph[url_hash].append(i)
            q.put(i['url'])
        
        url_pool.append(url_hash)

    except Exception as e:
        print(e)

q.put(_domain)

while q.qsize() > 0:
    dive(q.get())