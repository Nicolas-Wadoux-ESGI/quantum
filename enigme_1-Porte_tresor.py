import numpy as np
from qiskit import *
from qiskit import Aer
from qiskit.visualization import plot_state_city

rightGuard = 0
leftGuard = 1
lieLine = 2

# création des trois lignes, les 2 gardes et la ligne de mensonge
# le second argument est un nombre de bits pour mesurer
circ = QuantumCircuit(3, 3)

###################################################
#### ETAPE 1 - Les gardes savent la même chose ####
###################################################

# le premier guard à 50% de chance d'avoir la porte, donc on le mets en superposition (50% 0 et 50% 1)
# de même pour le mensonge, 50% de chance que rightGuard mente
circ.h(rightGuard)
circ.h(lieLine)

# Les 2 gardes doivent donner la même réponse au début, puisque les deux connaissent la réponse
circ.cx(rightGuard, leftGuard)

#########################################################################
#### ETAPE 2 - Le garde designé par la ligne de mensonge doit mentir ####
#########################################################################


# si lie = 0, le garde de droite doit mentir, sinon c'est le gauche qui ment
def makeGuardLie(circ):
    circ.barrier() # pour afficher une séparation visuelle
    # Si lieLine = 1, gauche ment, CNOT va donc inverser la reponse de gauche (sinon rien ne change)
    circ.cx(lieLine, leftGuard)
    # inverser lieLine, pour que lautre garde ne fasse pas comme le premier (pour qu'il mente ou dise la vérité)
    circ.x(lieLine)
    # Si Lieline etait de 0, maintenant c'est 1, donc on inverse la réponse du garde
    circ.cx(lieLine, rightGuard)
    # remise au point de départ du lieLine que la porte H aurait choisi
    circ.x(lieLine)
    circ.barrier()
    
makeGuardLie(circ)


######################################################################################################
#### ETAPE 3 - La négation permet de forcer les 2 gardes à donner la même reponse, la bonne porte ####
######################################################################################################

# on veut savoir ce que va dire l'autre garde, donc on inverse leurs réponses
circ.swap(rightGuard, leftGuard)

# On veut celle qu'on ne doit pas prendre, pour qu'ils donnent la même réponse, donc on inverse leurs valeurs
circ.x(leftGuard)
circ.x(rightGuard)

# on applique de nouveau le circuit de mensonge car un ment sur ce que l'autre gardien devrait dire
makeGuardLie(circ)

# verification du circuit
circ.draw('mpl')

##########################################
#### ETAPE 4 - Affichage de resultats ####
##########################################

def getResult(circ):
    backend = Aer.get_backend('statevector_simulator')
    job = backend.run(circ)
    return job.result()

# Verification qu'on a bien les 4 possibilités (000, 111, 011, 100)
result = getResult(circ)
outputstate = result.get_statevector(circ, decimals=3)
plot_state_city(outputstate)

# Pour mesurer les états des qubits lors du resultat d'un essai
circ.measure([0, 1, 2], [0, 1, 2])
result = getResult(circ)
counts = result.get_counts(circ) # Affichage d'un résultat au hasard
resultLie, resultGuardLeft, resultGuardRight = list(counts)[0]
print({'liar': 'rightGuard' if resultLie == '0' else 'leftGuard', 'resultGuardLeft': resultGuardLeft, 'resultGuardRight': resultGuardRight})

