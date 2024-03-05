import pygame as pg
import sys

# Initialize Pygame
pg.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Multiple Choice Quiz")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)

# Define fonts
font = pg.font.Font(None, 32)

# Define questions, choices, and answers
questions = [
    "Wat is de oprichter van Microsoft, Bill Gates, zijn echte volledige naam?",
    "In welk jaar richtte Bill Gates Microsoft op?",
    "Welke prestigieuze onderscheiding heeft Bill Gates ontvangen voor zijn filantropisch werk?",
    "Wat is de naam van de stichting die Bill en Melinda Gates hebben opgericht om wereldwijde gezondheids- en onderwijsproblemen aan te pakken?",
    "Wat is de geschatte nettowaarde van Bill Gates volgens Forbes in 2022?"
]

choices = [
    ["a) William Gates III", "b) Billy Gates", "c) William Henry Gates II", "d) Billie Gates"],
    ["a) 1975", "b) 1980", "c) 1985", "d) 1990"],
    ["a) Nobel Peaces Prize", "b) Pulitzer Prize", "c) Presidential Medal of Freedom", "d) Legion of Honour"],
    ["a) Gates Foundation", "b) Hope Foundation", "c) Gates & Melinda Foundation", "d) Bill & Melinda Gates Foundation"],
    ["a) $50 miljard", "b) $100 miljard", "c) $150 miljard", "d) $200 miljard"]
]

# Answers
answers = [0, 0, 0, 0, 0] # Index of the correct choice for each question

# # Vragen
# questions = [
#     "Wat was de oorspronkelijke naam van het sociale netwerk dat Mark Zuckerberg oprichtte?",
#     "In welk jaar richtte Mark Zuckerberg Facebook op?",
#     "Welke universiteit heeft Mark Zuckerberg bijgewoond voordat hij Facebook oprichtte?",
#     "Hoe oud was Mark Zuckerberg toen hij Facebook lanceerde?",
#     "Wat is de geschatte nettowaarde van Mark Zuckerberg volgens Forbes in 2022?"
# ]

# # Keuzes
# choices = [
#     ["a) MySpace", "b) Facebook", "c) Twitter", "d) LinkedIn"],
#     ["a) 2002", "b) 2004", "c) 2006", "d) 2008"],
#     ["a) Harvard University", "b) Stanford University", "c) Massachusetts Institute of Technology (MIT)", "d) Yale University"],
#     ["a) 18", "b) 20", "c) 22", "d) 24"],
#     ["a) $50 miljard", "b) $100 miljard", "c) $200 miljard", "d) $500 miljard"]
# ]

# # Antwoorden
# answers = ['b', 'b', 'a', 'c', 'c']


# Define variables
score = 0
current_question = 0

# Function to display text
def display_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to display question and choices with buttons
def display_question(question_num):
    screen.fill(WHITE)
    display_text(questions[question_num], 50, 50)
    
    # Display choices with buttons
    for i, choice in enumerate(choices[question_num]):
        button_rect = pg.Rect(50, 100 + i * 50, 400, 40)
        
        # Change button color when hovered over
        if button_rect.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(screen, LIGHT_GRAY, button_rect)
        else:
            pg.draw.rect(screen, GRAY, button_rect)
        
        display_text(choice, button_rect.x + 10, button_rect.y + 10, BLACK)

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    display_question(current_question)
    
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            # Check if any button is clicked
            for i, choice in enumerate(choices[current_question]):
                button_rect = pg.Rect(50, 100 + i * 50, 200, 40)
                if button_rect.collidepoint(event.pos):
                    # Check if the clicked button is correct
                    if i == answers[current_question]:
                        score += 1
                    # Move to the next question
                    current_question += 1
                    if current_question >= len(questions):
                        running = False
                        
    pg.display.flip()

# Display final score
screen.fill(WHITE)
display_text(f"Your score is: {score}", 50, 50)
pg.display.flip()

# Wait for a moment before quitting
pg.time.wait(3000)
pg.quit()
sys.exit()
