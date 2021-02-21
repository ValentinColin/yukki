#!/usr/bin/env python3.9
"""Fichiers de multi_index."""
import re
from copy import copy


class MultiIndex:
    """Classe de multi_index."""

    @staticmethod
    def stringToList(chaine: str) -> list:
        return [int(i) for i in chaine.split(".")]

    @staticmethod
    def listToString(liste: list) -> str:
        return ".".join([str(i) for i in liste])

    @classmethod
    def extract(
        cls, path_file: str, regex: str = r"{[\d\.]*}", max_per_line: int = 1
    ) -> list:
        """Renvoie la liste des multi_index"""
        with open(path_file, "r") as file:
            list_multi_index = []
            reg = re.compile(regex)
            for ligne in file:
                list_founded = reg.findall(ligne)
                if len(list_founded) > 0:
                    if (
                        len(list_founded) <= max_per_line
                    ):  # j'en est pas trouver beaucoup
                        list_multi_index += [cls(m_i) for m_i in list_founded]
                    else:  # j'en est trouver trop
                        list_multi_index += [
                            cls(m_i) for m_i in list_founded[:max_per_line]
                        ]
        return list_multi_index

    @classmethod
    def get_from_text(cls, txt: str, regex: str = r"({...})") -> list:
        """Renvoie la liste des multi_index à partir d'une chaine."""
        return [cls(m_i) for m_i in re.compile(regex).findall(txt)]

    def __init__(self, txt):
        """Initialise avec un string ou une liste d'entier"""
        if isinstance(txt, str):
            if (txt[0], txt[-1]) == ("{", "}"):  # car de la forme {1.2.3}
                txt = txt[1:-1]
            elif txt[-1] in (".", ")"):
                txt = txt[:-1]
            self.levels = [
                int(i) for i in txt.split(".")
            ]  # list -> [1, 3, 5] pour 1.3.5
            self.levels_string = txt
        elif isinstance(txt, list):
            liste = txt
            self.levels = liste
            self.levels_string = self.listToString(liste)
        else:
            raise TypeError(f"Only accept list[int] or str, not type: {type(txt)}")

    @property
    def level(self):
        """Renvoie le niveau de profondeur du multi_index."""
        return len(self.levels)

    @property
    def father(self):
        """Renvoie l'index parent."""
        return self.levels[-2]

    def parent(self):
        """Renvoie l'index parent."""
        return self.levels[-2]

    def children(self, list_of_multi_index: list) -> list:
        """Renvoie la liste des enfants (direct) de self à partir d'une liste."""
        father_level = self.level
        children = []
        for node in list_of_multi_index:
            match = True
            if node.level == (
                father_level + 1
            ):  # Bon nombre de niveau pour être un enfant (bonne génération)
                for lvl in range(father_level):
                    if (
                        node[lvl] != self[lvl]
                    ):  # Chaque niveau doivent se correspondre (même lignée)
                        match = False
                        break
                if match:
                    children.append(node)
        return children

    def make_child(self, i: int):
        """Renvoie le n-ième enfant de self."""
        return MultiIndex(self.levels + [i])

    def is_son_of(self, father) -> bool:
        """Vérifie si 'father' est le multi_index père (direct) de self."""
        if (len(self) - 1) == len(father):
            for index in range(len(father)):
                if father[index] != self[index]:
                    result = False
                    break
        else:
            result = False
        return result

    def is_father_of(self, son) -> bool:
        """Vérifie si 'son' le multi_index fils (direct) de self."""
        result = True
        if (len(son) - 1) == len(self):
            for index in range(len(self)):
                if son[index] != self[index]:
                    result = False
                    break
        else:
            result = False
        return result

    def __contains__(self, child) -> bool:
        """Vérifie si child fait partie de la descendance de self.
        Opérateur booléen 'in'.
        """
        for index in range(len(self)):
            if child[index] != self[index]:
                return False
        return True

    def __add__(self, n):
        """"""
        lvl = copy(self.levels)
        lvl[-1] += n
        string = self.listToString(lvl)
        return MultiIndex(string)

    __radd__ = __add__

    def __iadd__(self, n):
        """"""
        self.levels[-1] += n
        self.levels_string = self.listToString(self.levels)

    def __len__(self):
        """Renvoie le niveau du multi_index."""
        return len(self.levels)

    def __getitem__(self, lvl: int):
        """Renvoie l'index de niveau de donnée."""
        if -len(self) <= lvl < len(self):
            return self.levels[lvl]
        else:
            raise IndexError

    def __setitem__(self, lvl: int, index: int):
        """Change l'index de niveau donnée."""
        if isinstance(index, int):
            self.levels[lvl] = index
        else:
            raise TypeError("int expected")

    def __iter__(self):
        """Initialise l'itérateur pour __next__."""
        self.iterator = 0
        return self

    def __next__(self):
        """Renvoie la valeur correspondante à l'itérateur.
        __next__ est définie pour ce cadre de vecteurs ayant 2 composantes.
        """
        if self.iterator < len(self):
            value = self[self.iterator]
            self.iterator += 1
            return value
        else:
            raise StopIteration

    def __contains__(self, child) -> bool:
        """Vérifie si child fait partie de la descendance de self.
        Opérateur booléen 'in'.
        """
        for index in range(len(self)):
            if child[index] != self[index]:
                return False
        return True

    def __str__(self) -> str:
        """Convertion en string."""
        return ".".join([str(i) for i in self.levels])
