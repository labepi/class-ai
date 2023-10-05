import re
import os
import sys
import graph

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

    def read(self, graph):
        """
        """
        if os.path.isfile(self.path):

            handle = open(self.path)
            lines = handle.read().strip().split('\n')
            handle.close()

            read_function = self.read_node
            for line in lines:
                line = line.strip()
                if line[0] == "#":
                    d = line.split(' ')
                    self.dimension = (int(d[1]), int(d[2]))
                    read_function = self.read_edge
                else:
                    read_function(line, graph)

    def print(self):
        """
        """
        print(self.dimension)

if __name__ == "__main__":
    t = TGF(sys.argv[1])
    t.read(graph.Graph())
    t.print()
