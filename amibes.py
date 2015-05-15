#------------------------------------------------------------------------------#
#																			   #
#								  AMIBES							  		   #
#																			   #
#------------------------------------------------------------------------------#

N = 'normal'
V = 'vibration'
D = 'diffusion'
M = 'mort'

n = 'nourriture'
o = 'obstacles'

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
		return "L'amibe est en position (%d - %d) et est dans l'état %s"%(self.x, self.y, self.etat_actuel)

#Fonctions qui permet de bouger en fonction du poids des matrices autour. En sachant qu'on 
#a pas a gerer les effets de bords car on a dit qu'on mettrais 0 partout ailleurs
#Pour que jamais il n'aille de ce cote. Mais je n'ai pas coder l'hypothese ou on a deux poids
#Egaux de chaque cote. Je ne me souviens plus trop de ce qu'on avait convenu comme marche a suivre
#J'ai gerer le fait qu'il puisse y avoir un obstacle


	def bouger (self,grille):
		if grille[self.x][self.y] != 100 : # Si l'amibe a trouve la nourriture, elle ne bouge plus

			temp = 0
			xtemp = self.x
			ytemp = self.y
		

			if (grille[self.x+1][self.y] > temp and grille[self.x+1][self.y]!=o):
				temp = grille[self.x+1][self.y]
				xtemp = self.x+1
				ytemp = self.y

			if (grille[self.x+1][self.y-1] > temp and grille[self.x+1][self.y-1]!=o):
				temp = grille[self.x+1][self.y-1]
				xtemp = self.x+1
				ytemp = self.y-1

			if (grille[self.x][self.y-1]>temp and grille[self.x][self.y-1]!=o):
				temp = grille[self.x][self.y-1]
				xtemp = self.x
				ytemp = self.y-1

			if (grille[self.x-1][self.y-1]>temp and grille[self.x-1][self.y-1]!=o):
				temp = grille[self.x-1][self.y-1]
				xtemp = self.x-1
				ytemp = self.y-1

			if (grille[self.x-1][self.y]>temp and grille[self.x-1][self.y]!=o):
				temp = grille[self.x-1][self.y]
				xtemp = self.x-1
				ytemp = self.y

		
			if (grille[self.x-1][self.y+1]>temp and grille[self.x-1][self.y+1]!=o):
				temp = grille[self.x-1][self.y+1]
				xtemp = self.x-1
				ytemp = self.y+1

			if (grille[self.x][self.y+1]>temp and grille[self.x][self.y+1]!=o):
				temp = grille[self.x][self.y+1]
				xtemp = self.x
				ytemp = self.y+1

			if (grille[self.x+1][self.y+1]>temp and grille[self.x+1][self.y+1]!=o):
				temp = grille[self.x+1][self.y+1]
				xtemp = self.x+1
				ytemp = self.y+1

			#print "La plus grande valeur est" , temp , "de coordonnee", xtemp,ytemp

			self.x = xtemp
			self.y = ytemp



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







test = Amibes(40,20,2,1)
print test.x , test.y , test.etats
grille = [[0,0,0,0,0],[0,2,o,1,0],[0,1,3,4,0],[0,0,0,0,0]]
print grille,grille[2][1]
test.bouger(grille)
