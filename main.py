import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

# constants definition

ORIGIN = (0, 0)

COLOR_BLACK = (0, 0, 0)
COLOR_BROWN = (160, 82, 45)
COLOR_CYAN = (0, 255, 255)
COLOR_DARK_CYAN = (0, 128, 128)
COLOR_GRAY = (128, 128, 128)
COLOR_GREEN = (0, 255, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)

SCREEN_SIZE = (1024,768)
SCREEN_DEPTH = 32
SCREEN_FLAGS = 0

BACKGROUND_COLOR = COLOR_CYAN
WARNING_COLOR = COLOR_DARK_CYAN
ENDGAME_COLOR = COLOR_BLACK

TABLE_SIZE = (SCREEN_SIZE[0], SCREEN_SIZE[1] * 3 / 4)
TABLE_COLOR = COLOR_BROWN

TABLECLOTH_SIZE = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] * 3/ 4)
TABLECLOTH_COLOR_IDLE = COLOR_RED
TABLECLOTH_COLOR_BUSY = COLOR_GREEN

HAND_SIZE = (SCREEN_SIZE[1] / 8, SCREEN_SIZE[1] / 8)
HAND_COLOR_IDLE = COLOR_GRAY
HAND_COLOR_BUSY = COLOR_WHITE

MOTHER_SIZE = (SCREEN_SIZE[0] / 4, SCREEN_SIZE[1] / 3)
MOTHER_COLOR_IDLE = COLOR_YELLOW
MOTHER_COLOR_BUSY = COLOR_ORANGE

LEFT_BUTTON = 1

# class and variable definitions

class Entity(object):
    IDLE, BUSY = range(2)

    def __init__ (self, size, color):
        self.surf = pygame.Surface(size, depth = SCREEN_DEPTH)
        self.rect = pygame.Rect(ORIGIN, size)
        self.surf.fill(color)
        self.state = Entity.IDLE

class Item(Entity):
    
    def __init__ (self, size, color, initial_position):
        Entity.__init__(self, size, color)

        self.initial_position = initial_position
        self.rect.center = initial_position

    def update(self):
        if self.state == Entity.BUSY:
            if self.rect.centerx >= self.initial_position[0] - SCREEN_SIZE[0] / 2:
                self.rect.centerx -= 50
            else:
                self.state == Entity.IDLE

            if self.rect.right < SCREEN_SIZE[0] / 2:
                self.surf.fill(COLOR_GRAY)

screen = pygame.display.set_mode(SCREEN_SIZE,SCREEN_FLAGS,SCREEN_DEPTH)

clock = pygame.time.Clock()


class Game():
    ON, OVER, WIN = range(3)

# initial settings
    
    def start(self):
        self.state = Game.ON
        
        self.Background = Entity(SCREEN_SIZE, BACKGROUND_COLOR)

        self.Mother = Entity(MOTHER_SIZE, MOTHER_COLOR_IDLE)
        self.Mother.rect.left = SCREEN_SIZE[0] * 1 / 4

        self.Table = Entity(TABLE_SIZE, TABLE_COLOR)
        self.Table.rect.top = SCREEN_SIZE[1] / 3

        self.Tablecloth = Entity(TABLECLOTH_SIZE, TABLECLOTH_COLOR_IDLE)
        self.Tablecloth.rect.top = SCREEN_SIZE[1] / 3

        self.Left_hand = Entity(HAND_SIZE, HAND_COLOR_IDLE)
        self.Left_hand.rect.top = SCREEN_SIZE[1] * 7 / 8
        self.Left_hand.rect.left = SCREEN_SIZE[0] * 2 / 8

        self.Right_hand = Entity(HAND_SIZE, HAND_COLOR_IDLE)

        self.stuff = []
        
        for index in range(5):
            new_item = Item(HAND_SIZE, ENDGAME_COLOR, ((randint(0, 2) + 5) * SCREEN_SIZE[0] / 8, (randint(0, 2) * 3 + 8) * SCREEN_SIZE[1] / 16))

            for tries in range (200):
                for test in self.stuff:
                    if test.rect.colliderect(new_item.rect):
                        new_item.rect.center = ((randint(0, 2) + 5) * SCREEN_SIZE[0] / 8, (randint(0, 2) * 3 + 8) * SCREEN_SIZE[1] / 16)

            self.stuff.append(new_item)

        self.Hand_set = 0
        self.Timer = 0
        self.Reset = 0
        self.Count = 0
        self.Mother_turn_time = randint(2, 3) * 60

# loop

        while True:
            if self.state == Game.ON:
                self.begin()
            elif self.state == Game.OVER:
                self.end()
            elif self.state == Game.WIN:
                self.win()
    
#game start

    def begin(self):

        Count = 0


        if self.Reset:
            self.Mother_turn_time = randint(2, 3) * 60
            self.Reset = 0
        
        if not self.Hand_set:
            self.Left_hand.state = Entity.IDLE
            self.Left_hand.surf.fill(HAND_COLOR_IDLE)
            self.Tablecloth.state = Entity.IDLE
            self.Tablecloth.surf.fill(TABLECLOTH_COLOR_IDLE)
        
# events

        for event in pygame.event.get():

            if event.type == QUIT:
                exit()
        
# left hand action

            if event.type == KEYDOWN:

                if event.key == K_r:
                    self.Hand_set = 1
                
                elif event.key == K_SPACE:
                    if self.Hand_set:
                        self.Left_hand.state = Entity.BUSY
                        self.Left_hand.surf.fill(HAND_COLOR_BUSY)

                        if self.Tablecloth.state == Entity.BUSY:
                            self.Tablecloth.state = Entity.IDLE
                            self.Tablecloth.surf.fill(TABLECLOTH_COLOR_IDLE)

                elif event.key == K_q:
                    if self.Mother.state == Entity.BUSY:
                        self.Mother_turn_time = randint (3, 5) * 60
                        self.Mother.state = Entity.IDLE
                        self.Mother.surf.fill(MOTHER_COLOR_IDLE)
                        self.Timer = 0

            if event.type == KEYUP:

                if event.key == K_r:
                    self.Hand_set = 0
                
                elif event.key == K_SPACE:
                    if self.Hand_set:
                        self.Tablecloth.state = Entity.BUSY
                        self.Tablecloth.surf.fill(TABLECLOTH_COLOR_BUSY)

                    if self.Mother.state == Entity.BUSY:
                        screen.blit(self.Tablecloth.surf, self.Tablecloth.rect)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        self.state = Game.OVER


# right hand action

            if event.type == MOUSEBUTTONDOWN:

                if event.button == LEFT_BUTTON:

                    self.Right_hand.state = Entity.BUSY
                    self.Right_hand.surf.fill(HAND_COLOR_BUSY)

                    for item in self.stuff:
                        if self.Right_hand.rect.colliderect(item.rect):
                            if self.Tablecloth.state == Entity.BUSY:
                                item.state = Entity.BUSY

            if event.type == MOUSEBUTTONUP:

                if event.button == LEFT_BUTTON:
                
                    self.Right_hand.state = Entity.IDLE
                    self.Right_hand.surf.fill(HAND_COLOR_IDLE)

        self.Right_hand.rect.centerx, self.Right_hand.rect.centery = pygame.mouse.get_pos()

# warning

        if self.Timer == self.Mother_turn_time - 30:
            self.Background.surf.fill(WARNING_COLOR)

# when mother turns around

        if self.Timer == self.Mother_turn_time:
            self.Mother.state = Entity.BUSY
            self.Mother.surf.fill(MOTHER_COLOR_BUSY)
            self.Background.surf.fill(BACKGROUND_COLOR)

            self.Timer = 0

            if self.Tablecloth.state == Entity.BUSY:
                screen.blit(self.Mother.surf, self.Mother.rect)

                pygame.display.update()

                pygame.time.wait(1000)
                self.state = Game.OVER

        if self.Timer == 60 and self.Mother.state == Entity.BUSY:
            self.Mother.state = Entity.IDLE
            self.Mother.surf.fill(MOTHER_COLOR_IDLE)
            self.Timer = 0
            self.Mother_turn_time = randint (3, 5) * 60

# screen drawing and next step

        screen.blit(self.Background.surf, self.Background.rect)
        screen.blit(self.Mother.surf, self.Mother.rect)
        screen.blit(self.Table.surf, self.Table.rect)
        screen.blit(self.Tablecloth.surf, self.Tablecloth.rect)

        for item in self.stuff:
            screen.blit(item.surf, item.rect)
            item.update()

        screen.blit(self.Left_hand.surf, self.Left_hand.rect)
        screen.blit(self.Right_hand.surf, self.Right_hand.rect)

        pygame.display.update()

        self.Timer += 1
        clock.tick(60)

        for item in [i for i in self.stuff if i.rect.colliderect(self.Tablecloth.rect)]:
            Count +=1
            if Count == 5:
                screen.blit(item.surf, item.rect)
                pygame.display.update()
                pygame.time.wait(1000)
                self.state = Game.WIN

# endgame definition
        
    def end(self):
        Endgame = Entity(SCREEN_SIZE,ENDGAME_COLOR)
        screen.blit(Endgame.surf, Endgame.rect)
        pygame.display.update()

# endgame controls
        
        for event in pygame.event.get():

            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:

                if event.key == K_r:
                    self.state = Game.ON
                    self.Mother_turn_time = randint (3, 5) * 60
                    self.Timer = 0

# game start mantra

    def win(self):
        Endgame = Entity(SCREEN_SIZE,(255, 255, 255))
        screen.blit(Endgame.surf, Endgame.rect)
        pygame.display.update()

# endgame controls
        
        for event in pygame.event.get():

            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:

                if event.key == K_r:
                    self.state = Game.ON
                    self.Mother_turn_time = randint (3, 5) * 60
                    self.Timer = 0


if __name__ == "__main__":
    game = Game()
    game.start()
