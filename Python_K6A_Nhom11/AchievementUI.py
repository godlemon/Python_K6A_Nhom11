import pygame
import sys
import pandas as pd


class Scoreboard:
    def __init__(self, width=800, height=600):
        pygame.init()

        # Kích thước cửa sổ
        self.width = width
        self.height = height

        # Màu sắc
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Tạo cửa sổ
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Thành tựu")

        # tài nguyên
        self.background = pygame.image.load('Resources/Image/achivement.jpg').convert_alpha()
        self.x = (width - self.background.get_width()) // 2
        self.y = (height - self.background.get_height()) // 2
        self.font = pygame.font.SysFont("timesnewroman", 36)
        self.font2 = pygame.font.Font("Resources\Font\dlxfont.ttf", 36)

    def draw_scoreboard(self, scores):
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.background, (self.x, self.y))
        title_text = self.font2.render("Hight Score", True, self.BLACK)
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 20))

        y_position = 70
        for index, (player, score) in enumerate(scores.iterrows(), start=1):
            player_text = self.font2.render(str(player), True, self.BLACK)
            score_text = self.font2.render(str(int(score['HighScore'])), True, self.BLACK)

            self.screen.blit(player_text, (20, y_position))
            self.screen.blit(score_text, (self.width - 420, y_position))

            y_position += 40

    def main(self):
        try:
            scores = pd.read_csv('HightScore.txt', header=None, names=['HighScore'])
        except FileNotFoundError:
            scores = pd.DataFrame(columns=['HighScore'])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw_scoreboard(scores)
            pygame.display.flip()



