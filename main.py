from tkinter import *
from tkinter import Button
import pandas
import random

to_learn = {}
current_card = {}
BACKGROUND_COLOR = "#B1DDC6"
# You can easily change language to learn to German, by typing "German" instead "English"
LANGUAGE_TO_LEARN = "English"

try:
    data = pandas.read_csv("to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/translator_en_de_pl.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global timer, current_card
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(language_text, text=LANGUAGE_TO_LEARN, fill="black")
    canvas.itemconfig(word_text, text=current_card[LANGUAGE_TO_LEARN], fill="black")
    timer = window.after(3000, translation)


def translation():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(language_text, text="Polish", fill="white")
    canvas.itemconfig(word_text, text=current_card["Polish"], fill="white")


def already_learned():
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashcards")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, translation)

canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 265, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
language_text = canvas.create_text(400, 150, text="Language", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="word", font=("Ariel", 40, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
correct_image = PhotoImage(file="./images/right.png")
button_correct = Button(image=correct_image, highlightthickness=0, command=already_learned)
button_correct.grid(row=2, column=0)

wrong_image = PhotoImage(file="./images/wrong.png")
button_wrong = Button(image=wrong_image, highlightthickness=0, command=next_card)
button_wrong.grid(row=2, column=1)

next_card()

window.mainloop()




