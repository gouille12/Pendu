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

from WordLetter import *
import random
import sys
import getpass

class GamePendu:

	def __init__(self, number_players, word_chosen = None):

		self.number_max_errors = 5
		self.number_players = number_players
		self.word_chosen = word_chosen

		if self.number_players == 1:
			self.file_words = open("WordsList.txt", "r")
			self.words_lines = self.file_words.readlines()
			self.lines_number = len(self.words_lines)
			self.random_index = random.randint(0, self.lines_number)
			self.printable_solution = self.words_lines[self.random_index].strip()
			self.file_words.close()
		
		elif self.number_players == 2:
			self.printable_solution = self.word_chosen
			self.printable_solution = self.printable_solution.lower()

		self.key_word = Word(self.printable_solution, self.number_max_errors)
		self.every_letters_tried = []


	def try_letter(self, letter):

		self.letter_tried = letter		
		if (self.letter_tried.isalpha() == True and
			self.letter_tried.lower() not in self.every_letters_tried and
			len(self.letter_tried) == 1):

			self.letter_tried = self.letter_tried.lower()
			self.every_letters_tried.append(self.letter_tried)
			self.key_word.add_try()

			if self.key_word.contains(self.letter_tried) == False:
				self.key_word.add_error()
			else:
				for individual_position in self.key_word.contains(self.letter_tried):
					element = self.key_word.get_character(individual_position)
					element.set_revealed(True)
		else:
			return False


	def get_game_stats(self):

		self.count = 1
		self.printable_every_letters_tried = "[ "
		for element in self.every_letters_tried:
			self.printable_every_letters_tried += str(element)
			if self.count != len(self.every_letters_tried):
				self.printable_every_letters_tried += ", "
			self.count += 1
		self.printable_every_letters_tried += " ]"

		return (self.key_word.get_tries(), self.key_word.get_errors(), self.printable_every_letters_tried)


	def get_key_word(self):

		return self.key_word


	def game_status(self):

		return (self.key_word.get_winning(), self.key_word.get_losing())


	def reveal_word(self):

		return self.printable_solution


	def write_history(self):

		if self.key_word.get_winning() == True:
			self.printable_winning = "Oui"
		else:
			self.printable_winning = "Non"
		self.history_file = open("History.txt", "a")
		self.history_file.write("Mot : {} --- Mode : {} joueur(s) --- Réussite : {} --- "
		"Essais : {}\n".format(self.printable_solution, self.number_players, self.printable_winning, 
			self.key_word.get_tries()))
		self.history_file.close()