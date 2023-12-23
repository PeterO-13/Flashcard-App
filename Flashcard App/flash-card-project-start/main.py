from tkinter import *
import random
import pandas

# Attempt to load existing data file or load the default if not found
try:
    data_file = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data_file = pandas.read_csv("data/french_words.csv")
    main_data = [{"english": row.English, "french": row.French} for index, row in data_file.iterrows()]
else:
    main_data = [{"english": row.english, "french": row.french} for index, row in data_file.iterrows()]

BACKGROUND_COLOR = "#B1DDC6"
word = {}

# Function to fetch a random word from the dataset
def get_word():
    return random.choice(main_data)

# Function to display the English word on the flashcard
def flip_card():
    global word
    canvas.itemconfig(card_image, image=bg_image_back)
    canvas.itemconfig(title_text, text="English", fill="#ffffff")
    canvas.itemconfig(word_text, text=word["english"], fill="#ffffff")

# Function to display the French word on the flashcard and set a timer to flip the card automatically
def set_word():
    global word, flip_timer
    window.after_cancel(flip_timer)
    word = get_word()
    canvas.itemconfig(card_image, image=bg_image_front)
    canvas.itemconfig(title_text, text="French", fill="#000000")
    canvas.itemconfig(word_text, text=word["french"], fill="#000000")
    flip_timer = window.after(3000, flip_card)

# Function to mark a word as known, remove it from the study list, and save the updated list to a file
def is_known():
    global word
    main_data.remove(word)
    data = pandas.DataFrame(main_data)
    data.to_csv("data/words_to_learn.csv")
    set_word()
    print(len(main_data))

# WINDOW SETUP
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flash Cards")
flip_timer = window.after(3000, flip_card)

# Loading images for card fronts, right button, and wrong button
bg_image_front = PhotoImage(file="images/card_front.png")
bg_image_back = PhotoImage(file="images/card_back.png")
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

# CANVAS SETUP
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(400, 268, image=bg_image_front)
title_text = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, font=("Arial", 60, "bold"))
canvas.grid(row=1, column=1, columnspan=2)

# BUTTONS
right_btn = Button(text="", image=right_image, border=0, highlightthickness=0, command=is_known)
right_btn.grid(row=2, column=2)

wrong_btn = Button(text="", image=wrong_image, highlightthickness=0, border=0, command=set_word)
wrong_btn.grid(row=2, column=1)

# Initial setup to display the first word
set_word()

window.mainloop()
