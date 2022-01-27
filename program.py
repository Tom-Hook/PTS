"""Program file
"""
import os
import random as r

import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
from matplotlib.patches import ConnectionPatch
from matplotlib.animation import FuncAnimation

from environnement import Environnement
from ville import Ville



def main():
    """Main function
    """
    r.seed(2)
    player = "ordi"
    env = Environnement()
    villes = [
        "Paris",
        "Marseille",
        "St Rem",
        "Toulouse",
        "Bordeau",
        "Lyon",
        "Lille",
        "Toulon",
        "Starsbourg",
        "Montpellier"
    ]
    for ville in villes:
        env.add_ville(ville, r.random()*4000+500, r.random()*4000+500)

    ville_depart = r.choice(env.l_ville)
    env.ville_actuelle = ville_depart
    env.villes_parcourues.append(ville_depart)


    fig, ax_ = plt.subplots(figsize=(16, 8))

    update_graphe(ax_, env)

    if player == "ordi":
        save_total = dict()
        i = 1
        save_total[0] = {
            "actuelle": env.ville_actuelle.nom,
            "parcourues": [ville.nom for ville in env.villes_parcourues],
            "distance": 0
        }
        while not env.voyage_fini:
            ville_choisie = env.choix_ville()
            env.changement_ville_actuelle(ville_choisie)
            save_total[i] = {
                "actuelle": env.ville_actuelle.nom,
                "parcourues": [ville.nom for ville in env.villes_parcourues],
                "distance": env.distance_parcourue
            }
            i += 1

        def update_anim(frame_number):
            # Get an index which we can use to re-spawn the oldest raindrop.
            if frame_number > len(save_total)-1:
                frame_number = len(save_total)-1
            update_graphe(ax_, env, save_total[frame_number], frame_number)

        # Construct the animation, using the update function as the animation director.
        animation = FuncAnimation(fig, update_anim, interval=600, save_count=len(save_total))

        name = "PTS_random"
        report_name = os.path.join("Simu", name)
        # Create new folder verify if it exist too
        if os.path.exists(report_name + ".gif"):
            # Try to add a sufix
            incr = 1
            while os.path.exists(report_name + "_" + str(incr) + ".gif"):
                incr += 1
            # Make it the report name
            report_name += "_" + str(incr)


        #animation.save(f"{report_name}.gif", fps=10)
        #print("Fichier config genere dans : %s" % os.path.abspath(name), end="\n\n")

    if player == "joueur":
        def choix_voyageur(event):
            if not env.voyage_fini:
                ville_choisie: Ville = None
                for ville in env.l_ville:
                    if abs(ville.pos_x - event.xdata) < 60 and abs(ville.pos_y - event.ydata) < 60:
                        ville_choisie = ville
                        break
                if ville_choisie is None:
                    update_graphe(ax_, env)
                    ax_.text(
                        2000,
                        5100,
                        "Cliquer sur une ville !",
                        fontsize=15
                    )
                elif ville_choisie not in env.villes_parcourues:
                    env.changement_ville_actuelle(ville_choisie)
                    update_graphe(ax_, env)
                else:
                    update_graphe(ax_, env)
                    ax_.text(
                        2000,
                        5100,
                        f"{ville_choisie.nom} a déjà été visitée !",
                        fontsize=15
                    )
            if env.voyage_fini:
                ax_.text(
                    1000,
                    2500,
                    f"VOYAGE FINI ! \nDistance totale : {round(env.distance_parcourue)} km !",
                    fontsize=20
                )
            plt.draw()

        _ = fig.canvas.mpl_connect('button_press_event', choix_voyageur)

    plt.show()


def update_graphe(ax_: Axes, env: Environnement, save: list()=None, frame_number: int = None):
    """Update the graph

    Args:
        ax (Axes): [description]
    """
    ax_.clear()

    coords_a = "data"
    coords_b = "data"
    if len(env.villes_parcourues) > 1:
        for index in range(len(env.villes_parcourues) - 1):
            if frame_number is not None and frame_number < index + 1:
                continue
            xy_a = (env.villes_parcourues[index].pos_x, env.villes_parcourues[index].pos_y)
            xy_b = (env.villes_parcourues[index + 1].pos_x, env.villes_parcourues[index + 1].pos_y)
            # On crée un lien entre chaque paire de noeuds s'ils sont voisins
            con = ConnectionPatch(xy_a, xy_b, coords_a, coords_b,
                                arrowstyle="-", shrinkA=5, shrinkB=5,
                                mutation_scale=20, fc="w")
            ax_.add_artist(con)

    for ville in env.l_ville:
        color = "black"
        if save is None:
            if ville.visitee:
                color = "red"
            if ville == env.ville_actuelle:
                color = "green"
        else:
            if ville.nom in save["parcourues"]:
                color = "red"
            if ville.nom == save["actuelle"]:
                color = "green"
        ax_.add_artist(plt.Circle((ville.pos_x, ville.pos_y), 40, color=color, fill=True))
        ax_.plot(ville.pos_x, ville.pos_y, "o", color=color, markersize=15)
        # On ajoute un text pour afficher le nom de la ville
        ax_.text(
            ville.pos_x + 60,
            ville.pos_y + 60,
            ville.nom,
            fontsize="x-small"
        )

    if save is None:
        txt = round(env.distance_parcourue)
    else:
        txt = round(save["distance"])
    ax_.text(
        0,
        5100,
        f"Distance parcourue : {txt} km",
        fontsize=12
    )

    ax_.set_xlim(0, 5000)
    ax_.set_ylim(0, 5000)

if __name__ == "__main__":
    main()
