import pygame
import os
from math import *
pygame.init()

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

screen = pygame.display.Info()
WIDTH = screen.current_w
HEIGHT = screen.current_h
wn = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.FULLSCREEN)

background_img = pygame.transform.scale(
    pygame.image.load("images/table.jpg"), (WIDTH, HEIGHT))

games_list = {"Blackjack": pygame.image.load("images/logos/Blackjack.jpg")}

page = 0


def triangle(surf, p1, p2, p3, clicked, mouse_pos):
    pygame.draw.polygon(surf, (0, 0, 0), [p1, p2, p3])
    if clicked:
        areaOrigi = abs((p2[0] - p1[0]) * (p3[1] - p1[1]) -
                        (p3[0] - p1[0]) * (p2[1] - p1[1]))

        area1 = abs((p1[0] - mouse_pos[0]) * (p2[1] - mouse_pos[1]) -
                    (p2[0] - mouse_pos[0]) * (p1[1] - mouse_pos[1]))
        area2 = abs((p2[0] - mouse_pos[0]) * (p3[1] - mouse_pos[1]) -
                    (p3[0] - mouse_pos[0]) * (p2[1] - mouse_pos[1]))
        area3 = abs((p3[0] - mouse_pos[0]) * (p1[1] - mouse_pos[1]) -
                    (p1[0] - mouse_pos[0]) * (p3[1] - mouse_pos[1]))

        if int(area1 + area2 + area3) == int(areaOrigi):
            return True
    return False


def menu(width, height, mouse_pos=None, clicked=None, first=False):
    global page
    new = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()

    icon_size = min(int(height / 4.5), int(width / 8.25))
    icon_rect = (icon_size, icon_size)
    icon_gap = icon_size / 4

    if not first:
        arrow_x = cos(radians(30)) * icon_gap
        arrow_y = sin(radians(30)) * icon_gap
        if len(games_list) > (page + 1) * 18:
            if triangle(new, (width - 5, height / 2), (width - 5 - arrow_x, height / 2 - arrow_y), (width - 5 - arrow_x, height / 2 + arrow_y), clicked, mouse_pos):
                page += 1

        if page > 0:
            if triangle(new, (5, height / 2), (5 + arrow_x, height / 2 -
                                               arrow_y), (5 + arrow_x, height / 2 + arrow_y), clicked, mouse_pos):
                page -= 1

        x_off = (width - icon_size * 7.25) / 2
        y_off = (height - icon_size * 3.5) / 2

        font = pygame.font.SysFont("arial", int(icon_gap / 2))
        for i, game in enumerate(games_list):
            if page * 18 <= i < (page + 1) * 18:
                x = (i - page * 18) % 6
                y = (i - page * 18) // 6
                pos = (x_off + x * (icon_size + icon_gap), 
                       y_off + y * (icon_size + icon_gap))
                new.blit(games_list[game], pos)
                text = font.render(game, True, (0, 0, 0))
                new.blit(text, (pos[0] + icon_size / 2 -
                         text.get_width() / 2, pos[1] + icon_size))

                if clicked:
                    if x_off + x * (icon_size + icon_gap) <= mouse_pos[0] <= x_off + x * (icon_size + icon_gap) + icon_size:
                        if y_off + y * (icon_size + icon_gap) <= mouse_pos[1] <= y_off + y * (icon_size + icon_gap) + icon_size:
                            return game

        return new
    else:
        for game in games_list:
            img = games_list[game]
            games_list[game] = pygame.transform.scale(img, icon_rect)


def redraw(mouse_pos, clicked):
    game_layer = None
    game_layer = menu(WIDTH, HEIGHT, mouse_pos, clicked)

    if isinstance(game_layer, str):
        return game_layer

    wn.blit(background_img, (0, 0))

    wn.blit(game_layer, (0, 0))

    pygame.display.update()

    return None


def main_menu():

    menu(WIDTH, HEIGHT, first=True)

    run = True
    while run:
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        selected_game = redraw(mouse_pos, clicked)

        if selected_game:
            print("ok")


if __name__ == "__main__":
    main_menu()
