import pygame
from pygame.constants import MOUSEBUTTONDOWN
from tbVectors import Vector
from PygameTemplates import Button, Label
from deckfuncs import get_deck
import os

card_imgs = {}
for img in os.listdir("images/cards"):
    card_imgs[img.split(".")[0]] = pygame.image.load(f"images/cards/{img}")

hit_btn = Button(0, 0, 0, 0, message="HIT", fit_text_options="text", base_colour=None, horizontal_alignment="center", verticle_alignment="center")
stand_btn = Button(0, 0, 0, 0, message="STAND", fit_text_options="text", base_colour=None, horizontal_alignment="center", verticle_alignment="center")
bust_lbl = Label(0, 0, 0, 0, message="BUST", font_colour=(255, 0, 0), bold=True, fit_text_options="text", base_colour=None, border_colour=None, horizontal_alignment="center", verticle_alignment="center")
outcome_lbl = Label(0, 0, 0, 0, message="", font_colour=(0, 0, 0), fit_text_options="text", base_colour=None, border_colour=None, horizontal_alignment="center", verticle_alignment="center")
back_btn = Button(0, 0, 0, 0, message="BACK", fit_text_options="text", base_colour=None, horizontal_alignment="center", verticle_alignment="center")
play_again_btn = Button(0, 0, 0, 0, message="PLAY AGAIN", fit_text_options="text", base_colour=None, horizontal_alignment="center", verticle_alignment="center")


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.deck = get_deck()
        self.show = False

        self.hand_total = 0
        self.dealer_total = 0
        self.hand_ace = 0
        self.dealer_ace = 0
        self.hand = [self.draw_card(True), self.draw_card(True)]
        self.dealer = [self.draw_card(False), self.draw_card(False)]

        self.max_anim = 4999
        self.hand_anim = 0
        self.dealer_anim = 0
        self.flip_card = 0
        self.dealing = False

        self.hand_bust = False
        self.dealer_bust = False
        self.stood = False
        self.playing = False
        self.game_over = False

    def draw_card(self, hand):
        card = self.deck.pop(0)
        value = card[:-1]
        if hand:
            if value.isnumeric():
                self.hand_total += int(value)
            elif value == "A":
                self.hand_total += 11
                self.hand_ace += 1
            else:
                self.hand_total += 10
            if self.hand_total > 21 and self.hand_ace:
                self.hand_total -= 10
                self.hand_ace -= 1
        else:
            if value.isnumeric():
                self.dealer_total += int(value)
            elif value == "A":
                self.dealer_total += 11
                self.dealer_ace += 1
            else:
                self.dealer_total += 10
            if self.dealer_total > 21 and self.dealer_ace:
                self.dealer_total -= 10
                self.dealer_ace -= 1

        return card
    
    def is_bust(self, hand=True):
        if hand:
            self.hand_bust = self.hand_total > 21
            if self.hand_bust:
                self.stand()
        else:
            self.dealer_bust = self.dealer_total > 21

    def hit(self):
        self.playing = True
        if not self.dealing and not self.stood:
            self.hand.append(self.draw_card(True))
            self.hand_anim = self.max_anim
            self.dealing = True

    def stand(self):
        if not self.dealing:
            self.stood = True
            self.show = True
            self.flip_card = self.max_anim
            self.dealing = True

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
            self.dealing = False
            self.is_bust()

        dealer_extra = (right - left) / (len(self.dealer) - 1)
        for i, card in enumerate(self.dealer):
            anim_offset = 0
            if i != 0:
                if self.dealer_anim != 0:
                    if i == len(self.dealer) - 1:
                        anim_offset = Vector.squish(self.dealer_anim, 0, self.max_anim, 0, self.width - right)
                        self.dealer_anim -= 50
                    else:
                        anim_offset = Vector.squish(self.dealer_anim, 0, self.max_anim, 0, dealer_extra) * (i / (len(self.dealer) - 2))
            
            if not self.show and i == 1:
                wn.blit(card_imgs["back"], (left + dealer_extra * i + anim_offset, top))
            else:
                wn.blit(card_imgs[card], (left + dealer_extra * i + anim_offset, top))

        if self.dealer_anim < 0:
            self.dealer_anim = 0
            self.dealing = False

    def dealers_turn(self):
        if self.flip_card == 0:
            if self.dealer_total < 17:
                if not self.dealing:
                    self.dealer.append(self.draw_card(False))
                    self.dealer_anim = self.max_anim
                    self.dealing = True
                    self.is_bust(False)
            elif not self.dealing:
                return self.winner()

        elif self.flip_card < 0:
            self.flip_card = 0
            self.dealing = False
        else:
            self.flip_card -= 100
        return ""

    def winner(self):
        self.playing = False
        self.game_over = True
        if self.hand_bust and self.dealer_bust:
            return "Draw"
        elif self.hand_bust and not self.dealer_bust:
            return "You Lose"
        elif not self.hand_bust and self.dealer_bust:
            return "You Win"
        elif self.hand_total == self.dealer_total:
            return "Draw"
        elif self.hand_total < self.dealer_total:
            return "You Lose"
        elif self.hand_total > self.dealer_total:
            return "You Win"


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
    
    bust_lbl.width = c_width
    bust_lbl.height = int(c_height / 3)
    bust_lbl.fit_text(bust_lbl.message)
    bust_lbl.x = int(width / 2 - bust_lbl.width / 2)
    bust_lbl.y = int(height / 2 - bust_lbl.height / 2)
    
    outcome_lbl.width = c_width
    outcome_lbl.height = int(c_height / 3)
    outcome_lbl.fit_text(outcome_lbl.message)
    outcome_lbl.x = int(width / 2 - outcome_lbl.width / 2)
    outcome_lbl.y = int(height / 2 - outcome_lbl.height * 1.5)
    outcome_lbl.message = ""
    
    back_btn.width = int(c_width / 2)
    back_btn.height = int(c_height / 6)
    back_btn.fit_text(back_btn.message)
    back_btn.x = 10
    back_btn.y = 10
    
    play_again_btn.width = int(c_width / 2)
    play_again_btn.height = int(c_height / 6)
    play_again_btn.fit_text(play_again_btn.message)
    play_again_btn.x = int(width / 2 - play_again_btn.width / 2)
    play_again_btn.y = int(height / 2 + bust_lbl.height / 2 + play_again_btn.height / 2)
    

def redraw(wn, bg_img, game):
    wn.blit(bg_img, (0, 0))

    game.display_cards(wn)
    hit_btn.draw(wn)
    stand_btn.draw(wn)
    if game.hand_bust:
        bust_lbl.draw(wn)
    outcome_lbl.draw(wn)
    if not game.playing:
        back_btn.draw(wn)
    if game.game_over:
        play_again_btn.draw(wn)

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
                    if stand_btn.click(mouse):
                        game.stand()
                    if back_btn.click(mouse) and not game.playing:
                        return "back"
                    if play_again_btn.click(mouse) and game.game_over:
                        setup(WIDTH, HEIGHT)
                        game = Game(WIDTH, HEIGHT)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
            
            if event.type == pygame.QUIT:
                return "quit"

        if game.stood:
            outcome_lbl.message = game.dealers_turn()

        redraw(wn, bg_img, game)
