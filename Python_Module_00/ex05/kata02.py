import datetime
kata = (2019, 9, 25, 3, 30)
kata_date = datetime.datetime(*kata)
kata_date = kata_date.strftime("%m/%d/%Y %H:%M")
print(kata_date)