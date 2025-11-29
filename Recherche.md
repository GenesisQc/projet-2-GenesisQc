# Étape 1 : Définir la classe Portal afin de lui attribuer ses valeurs
# Étape 2 : Définir les différentes valeurs nécessaire pour le portail comme le layout du maze, la taille, la largeur et la couleur 
# Étape 3 : Puisque nous voulons que le portail apparait seulement dans les couloirs on code une boucle qui relance tant et autant que les coordonnées du portail se retrouvent dans les couloirs et non les murs
# Étape 4 : Faire référence à la classe parente pour le reste des choses nécessaire
# Étape 5 : définir une fonction update qui va mettre à jour les coordonnées des entitées qui vont entrer le portail
# Étape 6 : Définir la fonction qui va permettre de dessiner le portail sur l'écran avec sa couleur assigné
# Étape 7 : Maintenant tourner notre attention au fichier game.py pour définir les fonctions qui vont permettre les téléportations entre les portails lorsqu'une entité entre à l'intérieur
# Étape 8 : créer deux instances de portails "portal_blue" et "portal_orange" et définir un cooldown pour les entitées lorsqu'elle entre le portail pour éviter qu'elles restent coincer
# Étape 9 : Créer la fonction handle_teleportation qui calculera les hitbox des portails et vérifiera le cooldown d'une entité avant de la laisser par la suite se téléporter si il y a colision entre le portail et l'entité qui ensuite rajoutera un cooldown de 30 fps ou secondes pour empêcher l'entité de se téléporter à l'infinie
# Étape 10 : Définir la fonction qui va calculer les nouvelles coordonnées des entitées suite à leur téléportation
# Étape 11 : Finir le tout en rajoutant les instances dans draw pour que les portails soient dessiner dans le jeu
# En terme de difficulté, il n'était pas aussi simple que prévu d'intégrer une nouvelle classe dans un jeu déja complet sans créer de nouveaux problèmes. Bien sûr l'avantage d'avoir coder des fonctions similaires dans le projet comme draw et se fier aux classes déja définies m'a permis de pouvoir définir la classe Portail sans grand problème. Ensuite, l'intégration du tout dans le fichier game.py n'a pas été aussi simple elle aussi, mais en faisant des tests avec des échecs et des erreurs il a été possible de faire le tout. 