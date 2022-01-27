

class Ville:

    def __init__(self, p_nom: str, p_pos_x: float, p_pos_y: float) -> None:

        self.nom = p_nom

        self.pos_x = p_pos_x
        self.pos_y = p_pos_y

        self.visitee = False
