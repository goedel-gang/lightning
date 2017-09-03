from collections import namedtuple

Electron = namedtuple('Electron', ['x', 'y'], verbose=False)

def dist_from_table(x1, y1, x2, y2, table):
    return table[x2-x1, y2-y1]

class ElectronTree(object):
    WEIGHT_GAIN = 10000
    HIGH_WEIGHT = 2
    s_table = [sqrt(i / float(WEIGHT_GAIN)) for i in range(WEIGHT_GAIN)]

    def __init__(self, parent, el, weight, available, escape, escapekeys, close_dist, max_x, max_y, d_table):
        self.el = x, y = el
        self.parent = parent
        self.weight = weight
        available[x][y] = False
        for ex in xrange(x, x + close_dist + 1):
            for ey in xrange(y - close_dist - 1, y + close_dist + 1):
                k = available[constrain(ex, 0, max_x - 1)][constrain(ey, 0, max_y - 1)]
                if k and k != self.el:
                    d = dist_from_table(x, y, k.x, k.y, d_table)
                    if d <= close_dist:
                        if k in escape:
                            if escape[k][1] > d:
                                escape[k] = (self, d)
                        else:
                            escape[k] = (self, d)
                            escapekeys.append(k)
        self.children = []
    
    def add_node(self, n):
        self.children.append(n)
        self.add_weight()
        
    def add_weight(self):
        if self.weight < self.WEIGHT_GAIN:
            self.weight += 1
        if self.parent:
            self.parent.add_weight()
    
    def draw(self):
        for child in self.children:
            if child.weight > 2:
                child.draw()
                norm_s = self.s_table[child.weight]
                strokeWeight(norm_s * self.HIGH_WEIGHT)
                stroke(norm_s * 255 * 0.8, 255, 255)
                line(self.el.x, self.el.y, *child.el)