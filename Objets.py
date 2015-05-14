class objets : 

	def __init__(self,x,y):

		#Correspond aux coordonnées de l'objet
		self.x =x
		self.y = y

		#Correspond au poids que l'on va donner à l'objet 
		#Si il s'agit d'un obstacle ça sera 0  
		#Si il s'agit de nourriture ce sera 10 000 par exemple
		self.p =0

	##On appelle la methode nourriture pour donner le poid 10 000 à la case. 7
	## Mais est ce que c'est vraiment necessaire d'avoir une classe pour ça. 
	### On peut nous memem manuellement remplacer des cases par 0 ou 10000 et placer
	#Nos obstacles et notre nourriture comme bon nous semble non ?

	def nourriture (self):
		self.p = 10000

