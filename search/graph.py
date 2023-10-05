import re
import math
import tgf

USAGE = """\
Find a path from the first to the last node.

{} <method> <graph>
  <method> - a: A-STAR (heuristic: Euclidean distance), b: BFS, d: DFS.
  <graph> - The graph description from a TGF file.\
"""

AST = 1
BFS = 2
DFS = 3

METHOD = {'a': AST, 'b': BFS, 'd': DFS}

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

    def search(self, start, goal, method):
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
        # choosing method
        if method == AST:
            self.insert_ordered(memory, start, goal)
        else:
            memory.append(start) # both
        while memory:
            # choosing method
            if method == AST:
                node_a = self.remove_nearest(memory, goal)
            elif method == DFS:
                node_a = memory.pop() # lifo
            else:
                node_a = memory.pop(0) # fifo
            if not visited[node_a]:
                visited[node_a] = True
                for node_b in self.adjacency[node_a]:
                    if not visited[node_b]:
                        # choosing method
                        if method == AST:
                            self.insert_ordered(memory, node_b, goal)
                        else:
                            memory.append(node_b) # both
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


if __name__ == "__main__":
    """
    """
    import sys
    if len(sys.argv) > 2:
        m = METHOD[sys.argv[1]]
        g = Graph()
        tgf.TGF(sys.argv[2]).read(g)
        ans = g.search(g.nodes[0], g.nodes[-1], m)
        node = g.nodes[-1]
        g.heuristic(g.nodes[0], g.nodes[-1])
        found = 0
        count = 0
        while node != None:
            if node != ans[node]:
                node = ans[node]
            else:
                found = count
                node = None
            count = count + 1
        print(found)
    else:
        print(USAGE.format(sys.argv[0]))
