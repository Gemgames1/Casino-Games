import pygame
from pygame.constants import APPINPUTFOCUS
from pygame.version import ver
from tbVectors import Vector
from PygameTemplates import Button
from deckfuncs import get_deck
import os

card_imgs = {}
for img in os.listdir("images/cards"):
    card_imgs[img.split(".")[0]] = pygame.image.load(f"images/cards/{img}")

hit_btn = Button(0, 0, 0, 0, message="HIT", fit_text_options="text", base_colour=None, horizontal_alignment="center", verticle_alignment="center")
stand_btn = Button(0, 0, 0, 0, message="STAND", fit_text_options="text", base_colour=None, horizontal_alignment="center", verticle_alignment="center")


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.deck = get_deck()
        self.show = False

        self.hand = [self.draw_card(), self.draw_card()]
        self.dealer = [self.draw_card(), self.draw_card()]

        self.max_anim = 5000
        self.hand_anim = 0
        self.dealer_anim = 0

    def draw_card(self):
        return self.deck.pop(0)

    def hit(self):
        self.hand.append(self.draw_card())
        self.hand_anim = self.max_anim

    def display_cards(self, wn):
        c_width = card_imgs["back"].get_width()
        c_height = card_imgs["back"].get_height()

        top = 10
        bottom = self.height - c_height - 10
        left = self.width / 2 - c_width * 1.5
        right = self.width / 2 + c_width / 2

        hand_extra = (right - left) / (len(self.hand) - 1)
        for i, card in enumerate(self.hand):
            anim_offset = 0
            if i != 0:
                if self.hand_anim != 0:
                    if i == len(self.hand) - 1:
                        anim_offset = Vector.squish(self.hand_anim, 0, self.max_anim, 0, self.width - right)
                        self.hand_anim -= 50
                    else:
                        anim_offset = Vector.squish(self.hand_anim, 0, self.max_anim, 0, hand_extra) * (i / (len(self.hand) - 2))
            wn.blit(card_imgs[card], (left + hand_extra * i + anim_offset, bottom))

        if self.hand_anim < 0:
            self.hand_anim = 0

        dealer_extra = (right - left) / (len(self.dealer) - 1)
        for i, card in enumerate(self.dealer):
            anim_offset = 0
            if i != 0:
                if self.dealer_anim != 0:
                    if i == len(self.dealer) - 1:
                        anim_offset = Vector.squish(self.dealer_anim, 0, self.max_anim, 0, left)
                        self.dealer_anim -= 50
                    else:
                        anim_offset = Vector.squish(self.dealer_anim, 0, self.max_anim, 0, dealer_extra) * (i / (len(self.dealer) - 2))
            
            if not self.show and i == 1:
                wn.blit(card_imgs["back"], (right - dealer_extra * i - anim_offset, top))
            else:
                wn.blit(card_imgs[card], (right - dealer_extra * i - anim_offset, top))

        if self.dealer_anim < 0:
            self.dealer_anim = 0



def setup(width, height):
    c_height = int(height / 3)
    c_width = int(c_height / 1.5)
    for card in card_imgs:
        card_imgs[card] = pygame.transform.scale(card_imgs[card], (c_width, c_height))

    hit_btn.width = c_width
    hit_btn.height = int(c_height / 3)
    hit_btn.fit_text(hit_btn.message)
    hit_btn.x = int(width / 2 - c_width - hit_btn.width / 2)
    hit_btn.y = int(height / 2 - hit_btn.height / 2)

    stand_btn.width = c_width
    stand_btn.height = int(c_height / 3)
    stand_btn.fit_text(stand_btn.message)
    stand_btn.x = int(width / 2 + c_width - stand_btn.width / 2)
    stand_btn.y = int(height / 2 - stand_btn.height / 2)
    

def redraw(wn, bg_img, game):
    wn.blit(bg_img, (0, 0))

    game.display_cards(wn)
    hit_btn.draw(wn)
    stand_btn.draw(wn)

    pygame.display.update()


def Blackjack(wn, WIDTH, HEIGHT, bg_img):
    setup(WIDTH, HEIGHT)

    game = Game(WIDTH, HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if hit_btn.click(mouse):
                        game.hit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
            
            if event.type == pygame.QUIT:
                return "quit"

        redraw(wn, bg_img, game)
