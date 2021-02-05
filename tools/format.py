#!/usr/bin/env python3.9
"""Fichiers de formatage des textes discord."""

def fcite(txt):
	"""Formate le texte en citation pour discord."""
	return '> ' + txt

def fcode(txt, code=''):
	"""Formate le texte dans un language donnée pour discord."""
	return f'```{code}\n' + txt + '```'

def fmarkdown(txt):
	"""Formate le texte en markdown pour discord."""
	return fcode(txt, code='md')

def fpython(txt):
	"""Formate le texte en python pour discord."""
	return fcode(txt, code='py')

def fmdcheck(txt, level=1):
	"""Formate le texte en markdown pour ajouter une ckeckbox devant."""
	space = (level - 1) * '    '
	return space + '- [ ] ' + txt