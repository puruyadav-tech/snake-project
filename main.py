import pygame
import random
from pygame.locals import *

# Constants
SIZE = 40
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        image = pygame.image.load("apple.jpg").convert_alpha()
        self.image = pygame.transform.scale(image, (SIZE, SIZE))
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self, snake_coords):
        while True:
            self.x = random.randint(0, (SCREEN_WIDTH - SIZE) // SIZE) * SIZE
            self.y = random.randint(0, (SCREEN_HEIGHT - SIZE) // SIZE) * SIZE
            if (self.x, self.y) not in snake_coords:
                break

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        image = pygame.image.load("block.jpg").convert()
        self.image = pygame.transform.scale(image, (SIZE, SIZE))
        self.direction = 'down'
        self.length = 1
        self.x = [SIZE]
        self.y = [SIZE]

    def move_left(self): self.direction = 'left'
    def move_right(self): self.direction = 'right'
    def move_up(self): self.direction = 'up'
    def move_down(self): self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def get_coords(self):
        return list(zip(self.x, self.y))

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg = pygame.image.load("background.jpg").convert()
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        return x1 >= x2 and x1 < x2 + SIZE and y1 >= y2 and y1 < y2 + SIZE

    def render_background(self):
        self.surface.blit(self.bg, (0, 0))

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(score, (850, 10))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.snake.draw()
        self.apple.draw()
        self.display_score()

        # Apple Collision
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move(self.snake.get_coords())

        # Wall Collision
        if self.snake.x[0] < 0 or self.snake.x[0] >= SCREEN_WIDTH or self.snake.y[0] < 0 or self.snake.y[0] >= SCREEN_HEIGHT:
            raise Exception("Wall Collision")

        # Self Collision
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("Self Collision")

        pygame.display.flip()

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 36)
        line1 = font.render(f"Game Over! Your score is {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press Enter to play again or Esc to exit.", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()
                        elif event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            self.clock.tick(10)  # Control speed

if __name__ == '__main__':
    game = Game()
    game.run()

