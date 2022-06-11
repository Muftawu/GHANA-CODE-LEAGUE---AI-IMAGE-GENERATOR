import pygame
from Buttons import Button
import Image_Scrapper as Im
import cv2
import numpy as np
import requests

pygame.init()

WIDTH, HEIGHT = 1300, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_select = screen
pygame.display.set_caption("Image Genereator From Test AI")

clock = pygame.time.Clock()

# Parameters
font = pygame.font.Font("Marcellus-Regular.ttf", 35)
textPrompt = "Enter text to generate image"
textHeading = "AI Image Generator"
main_font_color = (200, 150, 180)
blue = (0, 0, 255)
green = (0, 255, 0)
text_box_color = (100, 100, 100)
text_box_rect = (00, 170, 700, 100)

# User input parameters
user_input_text = " "
input_active = True
red = (255, 0, 0)
color = (102, 102, 51)
white = (255, 255, 255)


# Image Scrapper objects

def PutText(text, x, y, color):
    heading = font.render(text, True, color)
    screen.blit(heading, (x, y))


def textBox(color, rect):
    pygame.draw.rect(screen, color, rect, 0, 40)


def main():
    run = True
    # screen.fill((100, 200, 100))

    # draw our buttons
    button1 = Button(220, 430, 150, 70)

    while run:
        clock.tick(30)

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False

            elif events.type == pygame.MOUSEBUTTONDOWN:
                global input_active, user_input_text
                input_active = True
                # user_input_text = "|"

            if events.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                generate_button_rect = (250, 490, 190, 70)

                # Revisit this portion again
                if 250 < x < 440 and 490 < y < 560:
                    color = (0, 200, 0)
                    textBox(color, generate_button_rect)
                    PutText(str("Generate"), 270, 500, red)

                    # Scrapper objects
                    # wd = Im.load_web_browser(Im.PATH)
                    wd = Im.load_web_browser(Im.PATH)
                    urls = Im.get_images_from_google(wd, 1, 1, user_input_text)

                    for i, url in enumerate(urls):
                        wd.minimize_window()
                        Im.display_image("imgs/", url, str(i) + ".jpg")
                        downloaded_img = cv2.imread("imgs/0.jpg")
                        Im.place_image_on_UI(screen, 750, 20, downloaded_img)
                    wd.quit()
                    # wd.close()

            elif events.type == pygame.KEYDOWN and input_active:
                if events.key == pygame.K_RETURN:
                    input_active = False
                elif events.key == pygame.K_BACKSPACE:
                    user_input_text = user_input_text[:-1]
                elif events.key == pygame.K_ESCAPE:
                    user_input_text = ""
                else:
                    user_input_text += events.unicode

            textBox((0, 190, 0), (250, 490, 190, 70))
            # textBox(text_box_color, text_box_rect)
            PutText(str("Generate"), 270, 500, white)
            PutText(textHeading, 190, 20, main_font_color)
            PutText(textPrompt, 100, 290, main_font_color)
            PutText("Use the ESC key to clear all text", 80, 380, main_font_color)
            PutText(user_input_text, 90, 170, (255, 0, 0))
            pygame.draw.rect(screen, white, (750, 20, 500, 600), 1)

        # screen.fill(0)
        textBox((0, 0, 0), text_box_rect)
        pygame.draw.line(screen, (255, 255, 77), (10, 220), (700, 220), 2)
        text_surf = font.render(user_input_text, True, (255, 0, 0))
        screen.blit(text_surf, text_box_rect)
        # pygame.display.update(text_box_rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()
