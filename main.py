import pygame

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)


# Объект Стены
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pass


# Функция отрисовки карты
def Map(all_sprites_list):
    pass


# Объект Игрока
class Player(pygame.sprite.Sprite):
    pass


# Класс противника
class npc(Player):
    pass


pygame.init()
screen = pygame.display.set_mode([606, 606])
pygame.display.set_caption('Pacman')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)
clock = pygame.time.Clock()


# Функция запсука игры
def startGame():
    main()


# Основной цикл игры
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    pass
        pygame.display.flip()

        clock.tick(10)


if __name__ == '__main__':
    startGame()
    pygame.quit()
