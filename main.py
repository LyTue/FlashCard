from tkinter import *
import time
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}

try:
    data = pandas.read_csv("data/word_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ------------------ ACTION --------------------->
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    print(current_card)
    global word_learned
    word_learned.append(current_card)
    print(word_learned)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=img_card_front)
    flip_timer = window.after(3000, func=answer_card)


def answer_card():
    global current_card
    canvas.itemconfig(canvas_image, image=img_card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


# ------------------------ ADD WORD LEARED TO NEW CSV ---------- >
word_learned = []


def word_not_know():
    to_learn.remove(current_card)
    print(len(to_learn))
    next_card()
    word_learned = pandas.DataFrame(to_learn)
    word_learned.to_csv("data/word_to_learn.csv", index=False)


# Setup

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=answer_card)

# IMAGE-CARD
img_card_front = PhotoImage(file="./images/card_front.png")
img_card_back = PhotoImage(file="./images/card_back.png")
# Cards

canvas = Canvas(height=526, width=800, background=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(410, 270, image=img_card_front)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 270, text="", font=("Ariel", 50, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons

right_img_button = PhotoImage(file="./images/right.png")
button_right = Button(image=right_img_button, highlightthickness=0, command=word_not_know)
button_right.grid(column=0, row=1)

wrong_img_button = PhotoImage(file="./images/wrong.png")
button_wrong = Button(image=wrong_img_button, highlightthickness=0, command=next_card)
button_wrong.grid(column=1, row=1)

# 

next_card()

window.mainloop()
