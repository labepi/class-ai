import os
import re
import math

class Graph:
    """
    """
    def __init__(self, nodes=[], edges=[]):
        """
        """
        self.nodes = nodes
        self.edges = edges
        self.infos = {}
        self.adjacency = {}
        self.distances = {}

    def add_node(self, node, info=""):
        """
        """
        if node not in self.nodes:
            self.nodes.append(node)
        if len(info) > 0:
            self.infos[node] = info

    def add_edge(self, edge, info=""):
        """
        """
        (a, b) = edge
        self.add_node(a)
        self.add_node(b)

        if edge not in self.edges:
            self.edges.append(edge)
        if len(info) > 0:
            self.infos[edge] = info

    def create_adjacency(self):
        """
        """
        self.adjacency = {}

        for node in self.nodes:
            self.adjacency[node] = []

        for (a, b) in self.edges:
            self.adjacency[a].append(b)
            self.adjacency[b].append(a)

    def heuristic(self, node_a, node_b):
        """
        """
        pattern = "^\(([0-9]+),([0-9]+)\)$"
        info = self.infos[node_a]
        ans = re.fullmatch(pattern, info)
        x1, y1 = [int(i) for i in ans.groups()]
        info = self.infos[node_b]
        ans = re.fullmatch(pattern, info)
        x2, y2 = [int(i) for i in ans.groups()]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def remove_nearest(self, memory, goal):
        """
        """
        return memory.pop(0)

    def insert_ordered(self, memory, node, goal):
        """
        """
        if node not in memory:
            self.distances[node] = self.heuristic(node, goal)
            memory.insert(0, node)
            for i in range(1, len(memory)):
                if self.distances[memory[i]] < self.distances[node]:
                    memory[i - 1], memory[i] = memory[i], memory[i - 1]
                else:
                    return True
            return True
        return False

    def search(self, start, goal):
        """
        """
        visited = {}
        origin = {}
        for node in self.nodes:
            visited[node] = False
            origin[node] = None
        origin[start] = start

        memory = []
        self.create_adjacency()
        self.insert_ordered(memory, start, goal)
        while memory:
            node_a = self.remove_nearest(memory, goal)
            if not visited[node_a]:
                visited[node_a] = True
                for node_b in self.adjacency[node_a]:
                    if not visited[node_b]:
                        self.insert_ordered(memory, node_b, goal)
                        origin[node_b] = node_a
                    if node_b == goal:
                        return origin

        return origin

    def __str__(self):
        """
        """
        content = []
        content.append("node: %s" % self.nodes)
        content.append("edge: %s" % self.edges)
        content.append("info: %s" % self.infos)
        return '\n'.join(content)

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
        g = TGF(sys.argv[1]).read()
        ans = g.search(g.nodes[0], g.nodes[-1])
        node = g.nodes[-1]
        g.heuristic(g.nodes[0], g.nodes[-1])
        while node != None:
            print(node, g.infos[node])
            if node != ans[node]:
                node = ans[node]
            else:
                node = None
