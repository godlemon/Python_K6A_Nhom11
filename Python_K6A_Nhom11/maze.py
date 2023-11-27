from random import shuffle


class Maze:
    def __init__(self, rows=30, cols=40):

        self.rows = rows
        self.cols = cols
        self.keep_going = 1

        self.maze = {}
        for y in range(rows):
            for x in range(cols):
                cell = {'south': 1, 'east': 1, 'visited': 0}
                self.maze[(x, y)] = cell

    def generate(self, start_cell=None, stack=[]):

        if start_cell is None:
            start_cell = self.maze[(self.cols - 1, self.rows - 1)]

        if not self.keep_going:
            return

        self.check_finished()
        neighbors = []

        if len(stack) == 0:
            stack.append(start_cell)

        curr_cell = stack[-1]

        neighbors = self.get_neighbors(curr_cell)
        shuffle(neighbors)

        for neighbor in neighbors:
            if neighbor['visited'] == 0:
                neighbor['visited'] = 1
                stack.append(neighbor)
                self.knock_wall(curr_cell, neighbor)
                self.generate(start_cell, stack)

    def get_coords(self, cell):
        coords = (-1, -1)
        for k in self.maze:
            if self.maze[k] is cell:
                coords = (k[0], k[1])
                break
        return coords

    def get_neighbors(self, cell):
        neighbors = []

        (x, y) = self.get_coords(cell)
        if (x, y) == (-1, -1):
            return neighbors

        north = (x, y - 1)
        south = (x, y + 1)
        east = (x + 1, y)
        west = (x - 1, y)

        if north in self.maze:
            neighbors.append(self.maze[north])
        if south in self.maze:
            neighbors.append(self.maze[south])
        if east in self.maze:
            neighbors.append(self.maze[east])
        if west in self.maze:
            neighbors.append(self.maze[west])

        return neighbors

    def knock_wall(self, cell, neighbor):
        xc, yc = self.get_coords(cell)
        xn, yn = self.get_coords(neighbor)

        if xc == xn and yc == yn + 1:
            # liền kề phía trên, đập bỏ bức tường phía nam đơn vị liền kề
            neighbor['south'] = 0
        elif xc == xn and yc == yn - 1:
            # liền kề  bên dưới, đập bỏ bức tường phía nam của đơn vị
            cell['south'] = 0
        elif xc == xn + 1 and yc == yn:
            # bên trái đơn vị liền kề, đập bỏ bức tường phía đông đơn vị liền kề
            neighbor['east'] = 0
        elif xc == xn - 1 and yc == yn:
            # đơn vị liền kề bên phải, đánh sập bức tường phía đông của đơn vị
            cell['east'] = 0

    def check_finished(self):
        # Kiểm tra xem đã tạo xong chưa
        done = 1
        for k in self.maze:
            if self.maze[k]['visited'] == 0:
                done = 0
                break
        if done:
            self.keep_going = 0
