from recipe import Recipe
from book import Book

if __name__ == '__main__':
    listy = ['Eggs', 'Milk', 'Flour']
    cake = Recipe("Cake", 3, 20, listy, "", "lunch")
    
    listy = ['Ham', 'Bread', 'Tomatoes']
    bocadillo = Recipe("Bocadillo", 3, 10, listy, "Un bocadillo bien rico", "")
    
    first_book = Book("First book")
    
    first_book.add_recipe(cake)
    first_book.add_recipe(bocadillo)
    
    Book.get_recipes_by_types(first_book, 'lunch')
    first_book.get_recipe_by_name('cake')
    print("")
    print(bocadillo)
    print(cake)