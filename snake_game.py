import time
import pygame
import random

from pygame import Color
from enum import Enum
from pygame.font import Font


class Food(object):
    spawn: bool = False
    position: list = []
    color: Color

    def __init__(self, position: list, color: Color):
        self.position = position
        self.color = color

        self.spawn_new(position[0], position[1])

    def set_position(self, dx: int, dy: int) -> list:
        self.position = [dx, dy]
        return self.position

    def set_spawn(self, is_spawn: bool):
        self.spawn = is_spawn

    def is_spawn(self) -> bool:
        return self.spawn

    def spawn_new(self, x, y):
        if not self.spawn:
            self.position = [x, y]
            self.spawn = True

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], 10, 10))


class Snake(object):

    class Direction(Enum):
        LEFT: int = 1
        RIGHT: int = 2
        UP: int = 3
        DOWN: int = 4

    body: list[list] = []
    position: list = []
    direction: int = Direction.RIGHT
    color: Color

    def __init__(self,
                 position: list[int, int],
                 color: Color,
                 block_size: int = 10,
                 body_size: int = 3):
        self.position = position
        self.block_size = block_size
        self.color = color

        if body_size > 0:
            x = self.position[0]
            y = self.position[1]
            for i in range(body_size):
                bx = x - self.block_size
                by = y
                self.body.append([bx, by])
                x = bx
                y = by

    def move(self, step: int):
        if self.direction == self.Direction.LEFT:
            self.position[0] -= step
        if self.direction == self.Direction.RIGHT:
            self.position[0] += step
        if self.direction == self.Direction.UP:
            self.position[1] -= step
        if self.direction == self.Direction.DOWN:
            self.position[1] += step

    def set_direction(self, new_direction: int):
        self.direction = new_direction

    def get_direction(self) -> int:
        return self.direction

    def pop(self):
        return self.body.pop()

    def insert(self, _index: int, _object: list):
        self.body.insert(_index, list(_object))

    def draw(self, surface: pygame.Surface):
        for pos in self.body:
            pygame.draw.rect(surface=surface,
                             color=self.color,
                             rect=pygame.Rect(pos[0], pos[1], self.block_size, self.block_size))

    def is_collision_itself(self) -> bool:
        collipsed: bool = False

        bodies: list = self.body[1:]
        if self.position in bodies:
            collipsed = True

        return collipsed


def show_score(surface: pygame.Surface, score: int, font: str = '', font_size: int = 24):
    font: str = font if len(font) > 0 else pygame.font.get_default_font()

    score_font: Font = pygame.font.Font(font, font_size)
    score_surface:pygame.Surface = score_font.render(f'Score: {score}', True, white)
    score_rect = score_surface.get_rect()

    surface.blit(source=score_surface, dest=score_rect)


# window size
window_x: int = 720
window_y: int = 480

# snake movement speed
speed: int = 15

# inital colors
black: Color = Color(0, 0, 0)
white: Color = Color(255, 255, 255)
blue: Color = Color(0, 0, 255)
red: Color = Color(255, 0, 0)

# Initial pygame window
pygame.init()
surface: pygame.Surface = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Snake Game by Python")

fps = pygame.time.Clock()

# Initial snake
snake_x: int = 100
snake_y: int = 100
snake = Snake(position=[snake_x, snake_y], color=blue)

# Initial food
food_x: int = random.randrange(1, (window_x // 10)) * 10
food_y: int = random.randrange(1, (window_y // 10)) * 10
food = Food(position=[food_x, food_y], color=red)

score: int = 0

game_over: bool = False

while not game_over:
    # Handling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.get_direction() != snake.Direction.RIGHT:
                snake.set_direction(snake.Direction.LEFT)
            if event.key == pygame.K_RIGHT and snake.get_direction() != snake.Direction.LEFT:
                snake.set_direction(snake.Direction.RIGHT)
            if event.key == pygame.K_DOWN and snake.get_direction() != snake.Direction.UP:
                snake.set_direction(snake.Direction.DOWN)
            if event.key == pygame.K_UP and snake.get_direction() != snake.Direction.DOWN:
                snake.set_direction(snake.Direction.UP)

    snake.move(10)
    snake.insert(0, snake.position)

    if snake.position[0] == food.position[0] and snake.position[1] == food.position[1]:
        score += 10
        food.set_spawn(False)
    else:
        snake.pop()

    if not food.is_spawn():
        food.set_position(random.randrange(1, window_x // 10) * 10, random.randrange(1, window_y // 10) * 10)
        food.set_spawn(True)

    surface.fill(color=black)

    snake.draw(surface)
    food.draw(surface)

    if (snake.position[0] < 0) or (snake.position[0] > window_x - 10) or (snake.position[1] < 0) or (snake.position[1] > window_y - 10) or snake.is_collision_itself():
        game_over = True

    # Show score.
    show_score(surface, score)

    pygame.display.update()

    fps.tick(speed)

# After game over.
end_font: Font = pygame.font.Font(pygame.font.get_default_font(), 32)
end_surface: surface = end_font.render(f'Your Scored : {score}', True, red, black)

end_rect = end_surface.get_rect()
end_rect.midtop = (window_x/2, window_y/2)

surface.blit(source=end_surface, dest=end_rect)
pygame.display.flip()
time.sleep(3)
