"""
This is a file for storing controls for menus
Please don't use these for your game (you can make your own, I believe in you!)
"""
import global_values as g
import pygame

class Control:
    """
    Base class for all controls
    """
    def __init__(self, rect, active_states):
        self.rect = rect
        self.active_states = active_states

        g.controls.append(self)
        self.deleted = False

    def get_active(self):
        """
        Check whether this control should be ative
        """
        if g.state in self.active_states:
            return True
        else:
            return False

    def click(self):
        return False

    def update(self):
        pass

    def draw(self):
        pass

    def delete(self):
        if not self.deleted:
            self.deleted = True
            g.controls.remove(self)

class ScrollBar(Control):
    """
    Class for scroll bars
    """
    def __init__(self, rect, handle_color, bar_color, active_states, handle_height=16):
        super().__init__(rect, active_states)
        self.scroll_value = 0

        self.handle_color = handle_color
        self.bar_color = bar_color

        self.handle_height = handle_height
        self.handle_rect = pygame.Rect(self.rect.x, 0, self.rect.w, self.handle_height)

        self.handling = False

    def update(self):
        ml = pygame.mouse.get_pressed()[0]
        mx, my = pygame.mouse.get_pos()
        if not self.handling:
            if ml and self.rect.collidepoint((mx, my)):
                self.handling = True
        else:
            if not ml:
                self.handling = False

        if self.handling:
            self.scroll_value = max(min((my-self.rect.y)/self.rect.h, 1.0),0.0)

        handle_y = (self.rect.h - self.handle_height)*self.scroll_value
        self.handle_rect.centery = handle_y


    def draw(self):
        pygame.draw.rect(g.screen, self.bar_color, self.rect, border_radius=8)    
        pygame.draw.rect(g.screen, self.handle_color, self.handle_rect)

class Button(Control):
    """
    Class for all sorts of buttons
    """
    def __init__(self, rect, unpressed_gfx, highlighted_gfx, pressed_gfx, active_states, function):
        super().__init__(rect, active_states)
        self.unpressed_gfx = unpressed_gfx
        self.highlighted_gfx = highlighted_gfx
        self.pressed_gfx = pressed_gfx

        self.highlighted = False
        self.pressed = False

        #function to call on pressed
        self.function = function

    def press(self):
        self.function()

    def update(self):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint((mx, my)):
            self.highlighted = True
        else:
            self.highlighted = False

        ml = pygame.mouse.get_pressed()[0]
        if ml:
            if self.highlighted:
                self.pressed = True
            else:
                self.pressed = False
        else:
            self.pressed = False

    def click(self):
        self.press()
        return True

    def draw(self):
        if self.highlighted:
            if self.pressed:
                surf = self.pressed_gfx
            else:
                surf = self.highlighted_gfx
        else:
            surf = self.unpressed_gfx
        g.screen.blit(surf, self.rect)

class TextBox(Control):
    """
    Class for showing text.
    The text can either be static or evaluated over time
    """
    def __init__(self, pos, text, font, timer, color, do_eval_text, active_states, cx=True, cy=False):
        self.pos = pos
        self.font = font
        self.color = color
        #whether to center this control
        self.cx = cx
        self.cy = cy

        self.do_eval_text = do_eval_text
        if self.do_eval_text:
            self.eval_text = ""

        self.text = text

        if self.do_eval_text:
            self.set_text(str(eval(self.text)))
        else:
            self.set_text(self.text)

        if timer:
            deletion_event = pygame.event.Event(g.TEXT_BOX_DELETE_EVENT, {"control":self})
            pygame.time.set_timer(deletion_event, timer*1000, loops=1)

        super().__init__(pygame.Rect(pos[0], pos[1], 1, 1), active_states)

    def update(self):
        if self.do_eval_text:
            old_text = self.eval_text
            self.eval_text = str(eval(self.text))

            if old_text != self.eval_text:
                self.set_text(self.eval_text)

    def set_text(self, text):
        self.rendered_text = self.font.render(text, True, self.color)
        self.rendered_shadow_text = self.font.render(text, True, "black")

    def draw(self):
        x, y = self.pos
        if self.cx:
            x -= self.rendered_text.get_width()/2
        if self.cy:
            y -= self.rendered_text.get_height()/2

        shadow_x = x + 2
        shadow_y = y + 2
        g.screen.blit(self.rendered_shadow_text, (shadow_x, shadow_y))

        g.screen.blit(self.rendered_text, (x,y))


        
def create_button(rect, text, font, function, color, background_color, active_states, border_width=32, border_radius=32):
    """
    Create a button from set parameters. Convinience function
    """
    #create normal surf
    button_text = font.render(text, True, "black")
    button_shadow_text = font.render(text, True, "black")
    button_shadow_text.set_alpha(128)

    button_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    button_surf.fill((0,0,0,0))

    pygame.draw.rect(button_surf, background_color, pygame.Rect(0,0,rect.w,rect.h), border_radius=border_radius)
    border_rect = pygame.Rect(0,0,rect.w,rect.h)
    border_rect.center = (rect.w/2, rect.h/2)
    pygame.draw.rect(button_surf, "gray", border_rect, width=border_width, border_radius=border_radius)

    text_width, text_height = button_text.get_size()
    button_surf.blit(button_text, ( (rect.w/2)-(text_width/2) , (rect.h/2)-(text_height/2) ))
    shadow_x = 1
    shadow_y = 1
    button_surf.blit(button_shadow_text, ( (rect.w/2)-(text_width/2)+shadow_x , (rect.h/2)-(text_height/2)+shadow_y ))

    #darkening effect (for highlighting and pressing)
    darkening_surf = pygame.Surface((rect.w, rect.h))
    darkening_surf.fill((64,64,64))

    #create highlight surf
    button_highlight_surf = button_surf.copy()
    button_highlight_surf.blit(darkening_surf, (0,0), special_flags=pygame.BLEND_SUB)

    #create press surf
    button_pressed_surf = button_surf.copy()
    button_pressed_surf.blit(darkening_surf, (0,0), special_flags=pygame.BLEND_SUB)
    button_pressed_surf.blit(darkening_surf, (0,0), special_flags=pygame.BLEND_SUB)

    return Button(rect, button_surf, button_highlight_surf, button_pressed_surf, active_states, function)



class Gallery(Control):
    """
    Control for showing a gallery of microgames
    """
    def __init__(self, rect, game_classes, active_states):
        super().__init__(rect, active_states)

        self.game_classes = game_classes

        self.thumbnail_width = 64
        self.thumbnail_height = 64

        self.scroll = 0
        self.max_scroll = 0

        self.selected_index = None
        self.pressed = False

        self.thumbnails = []
        for game_class in game_classes:
            game = game_class()
            thumbnail = pygame.transform.scale(game.metadata["thumbnail"], (self.thumbnail_width, self.thumbnail_height) )
        
            self.thumbnails.append(thumbnail)

        self.thumbnail_rects = []

        rect = pygame.Rect(self.rect.right-16, 0, 16, self.rect.h)
        self.scrollbar = ScrollBar(rect, "red", "blue", self.active_states, handle_height=16)

    def update(self):
        mx, my = pygame.mouse.get_pos()
        ml, mm, mr = pygame.mouse.get_pressed()
        i = 0

        #check for click
        self.selected_index = None
        for rect in self.thumbnail_rects:
            if rect.collidepoint((mx, my)):
                self.selected_index = i

                break
            i += 1

        if ml:
            self.pressed = True
        else:
            self.pressed = False

        self.scroll = self.scrollbar.scroll_value*self.max_scroll

    def click(self):
        if self.pressed and self.selected_index is not None:
            g.state = "main_menu"
            
            game_event = pygame.event.Event(g.RUN_GAME_EVENT, {"game":self.game_classes[self.selected_index]})
            pygame.time.set_timer(game_event, 1000, loops=1)
            return True
        else:
            return False

    def draw(self):
        self.thumbnail_rects = []

        sep_width = 10
        sep_height = 10

        thumbnail_rect = pygame.Rect(sep_width, sep_height-self.scroll+self.rect.y, self.thumbnail_width, self.thumbnail_height)

        i = 0
        for thumbnail in self.thumbnails:
            if self.rect.colliderect(thumbnail_rect):
                #crop and draw thumbnail
                if not thumbnail_rect in self.rect:
                    thumbnail_crop_rect = thumbnail_rect.clip(self.rect)
                    thumbnail_crop_rect.x = 0
                    thumbnail_crop_rect.y = thumbnail_rect.height-thumbnail_crop_rect.height
                    
                    g.screen.blit(thumbnail, thumbnail_rect.move(0,thumbnail_rect.height-thumbnail_crop_rect.height), thumbnail_crop_rect)
                else:
                    g.screen.blit(thumbnail, thumbnail_rect)

            self.thumbnail_rects.append(thumbnail_rect.copy())

            if i is self.selected_index:
                if self.pressed:
                    color = "green"
                else:
                    color = "white"
                pygame.draw.rect(g.screen, color, thumbnail_rect, 2)

            thumbnail_rect.x += self.thumbnail_width+sep_width
            if thumbnail_rect.right > self.rect.right-sep_width:
                thumbnail_rect.x = sep_width
                thumbnail_rect.y += self.thumbnail_height+sep_height

            i += 1

        self.max_scroll = thumbnail_rect.bottom