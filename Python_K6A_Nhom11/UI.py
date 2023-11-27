import pygame
import sys

class UI:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Mở rộng lãnh địa')
        self.clock = pygame.time.Clock()
        #khởi tạo nút
        self.button_start = pygame.Rect(300, 350, 300, 50)
        self.button_achievement = pygame.Rect(300, 420, 300, 50)
        self.button_exit = pygame.Rect(300, 490, 300, 50)
        #tài nguyên
        self.font = pygame.font.SysFont("timesnewroman", 36)
        self.background = pygame.image.load('Resources/Image/background.jpg').convert_alpha()
        self.button = pygame.image.load('Resources/Image/green_button.png').convert_alpha()

    def draw_text(self, text, x, y):
        surface = self.font.render(text, True, (0, 0, 0))
        rect = surface.get_rect()
        rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def draw_buttons(self):
        self.screen.blit(self.button, self.button_start)
        self.screen.blit(self.button, self.button_achievement)
        self.screen.blit(self.button, self.button_exit)
        # pygame.draw.rect(self.screen, (0, 255, 0), self.button_start)
        # pygame.draw.rect(self.screen, (0, 255, 0), self.button_achievement)
        # pygame.draw.rect(self.screen, (0, 255, 0), self.button_exit)
        self.draw_text('Chơi', self.button_start.x + 60, self.button_start.y)
        self.draw_text('Thành tích', self.button_achievement.x + 20, self.button_achievement.y)
        self.draw_text('Thoát', self.button_exit.x + 50, self.button_exit.y)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.button_start.collidepoint(event.pos):
                            return "run"
                        elif self.button_achievement.collidepoint(event.pos):
                            return "achievement"
                        elif self.button_exit.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0,0))
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(30)


