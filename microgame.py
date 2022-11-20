"""
Base class for all microgames
DO NOT MODIFY THIS, INHERIT IT INSTEAD
"""
import pygame
import controls
import global_values as g

class Microgame():
    def __init__(self, _metadata={}):
        #metadata regarding the microgame
        self.metadata = {
            "author":"Anonymous", #who made the game (please include Discord tags!)
            "width":300, #resolution
            "height":300,
            "thumbnail":None, #surface to use as a thumbnail for this game, if None, a default is used
            "show_cursor":True,
            "time":5, #how long does the player have?
            "post_time":1, #how long after winning/losing until we move on?

            "comments":"", #anything extra you want to add
        }
        self.metadata.update(_metadata)

        #whether this microgame is running in any capacity
        self.running = False

        #whether the game has "ended", i.e. whether the player has won/lost
        self.ended = True

        #the surface used for drawing on. Note that you don't have to use this if you don't want to, as the
        #thing that's drawn onto the screen is whatever is returned by the draw method. You could always draw
        #onto a different surface and return that, though there wouldn't be much point.
        self.surf = pygame.Surface((self.metadata["width"], self.metadata["height"]))

        #when this game started running
        self.start_time = None

        if not self.metadata["thumbnail"]:
            thumbnail_width = 64
            thumbnail_height = 64
            thumbnail = pygame.Surface((thumbnail_width, thumbnail_height))
            thumbnail.fill("white")

            pygame.draw.rect(thumbnail, "red", pygame.Rect(0, 0, thumbnail_width, thumbnail_height), 2)

            #TODO: remove this and replace with something better?
            thumbnail_font = pygame.font.SysFont("Consolas", 16)
            thumbnail_string = self.__class__.__name__[:min(len(self.__class__.__name__),4)]
            thumbnail_text = thumbnail_font.render(thumbnail_string, True, "black")
            thumbnail.blit(thumbnail_text, ( (thumbnail.get_width()/2)-(thumbnail_text.get_width()/2) , (thumbnail.get_height()/2)-(thumbnail_text.get_height()/2) ))
            

            self.metadata["thumbnail"] = thumbnail


    def get_mouse_pos(self):
        """
        Get the mouse position relative to the top corner of the microgame box
        """
        mx, my = pygame.mouse.get_pos()
        ox = (g.WIDTH/2) - (self.metadata["width"]/2)
        oy = (g.HEIGHT/2) - (self.metadata["height"]/2)
        x = mx - ox
        y = my - oy
        return x, y

    def run(self):
        """
        Run the microgame
        """
        self.running = True
        self.ended = False
        g.current_game = self

        self.start_time = pygame.time.get_ticks()
        self.finish_text = None

        if self.metadata["show_cursor"]:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

        #timeout event
        end_event = pygame.event.Event(g.MICROGAME_TIMEOUT_EVENT, {"game":type(self)})
        pygame.time.set_timer(end_event, self.metadata["time"]*1000, loops=1)
        
        #GUI
        #TODO: CHANGE ACTIVE STATES
        timer_pos = (g.WIDTH/2, (g.HEIGHT/2) - (self.metadata["height"]/2))
        self.timer_text = controls.TextBox(timer_pos, "g.current_game.get_formatted_time()", pygame.font.SysFont("Consolas", 32), self.metadata["time"], "white", True, set(("main_menu",)), cx=True, cy=False)

    def get_formatted_time(self):
        if self.start_time is None:
            text = "N/A"
        else:
            diff = self.metadata["time"]*1000 - (pygame.time.get_ticks() - self.start_time)
            seconds = int(diff // 1000)
            centiseconds = int(diff % 1000 // 10)
            text = f"{ str(seconds).zfill(2) }:{ str(centiseconds).zfill(2) }"

        return text

    def finish(self, win):
        """
        Finish this microgame. This is called whenever "Microgame.win" or "Microgame.lose" is called
        """
        self.ended = True
        end_event = pygame.event.Event(g.MICROGAME_END_EVENT)
        pygame.time.set_timer(end_event, self.metadata["post_time"]*1000, loops=1)

        #finish text
        finish_pos = (g.WIDTH/2, (g.HEIGHT/2) - (self.metadata["height"]/2) + 50)
        if win:
            text = "Success"
            color = "yellow"
        else:
            text = "Failure"
            color = "red"

        #TODO change active states
        self.finish_text = controls.TextBox(finish_pos, text, pygame.font.SysFont("Consolas", 32), self.metadata["post_time"], color, False, set(("main_menu",)), cx=True, cy=False)

        print("delete")
        self.timer_text.delete()

    def end(self):
        """
        Fully end the microgame. This is called automatically some time after "Microgame.finish" is called
        """
        print("end")
        self.running = False
        g.current_game = None

        pygame.mouse.set_visible(True)

    def win(self):
        """
        Finish this microgame with a win. Call this if the player meets the win condition.
        Note that after this is called, the game won't truly "end" until the time specified in the "post_time" metadata has elapsed.
        It's recommended that if you overwrite this in your game, you call the parent version of this method with "super().win()"
        """
        self.finish(True)

    def lose(self):
        """
        Finish this microgame with a loss. Call this if the player hits a loss condition.
        This is also automatically called if the player runs out of time.
        Note that after this is called, the game won't truly "end" until the time specified in the "post_time" metadata has elapsed.
        It's recommended that if you overwrite this in your game, you call the parent version of this method with "super().lose()"
        """
        self.finish(False)


    def handle_input(self, event_list):
        """
        Handle all the events that occured since the previous frame.
        This is similar to pygame.event.get(), though event_list will not contain
        events with the pygame.QUIT event type. This is automatically called every frame.
        Please implement this function within your own microgame.
        """
        pass

    def update(self, delta):
        """
        Update the microgame. This is automatically called every frame.
        Please implement this function within your own microgame.
        """
        if self.ended:
            drift = 0.1
            
            x, y = self.finish_text.pos
            self.finish_text.pos = (x, y + (drift*delta) ) 

    def draw(self):
        """
        Draw the microgame and return the result.
        This is automatically called every frame.
        Please implement this function within your own microgame.
        """
        return pygame.Surface((self.metadata["width"], self.metadata["height"]))
            
            

