import pygame
from pygame import Color
from sys import exit

from boid import Boid


class App():
    def __init__(self,
                 screen_width=800,
                 screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = 60
        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height))

        self.flock = []

        self.__build__(flock_size=100)

    def handle_events(self):
        """
        Handle any keypressed
        q - quit

        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.unicode == 'q':
                    exit()

            if event.type == pygame.QUIT:
                exit()

    def __build__(self, flock_size: int):
        """
        Initiate flock

        :param: flock_size : int
            Boids amount
        """
        for i in range(flock_size):
            self.flock.append(Boid())

    def update(self):
        for boid in self.flock:
            boid.update(self.flock)

    def draw(self):
        self.screen.fill(Color('black'))
        # --------------------

        for boid in self.flock:
            boid.draw(self.screen)

        # --------------------
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()

        while True:

            self.handle_events()
            self.draw()
            self.update()

            pygame.display.update()

            clock.tick(self.fps)
