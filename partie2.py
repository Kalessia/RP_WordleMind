import random
import numpy as np



random.seed(42)

class algorithmeGenetique():
    """
    ensE : ensembe des mots comp
    """
    def __init__(self, motPrec, domainesMotPrec, taillePop, maxSizeEnsE, maxGen, timeout, opCroisement = None, opMutation = None, probaMutation = 0.5, ):
        self.tailleIndividu = len(domainesMotPrec)
        self.motPrec = motPrec
        self.domainesMotPrec = domainesMotPrec
        self.taillePop = taillePop
        self.tailleEnsE = maxSizeEnsE
        self.maxGen = maxGen
        self.tempsExtra = timeout # temps maximal autorisé pour la recherche d'un mot compatible. Ce temps passé, l'algo échoue
        self.opCroisement = opCroisement
        self.opMutation = opMutation
        self.probaMutation = probaMutation

        self.ensE = [] # ensemble de mots compatibles avec l'ensemble des essais precedents
        self.pop = self.motPrec
        self.tabFitnesses = [0] * self.taillePop  # une case fitness pour chaque individu
        
    #---------------------------------------------------------------------------

    def generePopulation(self):
        """Initialisation de la population de mots initiale
        """
        pop = self.pop
        taillePopCourante = len(self.pop) # Cette taille pop se réfere à la taille de la population courante, qui vaut 1 en initialisation
        parentDomaines = self.domainesMotPrec


        # adapter a n importe quelle taille pop
        # for p in range(self.taillePop): # Cette taille pop se réfere à la taille finale que la population devra avoir
        #     if self.opCroisement != None:
        #         enfant = self.opCroisement(parent)
        #     if self.opMutation != None:
        #         enfant = self.opCroisement(parent, parentDomaines, self.probaMutation)
        #     pop.append(enfant)
        return pop


    #---------------------------------------------------------------------------
    # Operateurs de croisement
    #---------------------------------------------------------------------------

    def onePointCrossover(self, parent1, parent2):
        """ parent1, parent2 : deux mots
        """
        if len(parent1) < 2:
            return parent1
           
        enfant = []
        pointCoupure = random.randint(1, len(parent1)-1) # on exclut la 1ère case
       
        for i in range(len(parent1)):
            if i < pointCoupure:
                enfant.append(parent1[i])
            else:
                enfant.append(parent2[i])
       
        return enfant

    #---------------------------------------------------------------------------

    def twoPointsCrossover(self, parent1, parent2):
        """ parent1, parent2 : deux mots
        """
        if len(parent1) < 3:
            return parent1
           
        enfant = []
        tailleEnfant = len(parent1)
       
        pointCoupure1 = random.randint(1, tailleEnfant-1) # on exclut la 1ère case
        pointCoupure2 = random.randint(2, tailleEnfant-1)
       
        # On veut que le  pointCoupure1 précède le pointCoupure2 comme position
        while pointCoupure2 <= pointCoupure1:
            pointCoupure1 = random.randint(1, tailleEnfant-1)
            pointCoupure2 = random.randint(2, tailleEnfant-1)
           
        for i in range(tailleEnfant):
            if i < pointCoupure1 or i >= pointCoupure2:
                enfant.append(parent1[i])
            else:
                enfant.append(parent2[i])
       
        return enfant

    #---------------------------------------------------------------------------

    def aleaCharMutation(self):
        """ 
        """
        enfant = list(self.motPrec)
        domainesEnfant = list(self.domainesMotPrec)
       
        if random.random() >= self.probaMutation:
            posLettre = random.randint(len(enfant)-1)
            enfant[posLettre] = random.choice(domainesEnfant[posLettre])
       
        return enfant

    #---------------------------------------------------------------------------

    def opSelection_kTournament(self, k):
        """ populationCourante : liste de mots [param1, ... , paramN]
            tabFitness : liste des fitness rélatives à chaque jeu de paramètres
            k : nombre de individus à sélectionner dans la population résultante
        """
        assert len(self.taillePop) >= k 

        indicesMax = list(np.argmax(np.arrayself.tabFitnesses)[0:3])
        newParents = [self.pop[indice] for indice in indicesMax]

        pop = self.generePopulation()
        return pop

        # Calcul des fitness associées à chaque individu de la population



    # def kTournement(populationCourante, tabFitness, nbIndAEcarter):
    #     """ populationCourante : liste de jeux de paramètres [param1, ... , paramN]
    #         tabFitness : liste des fitness rélatives à chaque jeu de paramètres
    #         nbIndAEcarter : nombre de individus à exclure dans la population résultante
    #     """
       
    #     if len(populationCourante) <= nbIndAEcarter:
    #         nbIndAEcarter = len(populationCourante) - 1 # newPopulation contiendra un seul individu au dernier tournoi

    #     borneMaximale = 10000000

    #     newPopulation = list(populationCourante)
    #     tabFitness_copy = list(tabFitness)
   
    #     for i in range(nbIndAEcarter):          
    #         minFitness = min(tabFitness_copy)
    #         indiceMinFitness = [r for r, j in enumerate(tabFitness_copy) if j == minFitness]
    #         tabFitness_copy[indiceMinFitness[0]] = borneMaximale
    #         del newPopulation[indiceMinFitness[0]]
           
    #     return newPopulation

    #---------------------------------------------------------------------------

    def determinerProchaineTentative(self):

        #cond d arret = maxsize ens e atteinte
        #cond d arret = apres maxgen generations


        prochaineTentative = random.choice(self.ensE, 1)
        return prochaineTentative




################################################################################################
################################################################################################
################################################################################################
################################################################################################






    #---------------------------------------------------------------------------
    #   Operateurs de sélection
    #       - fitness proportionate : sélection proportionnelle à fitness
    #       - k-tournement : sélection progressive de k individus parmi N
    #       - plus-sélection (u+l) : on génère l enfants à partir des meilleurs u, on garde u et l
    #       - comma-sélection (u,l) : on génère l enfants à partir des meilleurs u, on ne garde que l
    #---------------------------------------------------------------------------

    def f_operateurSelection(opSel, populationCourante, tabFitness, u, l, Y, nbIndAExtraire, nbIndAEcarter, opVar):
        if opSel == 1:
            return fitnessProportionate(populationCourante, tabFitness, nbIndAExtraire)
        if opSel == 2:
            return kTournement(populationCourante, tabFitness, nbIndAEcarter)
        if opSel == 3:
            return plusSelection(populationCourante, tabFitness, u, l, Y, opVar)
        if opSel == 4:
            return commaSelection(populationCourante, tabFitness, u, l, Y, opVar)
   
    #---------------------------------------------------------------------------

    def fitnessProportionate(populationCourante, tabFitness, nbIndAExtraire):
        """ populationCourante : liste de jeux de paramètres [param1, ... , paramN]
            tabFitness : liste des fitness rélatives à chaque jeu de paramètres
            nbIndAExtraire : nombre de individus constituant la population résultante
        """
       
        if len(populationCourante) <= nbIndAExtraire:
            return populationCourante
         
        newPopulation = []  
       
        # Création d'un tableau de poids probaProportionate
        probaProportionate = []
        totFitness = sum(tabFitness)
        for i in range(len(tabFitness)):
            probaProportionate.append(tabFitness[i]/totFitness)
       
        # La probabilité d'un individu d'être selectionné depend de sa valeur fitness
        populationCourante_indices = [i for i in range(len(populationCourante))]
        for i in range(nbIndAExtraire):
            indiceAExtraire = random.choices(populationCourante_indices, weights=probaProportionate, k=1)
            newPopulation.append(populationCourante[indiceAExtraire[0]])
            probaProportionate[indiceAExtraire[0]] = 0
           
        return newPopulation
 
    #---------------------------------------------------------------------------
 
    def kTournement(populationCourante, tabFitness, nbIndAEcarter):
        """ populationCourante : liste de jeux de paramètres [param1, ... , paramN]
            tabFitness : liste des fitness rélatives à chaque jeu de paramètres
            nbIndAEcarter : nombre de individus à exclure dans la population résultante
        """
       
        if len(populationCourante) <= nbIndAEcarter:
            nbIndAEcarter = len(populationCourante) - 1 # newPopulation contiendra un seul individu au dernier tournoi

        borneMaximale = 10000000

        newPopulation = list(populationCourante)
        tabFitness_copy = list(tabFitness)
   
        for i in range(nbIndAEcarter):          
            minFitness = min(tabFitness_copy)
            indiceMinFitness = [r for r, j in enumerate(tabFitness_copy) if j == minFitness]
            tabFitness_copy[indiceMinFitness[0]] = borneMaximale
            del newPopulation[indiceMinFitness[0]]
           
        return newPopulation
 
    #---------------------------------------------------------------------------
 
    def plusSelection(tabParents, tabFitness, u, l, Y, opVar):
        """ tabParents (populationCourante) : liste de jeux de paramètres [param1, ... , paramN]
            tabFitness : liste des fitness rélatives à chaque jeu de paramètres
            u : nombre de meilleurs parents constituant la population résultante
            l : nombre d'enfants constituant la population résultante
            Y : espace de recherche
            opVar : operateur de variation à appliquer pour la génération des enfants
        """
       
        if u >= len(tabParents) or u+l != len(tabParents) :
            return tabParents
       
        newPopulation = []
        tabFitness_copy = list(tabFitness)
               
        # Sélection des meilleurs parents u
        tabBestU = []
        for i in range(u):
            maxFitness = max(tabFitness_copy)
            indiceMaxFitness = [r for r, j in enumerate(tabFitness_copy) if j == maxFitness]
            tabBestU.append(tabParents[indiceMaxFitness[0]])
            tabFitness_copy[indiceMaxFitness[0]] = 0
        newPopulation = list(tabBestU)
       
        # Ajout des enfants générés à partir des meilleurs parents u
        for i in range(l):
            tabBestU_copy = list(tabBestU)
            parent1 = random.choice(tabBestU_copy)
            tabBestU_copy.remove(parent1)
            if len(tabBestU_copy) > 0:
                parent2 = random.choice(tabBestU_copy)
            else:
                parent2 = list(parent1)
            newEnfant = f_operateurVariation(opVar, parent1, parent2, Y)
            newPopulation.append(newEnfant)
           
        return newPopulation
       
    #---------------------------------------------------------------------------
   
    def commaSelection(tabParents, tabFitness, u, l, Y, opVar):
        """ tabParents (populationCourante) : liste de jeux de paramètres [param1, ... , paramN]
            tabFitness : liste des fitness rélatives à chaque jeu de paramètres
            u : nombre de meilleurs parents générant la population résultante
            l : nombre d'enfants constituant la population résultante
            Y : espace de recherche
            opVar : operateur de variation à appliquer pour la génération des enfants
        """
       
        if u >= len(tabParents) or l != len(tabParents) or len(tabParents) == 1:
            return tabParents
       
        newPopulation = []
        tabFitness_copy = list(tabFitness)
               
        # Sélection des meilleurs parents u
        tabBestU = []
        for i in range(u):
            maxFitness = max(tabFitness_copy)
            indiceMaxFitness = [r for r, j in enumerate(tabFitness_copy) if j == maxFitness]
            tabBestU.append(tabParents[indiceMaxFitness[0]])
            del tabFitness_copy[indiceMaxFitness[0]]
       
        # Sélection des enfants générés à partir des meilleurs parents u            
        for i in range(l):
            tabBestU_copy = list(tabBestU)
            parent1 = random.choice(tabBestU_copy)
            tabBestU_copy.remove(parent1)
            if len(tabBestU_copy) > 0:
                parent2 = random.choice(tabBestU_copy)
            else:
                parent2 = list(parent1)
            newEnfant = f_operateurVariation(opVar, parent1, parent2, Y)
            newPopulation.append(newEnfant)
           
        return newPopulation
           
           
           

           
    #---------------------------------------------------------------------------
       
    def swapMutation(parent):
        """ parent : jeu de paramètres [val1, ... , valN]
        """
        if len(parent) < 2:
            return parent
       
        # On s'assure que le parent n'est pas constitué d'une seule valeur identique pour toutes les cases  
        for i in range(1, len(parent)):
            if parent[0] != parent[i]:
                break
            else:
                if i == len(parent)-1:
                    return parent
           
        enfant = list(parent)
       
        indiceBit1 = random.randint(0, len(enfant)-1)   # intervalle fermé [0, len(enfant)-1]
        indiceBit2 = random.randint(0, len(enfant)-1)
                   
        while indiceBit2 == indiceBit1 or enfant[indiceBit2] == enfant[indiceBit1]:
            indiceBit2 = random.randint(0, len(enfant)-1)
       
        tmp = enfant[indiceBit1]
        enfant[indiceBit1] = enfant[indiceBit2]
        enfant[indiceBit2] = tmp
       
        return enfant
       
    #---------------------------------------------------------------------------
   

    #---------------------------------------------------------------------------
    #   Algorithmes d'optimisation
    #---------------------------------------------------------------------------

    def comportement3(nbIndividus, dimParam, Y, dureeUneEval, nbMaxEval, seuilConvergence, opSel, u, l, opVar, nbIndAExtraire, nbIndAEcarter, fCtrl, fEval, verbose, boolPlot, nomFichier):
        global param, populationCourante, bestParam, bestFitness, cptConvergence, tabEvalCourante, bestFitness
       
        # Vérification des critères d'arrèt de la phase d'optimisation
        evalCourante = iterationCourante/dureeUneEval
        if evalCourante > nbMaxEval or cptConvergence >= seuilConvergence:
            t, r = f_fonctionControle(fCtrl, bestParam)
            return t, r
       
        # Initialisation de la population initiale. populationCourante est une liste de param
        if iterationCourante == 0:
            populationCourante = genereAleaPopInitiale(nbIndividus, dimParam, Y)
            bestParam = random.choices(Y, k=dimParam)
         
        # Après chaque 'dureeUneEval' itérations :
        #   - évaluation des individus appartenants à la population courante (tabFitness)
        #   - choix du meilleur jeu de paramètres:
        #       - détection de la meilleure des fitness dans tabFitness (maxFitness)
        #       - si maxFitness est meilleure de la bestFitness de l'évaluation précedente :
        #           - on note cette évaluation comme BestEval
        #           - on adopte le nouveau jeu de paramètres param (param courant = celui qui vient
        #             d'être évalué)
        #       - sinon :
        #           - maintien de l'ancien jeu de paramètres (bestParam) rélatif à la dernière bestEval
       
        if iterationCourante % dureeUneEval == 0:
            tabFitness = []
            for p in range(len(populationCourante)):
                tabFitness.append(f_fitness(fEval, populationCourante[p]))
            maxFitness = max(tabFitness)
            indiceMaxFitness = [i for i, j in enumerate(tabFitness) if j == maxFitness]
           
            if (verbose):
                print("\n-------------------------------------------------------")
                print("Géneration n.", evalCourante, ":")
                print("\tPopulation courante :\t", populationCourante)
                print("\tFitness population :\t", tabFitness)
           
            if maxFitness > bestFitness:
                bestFitness = maxFitness
                bestEval = evalCourante
                bestParam = populationCourante[indiceMaxFitness[0]]      
                cptConvergence = 0
            else:
                cptConvergence += 1            
           
            populationCourante = f_operateurSelection(opSel, populationCourante, tabFitness, u, l, Y, nbIndAExtraire, nbIndAEcarter, opVar)
           
            if (verbose):
                print("\tMeilleur jeu de paramètres :\t", bestParam, "avec fitness =", bestFitness)
                print("\tConvergence :\t", cptConvergence, "\n")
                if evalCourante == nbMaxEval or cptConvergence == seuilConvergence:  
                    print("\n-------------------------------------------------------")
                    print("Fin phase d'optimisation!")
                    print("\tMeilleur jeu de paramètres :\t", bestParam, "avec fitness =", bestFitness)
                    print("-------------------------------------------------------\n")            
                         
            # Construction et affichage du graphique, à la fin de la phase d'optimisation
            if boolPlot:
                tabEvalCourante.append(evalCourante)
                tabBestFitness.append(bestFitness)
                if evalCourante == nbMaxEval or cptConvergence == seuilConvergence:    
                    plotResults(tabEvalCourante, tabBestFitness, nomFichier)
       
       
               
        t, r = f_fonctionControle(fCtrl, bestParam)

        return t, r
   


####################################################################################################


       
####################################################################################################
   


    ############################################################################
    #   Représentation graphique des résultats
    ############################################################################

    def plotResults(evalCourante, bestFitness, nomFichier):
        x = evalCourante # abscisses : evaluations
        y = bestFitness # ordonnées : performance
       
        plt.figure()
        plt.suptitle("Fin optimisation ! Evolution des solutions candidates", color = 'red')
        texte = "bestParam optimisé = " + "".join(str(bestParam))
        plt.title(texte)
        plt.xlabel("Evaluations")
        plt.ylabel("Fitness")
        plt.scatter(x, y, marker='o', color='red')
        plt.show()

        # Sauvegarde du tracé
        if nomFichier != None:
            plt.savefig(nomFichier, transparent = True)



    ############################################################################
    # Séléction du comportement à appliquer pour cette bataille :
    #   - vitesse de translation (entre -1 et +1)
    #   - vitesse de rotation (entre -1 et +1)
    ############################################################################
   
    # paramètres à initialiser pour tous les Comportements
    verbose = True     # Mettre à True si l'on souhaite afficher des informations détaillées sur le déroulement du jeu
   
    #---------------------------------------------------------------------------
   
    # paramètres à initialiser en cas de Comportement type 3 (algorithmes génétiques)
   
    nbIndividus = 3     # nombre d'individus de la population initiale. nbIndividus doit être > 1
    dimParam = 8        # dimension de la liste de paramètres param
    Y = [-1, 0, 1]      # espace de recherche = ensemble des valeurs possibles des paramètres
   
    dureeUneEval = 500  # durée d'une évaluation exprimée en nombre d'itérations
    nbMaxEval = 10      # budget maximal d'évaluations permis pour cette optimisation (critère d'arrèt)
    seuilConvergence = 8 # nombre d'évaluations minimal accepté pour établir une convergence (critère d'arrèt)
   
    opSel = 3           # opSel = operateur de sélection à appliquer
    nbIndAExtraire = 2  #   - 1 : fitnessProportionate
    nbIndAEcarter = 2   #   - 2 : kTournement
    u = 1               #   - 3 : plusSelection
    l = 2               #   - 4 : commaSelection
   
    opVar = 1           # opVar = operateur de variation à appliquer
                        #   - 1 : bitFlipMutation
                        #   - 2 : swapMutation
                        #   - 3 : onePointCrossover
                        #   - 4 : twoPointsCrossover
                       
    fCtrl = 2           # fCtrl = fonction de controle à appliquer
                        #   - 1 : fonction issue du TP2 (optimisation.py)
   
    fEval = 2           # fEval = fonction fitness à appliquer
                        #   - 1 : distance moyenne parcourue
   
    boolPlot = True     # Mettre à True si l'on souhaite afficher à l'écran le graphique
    nomFichier = ""     # Ajouter un nom de fichier si l'on souhaire sauvegarder le graphique dans un fichier
   
    # Conseils de paramètrage :
    #   - nbMaxEval <= nombre d'itérations totales (2000?) / dureeUneEval
    #   - seuilConvergence < nbMaxEval
    #   - dimParam = nombre de paramètres utilisés dans fCtrl ou fEval
    #   - si opSel = 1, alors nbIndAExtraire < nbIndividus
    #   - si opSel = 2, alors nbIndAEcarter < nbIndividus
    #   - si opSel = 3, alors u < nbIndividus, u+l = nbIndividus
    #   - si opSel = 4, alors u < nbIndividus, l = nbIndividus
    #   - si opVar = 1, alors dimParam > 1
    #   - si opVar = 2, alors dimParam > 2
    #   - si opVar = 3, alors dimParam > 1, nbIndividus > 1
    #   - si opVar = 4, alors dimParam > 2, nbIndividus > 1
 
    #---------------------------------------------------------------------------
   
    # Choix du comportement de type 1, 2 ou 4 (sans arguments)
    #translation, rotation = comportement2_2()
   
    # Choix du comportement de type 3 (algorithmes génétiques)
    translation, rotation = comportement3(nbIndividus, dimParam, Y, dureeUneEval, nbMaxEval, seuilConvergence, opSel, u, l, opVar, nbIndAExtraire, nbIndAEcarter, fCtrl, fEval, verbose, boolPlot, nomFichier)
   
    #---------------------------------------------------------------------------
   
    # Mise à jour de la valeur de l'itération courante
    iterationCourante += 1
