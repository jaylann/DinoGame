import math
import os
import random
import sys
import time
import pygame
from random import getrandbits


class Cactus:
    def __init__(self, large, x):
        """Generates a Cactus which the Dino needs to jump over

        :param large: if the cactus should be a large one or not
        :param x: x coordinate of cactus
        :return: Cactus Object
        """
        self.image = None
        self.x = x
        self.offset = 0
        self.SCALE_FACTOR = 5  # factor to scale images by. Scales by 1/n

        image_path = f"_internal/images/cactus_{'large' if large else 'small'}_{random.randint(1, 2)}.png"
        image = pygame.image.load(image_path)

        self.width = int(image.get_width() / self.SCALE_FACTOR)
        self.height = int(image.get_height() * (self.width / image.get_width()))

        self.image = (pygame.transform.scale(image, (self.width, self.height)))

        self.offset = self.width + 2  # space between this and next cactus

        if getrandbits(1):  # gets a single random bit representing true or false
            self.image = pygame.transform.flip(self.image, True, False)

        self.y = 135 - self.image.get_height()

    def move(self, x) -> bool:
        """Move Cactus on x-axis

        :param x: distance to move cactus
        :return: true if still on screen false if off-screen
        """
        self.x += int(x)
        return False if self.x < -self.offset else True

    def draw(self, display) -> None:
        """Draw cactus on display

        :param display: display to, well display the image on :)
        """
        display.blit(self.image, (self.x, self.y))


class World:
    def __init__(self):
        self.width = 600
        self.height = 150
        self.background_color = (247, 247, 247)
        self.display, self.dust, self.font = self._init_game()
        self.asset_color = (83, 83, 83)
        self.dino = Dino()
        self.cacti = []
        self.speed = 6
        self.display_speed = -math.log(self.speed, 1.5)

        self.tick_count = 0

    def _init_game(self) -> (pygame.display, list, pygame.font):
        """Initializes pygame and generates necessary assets
        :return: pygame display object, generated dust assets, loaded font
        """

        pygame.init()
        display = pygame.display.set_mode((self.width, self.height))
        dust = self.generate_dust()
        font = pygame.font.Font("_internal/fonts/PressStart2P-Regular.ttf", 15)
        return display, dust, font

    def run(self):
        clock = pygame.time.Clock()
        added = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.dino.jump()
            self.dino.move()
            self.tick_count += 1
            if self.tick_count > 60 / self.speed:
                self.dino.score += 1
                self.speed += 0.1 - math.log(self.speed, 4) / 50 if 0.1 - math.log(self.speed, 4) / 50 > 0 else 0
                self.tick_count = 0
            self.display_speed = -math.log(self.speed, 1.5)
            self.draw()
            if random.randint(1, 300) > 290 and not added:
                added = 60
                self.add_cacti(random.randint(1, int(1 + (self.speed - 6) / 6)))
            if self.dino.check_collision(self.cacti):
                break

            pygame.display.update()
            if added:
                added -= 1
            clock.tick(60)

    def add_cacti(self, amount) -> None:
        """Adds cacti to the game

        :param amount: amount of cacti to add
        """
        offset = 0
        for x in range(amount):
            cactus = Cactus(random.randint(0, 1), 1000 + offset)

            self.cacti.append(cactus)

            offset += cactus.offset

    def draw_dust(self) -> None:
        """Draws dust particles on ground
        :param x_offset: distance in pixel to move dust compared to previous image 
        """

        self.dust = self.move_rects(self.dust, int(self.display_speed))
        for rect in self.dust:
            pygame.draw.rect(self.display, self.asset_color, rect)

    def draw_floor(self) -> None:
        """Draws the floor of the game"""
        # TODO: Implement irregularities
        pygame.draw.rect(self.display, self.asset_color, pygame.Rect(0, 125, 600, 2))

    def generate_dust(self) -> list[pygame.rect]:
        """Generates a list of rectangles that represent the dust on the floor
        
        :return: list of rectangles
        """
        rects = []
        hor_distance = 0
        while hor_distance < self.width:
            width = random.randrange(3, 8, 1)
            hor_distance += random.randrange(10, 40, 4)
            vert_distance = random.randrange(2, 12, 2)

            # we use 128 here as a constant value for y so its always below 128 pixels
            rects.append(pygame.Rect(hor_distance, 128 + vert_distance, width, 2))
        return rects

    def draw_score(self) -> None:
        """Draws the current score"""
        x_offset = 0
        if self.dino.score > 99999:  # in case you exceed the 0 padded space 
            x_offset = 10  # offset x so that another letter fits on the screen

        # pad score with 0s so that score is always 5 characters long
        score_string = "0" * (5 - len(str(self.dino.score))) + str(self.dino.score)

        score_text = self.font.render(score_string, True, self.asset_color)

        self.display.blit(score_text, (525 - x_offset, 0))

    def move_rects(self, rects, x) -> list[pygame.rect]:
        """move given rectangles by x in x direction

        :param rects: list of rectangles to move
        :param x: offset to move rectangles
        :return: list of moved rectangles
        """
        for rect in rects:
            if rect.x + x < 0:  # if rectangle goes off-screen move it to the other side
                rect.x = 0
                rects[rects.index(rect)] = rect.move(x + 600, 0)
            else:
                rects[rects.index(rect)] = rect.move(x, 0)
        return rects

    def draw(self):
        """Draw the game"""

        self.display.fill(self.background_color)
        self.draw_floor()
        self.draw_score()

        # draw cacti and remove them if they are off-screen
        remove_list = []
        for cactus in self.cacti:
            if cactus.move(self.display_speed):
                cactus.draw(self.display)
            else:
                remove_list.append(cactus)
        for cactus in remove_list:
            self.cacti.remove(cactus)

        self.draw_dust()
        self.dino.draw(self.display)


class Dino:
    def __init__(self):
        self.speed = int((1.05 / 10) * 60)
        self.score = 0
        self.x = 20
        self.is_jumping = False
        self.y = 90
        self.jump_count = 0
        self.tick_count = 0
        self.jump_velocity = 0
        self.char = pygame.transform.scale(pygame.image.load('_internal/images/dino.png'), (40, 44))

    def jump(self):
        self.is_jumping = True
        self.jump_velocity = 9.25

    def move(self):
        if self.is_jumping:
            self.tick_count += 1
            self.jump_count += 1
            self.jump_velocity = 9.25 - 2.5 * (self.tick_count / 5)
            self.y -= self.jump_velocity
            if self.y > 90:
                self.y = 90
                self.is_jumping = False
                self.jump_velocity = 0
                self.tick_count = 0

    def draw(self, canvas):
        canvas.blit(self.char, (self.x, self.y))

    def check_collision(self, cacti):
        dino_box = self.char.get_rect()
        dino_box.topleft = (self.x, self.y)
        for cactus in cacti:
            if self.x-cactus.width < cactus.x < self.x+100:
                cactus_rect = cactus.image.get_rect()
                cactus_rect.topleft = (cactus.x, cactus.y)
                if dino_box.colliderect(cactus_rect):
                    return True
        return False

if __name__ == "__main__":
    w = World()
    w.run()
