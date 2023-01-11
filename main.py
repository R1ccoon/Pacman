import pygame
import os
import sys
import random

level_id = 0
frames_count = 0
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
point_group = pygame.sprite.Group()
player = None
enemy = None
player_group = pygame.sprite.Group()
fps = 60
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
background = pygame.Surface(screen.get_size())
background = background.convert()
n = []
maplist = []
mapfile = ['map.txt', 'map1.txt']

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


tile_width = tile_height = 30


def final_window():
    screen.fill((0, 0, 0))
    intro_text = "You WIN!!!!"
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
                return main()  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def game_over_window():
    screen.fill((0, 0, 0))
    intro_text = "GAME OVER"
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
                return main()  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


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
                return main()  # начинаем игру
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


class Point(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(point_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, new_enemy, x, y = None, None, None, None
    for y in range(len(level)):
        n = []
        for x in range(len(level[y])):
            if level[y][x] == '0':
                n.append(Tile('wall_0', x, y))
            elif level[y][x] == '1':
                n.append(Tile('wall_1', x, y))
            elif level[y][x] == '2':
                n.append(Tile('wall_2', x, y))
            elif level[y][x] == '3':
                n.append(Tile('wall_3', x, y))
            elif level[y][x] == '4':
                n.append(Tile('wall_4', x, y))
            elif level[y][x] == '5':
                n.append(Tile('wall_5', x, y))
            elif level[y][x] == '6':
                n.append(Tile('wall_6', x, y))
            elif level[y][x] == '7':
                n.append(Tile('wall_7', x, y))
            elif level[y][x] == '.':
                n.append(Point('point', x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = AnimatedSprite(load_image("pacman.png"), 3, 1, x, y)
                n.append(None)
            elif level[y][x] == '#':
                Tile('empty', x, y)
                new_enemy = AnimatedEnemy(load_image("ghost.png"), 4, 1, x, y)
                n.append(None)
        maplist.append(n)
    return new_player, new_enemy, x, y


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.sheet = sheet
        self.columns = columns
        self.rows = rows
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.posx = x
        self.posy = y
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(tile_width * self.posx, tile_height * self.posy)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if frames_count == 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def coordreturn(self):
        return self.posx, self.posy

    def rectmove(self, x, y):
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.posx = x
        self.posy = y
        self.rect = self.rect.move(tile_width * self.posx, tile_height * self.posy)


class AnimatedEnemy(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.sheet = sheet
        self.columns = columns
        self.move_x, self.move_y = 0, 0
        self.rows = rows
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.pos_x = x
        self.pos_y = y
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(tile_width * self.pos_x, tile_height * self.pos_y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if frames_count == 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def coordreturn(self):
        return self.pos_x, self.pos_y

    def rectmove(self, x, y):
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.pos_x = x
        self.pos_y = y
        self.rect = self.rect.move(tile_width * self.pos_x, tile_height * self.pos_y)
        # while True:


def enemies_brain(x_1, y_1, xplayer, yplayer):
    if x_1 == xplayer and y_1 == yplayer:
        global game_over
        game_over = True
    while True:
        direction = random.randint(1, 4)
        if direction == 1 and \
                (load_level(mapfile[level_id])[y_1][x_1 + 1] == '.'
                 or load_level(mapfile[level_id])[y_1][x_1 + 1] == '@'
                 or load_level(mapfile[level_id])[y_1][x_1 + 1] == '#'):
            x_1 += 1
            return x_1, y_1
        if direction == 2 and \
                (load_level(mapfile[level_id])[y_1][x_1 - 1] == '.'
                 or load_level(mapfile[level_id])[y_1][x_1 - 1] == '@'
                 or load_level(mapfile[level_id])[y_1][x_1 - 1] == '#'):
            x_1 -= 1
            return x_1, y_1
        if direction == 3 and \
                (load_level(mapfile[level_id])[y_1 + 1][x_1] == '.'
                 or load_level(mapfile[level_id])[y_1 + 1][x_1] == '@'
                 or load_level(mapfile[level_id])[y_1 + 1][x_1] == '#'):
            y_1 += 1
            return x_1, y_1
        if direction == 4 and \
                (load_level(mapfile[level_id])[y_1 - 1][x_1] == '.'
                 or load_level(mapfile[level_id])[y_1 - 1][x_1] == '@'
                 or load_level(mapfile[level_id])[y_1 - 1][x_1] == '#'):
            y_1 -= 1
            return x_1, y_1


def next_level():
    global n
    global all_sprites
    global tiles_group
    global point_group
    global maplist
    global player_group
    player_group = pygame.sprite.Group()
    n = []
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    point_group = pygame.sprite.Group()
    maplist = []
    screen.fill((0, 0, 0))
    return main()


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
game_over = False


def main():
    global game_over
    global frames_count
    global level_id
    screen.fill((0, 0, 0))
    player, enemy, level_x, level_y = generate_level(load_level(mapfile[level_id]))
    x, y = player.coordreturn()
    x_1, y_1 = enemy.coordreturn()
    count = 0
    move = 1
    map_point = []
    count_point = 0
    final_points = 0
    enemy_count = 0
    for i in load_level(mapfile[level_id]):
        n = list(i)
        final_points += i.count('.')
        map_point.append(n)
    while True:
        screen.fill((0, 0, 0))
        background.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move = 1
                if event.key == pygame.K_RIGHT:
                    move = 2
                if event.key == pygame.K_UP:
                    move = 3
                if event.key == pygame.K_DOWN:
                    move = 4
        if (load_level(mapfile[level_id])[y][x - 1] == '.' or load_level(mapfile[level_id])[y][x - 1] == '@'
            or load_level(mapfile[level_id])[y][x - 1] == '#') \
                and move == 1 and count == 15:
            x -= 1
        if (load_level(mapfile[level_id])[y][x + 1] == '.' or load_level(mapfile[level_id])[y][x + 1] == '@'
            or load_level(mapfile[level_id])[y][x + 1] == '#') \
                and move == 2 and count == 15:
            x += 1
        if (load_level(mapfile[level_id])[y - 1][x] == '.' or load_level(mapfile[level_id])[y - 1][x] == '@'
            or load_level(mapfile[level_id])[y - 1][x] == '#') \
                and move == 3 and count == 15:
            y -= 1
        if (load_level(mapfile[level_id])[y + 1][x] == '.' or load_level(mapfile[level_id])[y + 1][x] == '@'
            or load_level(mapfile[level_id])[y + 1][x] == '#') \
                and move == 4 and count == 15:
            y += 1
        if enemy_count == 5:
            x_1, y_1 = enemies_brain(x_1, y_1, x, y)
        all_sprites.draw(screen)
        enemy.rectmove(x_1, y_1)
        player.rectmove(x, y)
        clock.tick(fps)
        all_sprites.update()
        pygame.display.flip()
        count += 1
        frames_count += 1
        enemy_count += 1
        if frames_count > 10:
            frames_count = 0
        if enemy_count > 5:
            enemy_count = 0
        if count > 15:
            count = 0
        if map_point[y][x] == '.':
            maplist[y][x].kill()
            count_point += 1
            map_point[y][x] = ' '
        if count_point == final_points:
            if level_id < 1:
                level_id += 1
                screen.fill((0, 0, 0))
                return next_level()
            else:
                return final_window()
        if game_over:
            return game_over_window()


if __name__ == '__main__':
    start_screen()
