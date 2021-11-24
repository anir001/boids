import pygame
from pygame import Color
from pygame.math import Vector2

import random


class Boid():
    def __init__(self):
        super().__init__()
        self.size = 5
        self.position = Vector2(random.randint(self.size, 800 - self.size),
                                random.randint(self.size, 600 - self.size))
        # self.position = Vector2(300, 300)

        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity = self.__set_mag__(self.velocity, random.uniform(2, 4))
        
        self.max_speed = 5

        self.perception = 50
        self.align_factor = 0.3
        self.cohesion_factor = 0.05
        self.separation_factor = 0.1
        self.min_distance = 20

    def update(self, flock: list):
        self.flock(flock)

        # limit the speed

        self.velocity = self.__limit__(self.velocity, self.max_speed)
        self.move()

    def flock(self, flock):
        self.aligment(flock)
        self.cohesion(flock)
        self.separation(flock)

    def __set_mag__(self, vector: Vector2, mag: float):
        vector = vector.normalize() * mag
        return vector

    def __limit__(self, vector: Vector2, limit: float):
        if vector.magnitude() >= limit:
            vector = self.__set_mag__(vector, limit)
        return vector

    def aligment(self, flock: list):
        steering = Vector2()

        total = 0
        for other in flock:
            if other is not self and \
               self.position.distance_to(other.position) < self.perception:
                steering += other.velocity
                total += 1

        if total > 0:
            steering /= total

            self.velocity = self.velocity + \
                (steering - self.velocity) * self.align_factor

    def cohesion(self, flock: list):
        steering = Vector2()

        total = 0
        for other in flock:
            if other is not self and \
               self.position.distance_to(other.position) < self.perception:
                steering += other.position
                total += 1

        if total > 0:
            steering /= total

            self.velocity = self.velocity + \
                (steering - self.position) * self.cohesion_factor

    def separation(self, flock: list):
        sep = Vector2()

        for other in flock:
            if other is not self and \
               self.position.distance_to(other.position) < self.min_distance:
                sep = sep + (self.position - other.position)

        self.velocity = self.velocity + (sep * self.separation_factor)

    def move(self):
        self.position += self.velocity

        # wrap screen
        if self.position.x < 0:
            self.position.x = 800
        elif self.position.x > 800:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = 600
        elif self.position.y > 600:
            self.position.y = 0

    def draw(self, screen: pygame.display):
        pygame.draw.circle(screen, Color('grey'), self.position, self.size)
        pygame.draw.circle(screen, Color('grey'), self.position, self.size)
