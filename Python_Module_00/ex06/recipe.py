cookbook = {
	"sandwich":
	{
		"ingredients":["ham", "bread", "cheese", "tomatoes"],
		"meal": "lunch",
		"prep_time": 10
	},
	"cake":
	{
		"ingredients":["flour", "sugar", "eggs"],
		"meal": "dessert",
		"prep_time": 60
	},
	"salad":
	{
		"ingredients":["avocado", "arugula", "tomatoes", "spinach"],
		"meal": "lunch",
		"prep_time": 15
	}
}

def print_recipes():
	for item in cookbook:
		print(item)

def print_details(name):
		if name in cookbook:
			recipe = cookbook[name]
			print("Recipe for", name + ':')
			print("\tIngredients list:", recipe['ingredients'])
			print("\tTo be eaten for", recipe['meal'] + '.')
			print("\tTakes", recipe['prep_time'], "minutes of cooking.")

def delete_recipe(name):
	if name in cookbook:
		del cookbook[name]
		print("Recipe deleted.")

def add_recipe():
	print("Enter a name:")
	name = input()
	if name in cookbook:
		print("Recipe already exists.")
	else:
		print("Enter ingredients:")
		ingredients = []
		while True:
			item = input()
			if item != '':
				ingredients.append(item)
			else:
				break
		meal = input("Enter a meal type:")
		prep_time = input("Enter a preparation time:")
		recipe = {"ingredients": ingredients, "meal": meal, "prep_time":prep_time}
		cookbook[name] = recipe

def print_options():
	print("List of available option:")
	print("\t1: Add a recipe")
	print("\t2: Delete a recipe")
	print("\t3: Print a recipe")
	print("\t4: Print the cookbook")
	print("\t5: Quit\n")

print("Welcome to the Python Cookbook !")
print_options()

while True:
	print("Please select an option:")
	option = input()
	if option == '1':
		print('\n')
		add_recipe()
		print('\n')
	elif option == '2':
		print('\n')
		delete_recipe(input("Enter a name: "))
		print('\n')
	elif option == '3':
		print('\n')
		print_details(input("Please enter a recipe name to get its details:\n "))
		print('\n')
	elif option == '4':
		for item in cookbook:
			print('\n')
			print_details(item)
			print('\n')
	elif option == '5':
		print("Cookbook closed. Goodbye !")
		break
	else:
		print("Sorry, this option does not exist.")
		print_options()
