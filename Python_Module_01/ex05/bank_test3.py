from the_bank import Account, Bank

bank = Bank()
bank.add(Account(
    'Jane',
    zip='911-745',
    value=1000.0,
    ref='1044618427ff2782f0bbece0abd05f31'
))

jhon = Account(
    'Jhon',
    zip='911-745',
    value=1000.0,
    ref='1044618427ff2782f0bbece0abd05f31'
)

bank.add(jhon)

print("testing a valid transfer")
print(jhon.value)
bank.transfer("Jane", "Jhon", 500)
print(jhon.value)