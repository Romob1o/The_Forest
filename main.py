import pygame
import os
import sys
import time

pygame.init()
TILE_SIZE = 64
WIDTH = 1250
HEIGHT = 11 * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Forest")
lvl = 1
player = None

pygame.font.init()

FPS = 60
GRAVITY = 12
VELOCITY = 6
V_JUMP = 20
MAX_LVL = 2
clock = pygame.time.Clock()

ground_group = pygame.sprite.Group()
stone_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def font(size):
    return pygame.font.Font('Data\TunnelFront.ttf', size)


def load_image(name, colorkey=None):
    fullname = os.path.join('Data', name)
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


def load_level(filename):
    filename = "Levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    global player
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                player = Player(x, y)
            elif level[y][x] == "x":
                Stone(x, y)
            elif level[y][x] == "f":
                Flag(x, y)
            elif level[y][x] != ".":
                Tile(level[y][x], x, y)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('screensaver.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    text = font(25).render('press any button', True, (40, 40, 40))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200))
    text2 = font(100).render('The Forest', True, (0, 0, 0))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def level_completed():
    all_sprites.draw(screen)
    text = font(150).render(f'Level {lvl} completed', True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    text2 = font(25).render('press any button', True, (0, 0, 0))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 410))
    text3 = font(50).render(f"Your time: {minutes}.{seconds}", True, (0, 0, 0))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, 500))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if lvl == MAX_LVL:
                    finish_screen()
                global start
                start = time.time()
                return
        pygame.display.flip()
        clock.tick(FPS)


def next_level():
    global lvl
    lvl += 1
    for sprite in all_sprites:
        sprite.kill()
    generate_level(load_level(f"{lvl}_lvl.txt"))
    return


def game_over():
    all_sprites.draw(screen)
    text = font(150).render('Game Over', True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    text2 = font(25).render('press any button', True, (0, 0, 0))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 410))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in all_sprites:
                    sprite.kill()
                generate_level(load_level(f"{lvl}_lvl.txt"))
                global start
                start = time.time()
                return
        pygame.display.flip()
        clock.tick(FPS)


def finish_screen():
    screen.blit(pygame.transform.scale(load_image("screensaver.png"), (WIDTH, HEIGHT)), (0, 0))
    text = font(150).render('Forest is completed', True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    text2 = font(25).render('press any button', True, (0, 0, 0))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 410))
    text3 = font(150).render('Congratulations!!!', True, (0, 0, 0))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, 135))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in all_sprites:
                    sprite.kill()
                exit()
        pygame.display.flip()
        clock.tick(FPS)


BACKGROUND = pygame.transform.scale(load_image("background.png"), (WIDTH, HEIGHT))
BACKGROUND_COLOR = pygame.Color((66, 170, 255))


class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(stone_group, all_sprites)
        self.image = load_image("stone.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE + 10


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(flag_group, all_sprites)
        self.image = pygame.transform.scale(load_image("flag.png"), (45, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE + TILE_SIZE // 2 - self.rect.width // 2


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(ground_group, all_sprites)
        self.image = pygame.transform.scale(load_image(f"{tile_type}.png"), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.activity = ["idle"]
        self.jump = False
        self.v_jump = V_JUMP

        self.frames_idle = []
        for i in range(6):
            self.frames_idle.append(load_image(f"Idle{i}.png"))
        self.frames_idle_count = 0

        self.frames_run = self.frames_jump = []
        for i in range(7):
            self.frames_run.append(load_image(f"Run{i}.png"))
        self.frames_run_count = self.frames_jump_count = 0

        self.cur_frame = 0
        self.image = self.frames_idle[self.cur_frame]
        self.rect = self.frames_run[0].get_rect()
        self.rect.left = x * TILE_SIZE
        self.rect.bottom = (y + 1) * TILE_SIZE

    def get_status(self, buttons):
        keys = pygame.key.get_pressed()
        new_activity = []
        if self.jump or (buttons["space"] and pygame.sprite.spritecollideany(self, ground_group)):
            new_activity.append("jump")
        if keys[pygame.K_d]:
            new_activity.append("right")
        elif keys[pygame.K_a]:
            new_activity.append("left")
        if len(new_activity) == 0:
            new_activity.append("idle")
        return new_activity

    def check_on_screen(self):
        if self.rect.y > HEIGHT:
            return True
        else:
            return False

    def check_alive(self):
        if pygame.sprite.spritecollideany(self, stone_group):
            return True
        else:
            return False

    def check_on_finish(self):
        if pygame.sprite.spritecollideany(self, flag_group):
            return True
        else:
            return False

    def update(self, buttons):
        if self.check_on_screen() or self.check_alive():
            self.kill()
            game_over()
        if self.check_on_finish():
            self.kill()
            level_completed()
            next_level()

        self.rect.bottom += 1

        new_activity = self.get_status(buttons)

        self.rect.bottom -= 1

        if "jump" in new_activity:
            self.jump = True

        if self.activity != new_activity:
            self.frames_idle_count = 0
            self.frames_run_count = 0
            self.frames_jump_count = 0
            self.cur_frame = 0
            self.activity = new_activity

        if "idle" in new_activity:
            self.frames_idle_count = (self.frames_idle_count + 1) % 15
            if self.frames_idle_count == 14:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_idle)
                self.image = self.frames_idle[self.cur_frame]

        elif "jump" in new_activity:
            self.rect.y -= self.v_jump
            self.v_jump -= 1
            if pygame.sprite.spritecollideany(self, ground_group) and self.v_jump < 0:
                self.rect.bottom -= self.rect.bottom % TILE_SIZE
                self.jump = False
                self.v_jump = V_JUMP
            elif pygame.sprite.spritecollideany(self, ground_group) and self.v_jump > 0:
                self.rect.bottom += self.v_jump
                self.v_jump = 0

            if "right" in new_activity:
                self.rect.x += VELOCITY
                if pygame.sprite.spritecollideany(self, ground_group):
                    self.rect.x -= VELOCITY

            elif "left" in new_activity:
                self.rect.x -= VELOCITY
                if pygame.sprite.spritecollideany(self, ground_group):
                    self.rect.x += VELOCITY

            self.frames_jump_count = (self.frames_jump_count + 1) % 6
            if self.frames_jump_count == 5:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_jump)
                self.image = pygame.transform.flip(self.frames_jump[self.cur_frame], "left" in new_activity, False)

        elif "right" in new_activity:
            self.rect.x += VELOCITY
            if pygame.sprite.spritecollideany(self, ground_group):
                self.rect.x -= VELOCITY
            self.frames_run_count = (self.frames_run_count + 1) % 7
            if self.frames_run_count == 6:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_run)
                self.image = self.frames_run[self.cur_frame]

        elif "left" in new_activity:
            self.rect.x -= VELOCITY
            if pygame.sprite.spritecollideany(self, ground_group):
                self.rect.x += VELOCITY
            self.frames_run_count = (self.frames_run_count + 1) % 7
            if self.frames_run_count == 6:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_run)
                self.image = pygame.transform.flip(self.frames_run[self.cur_frame], True, False)

        # pygame.draw.rect(screen, pygame.Color("black"), self.rect, 1)

        if not self.jump:
            self.rect.bottom += GRAVITY
            if pygame.sprite.spritecollideany(self, ground_group):
                self.rect.bottom -= self.rect.bottom % TILE_SIZE


camera = Camera()

start_screen()
if __name__ == '__main__':
    running = True
    generate_level(load_level(f'1_lvl.txt'))
    start = time.time()
    while running:
        keys = {"space": False}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keys["space"] = True
        screen.fill(BACKGROUND_COLOR)
        screen.blit(BACKGROUND, (0, 0))
        now = time.time()
        minutes = str(int((now - start) // 60))
        seconds = u'%.2f' % ((now - start) % 60)
        text = font(30).render(f"{minutes}.{seconds}", True, (0, 0, 0))
        player_group.update(keys)
        camera.update(player)
        for spr in all_sprites:
            camera.apply(spr)
        player_group.draw(screen)
        ground_group.draw(screen)
        stone_group.draw(screen)
        flag_group.draw(screen)
        screen.blit(text, (10, 0))
        clock.tick(FPS)
        pygame.display.flip()

