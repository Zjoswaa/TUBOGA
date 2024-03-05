import pygame as pg


class Game(object):
    def __init__(self, width, height, title):
        # PyGame initialization
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        pg.display.set_icon(pg.image.load("res/icon.png"))

        # Game logic variables
        self.window_width = width
        self.window_height = height
        self.state_stack = []

        self.bg_color = (150, 150, 200)
        self.text_color = (0, 0, 0)
        self.color_red = (255, 0, 0)
        self.color_purple = (112, 48, 160)
        self.color_blue = (0, 176, 240)
        self.color_brown = (198, 89, 17)
        self.color_yellow = (255, 255, 0)
        self.color_green = (146, 208, 80)

        self.clock = pg.time.Clock()
        self.fps = 60

        self.font_100 = pg.font.Font("res/fonts/pixeltype.ttf", 100)
        self.font_50 = pg.font.Font("res/fonts/pixeltype.ttf", 50)

        self.pause_icon = pg.image.load("res/icon.png").convert_alpha()

    # Shows the start menu
    def start(self):
        hint_clock = 0
        hint_blink_speed = 30
        hint_black = True
        hint_color = (0, 0, 0)
        play_button = pg.Rect((80, 500), (200, 100))
        play_text = self.font_100.render("Play", False, self.color_blue).convert()
        quit_button = pg.Rect((1000, 500), (200, 100))
        quit_text = self.font_100.render("Quit", False, self.color_purple).convert()
        hint_text = [self.font_50.render("Press any key to play", False, hint_color).convert(),
                     self.font_50.render("ESC to quit", False, self.text_color).convert()]

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if quit_button.collidepoint(pg.mouse.get_pos()):
                        pg.quit()
                        exit(0)
                    elif play_button.collidepoint(pg.mouse.get_pos()):
                        # Go to main game loop
                        self.state_stack.append("GAME")
                        self.game()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        exit(0)
                    else:  # Any key pressed except escape
                        # Go to main game loop
                        self.state_stack.append("GAME")
                        self.game()

            # Update

            hint_clock += 1
            if hint_clock == hint_blink_speed:
                hint_clock = 0
                hint_black = not hint_black

            # Render

            self.screen.fill(self.bg_color)
            # Play button and text
            pg.draw.rect(self.screen, self.color_green, play_button)
            if play_button.collidepoint(pg.mouse.get_pos()):
                play_text = self.font_100.render("Play", False, self.color_brown).convert()
            else:
                play_text = self.font_100.render("Play", False, self.color_blue).convert()
            self.screen.blit(play_text, play_text.get_rect(center=(play_button.centerx + 5, play_button.centery + 5)))
            # Quit button and text
            pg.draw.rect(self.screen, self.color_red, quit_button)
            if quit_button.collidepoint(pg.mouse.get_pos()):
                quit_text = self.font_100.render("Quit", False, self.color_yellow).convert()
            else:
                quit_text = self.font_100.render("Quit", False, self.color_purple).convert()
            self.screen.blit(quit_text, quit_text.get_rect(center=(quit_button.centerx + 5, quit_button.centery + 5)))
            # Game icon
            self.screen.blit(self.pause_icon, self.pause_icon.get_rect(center=(self.window_width / 2, self.window_height / 2)))
            # Button press hint text
            if hint_black:
                hint_color = (0, 0, 0)
            else:
                hint_color = (255, 255, 255)
            hint_text[0] = self.font_50.render("Press any key to play", False, hint_color).convert()
            self.screen.blit(hint_text[0], hint_text[0].get_rect(center=(self.window_width / 2, 200)))
            # ESC to quit text
            self.screen.blit(hint_text[1], hint_text[1].get_rect(center=(self.window_width / 2, 525)))
            # PyGame Render
            pg.display.update()
            self.clock.tick(self.fps)

    # Shows the pause menu
    def pause(self):
        paused_text = self.font_100.render("Paused", False, self.text_color).convert()
        return_button = pg.Rect((80, 500), (250, 100))
        return_text = self.font_100.render("Return", False, self.color_blue).convert()
        quit_button = pg.Rect((1000, 500), (200, 100))
        quit_text = self.font_100.render("Quit", False, self.color_purple).convert()

        while self.state_stack[-1] == "PAUSE":
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if quit_button.collidepoint(pg.mouse.get_pos()):
                        pg.quit()
                        exit(0)
                    elif return_button.collidepoint(pg.mouse.get_pos()):
                        # Go back to previous state
                        self.state_stack.pop()
                        break
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # Go back to previous state
                        self.state_stack.pop()
                        break

            # Update

            # Render

            self.screen.fill(self.bg_color)
            # Paused text
            self.screen.blit(paused_text, paused_text.get_rect(center=(self.window_width / 2, 100)))
            # Return button
            pg.draw.rect(self.screen, self.color_green, return_button)
            if return_button.collidepoint(pg.mouse.get_pos()):
                return_text = self.font_100.render("Return", False, self.color_brown).convert()
            else:
                return_text = self.font_100.render("Return", False, self.color_blue).convert()
            self.screen.blit(return_text, return_text.get_rect(center=(return_button.centerx + 5, return_button.centery + 5)))
            # Quit button
            pg.draw.rect(self.screen, self.color_red, quit_button)
            if quit_button.collidepoint(pg.mouse.get_pos()):
                quit_text = self.font_100.render("Quit", False, self.color_yellow).convert()
            else:
                quit_text = self.font_100.render("Quit", False, self.color_purple).convert()
            self.screen.blit(quit_text, quit_text.get_rect(center=(quit_button.centerx + 5, quit_button.centery + 5)))
            # Game icon
            self.screen.blit(self.pause_icon, self.pause_icon.get_rect(center=(self.window_width / 2, self.window_height / 2)))
            # PyGame Render
            pg.display.update()
            self.clock.tick(self.fps)

    # Shows the game
    def game(self):
        text = self.font_100.render("Game", False, self.text_color).convert()

        while self.state_stack[-1] == "GAME":
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # Show pause menu
                        self.state_stack.append("PAUSE")
                        self.pause()

            # Update

            # Render
            self.screen.fill(self.bg_color)
            self.screen.blit(text, text.get_rect(center=(self.window_width / 2, self.window_height / 2)))

            pg.display.update()
            self.clock.tick(self.fps)
    