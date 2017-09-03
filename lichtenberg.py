import random as random_

from electron_tree import ElectronTree, Electron

def f_range(start_, stop_, step_):
    return (float(i) / step_ for i in xrange(start_, int(stop_ * step_)))

def generate_dist_table(close_dist):
    table = {}
    for x in range(0, close_dist + 1):
        for y in range(-close_dist - 1, close_dist + 1):
            table[x, y] = dist(0, 0, x, y)
    return table
    
def prune(e_keys, e, desired_length, tlr):
    max_x, _ = max(e_keys, key=(lambda x: x[0]))
    prune_from = int(max_x * tlr)
    l = len(e_keys)
    i = l
    while l > desired_length and i >= 0:
        i -= 1
        if e_keys[i].x < prune_from:
            e_keys[i], e_keys[-1] = e_keys[-1], e_keys[i]
            e.pop(e_keys.pop())
            l -= 1

class Lichtenberg(object):
    CLOSE_DIST = 5
    
    def __init__(self, x, y, point_distance):
        self.x = x // point_distance
        self.y = y // point_distance
        self.point_distance = point_distance
        self.available_points = [[Electron(x, y) for y in xrange(height // point_distance)] for x in xrange(width // point_distance)]
        self.max_x = len(self.available_points)
        self.max_y = len(self.available_points[0])
        self.escape = {}
        self.escapekeys = []
        self.d_table = generate_dist_table(self.CLOSE_DIST)
        self.tree = ElectronTree(None, Electron(self.x, self.y), 0, self.available_points, 
                                 self.escape, self.escapekeys, self.CLOSE_DIST, self.max_x, self.max_y, self.d_table)

    def update(self):
        if self.escape:
            if len(self.escapekeys) > 6000:
                print "pruned", len(self.escapekeys), len(set(self.escapekeys)),
                prune(self.escapekeys, self.escape, 4000, 0.9)
                print(len(self.escapekeys))
            i = random_.randrange(0, len(self.escapekeys))
            self.escapekeys[i], self.escapekeys[-1] = self.escapekeys[-1], self.escapekeys[i]
            e = self.escapekeys.pop()
            parent, _ = self.escape.pop(e)
            parent.add_node(ElectronTree(parent, e, 0, self.available_points, 
                                    self.escape, self.escapekeys, self.CLOSE_DIST, self.max_x, self.max_y, self.d_table))
        else:
            print("DONE")
    
    def draw(self, points=False):
        pushMatrix()
        scale(self.point_distance, self.point_distance)
        self.tree.draw()
        popMatrix()
        if points:
            loadPixels()
            for i in self.escapekeys:
                pixels[i.y * width * self.point_distance + i.x * self.point_distance] = color(255)
            updatePixels()