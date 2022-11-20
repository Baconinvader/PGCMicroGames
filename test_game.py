import pygame
import os
import global_values as g

from microgame import Microgame

class TestGame(Microgame):
    def __init__(self):
        super().__init__({"time":8, "show_cursor":False})

    def run(self):
        import random
        
        self.target_width = 32

        self.target_x = random.randint(0, self.metadata["width"])
        self.target_y = random.randint(0, self.metadata["height"])

        self.reticule = pygame.image.load( os.path.join("assets","reticule.png") )

        super().run()

    
    def handle_input(self, event_list):
        #check if we have clicked to fire
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.ended:
                    if event.button == 1:
                        self.fire()

    def get_distance(self, x1, y1, x2, y2):
        x = x2-x1
        y = y2-y1
        return ((x**2)+(y**2))**0.5

    def fire(self):
        #check if fire was on target
        mx, my = self.get_mouse_pos()
        dist = self.get_distance(mx, my, self.target_x, self.target_y)
        if dist <= self.target_width:
            self.win()

    def draw(self):
        self.surf.fill("gray")

        #draw target
        circle_width = 4
        for i in range( int(self.target_width//circle_width) ):
            if i%2:
                color = "red"
            else:
                color = "white"

            pygame.draw.circle(self.surf, color, (self.target_x, self.target_y), circle_width*i, circle_width)
        pygame.draw.circle(self.surf, "black", (self.target_x, self.target_y), self.target_width, 1)

        mx, my = self.get_mouse_pos()
        reticule_size = 8
        self.surf.blit(self.reticule, (mx-(reticule_size/2), my-(reticule_size/2)))

        return self.surf