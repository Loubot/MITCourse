balance = float(raw_input("What is the outstanding balance? "))
annInterest = float(raw_input("What is the interest rate? "))
minMonth = float(raw_input("What is the minimum monthly payment rate? "))
totalPaid =0.0
for i in range (0, 12, 1):
    monthInterest = annInterest / 12
    monthPayment = round(balance * minMonth, 2)
    print 'month ' , monthPayment
    interestPaid = round(balance * monthInterest, 2)
    princPaid = monthPayment - interestPaid

    print princPaid , ' princ'
    balance -= princPaid
    totalPaid += princPaid + interestPaid
    print 'balance ', balance
    
print 'total ',totalPaid
