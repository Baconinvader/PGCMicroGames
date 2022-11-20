import global_values as g
import controls

def handle_input():
    event_list = []
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            for control in g.controls:
                if control.rect.collidepoint(event.pos) and control.get_active():
                    result = control.click()
                    if result:
                        break

        #filter out certain events
        if event.type == pygame.QUIT: #quit
            pygame.display.quit()
            import sys
            sys.exit()

        elif event.type == g.MICROGAME_END_EVENT: #fully finish game
            g.current_game.end()

        elif event.type == g.MICROGAME_TIMEOUT_EVENT: #run out of time for game
            if event.game == type(g.current_game) and not g.current_game.ended:
                g.current_game.lose()

        elif event.type == g.TEXT_BOX_DELETE_EVENT: #delete text box
            for control in g.controls:
                if control == event.control:
                    control.delete()
                    break

        elif event.type == g.RUN_GAME_EVENT: #run new microgame
            new_game = event.game()
            new_game.run()

        else:
            if event.type == pygame.MOUSEWHEEL: #scroll gallery
                for control in g.controls:
                    if type(control) == controls.ScrollBar:
                        if control.get_active():
                            control.scroll_value = min(max(control.scroll_value-(0.01*event.y), 0), 1.0)
            
            event_list.append(event)

    if g.current_game:
        g.current_game.handle_input(event_list)

def update(dt):
    if g.current_game:
        g.current_game.update(dt)
    for control in g.controls:
        if control.get_active():
            control.update()

def load_game(game):
    """
    Load a new microgame
    """
    g.current_game = game

def draw():
    if g.current_game:
        #draw microgame at center of screen
        microgame_surf = g.current_game.draw()

        width = g.current_game.metadata["width"]
        height = g.current_game.metadata["height"]

        microgame_rect = pygame.Rect(0, 0, width, height)
        microgame_rect.center = (g.WIDTH/2, g.HEIGHT/2)

        g.screen.blit(microgame_surf, microgame_rect)

    for control in g.controls:
        if control.get_active():
            control.draw()

def enter_runner_mode():
    pass

def enter_gallery_mode():
    g.state = "gallery"

def back_to_menu():
    g.state = "main_menu"

def run_test_game():
    import test_game
    game = test_game.TestGame()
    game.run()

if __name__ == "__main__":
    import pygame
    
    clock = pygame.time.Clock()
    g.screen = pygame.display.set_mode((g.WIDTH, g.HEIGHT))

    pygame.font.init()
    default_font = pygame.font.SysFont("Consolas", 32)

    debug_text = controls.TextBox((g.WIDTH-200, 0), "g.state", default_font, 0, "white", True, set(("main_menu","gallery")), cx=True, cy=False)

    run_button = controls.create_button(pygame.Rect(0,32,128,64), "Runner", default_font, enter_runner_mode, "red", "white", set(("main_menu",)), border_width=4, border_radius=8)
    gallery_button = controls.create_button(pygame.Rect(0,96,128,64), "Gallery", default_font, enter_gallery_mode, "red", "white", set(("main_menu",)), border_width=4, border_radius=8)
    test_button = controls.create_button(pygame.Rect(0,160,128,64), "Test", default_font, run_test_game, "red", "white", set(("main_menu",)), border_width=4, border_radius=8)

    import test_game
    controls.Gallery(pygame.Rect(0, 50, g.WIDTH, g.HEIGHT), [test_game.TestGame]*50, set(("gallery",)) )
    return_to_menu_button = controls.create_button(pygame.Rect(g.WIDTH-110,g.HEIGHT-60,100,50), "Back", default_font, back_to_menu, "red", "white", set(("gallery",)), border_width=4)


    #setup window
    pygame.display.set_caption("Microgames")

    #core loop
    dt = 0
    while True:
        g.screen.fill("black")
        handle_input()
        update(dt)
        draw()
        pygame.display.flip()
        dt = clock.tick()

