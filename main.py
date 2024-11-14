from random import randint


class point:
    def __init__(self, x, y, etat):
        self.__coordone = x, y
        # etat est une liste, [numéro du player, état du pion], 0 est le pion et 1 est l'ancien emplacement
        self.__etat = etat

    def getEtat(self):
        return self.__etat

    def setEtat(self, etat):
        self.__etat = etat

    def getCoordone(self):
        return self.__coordone

    def couleurs(self):
        color = ["gray", "blue", "red"]
        return color[self.__etat[0]]


class fonctionnement:

    def __init__(self, n, p):
        self.__size = n
        self.__nbrPion = p
        self.newBoard()
        self.__player = 1
        self.__pion = [[], []]

    def getBoard(self):
        return self.__board

    def getPions(self):
        return self.__pion

    def getPlayer(self):
        return self.__player

    def getNbrPions(self):
        return self.__nbrPion

    def setNbrPions(self, nbrPions):
        self.__nbrPion = nbrPions

    def setBoard(self, board):
        self.__board = board

    def setPlayer(self, player):
        self.__player = player

    def setPions(self, pions):
        self.__pion = pions

    def setSize(self, size):
        self.__size = size

    def newBoard(self):
        self.__board = [[point(x, y, [0, -1]) for x in range(self.__size)] for y in range(self.__size)]

    def alignement(self, x, y):
        self.__compteur = 0
        a, b = x, x
        # vérfication pour chaque ligne
        while (a + 1 < self.__size and self.__board[y][a + 1].getEtat() == [self.__player, 1]) or (
                b - 1 >= 0 and self.__board[y][b - 1].getEtat() == [self.__player, 1]):
            self.__compteur += 1

            if self.__compteur >= self.__nbrPion - 1:
                return True
            elif (a + 1 < self.__size and self.__board[y][a + 1].getEtat() == [self.__player, 1]):
                a += 1
            else:
                b -= 1
        self.__compteur = 0

        # vérification pour chaque colonne
        a, b = y, y
        while (a + 1 < self.__size and self.__board[a + 1][x].getEtat() == [self.__player, 1]) or (
                b - 1 >= 0 and self.__board[b - 1][x].getEtat() == [self.__player, 1]):
            self.__compteur += 1
            if self.__compteur >= self.__nbrPion - 1:
                return True
            elif (a + 1 < self.__size and self.__board[a + 1][x].getEtat() == [self.__player, 1]):
                a += 1
            else:
                b -= 1
        self.__compteur = 0

        # vérification diagonale ascendante
        a, b = 1, 1
        while (x + a < self.__size and y - a >= 0 and self.__board[y - a][x + a].getEtat() == [self.__player, 1]) or (
                x - b >= 0 and y + b < self.__size and self.__board[y + b][x - b].getEtat() == [self.__player, 1]):
            self.__compteur += 1
            if self.__compteur >= self.__nbrPion - 1:
                return True
            elif x + a < self.__size and y - a < self.__size and self.__board[y - a][x + a].getEtat() == [self.__player,
                                                                                                          1]:
                a += 1
            else:
                b += 1
        self.__compteur = 0

        # vérification diagonale descendante
        a, b = 1, -1
        while (x + a < self.__size and y + a < self.__size and self.__board[y + a][x + a].getEtat() == [self.__player,
                                                                                                        1]) or (
                x + b >= 0 and y + b >= 0 and self.__board[y + b][x + b].getEtat() == [self.__player, 1]):
            self.__compteur += 1
            if self.__compteur >= self.__nbrPion - 1:
                return True
            elif x + a < self.__size and y + a < self.__size and self.__board[y + a][x + a].getEtat() == [self.__player,
                                                                                                          1]:
                a += 1
            else:
                b -= 1
        self.__compteur = 0

        return False

    def possible(self, x, y):
        """
        Vérifie toute les cases vides autour de la case x,y
        Si aucune case est vide renvoie False
        Sinon renvoie la liste de toutes les coordonées de possible 
        """
        liste1, liste2 = [-1, 1], [-2, 2]
        res = []
        for i in liste1:
            for j in liste2:
                if 0 <= x + i < self.__size and 0 <= y + j < self.__size and self.__board[y + j][x + i].getEtat() == [0,
                                                                                                                      -1]:
                    res.append([x + i, y + j])
                if 0 <= x + j < self.__size and 0 <= y + i < self.__size and self.__board[y + i][x + j].getEtat() == [0,
                                                                                                                      -1]:
                    res.append([x + j, y + i])
        return False if res == [] else res

    def move(self, x, y):
        coordonePion = self.__pion[self.__player - 1][0], self.__pion[self.__player - 1][1]
        if self.possible(coordonePion[0], coordonePion[1]) != False and [x, y] in self.possible(coordonePion[0],
                                                                                                coordonePion[1]):
            i, j = self.__pion[self.__player - 1]
            self.__board[j][i].setEtat([self.__player, 1])
            self.__board[y][x].setEtat([self.__player, 0])
            self.__pion[self.__player - 1] = [x, y]
            return True
        return False

    def again(self):
        res = False
        for y in range(self.__size):
            for x in range(self.__size):
                if self.__board[y][x].getEtat() == [self.__player, 1]:
                    if self.alignement(x, y):
                        return False
                prochainPlayer = 3 - self.__player
                if self.__board[y][x].getEtat() == [self.__player, 0] and self.possible(
                        self.__pion[prochainPlayer - 1][0], self.__pion[prochainPlayer - 1][1]) != False:
                    res = True
        return res

    def sauvegarde(self):
        fichier = open("sauvegarde.txt", "w")
        for ligne in self.__board:
            for valeur in ligne:
                fichier.write(str(valeur.getEtat()) + "],")
            fichier.write("\n")
        fichier.write(str(self.__player))
        fichier.write(str(self.__nbrPion))
        fichier.close()

    def chargerPartie(self):
        try:
            fichier = open("sauvegarde.txt", "r")
            ancienneSauvegarde = fichier.readlines()
            self.__size = len(ancienneSauvegarde) - 1
            self.newBoard()
            for i in range(len(ancienneSauvegarde)):
                if i == len(ancienneSauvegarde) - 1:
                    self.__nbrPion = int(ancienneSauvegarde[i][1])
                    self.__player = int(ancienneSauvegarde[i][0])
                else:
                    ligne = ancienneSauvegarde[i][0:-2]
                    etatPion = list(ligne.split('],'))
                    for j in range(len(etatPion)):
                        pion = []
                        chiffre = ""
                        for caractere in etatPion[j]:
                            if caractere not in ["[", ",", " ", "]"]:
                                chiffre = chiffre + caractere
                            elif caractere == ",":
                                pion.append(int(chiffre))
                                chiffre = ""
                        pion.append(int(chiffre))
                        if pion[1] == 0:
                            self.__pion[pion[0] - 1] = [j, i]
                        self.__board[i][j].setEtat(pion)
            fichier.close()
        except:
            print("Le fichier de sauvegarde n'a pas été trouvé")

    def bot(self):
        if self.__pion[1] == []:
            x = randint(0, self.__size)
            y = randint(0, self.__size)
            while self.__board[y][x].getEtat() != [0, -1]:
                x = randint(0, self.__size)
                y = randint(0, self.__size)
            self.__board.getBoard()[y][x].setEtat([self.__board.getPlayer(), 0])
        else:
            mouvementPossible = self.possible(self.__pion[1][0], self.__pion[1][1])
            choix = mouvementPossible[randint(0, len(mouvementPossible) - 1)]
            self.move(choix[0], choix[1])