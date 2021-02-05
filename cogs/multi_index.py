#!/usr/bin/env python3.9
"""Fichiers de multi_index."""


class MultiIndex:
	"""Classe de multi_index."""

	@staticmethod
	def stringToList(chaine):
		return [int(i) for i in chaine.split('.')]

	@staticmethod
	def listToString(liste):
		return '.'.join(liste)

	@classmethod
	def extract(cls, path: str):
		"""Renvoie la liste des multi_index"""
		pass

	def __init__(self, arg: str):
		""""""
		levels_string = arg
		levels = [int(i) for i in arg.split('.')] # list -> [1, 3, 5] pour 1.3.5

	def __add__(self, n):
		""""""
		lvl = self.levels[-1]
		lvl[-1] += n
		string = listToString(lvl)
		return MultiIndex(string)

	__radd__ = __add__

	def __iadd__(self, n):
		""""""
		self.levels[-1] += n
		self.levels_string = listToString(self.levels)
