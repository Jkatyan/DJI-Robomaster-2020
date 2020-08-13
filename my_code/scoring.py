import sys
from image_processing import image_processing
import random

sys.path.append("../auto_grader/")
from auto_grader import auto_grader
ag = auto_grader()

# Lists
pairs_list = []


class Move:
    def __init__(self, obj1, obj2, dist):
        self.x1 = obj1.x
        self.y1 = obj1.y
        self.x2 = obj2.x
        self.y2 = obj2.y
        self.dist = dist

    def __repr__(self):
        return "1: (" + str(self.x1) + ", " + str(self.y1) + ") 2: (" + str(self.x2) + ", " + str(self.y2) + ") dist = " + str(self.dist) + "\n\n"

    def __eq__(self, mov2):
        return \
            self.x1 == mov2.x1 and \
            self.y1 == mov2.y1 and \
            self.x2 == mov2.x2 and \
            self.y2 == mov2.y2


def start_scoring():
    global pairs_list
    grid = [[image_processing.Square() for i in range(10)] for j in range(10)]
    grid2 = [[image_processing.Square() for i in range(10)] for j in range(10)]

    lst_counter = 0
    for i in range(10):
        for j in range(10):
            if i == 0 or i == 9:
                grid[i][j] = image_processing.Square(-1, -1, j, i)
            else:
                if j == 0 or j == 9:
                    grid[i][j] = image_processing.Square(-1, -1, j, i)
                else:
                    grid[i][j] = image_processing.lst[lst_counter]
                    grid[i][j].x = j
                    grid[i][j].y = i
                    lst_counter += 1

    lst_counter = 0
    for i in range(10):
        for j in range(10):
            if i == 0 or i == 9:
                grid2[i][j] = image_processing.Square(-1, -1, j, i)
            else:
                if j == 0 or j == 9:
                    grid2[i][j] = image_processing.Square(-1, -1, j, i)
                else:
                    grid2[i][j] = image_processing.lst2[lst_counter]
                    grid2[i][j].x = j
                    grid2[i][j].y = i
                    lst_counter += 1

    def verify_grid():
        check_list = []
        watch_list = []
        for i in range(1, 9):
            for j in range(1, 9):
                check_list.append(grid[i][j])
                for k in range(1, 9):
                    for l in range(1, 9):
                        if matches(grid[i][j], grid[k][l]):
                            check_list.append(grid[k][l])
                if len(check_list) % 2 != 0:
                    for p in range(len(check_list)):
                        watch_list.append(check_list[p])
        for i in range(len(watch_list)):
            if watch_list[i].number != grid2[watch_list[i].y][watch_list[i].x].number:
                watch_list[i].number = grid2[watch_list[i].y][watch_list[i].x].number

    def is_obstacle(obj1, x, y):
        if not 10 > x >= 0 or not 10 > y >= 0:
            return True
        elif ((obj1.color != None or obj1.number != None) and not grid[y][x].edge) or (obj1.dist != grid[y][x].dist and grid[y][x].dist != 0):
            return True
        else:
            return False

    def matches(obj1, obj2):
        if obj1.x != obj2.x or obj1.y != obj2.y:
            if obj1.color == obj2.color and obj1.number == obj2.number:
                return True
        return False

    def try_adding_pair(startObj, obj1, dist):
        if matches(obj1, startObj):
            if not Move(startObj, obj1, dist) in pairs_list and not Move(obj1, startObj, dist) in pairs_list:
                pairs_list.append(Move(startObj, obj1, dist))
                return True
            return False
        return False

    def clear_moves():
        for i in range(10):
            for j in range(10):
                grid[i][j].dist = 0

    def search(startX, startY):
        clear_moves()
        startObj = grid[startY][startX]

        if not startObj.edge:
            nextCheckList = [startObj]

            dx = [1, 0, -1, 0]
            dy = [0, 1, 0, -1]

            dist = 0

            while dist < 4:
                check_list = nextCheckList.copy()
                while len(check_list) > 0:
                    obj1 = check_list.pop(0)

                    for i in range(4):
                        x = obj1.x
                        y = obj1.y
                        obstacle_hit = False
                        while not obstacle_hit:
                            x += dx[i]
                            y += dy[i]
                            if is_obstacle(startObj, x, y):
                                obstacle_hit = True
                                if 10 > x >= 0 and 10 > y >= 0:
                                    try_adding_pair(startObj, grid[y][x], dist + 1)
                            else:
                                obj2 = grid[y][x]
                                obj2.dist = dist + 1
                                nextCheckList.append(obj2)
                dist += 1

    current_move = 1
    def score():
        if len(pairs_list) == 0:
            last_len = len(pairs_list)
            for i in range(1, 9):
                for j in range(1, 9):
                    search(j, i)
            if not last_len == len(pairs_list):
                return
            what_is_left = []
            what_is_not_sure = []
            for y in range(1, 9):
                for x in range(1, 9):
                    if not grid[y][x].edge:
                        what_is_left.append(grid[y][x])
                        if not grid[x][y].isExact:
                            what_is_not_sure.append(grid[y][x])
            if len(what_is_not_sure) >= 2: plst = what_is_not_sure
            else: plst = what_is_left
            a = plst.pop(random.randint(0, len(plst)-1))
            b = plst.pop(random.randint(0, len(plst)-1))
            pairs_list.append(Move(a, b, 1))
        for i in range(1, 5):
            for exactA in [True, False]:
                for exactB in [True, False]:
                    for move in pairs_list:
                        if move.dist == i and grid[move.y1][move.x1].isExact == exactA and grid[move.y2][move.x2].isExact == exactB:
                            result = ag.link(move.y1-1, move.x1-1, move.y2-1, move.x2-1)
                            if type(result) != int:
                                grid[move.y1][move.x1].number = result[0][1]
                                grid[move.y1][move.x1].color = result[0][0]+1
                                grid[move.y2][move.x2].number = result[1][1]
                                grid[move.y2][move.x2].color = result[1][0]+1
                                grid[move.y1][move.x1].isExact = True
                                grid[move.y2][move.x2].isExact = True
                                return False
                            else:
                                grid[move.y1][move.x1].edge = True
                                grid[move.y2][move.x2].edge = True
                                grid[move.y1][move.x1].number = -1
                                grid[move.y2][move.x2].number = -1
                                grid[move.y1][move.x1].color = -1
                                grid[move.y2][move.x2].color = -1
                                return True

    def is_empty():
        for i in range(10):
            for j in range(10):
                if not grid[i][j].edge:
                    return False
        return True

    def print_map():
        for i in range(10):
            for j in range(10):
                print(grid[i][j], file=image_processing.stdout, end=" ")
            print(file=image_processing.stdout)

    verify_grid()
    while not is_empty():
        for i in range(1, 9):
            for j in range(1, 9):
                search(j, i)

        print(pairs_list, file=image_processing.stdout)

        score()
        pairs_list.clear()
        current_move += 1
