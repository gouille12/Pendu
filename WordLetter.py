#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Cédric Guyaz"
__date__ = "03 aout 2016"

"""
**********PROJET PENDU**********
WordLetter.py : Les classes contenant le mot à trouver
			 et les constituants du mot à trouver (Word, Letter)
GamePendu.py : La mécanique interne du jeu (GamePendu)
GraphicInterfacePendu.py : L'interface graphique (GraphicInterfacePendu)
Instructions.txt : Les instructions du jeu (en lecture seulement)
WordsList.txt : La liste de mot d'où l'ordinateur choisit un mot (en lecture seulement)
History.txt : L'historique des parties jouées (lecture et écriture)
BackgroundGame.png : le fond d'écran de l'interface graphique
"""

class Word:
	
	def __init__(self, word, number_max_errors):

		self.number_errors = 0
		self.number_tries = 0
		self.number_max_errors = number_max_errors
		self.every_letter_in_word = []
		for character in word:
			self.every_letter_in_word.append(Letter(character))


	def __str__(self):

		self.printed_word = ""
		for character in self.every_letter_in_word:
			if character.get_revealed() == False:
				self.printed_word += "*"
			else:
				self.printed_word += str(character)
		return self.printed_word


	def get_character(self, position):

		return self.every_letter_in_word[position]


	def contains(self, searched):

		if searched not in self.every_letter_in_word:
			return False

		else:
			i = -1
			positions = []
			for character in self.every_letter_in_word:
				i += 1
				if character == searched:
					positions.append(i)
			return positions


	def get_winning(self):

		if self.number_errors < self.number_max_errors:
			for letter in self.every_letter_in_word:
				if letter.get_revealed() != True:
					return False
			return True
		else:
			return False


	def get_losing(self):

		if self.number_errors >= self.number_max_errors:
			return True
		else:
			return False


	def get_errors(self):

		return self.number_errors


	def add_error(self):

		self.number_errors += 1


	def get_tries(self):

		return self.number_tries


	def add_try(self):

		self.number_tries += 1





class Letter:

	def __init__(self, character):

		self.character = character
		self.is_revealed = False


	def __eq__(self, compared):

		if self.character == compared:
			return True
		else:
			return False


	def __str__(self):

		return self.character


	def get_revealed(self):

		return self.is_revealed


	def set_revealed(self, value):

		self.is_revealed = value





