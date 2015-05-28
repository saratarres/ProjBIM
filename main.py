#------------------------------------------------------------------------------#
#																			   #
#								  PROJET 3BIM						  		   #
#																			   #
#------------------------------------------------------------------------------#

## (Elo) J'ai regroupe les deux fichiers afin de les tester ensemble et j'ai utilise 
## une autre methode pour bouger qui gere les deplacements aleatoire, les bords 
## et les obstacles

## Maintenant il va falloir gerer les autres modes : stress et famine.. pour ca 
## je pense qu'il faudrait discuter ensemble pour voir comment on fait.

## (Sam) J'ai fait le mode vibration de l'amibe
## en fait l'idee c'est que l'amibe bouge aleatoirement dans la grille:
## - Si au bout de trechercheMAX elle ne trouve pas de nourriture,
## elle se met en mode vibration, cad qu'elle bouge de un a gauche
## puis de un a droite en x infiniment
## - Si elle trouve de la nourriture avant trechercheMAX, elle va manger
## cad s'arreter pendant tmangerMAX. Au bout de tmangerMAX, la nourriture
## qu'elle vient de manger va disparaitre (et les poids autour aussi)
## et elle va reprendre son chemin aleatoire. etc etc

from random import*



############################# DEFINITION DES PARAMS ###########################
timer = 30

	# AMIBES
N = 'normal'
V = 'vibration'
D = 'diffusion'
M = 'mort'

tmangerMAX = 5 # temps pendant lequel l'amibe mange sur la case a 100.
# Au bout de 30 sec, la grille est reinitialise, cad la case ou il y avait de la nourriture et remise a 1.
# L'amibe se remet donc a bouger

trechercheMAX = 5 # temps de recherche maximale de nourriture

n = 'nourriture'
o = 'obstacles'

	# ENVIRONNEMENT 
PN = 'periode de nourriture'
S = 'stress'
F = 'famine'

# x est en ordonnee !!
# y est en abscisse !!
# (0,0) est en haut a gauche
xmax = 150 #!!! taille de la grille (il faut qua ca soit un multiple de 5) #X
ymax = 80 #!!! taille de la grille (il faut qua ca soit un multiple de 5) #Y
pixel = 10

# Definition des params de la grille
nbo = 10 # nombre d'obstacle dans la grille
nbn_PN = 6 # nombre de nourriture dans le mode PN
nbn_S = 2 # nombre de nourriture dans le mode S
nbn_F = 0 # nombre de nourriture dans le mode F




#################################### AMIBES ###################################

class Amibes : 

	def __init__(self):

		#Rayon de perception )= rp
		#self.rp= r

		#Position x et y initial de l'amibe 
		self.x = randint(0,xmax/pixel-1)
		self.y = randint(0,ymax/pixel-1)
		self.setPos(Env)

		#Etat dans lequel elle peut se trouver 
		self.etats = [N,V,D,M]

		#Etat dans lequel elle se trouve
		self.etat_actuel = [N]

		#Temps de recherche nourriture = trecherche
		self.trecherche = 0

		#Temps pendant lequel l'amibe bouffe
		self.tmanger = 0

		#Boolean pour que l'amibe vibre une fois a gauche et une fois a droite
		self.boole = True

	def __str__(self) :
		return "L'amibe est en position (%d - %d) et est dans l'etat %s"%(self.x, self.y, self.etat_actuel)

	#Fonctions qui permet de bouger en fonction du poids des matrices autour. En sachant qu'on 
	#a pas a gerer les effets de bords car on a dit qu'on mettrait 0 partout ailleurs
	#Pour que jamais il n'aille de ce cote. Mais je n'ai pas coder l'hypothese ou on a deux poids
	#Egaux de chaque cote. Je ne me souviens plus trop de ce qu'on avait convenu comme marche a suivre
	#J'ai gerer le fait qu'il puisse y avoir un obstacle

	def setPos(self,Envir):
		while Envir.grille[self.x][self.y] == 0 or Envir.grille[self.x][self.y] == 100:
		 	self.x = randint(0,xmax/pixel-1)
		 	self.y = randint(0,ymax/pixel-1)

	def bouger (self,Envir):
		if self.etat_actuel[0] == N:
			# Si l'amibe a trouve la nourriture, elle ne bouge plus pendant tmangerMAX
			if Envir.grille[self.x][self.y] != 100 : 

				temp = 0
				xtemp = self.x
				ytemp = self.y
			
				# on parcours le cercle autour de l'amibe
				for i in xrange(xtemp-1, xtemp+2):
					for j in xrange(ytemp-1, ytemp+2):

						# Le deplacement doit rester dans la grille 
						if i>=0 and i<len(Envir.grille) and j>=0 and j<len(Envir.grille[0]) :
							if Envir.grille[i][j]>Envir.grille[xtemp][ytemp] :
								xtemp = i
								ytemp = j

				#print "La plus grande valeur est" , temp , "de coordonnee", xtemp,ytemp
				if xtemp!=self.x or ytemp!=self.y :
					self.x = xtemp
					self.y = ytemp

				else :
					val = self.__bougerRDM(Envir.grille, xtemp, ytemp)
					self.x = val[0]
					self.y = val[1]
					self.trecherche += 1 #Si deplacement aleatoire, on augmente le temps de recherche de 1
					self.stress(self.x,self.y)

			else :
				self.tmanger += 1
				if self.tmanger > tmangerMAX:
					self.tmanger = 0
					Envir.grille[self.x][self.y] = 1
					Envir.remettreAUnLesCasesJuxtaposee(self.x,self.y)
					self.bouger(Envir)

		elif self.etat_actuel[0] == V:
			self.stress(self.x,self.y)


	### Methode qui permet de bouger aleatoirement sans etre dans les obstacles
	def __bougerRDM(self, grille, xt, yt) :
		a = randint(-1,1)
		b = randint(-1,1)
		newX = xt + a
		newY = yt + b
		if newX<0:
			newX = newX + 2
		if newX>len(grille)-1:
			newX = newX - 2
		if newY<0:
			newY = newY + 2
		if newY>len(grille[0])-1:
			newY = newY - 2
		if grille[newX][newY] == 0:
			self.__bougerRDM(grille, xt, yt)
		return (newX, newY)

	### Methode qui va faire que l'amibe va rentrer dans un etat de stress
	def stress(self,a,b):
		if (self.trecherche>trechercheMAX):
			self.etat_actuel[0] = V
			self.vibre(a,b,self.boole)
			if self.boole==True:
				self.boole=False
			else:
				self.boole=True
	def vibre(self,a,b,vrai):
		if vrai==True:
			if a < xmax/pixel - 1:
				self.x = a + 1
			else:
				self.x = a
		else:
			if a > 1:
				self.x = a - 1
			else:
				self.x = a

	### Methode de modification du gradient lorsqu'un amibe a atteint de la nourriture 
	### Mais je ne suis pas sur du tout que c'est ca dont on avait parler
	### Car je vois pas comment mettre en place le rayon de perception la dedans

	def modif_gradient (self,grille):
		if (grille[self.x][self.y] == n):
			grille[self.x +1][self.y]=1000
			grille[self.x +2][self.y]=1000
			grille[self.x +3][self.y]=1000



################################# ENVIRONNEMENT ###############################


class Envir:
	def __init__ (self, xmax, ymax, mode):
		# Initialisation de la taille de la grille
		# On cree des case de taille 5x5
		self.xmax = xmax/pixel 
		self.ymax = ymax/pixel

		# Initialisation de la grille avec des 1
		self.grille = [[1 for a in range(self.ymax)] for b in range(self.xmax)]

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
		for i in range(self.xmax):
			for j in range(self.ymax):
				s += str(self.grille[i][j]) + "\t"
			s += "\n"
		return "La grille actuelle est\n%s"%s

	def __rempliNourriture(self, nb):
		v = nb
		for i in xrange(nb) :
			a = randint(0, (self.xmax - 1))
			b = randint(0, (self.ymax - 1))

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
			a = randint(0, (self.xmax - 1))
			b = randint(0, (self.ymax - 1))

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
				if i>=0 and i<self.xmax and j>=0 and j<self.ymax :

					# on rempli le premier cercle de diffusion (proche de la nourriture)
					if abs(a-i)==1 or abs(b-j)==1 :
						if self.grille[i][j]!=0 and self.grille[i][j]!=100 :
							self.grille[i][j] = 50

					# on rempli le second cercle de diffusion 
					if abs(a-i)>1 or abs(b-j)>1 :
						if self.grille[i][j]!=0 and self.grille[i][j]!=100 :
							self.grille[i][j] = 25

	# Methode associee a bouger pour remettre a 1 les cases ou l'amibe a bouffe la nourriture de la case (a,b)
	def remettreAUnLesCasesJuxtaposee(self,a,b):
		# on parcours le cercle de diffusion
		for i in xrange(a-2, a+3):
			for j in xrange(b-2, b+3):
				# La diffusion doit rester dans la grille 
				if i>=0 and i<self.xmax and j>=0 and j<self.ymax :
					self.grille[i][j] = 1


class Popu:

	def __init__(self,n):
		self.n = n
		self.tabamibes = [Amibes() for a in range(n)]


##################################### MAIN ####################################


#seed(0) # permet d'avoir toujours la meme grille 

Env = Envir(xmax, ymax, PN)
print Env

Ami = Amibes()
print Ami

for i in xrange(timer):
	Ami.bouger(Env)
	print Ami

print Env

n = 10
pop = Popu(n)
for i in range(n):
	print pop.tabamibes[i].x,pop.tabamibes[i].y
	pop.tabamibes[i].bouger(Env)
	print Ami