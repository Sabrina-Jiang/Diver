from pyquery import PyQuery as pq
from graphviz import Digraph
 
import hashlib

dot = Digraph(comment='Sitemap')
dot.format = 'svg'

class crawler:
    def __init__(self, d):
        self._domain = d
        self.graph_path = []

    def craw(self, target_url=None):
        target_url = self._domain
        d = pq(url=target_url)

        tree = d('a').map(
            lambda i, item: {
                "url": str(pq(item).attr('href')).replace(self._domain, ''),
                "text": pq(item).text(),
                "hash": hashlib.md5(pq(item).text().encode('utf-8')).hexdigest(),
                "slice": {
                    "tag": list(
                        filter(
                            lambda elem: len(elem) > 1,
                                list(str(pq(item).attr('href')).replace(self._domain, '').split('/'))
                        )
                    ),
                    "hash": list(
                        map(
                            lambda item: hashlib.md5(item.encode('utf-8')).hexdigest(),
                            list(
                                filter(
                                    lambda elem: len(elem) > 1,
                                    list(str(pq(item).attr('href')).replace(self._domain, '').split('/'))
                                )
                            )
                        )
                    )
                }
            }).filter(
            lambda i, item:
                (item['url'] is not None)
                and (len(item['url']) > 1)
                and (self._domain in item['url'] or item['url'][0] == '/')
            )

        root = hashlib.md5(target_url.encode('utf-8')).hexdigest()
        dot.node(root, target_url, href=target_url)

        for node in tree:
            # print(target_url + " ------> " + node["url"])
            pre_node = root
            for j in range(0, len(node["slice"]["tag"])):
                if pre_node + node["slice"]["hash"][j] not in self.graph_path:
                    dot.node(node["slice"]["hash"][j], node["slice"]["tag"][j], href=target_url)
                    dot.edge(pre_node, node["slice"]["hash"][j])
                    self.graph_path.append(pre_node + node["slice"]["hash"][j])

                pre_node = node["slice"]["hash"][j]

        dot.render('result', view=False)

        self.graph_path = []
        tree = []
        return open('result.svg').read()