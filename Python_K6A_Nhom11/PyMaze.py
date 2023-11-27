import sys
import psutil
import pygame
from pygame.locals import *
from maze import Maze
from tkinter import messagebox
import pandas as pd
import subprocess


class Game:

    def __init__(self, diff, dim, path):
        self.ControWD = 200
        self.width = 800 + self.ControWD
        self.height = 600
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Mê cung vô tận')
        # Màu sắc
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        font = pygame.font.SysFont(pygame.font.get_default_font(), 55)
        text = font.render("Loading...", 1, (255, 255, 255))
        rect = text.get_rect()
        rect.center = self.size[0] / 2, self.size[1] / 2
        self.screen.blit(text, rect)
        pygame.display.update(rect)
        self.diff = diff
        self.dim = map(int, dim.split('x'))
        self.path = path
        self.button_reset = pygame.Rect(self.size[0] - self.ControWD + 5, 20, 100, 50)
        self.pointKeep = pygame.Rect(self.size[0] - self.ControWD + 5, 80, 100, 50)
        self.AchivementKeep = pygame.Rect(self.size[0] - self.ControWD + 5, 150, 100, 50)
        self.point = 1000
        # tài nguyên
        #font
        self.font = pygame.font.SysFont("timesnewroman", 36)
        #âm thanh
        self.MoveNoise = pygame.mixer.Sound('Resources/Music/MoveNoise.ogg')
        self.BackgroundMusic = pygame.mixer.Sound('Resources/Music/backgroundmusic.mp3')
        self.victoryMusic = pygame.mixer.Sound('Resources/Music/victory.wav')

        #ảnh
        self.button = pygame.image.load('Resources/Image/green_button.png').convert_alpha()
        self.panel = pygame.transform.scale(pygame.image.load('Resources/Image/blue_panel.png').convert_alpha(), (190, 450))
        #file
        self.d = pd.read_csv('HightScore.txt', header=None, names=['HighScore'])
    def draw_text(self, text, x, y):
        surface = self.font.render(text, True, (0, 0, 0))
        rect = surface.get_rect()
        rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def reset_player(self):
        w, h = self.cell_width - 3, self.cell_height - 3
        rect = 0, 0, w, h
        base = pygame.Surface((w, h))
        base.fill((255, 255, 255))
        self.red_p = base.copy()
        self.green_p = base.copy()
        self.blue_p = base.copy()
        self.goldy = base.copy()
        if self.path == 1:
            r = (255, 0, 0)
            g = (0, 255, 0)
        else:
            r = g = (255, 255, 255)
        b = (0, 0, 255)
        gold = (0xc5, 0x93, 0x48)
        pygame.draw.ellipse(self.red_p, r, rect)
        pygame.draw.ellipse(self.green_p, g, rect)
        pygame.draw.ellipse(self.blue_p, b, rect)
        pygame.draw.ellipse(self.goldy, gold, rect)

        self.player_maze = {}
        for y in range(self.maze_obj.rows):
            for x in range(self.maze_obj.cols):
                cell = {'visited': 0}  # if 1, draws green. if >= 2, draws red.
                self.player_maze[(x, y)] = cell
                self.screen.blit(base, (x * self.cell_width + 2, y * self.cell_height + 2))

        self.screen.blit(self.goldy, (x * self.cell_width + 2, y * self.cell_height + 2))
        self.cx = self.cy = 0
        self.curr_cell = self.player_maze[(self.cx, self.cy)]  # starts at origin
        self.point = 1000
        self.last_move = None  # For last move fun

    def controRight(self):
        #Nút thử lại
        self.screen.blit(self.button, self.button_reset)
        self.draw_text('Thử lại', self.button_reset.x + 30, self.button_reset.y)
        pygame.display.update(self.button_reset)
        # Điểm số
        self.screen.blit(self.button, self.pointKeep)
        self.draw_text(f'Điểm: {self.point}', self.pointKeep.x + 10, self.pointKeep.y)
        pygame.display.update(self.pointKeep)
        # Thành tựu
        self.screen.blit(self.panel, self.AchivementKeep)
        self.draw_text("điểm cao", self.AchivementKeep.x + 40, self.AchivementKeep.y + 20)
        leng = 20
        for index, (player, score) in enumerate(self.d.iterrows(), start=1):
            leng +=30
            score_text = str(int(score['HighScore']))
            self.draw_text(f"{score_text}", self.AchivementKeep.x + 80, self.AchivementKeep.y + leng)
        pygame.display.update(self.AchivementKeep)


    def draw_maze(self):
        self.screen.fill((255, 255, 255))
        self.cell_width = (self.size[0] - self.ControWD) / self.maze_obj.cols
        self.cell_height = self.size[1] / self.maze_obj.rows

        for y in range(self.maze_obj.rows):
            for x in range(self.maze_obj.cols):
                if self.maze_obj.maze[(x, y)]['south']:  # draw south wall
                    pygame.draw.line(self.screen, (0, 0, 0), \
                                     (x * self.cell_width, y * self.cell_height + self.cell_height), \
                                     (x * self.cell_width + self.cell_width, \
                                      y * self.cell_height + self.cell_height))
                if self.maze_obj.maze[(x, y)]['east']:  # draw east wall
                    pygame.draw.line(self.screen, (0, 0, 0), \
                                     (x * self.cell_width + self.cell_width, y * self.cell_height), \
                                     (x * self.cell_width + self.cell_width, y * self.cell_height + \
                                      self.cell_height))
        # viền
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.size[0], self.size[1]), 1)
        pygame.display.update()

    def start(self):
        self.maze_obj = Maze(*self.dim)
        if self.diff == 0:
            self.maze_obj.generate(self.maze_obj.maze[(0, 0)])
        else:
            self.maze_obj.generate()
        self.draw_maze()
        self.reset_player()
        self.BackgroundMusic.play()

        self.loop()

    def loop(self):
        self.clock = pygame.time.Clock()
        self.keep_going = 1

        while self.keep_going:
            moved = 0
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.BackgroundMusic.stop()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.button_reset.collidepoint(event.pos):
                            self.reset_player()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.BackgroundMusic.stop()
                        self.keep_going = 0
                    if event.key == K_r:
                        self.reset_player()
                    if event.key == K_DOWN:
                        self.move_player('d')
                        moved = 1
                    if event.key == K_UP:
                        self.move_player('u')
                        moved = 1
                    if event.key == K_LEFT:
                        self.move_player('l')
                        moved = 1
                    if event.key == K_RIGHT:
                        self.move_player('r')
                        moved = 1
            keys = pygame.key.get_pressed()
            if not moved:
                if keys[K_DOWN]:
                    self.move_player('d')
                if keys[K_UP]:
                    self.move_player('u')
                if keys[K_LEFT]:
                    self.move_player('l')
                if keys[K_RIGHT]:
                    self.move_player('r')
            self.controRight()
            self.draw_player()
            pygame.display.update()

    def move_player(self, dir):
        no_move = 0
        try:
            if dir == 'u':
                if not self.maze_obj.maze[(self.cx, self.cy - 1)]['south']:
                    self.cy -= 1
                    self.curr_cell['visited'] += 1
                    self.point -= 1
                    self.MoveNoise.play()
                else:
                    no_move = 1
            elif dir == 'd':
                if not self.maze_obj.maze[(self.cx, self.cy)]['south']:
                    self.cy += 1
                    self.curr_cell['visited'] += 1
                    self.point -= 1
                    self.MoveNoise.play()
                else:
                    no_move = 1
            elif dir == 'l':
                if not self.maze_obj.maze[(self.cx - 1, self.cy)]['east']:
                    self.cx -= 1
                    self.curr_cell['visited'] += 1
                    self.point -= 1
                    self.MoveNoise.play()
                else:
                    no_move = 1
            elif dir == 'r':
                if not self.maze_obj.maze[(self.cx, self.cy)]['east']:
                    self.cx += 1
                    self.curr_cell['visited'] += 1
                    self.point -= 1
                    self.MoveNoise.play()
                else:
                    no_move = 1
            else:
                no_move = 1
        except KeyError:  # Tried to move outside screen
            no_move = 1

        # Handle last move...
        if ((dir == 'u' and self.last_move == 'd') or \
            (dir == 'd' and self.last_move == 'u') or \
            (dir == 'l' and self.last_move == 'r') or \
            (dir == 'r' and self.last_move == 'l')) and \
                not no_move:
            self.curr_cell['visited'] += 1

        if not no_move:
            self.last_move = dir
            self.curr_cell = self.player_maze[(self.cx, self.cy)]

        # Check for victory.
        if self.cx + 1 == self.maze_obj.cols and self.cy + 1 == self.maze_obj.rows:
            self.BackgroundMusic.stop()
            self.victoryMusic.play()
            d = self.d._append({'HighScore': self.point}, ignore_index=True)
            d = d.sort_values(by='HighScore', ascending=False)
            d = d.head(10)
            with open('HightScore.txt', 'w') as file:
                d.to_csv(file, index=False, header=False)

            if messagebox.askquestion("Chiến thắng", f"Bạn đã thắng điểm của bạn là {self.point}, chơi tiếp?", ) == "yes":
                self.reset_player()
            else:
                self.keep_going = 0


    def draw_player(self):
        for y in range(self.maze_obj.rows):
            for x in range(self.maze_obj.cols):
                if self.player_maze[(x, y)]['visited'] > 0:
                    if self.player_maze[(x, y)]['visited'] == 1:
                        circ = self.green_p
                    else:
                        circ = self.red_p
                    #vẽ đường đi
                    self.screen.blit(circ, (x * self.cell_width + 2, y * self.cell_height + 2))
        self.screen.blit(self.blue_p, (self.cx * self.cell_width + 2, \
                                       self.cy * self.cell_height + 2))

# if __name__ == '__main__':
#   pygame.init()
#   args = argv[1:]
#   diff = 0
#   dim = '30x40'
#   path = 1
#   for arg in args:
#     if '--diff' in arg:
#       diff = int(arg.split('=')[-1])
#     elif '--dim' in arg:
#       dim = arg.split('=')[-1]
#     elif '--path' in arg:
#       path = int(arg.split('=')[-1])
#
#   g = Game(diff, dim, path)
#   g.start()
