import sys

def valid_values(name, lvl, time, ingr, desc, rtype):
	"""Function to check if values are valid Recipe attributes"""
	valid = 1
	if not isinstance(name, str):
		print("Error: Name must be a string.")
		valid = 0
	try:
		if len(name) == 0:
			print("Error: Name cannot be empty.")
			valid = 0
	except TypeError:
		pass
	if not isinstance(lvl, int):
		print("Error: Cooking level must be an integer.")
		valid = 0
	try:
		if not 0 < lvl < 6:
			print("Error: Cooking level value is invalid.")
			valid = 0
	except TypeError:
		pass
	if not isinstance(time, int):
		print("Error: Prep time must be an integer.")
		valid = 0
	try:
		if time <= 0:
			print("Error: Prep time value is invalid.")
			valid = 0
	except TypeError:
		pass
	if not isinstance(ingr, list):
		print("Error: Ingredients must be a list.")
		valid = 0
	try:
		if len(ingr) == 0:
			print("Error: Ingredients cannot be empty.")
			valid = 0
	except TypeError:
		pass
	if not isinstance(desc, str):
		print("Error: Description must be a string.")
		valid = 0
	if not isinstance(rtype, str):
		print("Error: Recipe type must be a string.")
		valid = 0
	try:
		if len(rtype) == 0:
			print("Error: Recipe type cannot be empty.")
			valid = 0
	except TypeError:
		pass
	if rtype not in ('starter', 'lunch', 'dessert'):
		print("Error: Recipe type value must be starter, lunch or dessert.")
		valid = 0
	return valid



class Recipe:
	"""A class to represent a recipe"""

	def __init__(self, name, cooking_lvl, cooking_time, ingredients, description, recipe_type):
		if valid_values(name, cooking_lvl, cooking_time, ingredients, description, recipe_type):
			self.name = name
			self.cooking_lvl = cooking_lvl
			self.cooking_time = cooking_time
			self.ingredients = ingredients
			self.description = description
			self.recipe_type = recipe_type
		else:
			sys.exit()

	def __str__(self):
		"""Return the string to print with the recipe info"""
		txt = ""
		txt += "Recipe : " + self.name + "\n"
		txt += "Cooking Level: " + str(self.cooking_lvl) + "\n"
		txt += "Cooking Time: " + str(self.cooking_time) + "\n"
		txt += "Ingredients: " + ', '.join(self.ingredients) + "\n"
		txt += "Description: " + self.description + "\n"
		txt += "Recipe Type: " + self.recipe_type
		return txt