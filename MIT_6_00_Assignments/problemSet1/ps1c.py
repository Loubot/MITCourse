balance = float(raw_input("Enter the outstanding balance on your credit card: "))
interest = float(raw_input("What is the interest rate? "))

monthInterest = interest / 12
lowerB = balance / 12

upperB = (balance *(1 + monthInterest)**12) /12

print upperB
    
while True:
    calcBalance = balance
    print "upperb ", upperB, " lowerb ", lowerB
    monthPayment = (upperB + lowerB) / 2
    
    for i in range (1, 13, 1):
        interestPaid = round(calcBalance * monthInterest, 2)
        calcBalance += interestPaid - monthPayment
        if calcBalance < 0:
            break

        
    if (upperB - lowerB < .005):
        calcBalance = balance
        
        monthPayment = round(monthPayment, 2)
        print "Monthly payment to pay off debt in 1 year:", monthPayment
        for month in range (1,13):
            interestPaid = round(calcBalance * monthInterest, 2)
            calcBalance += interestPaid - monthPayment
            if balance <=0:
                break
        print "Number of months needed: ", month
        print "Balance: ", round(calcBalance,2)
        break
    elif(calcBalance < 0):
        upperB = monthPayment
    else:
        lowerB = monthPayment
        
