import pygame,math,time,random

class EatEatGame:
    def __init__(self):
# initializing
        pygame.init()
        pygame.mixer.pre_init()
        self.set_title_icon_screen()
        self.clock = pygame.time.Clock()
# variable definition
        self.norImg , self.ultiImg = "assets/mt.jpg" , "assets/ulti.jpg"
        self.tsound1, self.tsound2 = "sound/touchSound1.wav", "sound/touchSound2.wav"
        self.black,  self.white,    self.yellow,  self.red, self.blue, self.green,  self.gray = \
         (0, 0, 0),(255, 255, 255), (128,128,0), (255,0,0), (0,0,128),  (0,128,0), (128,128,128)
        self.FPS, self.speed  = 120, 15
        self.distance = 80
        self.win_point_init, self.win_point = 11,11
        self.cha_size, self.ball_size = (100, 100), (50, 50)
        self.touch1, self.touch2 = 0, 0
        self.playerX1_change, self.playerY1_change, self.playerX2_change, self.playerY2_change = 0, 0, 0, 0
    # coordinate spawning randomly
        self.ballX, self.ballY = random.randint(0, 560), random.randint(80, 760)
        self.playerX1, self.playerY1 = random.randint(0, 600), random.randint(0, 800)
        self.playerX2, self.playerY2 = random.randint(0, 600), random.randint(0, 800)
# sounds setting
        self.bkgdSound = pygame.mixer.Sound("sound/bkgdSound2.wav")
        self.touchSound = pygame.mixer.Sound(self.tsound1)
        self.spaceSound = pygame.mixer.Sound("sound/spaceSound.wav")
        self.endSound = pygame.mixer.Sound("sound/endSound.wav")
# assets setting
        self.font = pygame.font.Font("assets/Olympus Mount.ttf", 50)
        self.bkgd = (pygame.transform.scale(pygame.image.load(self.norImg), (600, 800))).convert()
        self.start_screen = (pygame.transform.scale(pygame.image.load("assets/startingImg1.jfif"), (600, 800))).convert() # 4x5
        self.end_screen = (pygame.transform.scale(pygame.image.load("assets/game_over.png"), (400, 300))).convert()
        self.character1 = (pygame.transform.scale(pygame.image.load("assets/man_1.png"), self.cha_size)).convert()
        self.character2 = (pygame.transform.scale(pygame.image.load("assets/man_2.png"), self.cha_size)).convert()
        self.ball = (pygame.transform.scale(pygame.image.load("assets/ball.png"), self.ball_size)).convert()
# running logic part
        self.run, self.game_start, self.game_active = True, True, False

        '''-----------------------SUBROUTINE------------------------'''

    def set_title_icon_screen(self,titleName = "The Eat Eat Game By Tim",iconImg = "assets/ghost.png" ,screenSize = (600,800)):
        pygame.display.set_caption(titleName)
        pygame.display.set_icon(pygame.image.load(iconImg))
        self.screen = pygame.display.set_mode(screenSize)

    def show_start_screen(self):
        self.screen.blit(self.start_screen, (0,0))
        self.show_text(10, 30, "WELCOME TO EATEATGAME !!", self.white)
        self.show_text(10, 100, "PLAYER 1 : UP DOWN LEFT RIGHT ", self.green)
        self.show_text(10, 170, "PLAYER 2 : W S A D", self.green)
        self.show_text(10, 240, "PRESS R TO RESTART", self.green)
        self.show_text(10, 310, "PRESS ESC TO QUIT", self.green)
        self.show_text(20, 600, "PRESS SPACE TO GET STARTED", self.gray)
        self.show_text(100, 750,"JUL 2021 DESIGNED BY TIM", self.yellow)

    def show_end_screen(self):
        self.screen.fill(self.black)
        self.screen.blit(self.end_screen,(100,250))
        self.show_text(50, 600, "PRESS SPACE TO CONTINUE", self.gray)
        self.show_text(100, 750, "JUL 2021 DESIGNED BY TIM", self.yellow)
        self.show_text(200, 200, "P1    "+str(self.touch1)+"-"+str(self.touch2)+"   P2", self.red)
        if self.touch1 == self.win_point:
            self.show_text(30,10, "PLAYER 1 WINS !!", self.white)
            self.show_text(30,80, "GAME_TIME : "+ str(round(self.time_cost,5)), self.white)
        if self.touch2 == self.win_point:
            self.show_text(30,10, "PLAYER 2 WINS !!", self.white)
            self.show_text(30,80, "GAME TIME : "+ str(round(self.time_cost,5)), self.white)
# show the images on the screen
    def show_bkgd(self):                     self.screen.blit(self.bkgd, (0, 0))
    def show_player(self,x, y,character):    self.screen.blit(character, (x, y))
    def show_ball(self,x, y):                self.screen.blit(self.ball, (x, y))
    def show_text(self,textX,textY,string,color):
        text = self.font.render(string ,True, color)
        self.screen.blit(text, (textX, textY))
    def show_touchSound(self):
        if self.isTouch(self.center_of_cha1,self.center_of_ball) is True or self.isTouch(self.center_of_cha2,self.center_of_ball) is True:
            self.touchSound.play()

    def move(self):
        self.playerX1 += self.playerX1_change
        self.playerY1 += self.playerY1_change
        self.playerX2 += self.playerX2_change
        self.playerY2 += self.playerY2_change

    def find_center(self):
        self.center_of_cha1 = (self.playerX1 + self.cha_size[0] / 2, self.playerY1 + self.cha_size[1] / 2)
        self.center_of_cha2 = (self.playerX2 + self.cha_size[0] / 2, self.playerY2 + self.cha_size[1] / 2)
        self.center_of_ball =   (self.ballX + self.ball_size[0] / 2,   self.ballY + self.ball_size[1] / 2)

    def distanceMeasuring(self,cen1,cen2):
        x, y = cen1[0] - cen2[0], cen1[1] - cen2[1]
        return math.hypot(x, y)

    def isTouch(self,cen1, cen2):
        x, y = cen1[0] - cen2[0], cen1[1] - cen2[1]
        distance = math.hypot(x, y)
        if distance < self.distance:
            return True
        return False

    def ifTouch(self, touch):
        touch += 1
        #print(f" touch1 = {touch}")
        self.ballX, self.ballY = random.randint(0, 560), random.randint(80, 760)
        self.show_ball(self.ballX, self.ballY)
        return touch

    def ifSpace(self):
        self.time_start = time.time()
        self.game_active, self.game_start = True, False
        self.win_point = self.win_point_init
        self.bkgd = (pygame.transform.scale(pygame.image.load(self.norImg), (600, 800))).convert()
        self.ball = (pygame.transform.scale(pygame.image.load("assets/ball.png"), self.ball_size)).convert()
        self.bkgdSound.stop()
        self.endSound.stop()
        self.spaceSound.play()
        self.touch1, self.touch2 = 0, 0
        self.speed = 15

    def ifDeuce(self):
        if self.touch1 == (self.win_point -1) and self.touch2 == (self.win_point -1):
            self.win_point += 1
            self.touchSound = pygame.mixer.Sound(self.tsound2)
            self.bkgd = (pygame.transform.scale(pygame.image.load(self.ultiImg), (600, 800))).convert()
            self.ball = (pygame.transform.scale(pygame.image.load("assets/ghost.png"), self.ball_size)).convert()
            self.bkgdSound.play()
            self.speed = 60
        if self.touch1 == self.touch2 and \
           self.touch1 ==  (self.win_point-2) and \
           self.touch1 != (self.win_point_init-2):  self.show_text(10,150, "DEUCE", self.blue)


    def isEnd(self):
        self.time_end = time.time()
        self.time_cost = self.time_end - self.time_start
        self.show_end_screen()
        self.bkgdSound.stop()
        self.endSound.play()
        self.game_active = False

    def boundary(self,up,down,left,right):
# player 1
        if self.playerX1 <= left:   self.playerX1 = left
        if self.playerX1 >= right:  self.playerX1 = right
        if self.playerY1 <= up:     self.playerY1 = up
        if self.playerY1 >= down:   self.playerY1 = down
# player 2
        if self.playerX2 <= left:   self.playerX2 = left
        if self.playerX2 >= right:  self.playerX2 = right
        if self.playerY2 <= up:     self.playerY2 = up
        if self.playerY2 >= down:   self.playerY2 = down

    def event_get(self):
        for event in pygame.event.get():
# click X
            if event.type == pygame.QUIT:      self.run = False
# press key
            if event.type == pygame.KEYDOWN:
    # player 1
                if event.key == pygame.K_UP:   self.playerY1_change = -self.speed
                if event.key == pygame.K_DOWN: self.playerY1_change = self.speed
                if event.key == pygame.K_LEFT: self.playerX1_change = -self.speed
                if event.key == pygame.K_RIGHT:self.playerX1_change = self.speed

    # player 2
                if event.key == pygame.K_w:    self.playerY2_change = -self.speed
                if event.key == pygame.K_s:    self.playerY2_change = self.speed
                if event.key == pygame.K_a:    self.playerX2_change = -self.speed
                if event.key == pygame.K_d:    self.playerX2_change = self.speed

    # Space & ESC & Restart
                if event.key == pygame.K_ESCAPE: self.run = False
                if event.key == pygame.K_r:      self.game_active, self.game_start = False, True
                if event.key == pygame.K_SPACE :
                    if self.game_start == True or self.game_active == False:
                        self.ifSpace()

# release key
            if event.type == pygame.KEYUP:
    # player 1
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:      self.playerY1_change = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:   self.playerX1_change = 0
    # player 2
                if event.key == pygame.K_w or event.key == pygame.K_s:          self.playerY2_change = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:          self.playerX2_change = 0

    def touchStatement(self):
# player 1 Statement
        if self.isTouch(self.center_of_cha1, self.center_of_ball) is False and self.game_active is True:
            self.show_ball(self.ballX, self.ballY)
        if self.isTouch(self.center_of_cha1, self.center_of_ball) is True:
            self.touch1 = self.ifTouch(self.touch1)
            if self.touch1 == self.win_point: self.isEnd()
# player 2 Statement
        if self.isTouch(self.center_of_cha2, self.center_of_ball) is False and self.game_active is True:
            self.show_ball(self.ballX, self.ballY)
        if self.isTouch(self.center_of_cha2, self.center_of_ball) is True:
            self.touch2 = self.ifTouch(self.touch2)
            if self.touch2 == self.win_point: self.isEnd()
# game point display
        if self.touch1 == (self.win_point -1) or self.touch2 == (self.win_point -1):
            self.show_text(10,150,"GAME POINT", self.red)
# deuce judgement & display
        self.ifDeuce()

    '''-----------------------MAIN FUNC'------------------------'''

    def main(self):
        while self.run:
            self.clock.tick(self.FPS)
            self.event_get()
            if self.game_start:  self.show_start_screen()
            if self.game_active:
                self.show_bkgd()
                self.show_player(self.playerX1, self.playerY1,self.character1)             # player 1
                self.show_player(self.playerX2, self.playerY2,self.character2)             # player 2
                self.show_text(10, 10, "SCORE PLAYER 1 : " + str(self.touch1), self.black)  # score player 1
                self.show_text(10, 80, "SCORE PLAYER 2 : " + str(self.touch2), self.black)  # score player 2
                self.boundary(0, 720, 0, 520)
                self.move()
                self.find_center()
                self.show_touchSound()
                self.touchStatement()
            pygame.display.update()

    '''---------------------------------------------------------'''

if __name__ == '__main__' : EatEatGame().main()

