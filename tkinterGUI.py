from tkinter import *

class WarmHeart:
    def __init__(self):
        window = Tk()
        self.width = 800
        self.height = 600
        self.canvas = Canvas(window, width = self.width, height = self.height, bg = "white")
        self.canvas.pack()

        self.LogoImage = PhotoImage(file = "WarmHeart로고.png")
        self.logo = Label(window, image = self.LogoImage)
        self.logo.place(x=0, y=0)


        window.mainloop()



WarmHeart()
