from scene import *
import sound
import pickle

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
        return point in self.bounds

class MenuButton(object):
    def __init__(self, text, bounds, font_size, height, action):
        self.text   = text
        x, y, w, h = bounds
        self.bounds = Rect(x - w, height - (y + h), w * 2, h)
        self.font_size = font_size
        self.action = action
    
    def draw(self):
        x, y = self.bounds.center()
        rect(*self.bounds)
        text(self.text,
             'AvenirNext-Heavy',
             self.font_size,
             x,
             y)
    
    def hit(self, point):
        return point in self.bounds

class DrumMachine(Scene):
    _pgwindowtitle = "Drum Machine"
    
    # Menu button actions
    def btnsave(self):
        pickle.dump(self.nodes, open('nodes.dat', 'w'))
    
    def btnload(self):
        try:
            self.nodes = pickle.load(open('nodes.dat'))
        except:
            pass
    
    def btnpause(self):
        self.paused = True
    
    def btnresume(self):
        self.paused = False
    
    # Class functions
    
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
        self.btncolor = (1, 0.6, 0.6)
        
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
        
        self.nodes    = self.generate_nodes(8, 16, self.size.w/8., self.size.h/16.)
        self.curline  = 0
        self.maxline  = len(self.nodes) - 1
        self.hitnode  = None
        self.touch_id = None
        self.touchloc = None
        self.menuopen = False
        self.menuh    = 0
        self.paused   = False
        
        self.fontsize = 30.0 * self.size.w/748.0
        
        self.menucolor = (0.3, 0.3, 0.3)
        self.bordercl  = (0.5, 0.5, 0.5)
        
        btns = self.nodes[0]
        y    = self.size.h - btns[0].bounds.center()[1]
        
        b1, b2, b3, b4 = [btns[1].bounds,
                          btns[3].bounds,
                          btns[5].bounds,
                          btns[7].bounds]
                          
        self.menubuttons = [
            MenuButton('Save', b1, self.fontsize, self.size.h, self.btnsave),
            MenuButton('Load', b2, self.fontsize, self.size.h, self.btnload),
            MenuButton('Pause', b3, self.fontsize, self.size.h, self.btnpause),
            MenuButton('Resume', b4, self.fontsize, self.size.h, self.btnresume),
        ]
        
        stroke(*self.bordercl)
        stroke_weight(1)
    
    def drawmenu(self):
        stroke(*self.menucolor)
        fill(*self.btncolor)
        for menubutton in self.menubuttons:
            menubutton.draw()
        
        stroke(*self.bordercl)
    
    def draw(self):
        if not self.paused:
            self.curline += 1
            if self.curline > self.maxline:
                self.curline = 0
            for index, line in enumerate(self.nodes):
                bright = False
                if index == self.curline:
                    bright = True
                for node in line:
                    node.draw(bright)
        
            fill(*self.menucolor)
            rect(0, self.size.h - self.menuh, self.size.w, self.menuh)
            if self.menuopen:
                self.drawmenu()

    def touch_began(self, touch):
        if not self.touch_id:
            self.touch_id = touch.touch_id
            self.touchloc = touch.location
        for line in self.nodes:
            for node in line:
                if node.hit(touch.location):
                    self.hitnode = node
                    return
    
    def touch_moved(self, touch):
        if not self.menuopen:
            diff = self.touchloc.y - touch.location.y
            if diff < 0:
                diff = 0
            if diff > self.size.h/16:
                diff = self.size.h/16
            self.menuh = diff
    
    def touch_ended(self, touch):
        if touch.touch_id == self.touch_id:
            if not self.menuopen:
                if self.menuh == self.size.h/16:
                    self.menuopen = True
                else:
                    self.menuh = 0
                if self.hitnode and self.hitnode.hit(touch.location) and\
                        not self.paused:
                    self.hitnode.toggle()
            else:
                hit = False
                for menubutton in self.menubuttons:
                    if menubutton.hit(touch.location):
                        menubutton.action()
                        hit = True
                if not hit and not self.paused:
                    self.menuh = 0
                    self.menuopen = False
            self.touch_id = None

run(DrumMachine(), PORTRAIT, 5)
