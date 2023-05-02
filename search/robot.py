class Grid:
    """
    """
    def __init__(self, width, height=None):
        """
        """
        if height == None:
            height = width
        self.dimension = (width, height)
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
        content.append('#')
        for (i, j, info) in self.edges:
            content.append("%d %d %s" % (i, j, info))
        return '\n'.join(content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        w, h = int(sys.argv[1]), int(sys.argv[2])
        g = Grid(w, h)
        print(g.to_tgf())
