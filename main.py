# file: sprite_move.py
import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite motion example")

# Тохиргоо
ASSETS_DIR = "assets"  # дүрсний кадр файлууд байрлах фолдер
PLAYER_SPEED = 300  # пиксел/секунд

def load_frames(prefix, count):
    """prefix = 'player_' , count = number of frames (0..count-1)"""
    frames = []
    for i in range(count):
        path = os.path.join(ASSETS_DIR, f"{prefix}{i}.png")
        img = pygame.image.load(path).convert_alpha()
        frames.append(img)
    return frames

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, frames, scale=1.0):
        super().__init__()
        self.frames = frames
        # optional: scale frames
        if scale != 1.0:
            self.frames = [pygame.transform.smoothscale(f, (int(f.get_width()*scale), int(f.get_height()*scale))) for f in self.frames]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = 0
        self.facing_right = True

        # animation timing
        self.anim_fps = 10  # кадр/сек
        self.anim_timer = 0.0

    def update(self, dt):
        # хөдөлгөөн
        self.rect.x += int(self.vel_x * dt)

        # анимаци (хэрэв хөдөлж байвал)
        if self.vel_x != 0:
            self.anim_timer += dt
            frame_duration = 1.0 / self.anim_fps
            if self.anim_timer >= frame_duration:
                self.anim_timer -= frame_duration
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
        else:
            # зогсоход эхний кадрт буцаах
            self.frame_index = 0
            self.image = self.frames[self.frame_index]

        # нүүрээ хальт (flip) - баруун зүг рүү харж байгааг харуулна
        if self.facing_right:
            self.image = pygame.transform.flip(self.frames[self.frame_index], False, False)
        else:
            self.image = pygame.transform.flip(self.frames[self.frame_index], True, False)

def main():
    clock = pygame.time.Clock()

    # frames-г ачаалж ав
    # assets фолдерт player_0.png ... player_3.png гэх мэт байхаар хий
    player_frames = load_frames("player_", 4)

    player = Player(WIDTH//2, HEIGHT//2, player_frames, scale=2.0)
    all_sprites = pygame.sprite.Group(player)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # секундээр (delta time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # input
        keys = pygame.key.get_pressed()
        vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx = -PLAYER_SPEED
            player.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx = PLAYER_SPEED
            player.facing_right = True
        else:
            vx = 0
        player.vel_x = vx

        # update
        all_sprites.update(dt)

        # draw
        WIN.fill((30, 30, 30))
        all_sprites.draw(WIN)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
