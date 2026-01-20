import pyxel
import math

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

class Stars():
    def __init__(self, y):
        self.x = pyxel.rndi(0, SCREEN_WIDTH)
        self.y = pyxel.rndi(y, SCREEN_HEIGHT)
        self.color = 1 + pyxel.rndi(5, 6)

class Spaceship():
    def __init__(self, sx, sy, l, ml, cl):
        self.x = sx
        self.y = sy
        self.level = l
        self.maxlevel = ml
        self.color = cl
        self.statement1 = {5:'Earth: Planet of Radar', 4:'Venus: Planet of Mobility', 9:'Mars: Planet of Calculation', 13:'Mercury: Planet of Arms',3:'Ceres: Planet of Energy'}
        self.statement2 = {5:'Press E to Search', 4:'Press V to Migrate (Spends GP)', 9:'Shows Range of the 1st Attack', 13:'Press M to Shoot (Spends 1200 GP)',3:'Press C to convert HP to GP'}
        self.state1 = self.statement1[int(self.color)]
        self.state2 = self.statement2[int(self.color)]
        self.dist = 0
        self.min_dist = 100
        self.Selected = False
        self.Available = False
        self.Hit = False
        self.Collided = False
        self.nearest = None

class Droplet():
    def __init__(self):
        self.x = SCREEN_WIDTH/2 + pyxel.rndi(-64, 64)
        self.y = pyxel.rndi(int(SCREEN_HEIGHT/5), int(SCREEN_HEIGHT/3))
        self.vx = 0
        self.vy = 0
        self.starty = self.y
        self.aim = 0
        self.speed = -1.6
        self.atkx = self.x + pyxel.rndi(-64, 64)
        self.atky = SCREEN_HEIGHT
        self.Visible = 0
        self.Attack = False
        self.Warped = False
        self.atkcount = 1
        if pyxel.rndi(0, 1) == 1:
            self.atkcount += pyxel.rndi(0, 1)
            if pyxel.rndi(0, 2) >= 1:
                self.atkcount += pyxel.rndi(0, 1)
    def attack(self):
        if self.Attack == False:
            self.vx = (self.atkx - self.x)
            self.vy = (self.atky - self.y)
            self.aim = math.atan2(-self.vy, self.vx)
            self.Attack = True
    def update(self):
        if self.Attack == True:
            self.x += self.speed*math.cos(self.aim)
            self.y -= self.speed*math.sin(self.aim)
            if self.Warped == False and self.speed <= 5:
                self.speed += 0.1
            if self.Warped == True and self.speed >= 1:
                self.speed -= 0.6
            if self.x > SCREEN_WIDTH:
                self.x = 0
            if self.x <0:
                self.x = SCREEN_WIDTH
            if self.y >= SCREEN_HEIGHT:
                if self.atkcount >= 2:
                    self.y = 0
                    self.atkcount -= 1
                else:
                    self.x = SCREEN_WIDTH/2
                    self.y = 24
                    self.Warped = True
            if self.y >= 7*self.starty/8 and self.Warped == True:
                self.__init__()

class Earth():
    def __init__(self):
        self.start = 0
        self.detectedx = 0
        self.detectedy = 0
        self.x_deviation = pyxel.rndi(-8, 8)
        self.y_deviation = pyxel.rndi(-8, 8)

class Venus():
    def __init__(self):
        self.cursorx = 0
        self.cursory = 0
        self.direction = 0
        self.x = 0
        self.y = 0
        self.innerr = 0
        self.outerr = 0

class Mars():
    def __init__(self):
        self.arms = []
        self.deviation = pyxel.rndi(-26, 26)

class Mercury():
    def __init__(self, x, y, d):
        self.start = 0
        self.x = x + pyxel.rndi(-2, 2)
        self.y = y + pyxel.rndi(-2, 2)
        self.vx = (pyxel.mouse_x + d*2*pyxel.rndi(-10, 10) - x)
        self.vy = (pyxel.mouse_y + d*2*pyxel.rndi(-10, 10) - y)
        self.aim = math.atan2(-self.vy, self.vx)
    def update(self):
        self.x += math.cos(self.aim)
        self.y -= math.sin(self.aim)

class Ceres():
    def __init__(self):
        self.start = 0
        self.speed = 0.1
        self.r = 1
        self.dr = 0

    def update(self):
        self.speed += 0.1
        self.r += self.speed * 0.6

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_WIDTH)
        pyxel.sounds[0].set(notes='C3C4', tones='NN', volumes='33', effects='NN', speed=10)
        pyxel.sounds[1].set(notes='G1D1', tones='NN', volumes='33', effects='NN', speed=10)
        pyxel.sounds[2].set(notes='E3E3E3', tones='PSP', volumes='33', effects='NNN', speed=10)
        pyxel.sounds[3].set(notes='A3A3A3', tones='SPP', volumes='33', effects='NNN', speed=10)
        pyxel.sounds[4].set(notes='G2A2G2A2', tones='SPSP', volumes='33', effects='NNNN', speed=10)
        pyxel.sounds[5].set(notes='A3A4A4', tones='SPP', volumes='33', effects='NNN', speed=10)
        pyxel.sounds[6].set(notes='C3C4C4', tones='TPP', volumes='33', effects='NNN', speed=10)
        self.genpoints = 9200
        self.genlevel = 1
        self.seconds = 0
        self.hp = 10000
        self.droplethp = 1000
        self.Start = False
        self.Evolution = False
        self.Enchant = False
        self.Dead = False
        self.Clear = False
        self.radar = []
        self.mobility = []
        self.droplet =[Droplet()]
        self.earth = (Spaceship(SCREEN_WIDTH/2, 3*SCREEN_HEIGHT/4, 6, 11, 5))
        self.ships = [self.earth]
        self.stars = []
        for a in range(40):
            self.stars.append(Stars(0))
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.Start = True
        if self.Start == False:
            return
        self.nearest = None
        self.min_dist = float("inf")
        for self.i in self.ships:
            self.i.Selected = False
            self.dist = (pyxel.mouse_x - self.i.x)**2 + (pyxel.mouse_y - self.i.y)**2
            if self.dist < self.min_dist:
                self.min_dist = self.dist
                self.nearest = self.i
        if self.nearest:
            self.nearest.Selected = True
            
        for self.d in self.droplet:
            self.d.update()
            if self.seconds % 40 == 30:
                self.d.attack()

        self.ship_count = len(self.ships)## Enchant,Evolution,level
        if self.genpoints >= 10000 and self.genlevel <= 4:
            self.Evolution = True
        else:
            self.Evolution = False

        if self.genlevel >= 2:
            if self.genpoints >= 5000:
                self.Enchant = True
            else:
                self.Enchant = False

        if self.Evolution == True and pyxel.btnp(pyxel.KEY_SPACE):
            self.genlevel += 1
            self.genpoints -= 10000

        for self.i in self.ships:
            if self.Enchant == True and self.i.Selected == True and pyxel.mouse_x - 20 < self.i.x < pyxel.mouse_x + 20 and pyxel.mouse_y - 20 < self.i.y < pyxel.mouse_y + 20:
                if self.i.level < self.i.maxlevel and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) == True:
                    self.genpoints -= 5000
                    self.i.level += 2
                    pyxel.play(1, 5)
        
        if self.genlevel >= 1: ## Earthの処理
            if self.radar == []:
                if pyxel.btnp(pyxel.KEY_E):
                    self.radar = [Earth()]
                    pyxel.play(1, 3)
            for self.r in self.radar:
                if self.r.start == 0:
                    self.r.x_deviation = self.r.x_deviation * (1.6-(self.earth.level/self.earth.maxlevel))
                    self.r.y_deviation = self.r.y_deviation * (1.6-(self.earth.level/self.earth.maxlevel))
                    self.r.start = self.seconds
                for self.d in self.droplet:
                    if pyxel.frame_count % 8 == 0:
                        self.r.detectedx = self.d.x
                        self.r.detectedy = self.d.y
                    if self.seconds >= self.r.start + 6 or self.d.Attack == True:
                        self.d.Visible = 1
                    elif self.seconds <= self.r.start + 2:
                        self.d.Visible = 0
                    if self.d.Attack == True and self.r.start <= self.seconds - 12:
                        self.r.start = self.seconds - 32
                    if self.seconds >= self.r.start + 32 and self.d.Attack == False and self.genlevel <= 4:
                        self.radar = []

        if self.genlevel >= 2:#Venusの処理
            if self.ship_count <= 1:
                self.venus = (Spaceship(SCREEN_WIDTH/2-50, 3*SCREEN_HEIGHT/4+30, 4, 8, 4))
                self.ships.append(self.venus) 
                pyxel.play(1, 4)
            if pyxel.btnp(pyxel.KEY_V) and self.genpoints >= 5:
                self.mobility = [Venus()]
            if pyxel.btnr(pyxel.KEY_V) or self.genpoints <= 4:
                self.mobility = []
            for self.m in self.mobility:
                for self.i in self.ships:
                    self.genpoints -= 4
                    if (pyxel.mouse_x - 4*self.venus.level < self.i.x < pyxel.mouse_x + 4*self.venus.level and pyxel.mouse_y - 4*self.venus.level < self.i.y < pyxel.mouse_y + 4*self.venus.level) or self.i.Selected:
                        self.m.cursorx = pyxel.mouse_x - self.i.x
                        self.m.cursory = pyxel.mouse_y - self.i.y
                        self.m.direction = math.atan2(-self.m.cursory, self.m.cursorx)
                        self.m.x = self.i.x + 0.15 * math.cos(self.m.direction) * self.venus.level
                        self.m.y = self.i.y - 0.15 * math.sin(self.m.direction) * self.venus.level
                        self.i.Collided = False
                        for self.other in self.ships:
                            if self.other is self.i:
                                continue
                            self.dx = self.m.x - self.other.x
                            self.dy = self.m.y - self.other.y
                            self.r = (self.i.maxlevel+1) + (self.other.maxlevel+1)
                            if self.dx*self.dx + self.dy*self.dy <= self.r*self.r or self.i.x < 0 + self.i.maxlevel or SCREEN_WIDTH - self.i.maxlevel < self.i.x or self.i.y < 31 + self.i.maxlevel or SCREEN_HEIGHT-20 - self.i.maxlevel < self.i.y:
                                self.i.Collided = True
                                if pyxel.frame_count % 120 == 0:
                                    if self.i.y -80 >= 0 and self.nearest.y < pyxel.mouse_y:
                                        self.nearest.y -= 20
                                    elif self.i.y +70 <= SCREEN_HEIGHT and self.nearest.y > pyxel.mouse_y:
                                        self.nearest.y += 20
                                break
                        if not self.i.Collided:
                            self.i.x = self.m.x
                            self.i.y = self.m.y
                        if self.i.x < 0 + self.i.maxlevel:
                            self.i.x += 0.1
                        if SCREEN_WIDTH - self.i.maxlevel < self.i.x:
                            self.i.x -= 0.1
                        if self.i.y < 31 + self.i.maxlevel:
                            self.i.y += 0.1
                        if SCREEN_HEIGHT - 20 - self.i.maxlevel < self.i.y:
                            self.i.y -= 0.1

        if self.genlevel >= 3: #Marsの処理
            if self.ship_count <= 2:
                self.mars = (Spaceship(SCREEN_WIDTH/2+50, 3*SCREEN_HEIGHT/4-10, 4, 10, 9))
                self.ships.append(self.mars)
                pyxel.play(1, 4)
                self.calculation = [Mars()]
                for self.c in self.calculation:
                    if pyxel.frame_count % 16 == 4:
                        self.c.deviation = pyxel.rndi(-30, 30)

        if self.genlevel >= 4:#Mercuryの処理
            if self.ship_count <= 3:
                self.mercury = (Spaceship(SCREEN_WIDTH/2-100, 3*SCREEN_HEIGHT/4+20, 3, 7, 13))
                self.ships.append(self.mercury)
                pyxel.play(1, 4)
                self.arms = []
            if pyxel.btnp(pyxel.KEY_M) and self.genpoints >= 1200 and 0 < pyxel.mouse_x < SCREEN_WIDTH and 0 < pyxel.mouse_y < SCREEN_HEIGHT:
                self.genpoints -= 1200
                pyxel.play(1, 2)
                self.arms.append(Mercury(self.mercury.x, self.mercury.y, 1.2-(self.mercury.level/self.mercury.maxlevel)))
            for self.a in self.arms:
                for s in range(8):
                    self.a.update()
                if self.a.start == 0:
                    self.a.start = self.seconds
                if self.seconds >= self.a.start + 4:
                    self.arms.remove(self.a)
                elif self.seconds >= self.a.start + 1 and self.a.x - 4 < self.d.x < self.a.x + 4 and self.a.y - 4 < self.d.y < self.a.y + 4:
                    self.droplethp -= pyxel.rndi(70, 120)
                    pyxel.play(1, 0)
                    self.arms.remove(self.a)
                if self.droplethp <= 0:
                    self.Clear = True
                    self.droplet = []


        if self.genlevel >= 5:
            if self.ship_count <= 4:
                self.ceres = (Spaceship(SCREEN_WIDTH/2+90, 3*SCREEN_HEIGHT/4-30, 2, 5, 3))
                self.ships.append(self.ceres)
                pyxel.play(1, 4)
                self.energy = []
            if self.seconds % 40 == 12:
                if self.energy == []:
                    self.energy = [Ceres()]
                    if self.Clear == False:
                        pyxel.play(1, 6)
            for self.e in self.energy:
                if self.e.start == 0:
                    self.e.start = self.seconds
                self.e.update()
                self.e.dr = (self.d.x - self.ceres.x)*(self.d.x - self.ceres.x) + (self.d.y - self.ceres.y)*(self.d.y - self.ceres.y)
                if self.e.dr < self.e.r*self.e.r:
                    self.d.Visible = 2
                if self.seconds >= self.e.start + 7:
                    self.energy.remove(self.e)
            if pyxel.btnp(pyxel.KEY_C) and self.hp >= 2000:
                self.hp -= 500
                self.genpoints += 2000 * self.ceres.level
                pyxel.play(1, 0)

        if pyxel.frame_count % 16 == 8:#秒数の処理
            self.seconds = self.seconds + 1
            for self.i in self.ships:
                self.i.x += pyxel.cos(90*(self.seconds % 4)) 
                self.i.y += pyxel.cos(90*(self.seconds % 4))
                self.i.y += pyxel.sin(90*(self.seconds % 4))
        if self.hp >= 0:#genポイント追加の処理(生存時)
            if self.seconds % 4 == 0 and self.Clear == False and self.Dead == False:
                self.genpoints = self.genpoints + pyxel.rndi(4, 8) * (self.genlevel + 2)
            if (pyxel.btn(pyxel.KEY_U) and pyxel.btn(pyxel.KEY_Y) and pyxel.btn(pyxel.KEY_I)) == True: ###テスト用
                self.genpoints = self.genpoints + 10000
        for self.d in self.droplet:##HPの処理
            for self.i in self.ships:
                if self.i.x - (self.i.level+1) <= self.d.x <= self.i.x + (self.i.level+1) and self.i.y - (self.i.level+1) <= self.d.y <= self.i.y + (self.i.level+1):
                    self.i.Hit = True
                    if self.Dead == False:
                        self.hp -= pyxel.rndi(350, 550)
                    if pyxel.frame_count % 2 == 0:
                        pyxel.play(1, 1)
                else:
                    self.i.Hit = False
            if self.genlevel >= 5 and 0 <= self.hp < 10000 and self.Clear == False:
                if self.seconds % 4 == 0 and pyxel.frame_count % 16 == 0:
                    self.hp += 25
        if self.hp <= 0:
            self.Dead = True
        if self.Dead == True or self.Clear == True or pyxel.btn(pyxel.KEY_RETURN):
            if pyxel.btnp(pyxel.KEY_R):
                self.genpoints = 9200
                self.genlevel = 1
                self.seconds = 0
                self.hp = 10000
                self.droplethp = 1000
                self.Start = False
                self.Evolution = False
                self.Enchant = False
                self.Dead = False
                self.Clear = False
                self.radar = []
                self.mobility = []
                self.droplet =[Droplet()]
                self.earth = (Spaceship(SCREEN_WIDTH/2, 3*SCREEN_HEIGHT/4, 6, 11, 5))
                self.ships = [self.earth]
                self.stars = []
                for a in range(40):
                    self.stars.append(Stars(0))
                pyxel.run(self.update, self.draw)
        
    def draw(self):
        pyxel.mouse(False)
        pyxel.cls(0)
        for self.s in self.stars:
            pyxel.pset(self.s.x, self.s.y, self.s.color)
            self.s.y += 0.5
            if self.s.y >= SCREEN_HEIGHT:
                self.s.y = pyxel.rndi(-10, 10)
                self.s.x = pyxel.rndi(0, SCREEN_WIDTH)
        pyxel.rect(0, 0, SCREEN_WIDTH, 30, 13)
        pyxel.line(0, 30, SCREEN_WIDTH, 30, 5)
        pyxel.line(0, 31, SCREEN_WIDTH, 31, 1)
        pyxel.rect(0, SCREEN_HEIGHT-20, SCREEN_WIDTH, 20, 13)
        pyxel.line(0, SCREEN_HEIGHT-21, SCREEN_WIDTH, SCREEN_HEIGHT-21, 5)
        pyxel.line(0, SCREEN_HEIGHT-22, SCREEN_WIDTH, SCREEN_HEIGHT-22, 1)
        if self.Start == False:
            pyxel.text(3, 2, 'A Hostile Planet threatens you.', 7)
            pyxel.text(3, 9, 'Strengthen your civilization, expand your power, and defeat it.', 7)
            pyxel.text(3, 23, 'Press ENTER to start', 7)
        for self.i in self.ships:
            pyxel.circ(self.i.x, self.i.y, self.i.level, self.i.color)
            if self.i.Hit == True:
                pyxel.circ(self.i.x, self.i.y, (self.i.level/3)*pyxel.rndi(1, 3), 14)
            if self.i.Selected == True:
                pyxel.text(3, 16, str(self.i.state1), 7)
                pyxel.text(3, 23, str(self.i.state2), 7)
                if self.genlevel >= 3:
                    pyxel.text(SCREEN_WIDTH-56, 23, "Attacks in "+str(math.floor((30 - (self.seconds % 40))/2)), 7)
                    if self.mars.level >= 6:
                        pyxel.text(SCREEN_WIDTH-68, 16, "Attack Count : "+str(self.d.atkcount), 7)
                    if self.mars.level >= 10:
                        pyxel.text(SCREEN_WIDTH-80, 9, "Droplet's HP : "+str(self.droplethp), 8)
                    
                if self.i.level < self.i.maxlevel and pyxel.mouse_x - 20 < self.i.x < pyxel.mouse_x + 20 and pyxel.mouse_y - 20 < self.i.y < pyxel.mouse_y + 20:
                    if self.Enchant == True and self.mobility == []:
                        pyxel.circb(self.i.x, self.i.y, self.i.level +1, 10)
                        if self.seconds % 2 == 1:
                            pyxel.text(3, 9, "Click to Enchant (-5000)", 7)
                        else:
                            pyxel.text(3, 9, "Click to Enchant (-5000)", 10)
                    else:
                        pyxel.circb(self.i.x, self.i.y, self.i.level +1, 13)
                for self.m in self.mobility:
                    if self.i.Collided == True:
                        pyxel.circb(self.i.x, self.i.y, self.i.maxlevel + 1, 7 + 5*(pyxel.frame_count % 2))

        for self.d in self.droplet:
            if self.d.y >= (self.d.starty + SCREEN_HEIGHT/3) or self.d.Warped == True:
                pyxel.circb(self.d.x, self.d.y, 1 + int(pyxel.frame_count % 2), 13)
            for self.r in self.radar:
                pyxel.circb(self.earth.x, self.earth.y, self.earth.level+(self.seconds % (self.earth.level)), 11)
                if self.genlevel >= 3:
                    pyxel.circb(self.mars.x, self.mars.y, self.mars.level+(self.seconds % (self.earth.level)), 11)
                if self.genlevel >= 5:
                    pyxel.circb(self.ceres.x, self.ceres.y, self.ceres.level+(self.seconds % (self.earth.level)), 11)
                if self.d.Visible >= 1:
                    if self.d.Attack == True:
                        if self.d.y < (self.d.starty + SCREEN_HEIGHT/2) and (self.d.Warped == False and self.d.atkcount >= 2):
                            pyxel.circb(self.r.detectedx + self.r.x_deviation * (1.2-(self.earth.level/self.earth.maxlevel)), self.r.detectedy + self.r.y_deviation * (1.2-(self.earth.level/self.earth.maxlevel)), 28 * (1.4-(self.earth.level/self.earth.maxlevel)) + (self.seconds % 3), 14)
                        if self.d.y > (self.d.starty + SCREEN_HEIGHT/2) or self.d.Warped == True or self.d.atkcount == 1:
                            pyxel.circb(self.r.detectedx + 6*math.cos(self.d.aim), self.r.detectedy - 6*math.sin(self.d.aim), 18 + (self.seconds % 3), 14)
                    if self.d.Attack == False:
                        pyxel.circb(self.r.detectedx + self.r.x_deviation, self.r.detectedy + self.r.y_deviation, 28 * (1.6-(self.earth.level/self.earth.maxlevel)) + (self.seconds % 3), 7)
                    if self.genlevel >= 3:
                        for self.c in self.calculation:
                            pyxel.rect(self.d.atkx-30*(1.6-(self.mars.level/self.mars.maxlevel))+self.c.deviation*(1.6-(self.mars.level/self.mars.maxlevel)), SCREEN_HEIGHT - 23, 60*(1.6-(self.mars.level/self.mars.maxlevel)), 3, 10)
                if self.d.Visible == 2 and pyxel.frame_count % 2 == 1:
                    pyxel.circb(self.d.x + pyxel.rndi(-8, 8), self.d.y + pyxel.rndi(-6, 6), 3 + int(pyxel.frame_count % 3), 7)
                    pyxel.circb(self.d.x + pyxel.rndi(-8, 8), self.d.y + pyxel.rndi(-6, 6), 1 + int((pyxel.frame_count+1) % 3), 12)

        for self.m in self.mobility:
            pyxel.circb(self.venus.x, self.venus.y, self.venus.level + (self.seconds % self.venus.level), 2)
        
        if self.genlevel >= 4:
            pyxel.circ(self.mercury.x, self.mercury.y, self.mercury.level-2, 5)
            pyxel.circb(self.mercury.x, self.mercury.y, self.mercury.level, 5)
            pyxel.circb(pyxel.mouse_x, pyxel.mouse_y, (15*(1.1-self.mercury.level/self.mercury.maxlevel)), 7)
            pyxel.circb(pyxel.mouse_x, pyxel.mouse_y, (12*(1.1-self.mercury.level/self.mercury.maxlevel)), 7)
            pyxel.line(pyxel.mouse_x+3, pyxel.mouse_y,pyxel.mouse_x-3, pyxel.mouse_y, 7)
            pyxel.line(pyxel.mouse_x, pyxel.mouse_y+3,pyxel.mouse_x, pyxel.mouse_y-3, 7)
            if self.seconds % 2 == 1 and self.genpoints >= 1200:
                pyxel.circb(pyxel.mouse_x, pyxel.mouse_y, (15*(1.1-self.mercury.level/self.mercury.maxlevel)), 8)
                pyxel.circb(pyxel.mouse_x, pyxel.mouse_y, (12*(1.1-self.mercury.level/self.mercury.maxlevel)), 8)
                pyxel.line(pyxel.mouse_x+3, pyxel.mouse_y,pyxel.mouse_x-3, pyxel.mouse_y, 8)
                pyxel.line(pyxel.mouse_x, pyxel.mouse_y+3,pyxel.mouse_x, pyxel.mouse_y-3, 8)
            for self.a in self.arms:
                pyxel.line(self.a.x - 15*math.cos(self.a.aim), self.a.y + 15*math.sin(self.a.aim), self.a.x, self.a.y, 2)
                pyxel.circ(self.a.x, self.a.y, 1.2 + int(pyxel.frame_count % 2), 2)
                if self.seconds >= self.a.start + 1:
                    pyxel.line(self.a.x - 12*math.cos(self.a.aim)+1, self.a.y + 12*math.sin(self.a.aim), self.a.x+1, self.a.y, 7)
                    pyxel.line(self.a.x - 12*math.cos(self.a.aim)-1, self.a.y + 12*math.sin(self.a.aim), self.a.x-1, self.a.y, 7)
                    pyxel.circb(self.a.x, self.a.y, 2.2 + int(pyxel.frame_count % 2), 7)
                    pyxel.circb(self.a.x - 12*math.cos(self.a.aim) + pyxel.rndi(-3, 3), self.a.y + 12*math.sin(self.a.aim) + pyxel.rndi(-3, 3), 0.6 + int(pyxel.frame_count % 2), 2)

        if self.genlevel >= 5:
            for self.e in self.energy:
                pyxel.circb(self.ceres.x, self.ceres.y, self.e.r - 6, 7)
                pyxel.circb(self.ceres.x, self.ceres.y, self.e.r, 3)
                pyxel.circb(self.ceres.x, self.ceres.y, self.e.r + 6, 7)

        if self.genlevel <= 3:
            pyxel.circb(pyxel.mouse_x, pyxel.mouse_y, 4, 7)
            if self.seconds % 2 == 1:
                pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, 3, self.nearest.color)
            pyxel.line(pyxel.mouse_x+1, pyxel.mouse_y, pyxel.mouse_x-1, pyxel.mouse_y, 7)
            pyxel.line(pyxel.mouse_x, pyxel.mouse_y+1, pyxel.mouse_x, pyxel.mouse_y-1, 7)
                

        if self.Evolution == True:
            if self.seconds % 2 == 1:
                pyxel.text(3, 2, "Press SPACE for Evolution (-10000)", 7)
            else:
                pyxel.text(3, 2, "Press SPACE for Evolution (-10000)", 10)
        pyxel.rect(0, SCREEN_HEIGHT-20, SCREEN_WIDTH*(self.genpoints/100000), 10, 11)
        pyxel.text(6, SCREEN_HEIGHT-17, "GP:" + str(self.genpoints), 7)
        pyxel.rect(0, SCREEN_HEIGHT-10, SCREEN_WIDTH*(self.hp/10000), 10, 8)
        pyxel.text(6, SCREEN_HEIGHT-7, "HP:" + str(self.hp), 7)

        if self.Dead == True:
            pyxel.text(70, 40, "Your Spaceships were Destroyed", 8)
            pyxel.text(79, 48, "You can no longer gain GP", 8)
            pyxel.text(6, SCREEN_HEIGHT-30, "Press R to Restart", 7 + (self.seconds % 2))
        if self.Clear == True:
            pyxel.text(68, 56, "You defeated the Hostile Planet !", 4*int((pyxel.frame_count % 16)/4))
            pyxel.text(6, SCREEN_HEIGHT-30, "Press R to Restart", 7 + 3*(self.seconds % 2))
            if self.Dead == True:
                pyxel.text(51, 56, "But,", 4*int((pyxel.frame_count % 16)/4))
App()