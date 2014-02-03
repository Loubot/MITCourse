balance = float(raw_input("Enter the outstanding balance: "))
interest = float(raw_input("Enter the annual interest rate: "))

monthCounter = 1
intPaid = 0.0
monthInterest = interest / 12
calcBalance = balance
monthPayment = 10
while calcBalance >0:
    if monthCounter >= 12:
        calcBalance = balance
        monthPayment += 10
        monthCounter = 0
    
    intPaid = calcBalance * monthInterest
    calcBalance -= monthPayment
    calcBalance += intPaid
    monthCounter +=1

print 'Number of months needed: ', monthCounter
print 'Monthly payment to pay off debt in 1 year: ' , monthPayment
print 'Balance: ', round(calcBalance, 2)
