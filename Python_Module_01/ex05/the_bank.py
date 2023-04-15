class Account(object):
    ID_COUNT = 1

    def __init__(self, name, **kwargs):
        self.__dict__.update(kwargs)

        self.id = self.ID_COUNT
        Account.ID_COUNT += 1
        self.name = name
        if not hasattr(self, 'value'):
            self.value = 0
        
        if self.value < 0:
            raise AttributeError("Attribute value cannot be negative")
        if not isinstance(self.name, str):
            raise AttributeError("Attribute name must be a string")

    def transfer(self, amount):
        self.value += amount

class Bank(object):
    """The bank"""
    def __init__(self):
        self.accounts = []

    def add(self, new_account):
        """ Add new_account in the Bank
            @new_account: Account() new account to append
            @return True if success, False if an error occurred
        """
        if isinstance(new_account, Account) and new_account not in self.accounts:
            self.accounts.append(new_account)
    
    def corrupted(self, account):
        """ Checks if the account is corrupted """
        if len(account.__dict__) % 2 == 0:
            return 1
        if 'name' not in account.__dict__.keys():
            return 1
        if 'id' not in account.__dict__.keys():
            return 1
        if 'value' not in account.__dict__.keys():
            return 1
        zip_check = 0
        addr_check = 0
        for key in account.__dict__.keys():
            if str(key).startswith('zip'):
                zip_check = 1
            if str(key).startswith('addr'):
                addr_check = 1
            if str(key).startswith('b'):
                return 1
        if zip_check == 0 and addr_check == 0:
            return 1
        return 0
    
    def transfer(self, origin, dest, amount):
        """ perform the fund transfer
            @origin:    str(name) of the first account
            @dest:      str(name) of the destination account
            @amount:    float(amount) amount to transfer
            @return     True if success, False if an error occured
        """
        origin_elem = 0
        dest_elem = 0
        for elem in self.accounts:
            if origin == elem.id or origin == elem.name:
                origin_elem = elem
            if dest == elem.id or dest == elem.name:
                dest_elem = elem
        if origin_elem == 0 or dest_elem == 0:
            print("Error, couldn't find account")
            return False
        if self.corrupted(origin_elem) or self.corrupted(dest_elem):
            print("Error, account corrupted")
            return False
        if amount <= 0 or origin_elem.value < amount:
            print("Error, amount is not valid")
            return False
        origin_elem.transfer(-amount)
        dest_elem.transfer(amount)
        print("Transfer succesfull.")
        return True

    def fix_account(self, name):
        """ A function to fix an account """
        corrupted = 0
        zip_check = 0
        addr_check = 0
        for elem in self.accounts:
            if name in elem.__dict__.values():
                corrupted = elem
        if corrupted == 0:
            print("Couldn't find corrupted account")
            return False
        keys = list(corrupted.__dict__.keys())
        if 'name' not in keys:
            corrupted.__dict__['name'] = 'Restored account'
        if 'value' not in keys:
            corrupted.__dict__['value'] = 0
        if 'id' not in keys:
            corrupted.__dict__['id'] = Account.ID_COUNT
            Account.ID_COUNT += 1
        for key in keys:
            if key.startswith('zip'):
                zip_check = 1
            if key.startswith('addr'):
                addr_check = 1
            if key.startswith('b'):
                corrupted.__dict__.pop(key)
        if zip_check == 0:
            corrupted.__dict__['zip'] = '00000'
        if addr_check == 0:
            corrupted.__dict__['addr'] = '42 rue des Corruptions'
        if len(corrupted.__dict__) % 2 == 0:
            for key in corrupted.__dict__.keys():
                if key == 'name' or key == 'id' or key == 'value':
                    pass
                elif key.startswith('zip') or key.startswith('addr'):
                    pass
                else:
                    corrupted.__dict__.pop(key)
                    break
        if self.corrupted(corrupted):
            print("Couldn't fix account")
            return False
        else:
            print("Succesfully fixed account!")
            return True


