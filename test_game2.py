import pygame
import os
import global_values as g

from microgame import Microgame

class TestGame2(Microgame):
    def __init__(self):
        super().__init__({"time":5, "show_cursor":True})

    def run(self):
        import random
        
        self.target_y = random.randint(100,200)
        self.bar_y = 0
        self.raising = False

        super().run()

    
    def handle_input(self, event_list):
        #check if we have clicked to fire
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.raising = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.raising = False

    def update(self, dt):
        super().update(dt)
        
        if self.raising:
            print(dt)
            self.bar_y += 0.5*dt
            if self.bar_y >= self.metadata["height"]:
                self.bar_y -= self.metadata["height"]

        if abs(self.target_y-self.bar_y) <= 3:
            self.win()



    def draw(self):
        self.surf.fill("gray")

        #draw target
        pygame.draw.line(self.surf, "black", (0,self.metadata["height"]-self.target_y), (self.metadata["width"],self.metadata["height"]-self.target_y), 4)

        #draw current
        pygame.draw.line(self.surf, "black", (0,self.metadata["height"]-self.bar_y), (self.metadata["width"],self.metadata["height"]-self.bar_y), 4)

        return self.surf