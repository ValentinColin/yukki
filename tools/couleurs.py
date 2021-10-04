"""
Module de couleurs répertoriant quelques constantes de couleurs RGB/RVB
"""
import re

# CONSTANTE DE COULEURS RGB

BLEU       = (  0,   0, 255)
ROUGE      = (255,   0,   0)
VERT       = (  0, 255,   0)
VERT_FONCE = (  0, 100,   0)
NOIR       = (  0,   0,   0)
BLANC      = (255, 255, 255)
JAUNE      = (255, 255,   0)
VIOLET     = (100,   0, 100)
ORANGE     = (255, 150,   0)
ROSE       = (255, 192, 203)

BLUE       = (  0,   0, 255)
RED        = (255,   0,   0)
GREEN      = (  0, 255,   0)
YELLOW     = (255, 255,   0)
BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
GREY       = (100, 100, 100)
PURPLE     = (100,   0, 100)
ORANGE     = (255, 165,   0)
HALFGREY   = ( 50,  50,  50)
DARKGREY   = ( 20,  20,  20)
DARKRED    = ( 10,  10,  10)
DARKGREEN  = ( 10,  10,  10)
DARKBLUE   = ( 10,  10,  10)
LIGHTRED   = (255, 200, 200)
LIGHTGREEN = (200, 255, 200)
LIGHTBLUE  = (200, 200, 255)
LIGHTBROWN = (229, 219, 222)
LIGHTGREY  = (200, 200, 200)
BEIGE      = (199, 175, 138)


def is_hex(txt):
    """Est un nombre hexa du type 5c8d3f ou FF12CE ou b42 ou A4F"""
    pattern_hex = r"^([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$"
    match = re.fullmatch(pattern_hex, txt)
    m = re.match(pattern_hex, txt)
    return match.group(0) == txt


def color_to_hex(color: tuple):
    """Converti un triplet rgb en valeur hex sous forme de string"""
    r, g, b = color
    return f"{r:02x}{g:02x}{b:02x}"


def convert_to_hex(*args):
    """Converti en hexadecimal, return None en cas d'erreur"""
    if len(args) == 1:
        arg = str(args[0]).upper()
        if arg in locals():
            return convert_to_hex(*(locals()[arg]))
        if is_hex(arg):
            return arg
        return None
    elif len(args) == 3:
        return color_to_hex(*args)
    else:
        return None
