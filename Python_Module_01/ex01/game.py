class GotCharacter:
    def __init__(self, first_name, is_alive=True):
        self.first_name = first_name
        self.is_alive = is_alive

class Student(GotCharacter):
    """A \033[32mclass\033[0m representing the 42 family. Or when up to you things happen to good people"""
    def __init__(self, first_name=None, is_alive=True):
        super().__init__(first_name=first_name, is_alive=is_alive)
        self.family_name = "Student"
        self.house_words = "Up to you!"
    
    def print_house_words(self):
        print(self.house_words)
    
    def die(self):
        self.is_alive = False

class Stark(GotCharacter):
    """A \033[32mclass\033[0m representing the Stark family. Or when bad things happen to good people"""
    def __init__(self, first_name=None, is_alive=True):
        super().__init__(first_name=first_name, is_alive=is_alive)
        self.family_name = "Stark"
        self.house_words = "Winter is Coming"

    def print_house_words(self):
        print(self.house_words)
    
    def die(self):
        self.is_alive = False

if __name__=='__main__':
    arya = Stark("Arya")
    print("Alive: ", arya.is_alive)
    arya.die()
    print("Alive: ", arya.is_alive)