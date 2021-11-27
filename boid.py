import pygame
from pygame import Color
from pygame.math import Vector2

import random


class Boid:
    def __init__(self):
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h

        self.size = 5
        self.position = Vector2(random.randint(self.size,
                                               self.screen_width - self.size),
                                random.randint(self.size,
                                               self.screen_height - self.size))

        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity = self.__set_speed__(self.velocity, random.uniform(2, 4))

        # for avoid edges
        self.margin = 25
        self.edges = [self.margin,
                      self.margin,
                      self.screen_width - self.margin,
                      self.screen_height - self.margin]

        self.max_speed = 5
        self.perception = 100
        self.align_factor = 0.1
        self.cohesion_factor = 0.002
        self.separation_factor = 0.01
        self.min_distance = 25

    def update(self, flock: list):
        """
        :param flock:
        :return:
        """
        self.flock(flock)
        self.avoid_edge()

        # limit the speed
        # self.velocity = self.__limit__(self.velocity, self.max_speed)
        self.velocity = self.__set_speed__(self.velocity, self.max_speed)

        self.move()

    def flock(self, flock: list):
        self.alignment(flock)
        self.cohesion(flock)
        self.separation(flock)

    @staticmethod
    def __set_speed__(vector: Vector2, mag: float):
        vector.scale_to_length(mag)
        return vector

    @staticmethod
    def __limit__(vector: Vector2, limit: float):
        if vector.magnitude() >= limit:
            vector = Boid.__set_speed__(vector, limit)
        return vector

    def alignment(self, flock: list):
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
                sep = (self.position - other.position) * self.separation_factor

        self.velocity = self.velocity + sep

    def move(self):
        self.position += self.velocity

        # wrap screen
        # if self.position.x < 0:
        #     self.position.x = self.screen_width
        # elif self.position.x > self.screen_width:
        #     self.position.x = 0
        # if self.position.y < 0:
        #     self.position.y = self.screen_height
        # elif self.position.y > self.screen_height:
        #     self.position.y = 0

    def avoid_edge(self):

        left = self.edges[0] - self.position.x
        up = self.edges[1] - self.position.y
        right = self.position.x - self.edges[2]
        down = self.position.y - self.edges[3]

        edge = max(left, up, right, down)

        if edge > 0:
            center = (self.screen_width / 2, self.screen_height / 2)
            steering = Vector2(center)
            steering = (steering - self.position) * 0.001
            self.velocity += steering

    def draw(self, screen: pygame.display):
        pygame.draw.circle(screen, Color('grey'), self.position, self.size)
