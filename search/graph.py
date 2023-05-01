import os
import re

class Graph:
    """
    """
    def __init__(self, nodes=[], edges=[]):
        """
        """
        self.nodes = nodes
        self.edges = edges
        self.info = {}

    def add_node(self, node, info=""):
        """
        """
        if node not in self.nodes:
            self.nodes.append(node)
        if len(info) > 0:
            self.info[node] = info

    def add_edge(self, edge, info=""):
        """
        """
        (a, b) = edge
        self.add_node(a)
        self.add_node(b)

        if edge not in self.edges:
            self.edges.append(edge)
        if len(info) > 0:
            self.info[edge] = info

    def __str__(self):
        """
        """
        ans = "node: %s \nedge: %s \ninfo: %s"
        return ans % (self.nodes, self.edges, self.info)

class TGF:
    """
    """
    def __init__(self, path=""):
        """
        """
        self.path = path
        self.graph = None

    def read_node(self, string, graph):
        """
        """
        pattern = "^([0-9]+) ?(.*)$"
        ans = re.fullmatch(pattern, string)
        (a, info) = ans.groups()
        graph.add_node(a, info)

    def read_edge(self, string, graph):
        """
        """
        pattern = "^([0-9]+) ([0-9]+) ?(.*)$"
        ans = re.fullmatch(pattern, string)
        (a, b, info) = ans.groups()
        graph.add_edge((a, b), info)

    def read(self):
        """
        """
        if os.path.isfile(self.path):

            handle = open(self.path)
            lines = handle.read().strip().split('\n')
            handle.close()

            self.graph = Graph()
            read_function = self.read_node
            for line in lines:
                line = line.strip()
                if line == "#":
                    read_function = self.read_edge
                else:
                    read_function(line, self.graph)

        return self.graph

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        g = TGF(sys.argv[1])
        print(g.read())
