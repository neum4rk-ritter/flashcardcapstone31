import tkinter
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
sheduled_show_answer = None
BASE_CSV_FILE = pandas.read_csv("data/french_words.csv")
try:
    df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    df = BASE_CSV_FILE.copy()
    df.to_csv("data/words_to_learn.csv", index=False)

to_learn = df.to_dict(orient="records")


# ---------------------------- REMOVING FROM DICTIONARY ------------------------------- #
def is_known():
    to_learn.remove(flashcard)
    new_flashcard()
    final_to_learn = pandas.DataFrame(to_learn)
    final_to_learn.to_csv("data/words_to_learn.csv", index=False)


# ---------------------------- CREATE NEW FLASH CARDS ------------------------------- #


def new_flashcard():
    canvas.itemconfig(card_image, image=card_front_img)
    global sheduled_show_answer, flashcard
    if sheduled_show_answer is not None:
        window.after_cancel(sheduled_show_answer)
    flashcard = random.choice(to_learn)
    canvas.itemconfig(title_txt, fill="black", text="French")
    canvas.itemconfig(word_txt, fill="black", text=flashcard["French"])
    sheduled_show_answer = window.after(3000, lambda: show_answer(flashcard))


def show_answer(word):
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(title_txt, fill="white", text="English")
    canvas.itemconfig(word_txt, fill="white", text=word["English"])

# print(word_dictionary[0]["Deutsch"])


# ---------------------------- USER INTERFACE ------------------------------- #
window = tkinter.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


canvas = tkinter.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = tkinter.PhotoImage(file="images/card_front.png")
card_back_img = tkinter.PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 260, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)

title_txt = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))

word_txt = canvas.create_text(400, 263, text="", fill="black",
                              font=("Arial", 60, "bold"))

correct_image = tkinter.PhotoImage(file="images/right.png")
correct_button = tkinter.Button(image=correct_image, highlightthickness=0, borderwidth=0, command=is_known)
correct_button.grid(row=1, column=1)

wrong_image = tkinter.PhotoImage(file="images/wrong.png")
wrong_button = tkinter.Button(image=wrong_image, highlightthickness=0, borderwidth=0, command=new_flashcard)
wrong_button.grid(row=1, column=0)

new_flashcard()
window.mainloop()
