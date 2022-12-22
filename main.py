import pygame
import os
import sys

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)
pygame.init()
size = width, height = 600, 330
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player = None
player_group = pygame.sprite.Group()
fps = 10
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
background = pygame.Surface(screen.get_size())
background = background.convert()
screen = pygame.display.set_mode(size)


# Объект Стены
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pass

    def pos(self):
        pass


# Функция отрисовки карты
def Map(all_sprites_list):
    def __init__(self):
        pass

    def loadmap(self):
        pass

    def changemap(self):
        pass


# Объект Игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def move(self):
        pass

    def point(self):
        pass


# Класс противника
class npc(Player):
    def __init__(self):
        pass

    def move(self):
        pass

    def kill(self):
        pass


# Функция запуска игры
# def startGame():
#     main()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = "PACMAN"
    fon = pygame.transform.scale(load_image('start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    text_coord = 50
    string_rendered = font.render(intro_text, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    # text_coord += 40
    intro_rect.top = text_coord
    intro_rect.x = 180
    # text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                Tile('wall_0', x, y)
            elif level[y][x] == '1':
                Tile('wall_1', x, y)
            elif level[y][x] == '2':
                Tile('wall_2', x, y)
            elif level[y][x] == '3':
                Tile('wall_3', x, y)
            elif level[y][x] == '4':
                Tile('wall_4', x, y)
            elif level[y][x] == '5':
                Tile('wall_5', x, y)
            elif level[y][x] == '6':
                Tile('wall_6', x, y)
            elif level[y][x] == '7':
                Tile('wall_7', x, y)
            elif level[y][x] == '.':
                Tile('point', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = AnimatedSprite(load_image("pacman.png"), 3, 1, x, y)
    return new_player, x, y


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


tile_images = {
    'wall_0': load_image('0.png'),
    'wall_1': load_image('1.png'),
    'wall_2': load_image('2.png'),
    'wall_3': load_image('3.png'),
    'wall_4': load_image('4.png'),
    'wall_5': load_image('5.png'),
    'wall_6': load_image('6.png'),
    'wall_7': load_image('7.png'),
    'point': load_image('8.png'),
    'empty': load_image('9.png')
}
tile_width = tile_height = 30
start_screen()

while True:
    background.fill(black)
    clock.tick(fps)
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_RETURN:
                pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            background.fill(black)
            player, level_x, level_y = generate_level(load_level('map.txt'))
    all_sprites.update()
    pygame.display.flip()



