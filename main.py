from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "arial"
current_card = {}

try:
    words = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    words = pandas.read_csv("./data/french_words.csv")
finally:
    words_list = words.to_dict(orient="records")


# -------------------------------- Read CSV Data ----------------------------- #


def flip_card():
    global current_card
    canvas.itemconfig(card_image, image=card_img_back)
    canvas.itemconfig(lang_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")


def new_word():
    global current_card, timer
    window.after_cancel(timer)
    canvas.itemconfig(card_image, image=card_img_front)
    current_card = random.choice(words_list)
    canvas.itemconfig(lang_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    window.after(3000, flip_card)


def is_known():
    global current_card, words_list
    words_list.remove(current_card)
    data_frame = pandas.DataFrame(words_list)
    data_frame.to_csv("./data/words_to_learn.csv", index=False)
    new_word()


# -------------------------------- UI Setup ---------------------------------- #
window = Tk()

window.title("Language Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526,
                highlightthickness=0, bg=BACKGROUND_COLOR)
card_img_front = PhotoImage(file="./images/card_front.png")
card_img_back = PhotoImage(file="./images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_img_front)
lang_text = canvas.create_text(
    400, 150, text="French", fill="black", font=(FONT_NAME, 28, "italic"))
word_text = canvas.create_text(
    400, 263, text="Word", fill="black", font=(FONT_NAME, 32, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
x_image = PhotoImage(file="./images/wrong.png")
x_button = Button(image=x_image, highlightthickness=0, command=new_word)
x_button.grid(row=1, column=0)

c_image = PhotoImage(file="./images/right.png")
c_button = Button(image=c_image, highlightthickness=0, command=is_known)
c_button.grid(row=1, column=1)

timer = window.after(3000, flip_card)
new_word()
window.mainloop()
