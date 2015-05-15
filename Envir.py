#------------------------------------------------------------------------------#
#																			   #
#								ENVIRONNEMENT								   #
#																			   #
#------------------------------------------------------------------------------#



from random import*

# Defenition des parametres 
PN = 'periode de nourriture'
S = 'stress'
F = 'famine'

N = 'normal'

h = 100 #!!! taille de la grille (il faut qua ca soit un multiple de 5)
w = 80 #!!! taille de la grille (il faut qua ca soit un multiple de 5)

# Definition des params de la grille
nbo = 10 # nombre d'obstacle dans la grille
nbn_PN = 4 # nombre de nourriture dans le mode PN
nbn_S = 2 # nombre de nourriture dans le mode S
nbn_F = 0 # nombre de nourriture dans le mode F



class Envir:

	def __init__ (self, h, w, mode):
		# Initialisation de la taille de la grille
		# On cree des case de taille 5x5
		self.h = h/5 
		self.w = w/5 

		# Initialisation de la grille avec des 1
		self.grille = [[1 for a in range(self.w)] for b in range(self.h)]

		# Initialisation du mode de la grille : 3 possibilites (PN, S, F)
		self.mode = mode

		# Le remplissage de la grille depend de son mode
			# remplissage des obstacles
		self.__rempliObstacle(nbo)
			# remplissage de la nourriture 
		if self.mode == PN :
			nbn = nbn_PN
		if self.mode == S :
			nbn = nbn_S
		if self.mode == F :
			nbn = nbn_F

		self.__rempliNourriture(nbn)


		## On avait parler de faire une jauge , il s'agit donc de l'etat de la jauge qui 
		## Varie en fonction de la nourriture.
		self.mode = [PN,S,F]

		### Etat de la case , c'est a dire nourriture , obstacles ou rien 
		## Mais je me demande si ca n'irait pas putot dans la classe amibes 
		self.etat_case = [N]

	def __str__(self): # permet d'afficher la grille avec un print env
		s = str()
		for i in range(self.h):
			for j in range(self.w):
				s += str(self.grille[i][j]) + "\t"
			s += "\n"
		return "La grille actuelle est\n%s"%s

	def __rempliNourriture(self, nb):
		v = nb
		for i in xrange(nb) :
			a = randint(0, (self.h - 1))
			b = randint(0, (self.w - 1))

			if self.grille[a][b]==0 or self.grille[a][b]==100 :
				self.__rempliNourriture(v)				

			else :
				self.grille[a][b] = 100
				# La nourriture a un gradient de perception
				self.__diffusion(a,b)

			v -= 1

	def __rempliObstacle(self, nb):
		val = nb
		for i in xrange(nb) :
			a = randint(0, (self.h - 1))
			b = randint(0, (self.w - 1))

			if self.grille[a][b] == 0 :
				self.__rempliObstacle(val)
			else :
				self.grille[a][b] = 0

			val -= 1

	def __diffusion(self, a, b) : # cette methode change le poids des cases autour de la nourriture
		# on parcours le cercle de diffusion
		for i in xrange(a-2, a+3):
			for j in xrange(b-2, b+3):

				# La diffusion doit rester dans la grille 
				if i>=0 and i<self.h and j>=0 and j<self.w :

					# on rempli le premier cercle de diffusion (proche de la nourriture)
					if abs(a-i)==1 or abs(b-j)==1 :
						if self.grille[i][j]!=0 and self.grille[i][j]!=100 :
							self.grille[i][j] = 50

					# on rempli le second cercle de diffusion 
					if abs(a-i)>1 or abs(b-j)>1 :
						if self.grille[i][j]!=0 and self.grille[i][j]!=100 :
							self.grille[i][j] = 25


# Main test des methodes
test = Envir(h, w, PN)
print test
