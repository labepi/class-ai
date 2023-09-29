import random

USAGE = """\
Create a TGF descrition of a rectangular Grid.

{} <width> <height> <obstacles>
  <width> - The required grid width.
  <height> - The required grid height.
  <obstacles> - The number of random placed obstacles.\
"""

class Grid:
    """
    """
    def __init__(self, width, height, obstacles=0):
        """
        """
        if height == None:
            height = width
        self.dimension = (width, height)
        self.obstacles = random.sample(range(1, width * height + 1), obstacles)
        self.create_nodes()
        self.create_edges()

    def create_nodes(self):
        """
        """
        width, height = self.dimension
        self.nodes = {}

        count = 1
        for i in range(1, width + 1):
            for j in range(1, height + 1):
                if count not in self.obstacles:
                    self.nodes[(i, j)] = (count, "(%d,%d)" % (i, j))
                count += 1

    def create_edges(self):
        """
        """
        width, height = self.dimension
        self.edges = []

        for (i, j) in self.nodes:
            delta = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]
            for (a, b) in delta:
                if (a, b) in self.nodes:
                    x, xi = self.nodes[(i, j)]
                    y, yi = self.nodes[(a, b)]
                    self.edges.append((x, y, "%s>%s" % (xi, yi)))

    def to_tgf(self):
        """
        """
        content = []
        for (i, j) in self.nodes:
            content.append("%d %s" % self.nodes[(i, j)])
        content.append("# %s %s" % self.dimension)
        for (i, j, info) in self.edges:
            content.append("%d %d %s" % (i, j, info))
        return '\n'.join(content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        w, h, o = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
        g = Grid(w, h, o)
        print(g.to_tgf())
    else:
        print(USAGE.format(sys.argv[0]))
