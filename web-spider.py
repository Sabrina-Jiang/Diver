from pyquery import PyQuery as pq
from graphviz import Digraph
 
import hashlib
import functools

dot = Digraph(comment='Sitemap')

_domain = "http://www.umass.edu"

url_pool = []
graph = {}


def my_hash(target):
    return hashlib.md5(target.encode('utf-8')).hexdigest()


def dive(target_url):
    try:
        url_hash = my_hash(target_url)
    
        if not _domain in target_url:
            target_url = _domain + target_url

        dot.node(my_hash(target_url), target_url)
        
        result = []
        d = pq(url=target_url)
        d('a').each(lambda i, item: result.append({"url": pq(item).attr('href'), "title": d('title').text(), "text": pq(item).text()}))
        result = list(filter(lambda node: (node['url'] != None) and (len(node['url']) > 1) and (_domain in node['url'] or node['url'][0] == "/"), result))
        
        for i in result:
            item_url = i['url']

            # if not _domain in item_url:
            #     item_url = _domain + item_url

            item_url = item_url.replace(_domain, "")
                
            if not item_url in url_pool:
                url_pool.append(item_url)
            else:
                continue
            
            print(target_url + " ------> " + item_url)


            item_array = [i for i in item_url.split('/') if i != '']
            hash_array = map(my_hash, item_array)
            
            if (len(item_array) < 2):
                continue

            dot.node(my_hash(item_array[0]), item_array[0])
            dot.edge(my_hash(target_url), my_hash(item_array[0]))


            for i in range(1, len(item_array)):
                dot.node(my_hash(item_array[i]), item_array[i])
                dot.edge(my_hash(item_array[i - 1]), my_hash(item_array[i]))

    except Exception as e:
        print(e)


# "slice": str(pq(item).attr('href')).split('/')

def crawler(target_url):

    d = pq(url=target_url)

    tree = d('a').map(
        lambda i, item: {
            "url": pq(item).attr('href'),
            "text": pq(item).text(),
            "hash": my_hash(pq(item).text()),
            "slice": {
                "tag": list(
                    filter(
                        lambda elem: len(elem) > 1,
                            list(str(pq(item).attr('href')).split('/'))
                    )
                ),
                "hash": list(
                    map(
                        lambda item: hashlib.md5(item.encode('utf-8')).hexdigest(),
                        list(
                            filter(
                                lambda elem: len(elem) > 1,
                                list(str(pq(item).attr('href')).split('/'))
                            )
                        )
                    )
                )
            }
        }).filter(
        lambda i, item:
            (item['url'] is not None)
            and (len(item['url']) > 1)
            and (_domain in item['url'] or item['url'][0] == '/')
        )

    root = my_hash(target_url)
    dot.node(root, target_url)

    for node in tree:
        print(target_url + " ------> " + node["url"])

        pre_node = root
        for j in range(0, len(node["slice"]["tag"])):
            dot.node(node["slice"]["hash"][j], node["slice"]["tag"][j])
            dot.edge(pre_node, node["slice"]["hash"][j])
            pre_node = node["slice"]["hash"][j]


    # print(list(result))
    # try:
    #
    #
    # except Exception as e:
    #     print(e)

crawler(_domain)

dot.view()
