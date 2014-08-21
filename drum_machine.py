from scene import *
import sound

class Node(object):
    def __init__(self, x, y, w, h, bgcolour, slcolour, drum):
        self.size   = Size(w, h)
        self.bounds = Rect(x, y, w, h)
        self.bg     = bgcolour # Default background colour
        self.sl     = slcolour # Background colour when selected
        self.state  = 0
        self.drum   = drum
        sound.load_effect(self.drum)
    
    def toggle(self):
        self.state = {0:1,1:0}[self.state]
    
    def draw(self, bright=False):
        colour   = self.sl if self.state else self.bg
        colormod = 1 if bright else 0.8
        fill(*[i*colormod for i in colour])
        rect(*self.bounds)
        if self.state and bright:
            sound.play_effect(self.drum)

    def hit(self, point):
        if point in self.bounds:
            self.toggle()
            return True

class DrumMachine(Scene):
    _pgwindowtitle = "Drum Machine"
    def generate_nodes(self, rows, lines, w, h):
        nodes = []
        for y in range(lines):
            line = []
            for x in range(rows):
                line.append(Node(x * w,
                                    y * h,
                                    w, h,
                                    self.nodebg,
                                    self.nodesl[x],
                                    self.drums[x]))
                x += 1
            y += 1
            nodes.append(line)
        return nodes

    def setup(self):
        self.nodebg  = (1, 1, 1)
        self.nodesl  = {
            0  : (  1,   0,   0),
            1  : (  1,   1,   0),
            2  : (  0,   1,   0),
            3  : (0.6,   1, 0.6),
            4  : (  0,   1,   1),
            5  : (  0,   0,   1),
            6  : (0.6, 0.6,   1),
            7  : (  1,   0,   1),
        }
        
        self.drums   = {
            0  : "Drums_01",
            1  : "Drums_02",
            2  : "Drums_03",
            3  : "Drums_04",
            4  : "Drums_05",
            5  : "Drums_06",
            6  : "Drums_07",
            7  : "Drums_08",
        }
        
        self.nodes   = self.generate_nodes(8, 16, self.size.w/8., self.size.h/16.)
        self.curline = 0
        self.maxline = len(self.nodes) - 1
        stroke(0.5, 0.5, 0.5)
        stroke_weight(1)
    
    def draw(self):
        self.curline += 1
        if self.curline > self.maxline:
            self.curline = 0
        for index, line in enumerate(self.nodes):
            bright = False
            if index == self.curline:
                bright = True
            for node in line:
                node.draw(bright)

    def touch_began(self, touch):
        for line in self.nodes:
            for node in line:
                if node.hit(touch.location): return

run(DrumMachine(), PORTRAIT, 5)
