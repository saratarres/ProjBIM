PN = 'periode de nourriture'
S = 'stress'
F = 'famine'

N = 'normal'


class Envir:

	def __init__ (self,n,objimm):
		self.grille = [] ##A definir nous meme je pense 

		## Correspond au nombre d'amibes présent dans l'Envir
		self.n = n

		##Corrrespond au nombre d'objets immobile dans l'Envir
		self.objimm=objimm


		## On avait parler de faire une jauge , il s'agit donc de l'état de la jauge qui 
		## Varie en fonction de la nourriture.
		self.mode = [PN,S,F]

		### Etat de la case , c'est à dire nourriture , obstacles ou rien 
		## Mais je me demande si ça n'irait pas putot dans la classe amibes 
		self.etat_case = [N]