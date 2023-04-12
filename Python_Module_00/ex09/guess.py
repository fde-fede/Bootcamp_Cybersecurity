import random

print("This is an interactive guessing game!")
print("You have to enter a number between 1 and 99 to find out the secret number.")
print("Type 'exit' to end the game.")
print("Good luck!")
secret_number = random.randint(1, 99)
count = 1

while True:
	print("What's your guess between 1 and 99?")
	number = input()
	try:
		number = int(number)
	except ValueError:
		if number == "exit":
			print("Goodbye!")
			exit()
		else:
			print("That's not a number")
			count += 1
			continue
	if number:
		if number == secret_number:
			if number == 42:
				print("The answer to the ultimate question of life, the universe and everything is 42")
			if count == 1:
				print("Congratulations! You got it on your first try!")
				exit()
			print("Congratulations, you've got it!")
			print("You won in", count, "attempts!")
			exit()
		elif number < secret_number:
			print("Too low!")
			count += 1
		elif number > secret_number:
			print("Too high!")
			count += 1
