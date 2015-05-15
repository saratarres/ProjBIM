#------------------------------------------------------------------------------#
#																			   #
#								  PROJET 3BIM						  		   #
#																			   #
#------------------------------------------------------------------------------#

## J'ai regroupe les deux fichiers afin de les tester ensemble et j'ai utilise 
## une atre methode pour bouger qui gère les deplacements aleatoire, les bords 
## et les obstacles

## Maintenant il va falloir gerer les autres modes : stress et famine.. pour ça 
## je pense qu'il faudrait discuter ensemble pour voir comment on fait.


from random import*



############################# DEFINITION DES PARAMS ###########################

	# AMIBES
N = 'normal'
V = 'vibration'
D = 'diffusion'
M = 'mort'

n = 'nourriture'
o = 'obstacles'

	# ENVIRONNEMENT 
PN = 'periode de nourriture'
S = 'stress'
F = 'famine'

h = 150 #!!! taille de la grille (il faut qua ca soit un multiple de 5)
w = 80 #!!! taille de la grille (il faut qua ca soit un multiple de 5)

# Definition des params de la grille
nbo = 10 # nombre d'obstacle dans la grille
nbn_PN = 6 # nombre de nourriture dans le mode PN
nbn_S = 2 # nombre de nourriture dans le mode S
nbn_F = 0 # nombre de nourriture dans le mode F





#################################### AMIBES ###################################


class Amibes : 

	def __init__(self,r,tmax,x,y):

		#Rayon de perception )= rp
		self.rp= r

		#Position x et y initial de l'amibe 
		self.x = x
		self.y=y

		#Etat dans lequel elle peut se trouver 
		self.etats = [N,V,D,M]

		#Etat dans lequel elle se trouve
		self.etat_actuel = [N]

		#Temps de recherche nourriture = trc
		self.trc = 0

		#Temps de recherche maximal de nourriture
		self.tmax = tmax

	def __str__(self) :
		return "L'amibe est en position (%d - %d) et est dans l'etat %s"%(self.x, self.y, self.etat_actuel)

	#Fonctions qui permet de bouger en fonction du poids des matrices autour. En sachant qu'on 
	#a pas a gerer les effets de bords car on a dit qu'on mettrais 0 partout ailleurs
	#Pour que jamais il n'aille de ce cote. Mais je n'ai pas coder l'hypothese ou on a deux poids
	#Egaux de chaque cote. Je ne me souviens plus trop de ce qu'on avait convenu comme marche a suivre
	#J'ai gerer le fait qu'il puisse y avoir un obstacle


	def bouger (self,grille):
		# Si l'amibe a trouve la nourriture, elle ne bouge plus
		if grille[self.x][self.y] != 100 : 

			temp = 0
			xtemp = self.x
			ytemp = self.y
		
			# on parcours le cercle autour de l'amibe
			for i in xrange(xtemp-1, xtemp+2):
				for j in xrange(ytemp-1, ytemp+2):

					# Le deplacement doit rester dans la grille 
					if i>=0 and i<len(grille) and j>=0 and j<len(grille[0]) :
						if grille[i][j]>grille[xtemp][ytemp] :
							xtemp = i
							ytemp = j


			#print "La plus grande valeur est" , temp , "de coordonnee", xtemp,ytemp
			if xtemp!=self.x or ytemp!=self.y :
				self.x = xtemp
				self.y = ytemp

			else :
				val = self.__bougerRDM(grille, xtemp, ytemp)
				self.x = val[0]
				self.y = val[1]

	### Methode qui permet de bouger aleatoirement sans etre dans les obstacles
	def __bougerRDM(self, grille, xt, yt) :
		a = randint(-1,1)
		b = randint(-1,1)
		newX = xt + a
		newY = yt + b
		if grille[newX][newY] == 0  or newX<0 or newX>=len(grille) or newY<0 or newY>=len(grille[0]) :
			self.__bougerRDM(grille, xt, yt)
		return (newX, newY)

	### Methodes qui va faire que l'amibe va rentrer dans un etat de stress

	def stress(self):
		if (t>T):
			self.etat_actuel[0] = V

	### Methode de modification du grandient lorsqu'un amibes a atteint de la nourriture 
	### Mais je ne suis pas sur du tout que c'est ca dont on avait parler
	### Car je vois pas comment mettre en place le rayon de perception la dedans

	def modif_gradient (self,grille):
		if (grille[self.x][self.y] == n):
			grille[self.x +1][self.y]=1000
			grille[self.x +2][self.y]=1000
			grille[self.x +3][self.y]=1000



################################# ENVIRONNEMENT ###############################


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



##################################### MAIN ####################################


#seed(0) # permet d'avoir toujours la meme grille 

Env = Envir(h, w, PN)
print Env

Ami = Amibes(5, 10, 4, 3)
print Ami

for i in xrange(10):
	Ami.bouger(Env.grille)
	print Ami