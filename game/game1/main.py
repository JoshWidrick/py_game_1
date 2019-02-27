import pygame
pygame.init()

screen_width = 500
screen_height = 480
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game")

walk_right_images = ["R1.png", "R2.png", "R3.png", "R4.png", "R5.png", "R6.png", "R7.png", "R8.png", "R9.png"]
walk_left_images = ["L1.png", "L2.png", "L3.png", "L4.png", "L5.png", "L6.png", "L7.png", "L8.png", "L9.png"]
walk_right = [pygame.image.load("images/" + img) for img in walk_right_images]
walk_left = [pygame.image.load("images/" + img) for img in walk_left_images]
bg = pygame.image.load("images/bg.jpg")
char = pygame.image.load("images/standing.png")

bullet_sound = pygame.mixer.Sound("images/bullet.wav")
hit_sound = pygame.mixer.Sound("images/hit.wav")
music = pygame.mixer.music.load("images/music.mp3")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

score = 0


class Player(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if (self.walk_count + 1) >= 27:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                win.blit(walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.left:
                win.blit(walk_left[0], (self.x, self.y))
            else:
                win.blit(walk_right[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.is_jump = False
        self.jump_count = 10
        self.x = 300
        self.y = 410
        self.walk_count = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render("-5", 1, (255, 0, 0))
        win.blit(text, ((screen_width / 2) - (text.get_width() / 2), (screen_height / 2) - (text.get_height() / 2)))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class Enemy(object):
    walk_right_images = ["R1E.png", "R2E.png", "R3E.png", "R4E.png", "R5E.png", "R6E.png", "R7E.png", "R8E.png", "R9E.png", "R10E.png", "R11E.png"]
    walk_left_images = ["L1E.png", "L2E.png", "L3E.png", "L4E.png", "L5E.png", "L6E.png", "L7E.png", "L8E.png", "L9E.png", "L10E.png", "L11E.png"]
    walk_right = [pygame.image.load("images/" + img) for img in walk_right_images]
    walk_left = [pygame.image.load("images/" + img) for img in walk_left_images]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if (self.walk_count + 1) >= 33:
                self.walk_count = 0

            if self.vel > 0:
                win.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            else:
                win.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50 / 10) * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if (self.x + self.vel) < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walk_count = 0
        else:
            if (self.x - self.vel) > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walk_count = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


class Projectile(object):

    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redraw_game_window():
    win.blit(bg, (0, 0))
    text = font.render(f"Score: {score}", 1, (0, 0, 0))
    win.blit(text, (385, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


font = pygame.font.SysFont("comicsans", 30, True)
man = Player(300, 410, 64, 64)
goblin = Enemy(50, 410, 64, 64, 450)
shoot_loop = 0
run = True
bullets = []
while run:
    clock.tick(27)

    if goblin.visible:
        if man.hitbox[1] < (goblin.hitbox[1] + goblin.hitbox[3]) and (man.hitbox[1] + man.hitbox[3]) > goblin.hitbox[1]:
            if (man.hitbox[0] + man.hitbox[2]) > goblin.hitbox[0] and man.hitbox[0] < (goblin.hitbox[0] + goblin.hitbox[2]):
                man.hit()
                score -= 5

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 3:
        shoot_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible:
            if (bullet.y - bullet.radius) < (goblin.hitbox[1] + goblin.hitbox[3]) and (bullet.y + bullet.radius) > goblin.hitbox[1]:
                if (bullet.x + bullet.radius) > goblin.hitbox[0] and (bullet.x - bullet.radius) < (goblin.hitbox[0] + goblin.hitbox[2]):
                    hit_sound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))

        if 0 < bullet.x < screen_width:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shoot_loop == 0:
        if len(bullets) < 5:
            bullet_sound.play()
            bullets.append(Projectile(round(man.x + (man.width // 2)),
                                      round(man.y + (man.height // 2)),
                                      6,
                                      (0, 0, 0),
                                      -1 if man.left else 1))
        shoot_loop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < (screen_width - man.width - man.vel):
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walk_count = 0
    if not man.is_jump:
        if keys[pygame.K_UP]:
            man.is_jump = True
            man.left = False
            man.right = False
            man.walk_count = 0
    else:
        if man.jump_count >= -10:
            neg = 1
            if man.jump_count < 0:
                neg = -1
            man.y -= (man.jump_count ** 2) * 0.5 * neg
            man.jump_count -= 1
        else:
            man.is_jump = False
            man.jump_count = 10

    redraw_game_window()


pygame.quit()
