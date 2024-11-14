from main import *
from tkinter import *
from tkinter import messagebox

class gui:
    def __init__(self, n=10, p=5):
        self.__size = n
        self.__nbrPion = p
        self.__board = fonctionnement(n, p)
        self.__root = Tk()
        self.__root.title("Game")
        self.__root.resizable(False, False)

        self.__frame1 = Frame(self.__root)
        self.__frame1.grid(row=0, column=0, rowspan=2)
        self.__frame1.config(height=self.__size * 50 + 1, width=self.__size * 50 + 1, highlightthickness=0, bd=0,
                             bg="lightgray", padx=50, pady=50)
        self.__frame2 = Frame(self.__root)
        self.__frame2.grid(row=0, column=1)
        self.__frame2.config(height=self.__size * 50 + 1, width=self.__size * 10 + 1, highlightthickness=0, bd=0)
        self.__frame3 = Frame(self.__root)
        self.__frame3.grid(row=1, column=1)
        self.__frame3.config(height=self.__size * 50 + 1, width=self.__size * 10 + 1, highlightthickness=0, bd=0)

        self.__text = Label(self.__frame2, text="Choisissez la taille du plateau", width=50)
        self.__text.pack()
        self.__numScale = IntVar()
        self.__scale = Scale(self.__frame2, variable=self.__numScale, from_=8, to=12, orient=HORIZONTAL)
        self.__scale.pack()
        self.__scale.set(10)
        self.__buttonScale = Button(self.__frame2, text='Validez', command=self.updateSize)
        self.__buttonScale.pack()

        self.__text = Label(self.__frame2, text="Choisissez le nombre de pion pour gagner", width=50)
        self.__text.pack()
        self.__numScalePion = IntVar()
        self.__scalePion = Scale(self.__frame2, variable=self.__numScalePion, from_=4, to=6, orient=HORIZONTAL)
        self.__scalePion.pack()
        self.__scalePion.set(5)
        self.__buttonScalePion = Button(self.__frame2, text='Validez', command=self.updateNbrPion)
        self.__buttonScalePion.pack()

        self.__bot = IntVar()
        self.__checkbuttonBot = Checkbutton(self.__frame2, text="Activation du bot", variable=self.__bot)
        self.__checkbuttonBot.pack()

        self.__buttonLoad = Button(self.__frame3, text='Charger une partie', command=self.charger, padx=20, pady=20)
        self.__buttonLoad.grid(row=0, column=0)
        self.__buttonReset = Button(self.__frame3, text='Recommencer la partie', command=self.restartPartie, padx=15,
                                    pady=20)
        self.__buttonReset.grid(row=0, column=1)
        self.__buttonSave = Button(self.__frame3, text='Sauvegarder', command=self.messageSauvegarde, padx=37, pady=20)
        self.__buttonSave.grid(row=1, column=0)
        self.__buttonQuit = Button(self.__frame3, text='Quitter la partie', command=self.quitterPartie, padx=34,
                                   pady=20)
        self.__buttonQuit.grid(row=1, column=1)

        self.__canvas = Canvas(self.__frame1)
        self.__canvas.config(width=self.__size * 50 + 1, height=self.__size * 50 + 1, highlightthickness=0, bd=0,
                             bg="lightgray")
        self.__canvas.bind('<Button-1>', self.click)
        self.__canvas.pack()

        self.__playerNum = StringVar()
        self.__textPlayer = Label(self.__frame1, textvariable=self.__playerNum, width=30, bg="lightgray", fg="blue",
                                  font=("Courier", 30))
        self.__textPlayer.pack(pady=10)
        self.updateLabels()
        self.display()

        self.__root.mainloop()

    def quitterPartie(self):
        reponse = messagebox.askquestion(title="Partie en cours",
                                         message="Êtes vous sûr de vouloir quitter la partie ?")
        if reponse == "yes":
            self.__root.destroy()

    def restartPartie(self):
        reponse = messagebox.askquestion(title="Partie en cours",
                                         message="Êtes vous sûr de vouloir recommencer la partie ?")
        if reponse == "yes":
            self.__board.newBoard()
            self.__board.setPions([[], []])
            self.__checkbuttonBot["state"] = NORMAL
            self.__board.setPlayer(1)
            self.updateLabels()
            self.display()
            self.__canvas.update()

    def charger(self):
        self.__board.chargerPartie()
        self.__size = len(self.__board.getBoard())
        self.__nbrPion = self.__board.getNbrPions()
        self.__numScalePion.set(self.__nbrPion)
        self.__numScale.set(self.__size)
        self.updateSize()
        self.updateNbrPion()
        self.updateLabels()
        self.display()
        self.previsualisation()

    def update(self):
        self.display()
        if self.__board.again():
            self.__board.setPlayer(3 - self.__board.getPlayer())
            if self.__board.getPlayer() == 2 and self.__bot.get() == 1:
                self.__board.bot()
                self.updateLabels()
                self.display()
                if not self.__board.again():
                    self.finPartie()
                self.__board.setPlayer(3 - self.__board.getPlayer())
            self.updateLabels()
            self.previsualisation()
        else:
            self.finPartie()

    def finPartie(self):
        messagebox.showwarning(title="Partie terminée", message="Joueur {} à gagné(e)".format(self.__board.getPlayer()))
        reponse = messagebox.askquestion(title="Partie terminée", message="Une nouvelle partie ?")
        if reponse == "no":
            self.__root.destroy()
        else:
            self.__board.newBoard()
            self.__board.setPions([[], []])
            self.__checkbuttonBot["state"] = NORMAL
            self.__board.setPlayer(1)
            self.display()

    def messageSauvegarde(self):
        self.__board.sauvegarde()
        messagebox.showwarning(title="Sauvegarde", message="Sauvegarde effectué avec succès !")
        reponse = messagebox.askquestion(title="Partie sauvegardée", message="Voulez-vous quitter la partie ?")
        if reponse == "yes":
            self.__root.destroy()

    def updateLabels(self):
        self.__playerNum.set('Player : {}'.format(self.__board.getPlayer()))
        self.__textPlayer.config(fg="blue" if self.__board.getPlayer() == 1 else "red")

    def updateSize(self):
        if self.__board.getPions() == [[], []]:
            self.__size = self.__numScale.get()
            self.__board.setSize(self.__size)
            self.__board.newBoard()
        self.__frame1.config(height=self.__size * 50 + 1, width=self.__size * 50 + 1, highlightthickness=0, bd=0,
                             bg="lightgray", padx=50, pady=50)
        self.__frame2.config(height=self.__size * 50 + 1, width=self.__size * 10 + 1, highlightthickness=0, bd=0)
        self.__canvas.config(width=self.__size * 50 + 1, height=self.__size * 50 + 1, highlightthickness=0, bd=0,
                             bg="lightgray")
        self.display()
        self.previsualisation()

    def updateNbrPion(self):
        if self.__board.getPions() == [[], []]:
            self.__nbrPion = self.__numScalePion.get()
        self.__board.setNbrPions(self.__nbrPion)

    def click(self, event):
        x = event.x // 50
        y = event.y // 50
        if self.__board.getPions()[self.__board.getPlayer() - 1] == []:
            if self.__board.getBoard()[y][x].getEtat() == [0, -1]:
                self.__board.getPions()[self.__board.getPlayer() - 1] = x, y
                self.__board.getBoard()[y][x].setEtat([self.__board.getPlayer(), 0])
                self.__board.setPlayer(3 - self.__board.getPlayer())
                if self.__bot.get() == 1:
                    x = randint(0, self.__size - 1)
                    y = randint(0, self.__size - 1)
                    while self.__board.getBoard()[y][x].getEtat() != [0, -1]:
                        x = randint(0, self.__size - 1)
                        y = randint(0, self.__size - 1)
                    self.__board.getBoard()[y][x].setEtat([self.__board.getPlayer(), 0])
                    self.__board.getPions()[self.__board.getPlayer() - 1] = x, y
                    self.__board.setPlayer(3 - self.__board.getPlayer())
                if self.__board.getPions()[0] != []:
                    self.__checkbuttonBot["state"] = DISABLED
                self.updateLabels()
                self.display()
                self.previsualisation()
        elif self.__board.move(x, y):
            self.update()

    def display(self):
        self.__canvas.delete("all")
        for y in range(self.__size):
            for x in range(self.__size):
                self.__case = self.__canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill="white",
                                                             outline='black')
                if self.__board.getBoard()[y][x].getEtat()[1] == 0:
                    self.__canvas.create_oval(x * 50 + 10, y * 50 + 10, (x + 1) * 50 - 10, (y + 1) * 50 - 10,
                                              fill=self.__board.getBoard()[y][x].couleurs(), outline="black")
                elif self.__board.getBoard()[y][x].getEtat()[1] == 1:
                    self.__canvas.create_line(x * 50 + 15, y * 50 + 15, (x + 1) * 50 - 15, (y + 1) * 50 - 15,
                                              fill=self.__board.getBoard()[y][x].couleurs(), width=4)
                    self.__canvas.create_line(x * 50 + 15, (y + 1) * 50 - 15, (x + 1) * 50 - 15, y * 50 + 15,
                                              fill=self.__board.getBoard()[y][x].couleurs(), width=4)
        self.__canvas.update()

    def previsualisation(self):
        if self.__board.getPions()[self.__board.getPlayer() - 1] != []:
            if self.__board.possible(self.__board.getPions()[self.__board.getPlayer() - 1][0],
                                     self.__board.getPions()[self.__board.getPlayer() - 1][1]) != False:
                for i in self.__board.possible(self.__board.getPions()[self.__board.getPlayer() - 1][0],
                                               self.__board.getPions()[self.__board.getPlayer() - 1][1]):
                    self.__case = self.__canvas.create_rectangle(i[0] * 50 + 10, i[1] * 50 + 10, (i[0] + 1) * 50 - 10,
                                                                 (i[1] + 1) * 50 - 10, fill="gray", outline='black')
                self.__canvas.update()

gui()