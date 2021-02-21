#!/usr/bin/env python3.9

"""Fichiers de formatage des textes discord."""


def fcite(txt: str) -> str:
    """Formate le texte en citation pour discord."""
    return "> " + txt

def fcode(txt: str, code="") -> str:
    """Formate le texte dans un language donnée pour discord."""
    return f"```{code}\n" + txt + "```"

def fmarkdown(txt: str) -> str:
    """Formate le texte en markdown pour discord."""
    return fcode(txt, code="md")

def fpython(txt: str) -> str:
    """Formate le texte en python pour discord."""
    return fcode(txt, code="py")

def fmdcheck(txt: str, level: int = 1) -> str:
    """Formate le texte en markdown pour ajouter une ckeckbox devant."""
    space = (level - 1) * "    "
    return space + "- [ ] " + txt

def flisting(elements: list[str]) -> str:
    """Formate le texte en liste markdown pour discord."""
    return "\n - ".join([""] + elements)
