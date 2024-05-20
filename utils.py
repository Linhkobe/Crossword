def afficher_grille(grille):
    for ligne in grille:
        print(" ".join([str(case) if case is not None else "." for case in ligne]))