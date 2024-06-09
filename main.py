from tkinter import *
import pandas
import random
import time

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

#================Next Word==========

try:
    data = pandas.read_csv("data/words_to_learn.csv.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    canvas.itemconfig(image, image=old_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(image, image=new_image)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


#-------------UI----------------

#window

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR, highlightthickness=0)
flip_timer = window.after(3000, func=flip_card)

#canvas

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
old_image = PhotoImage(file="images/card_front.png")
new_image = PhotoImage(file="images/card_back.png")
image = canvas.create_image(400, 263, image=old_image)
title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, font=("Ariel", 40, "italic"))
canvas.grid(row=0, column=0, columnspan=2)

#buttons

wrong_image = PhotoImage(file="images/wrong.png")
wrong = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right = Button(image=right_image, highlightthickness=0, command=is_known)
right.grid(row=1, column=1)

next_card()

window.mainloop()
