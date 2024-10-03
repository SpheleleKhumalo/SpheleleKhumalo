import math
#Providin a menu the user should select in order to be able to proceed.
print("Investment -  to calculate the amount of interest you'll earn on your investment.")
print("Bond       -  to calculate the amount you'll have to pay on a home loan.")
print("")
#Ask a user to enetr what they have selected from the menu above.
investment_bond = input("Enter either 'Investment' or 'Bond' from the menu above to proceed. ")

# calculations if the user choose investment from the menu. 
if investment_bond.lower() == "investment":
    #Ask for inputs to make investment calculations
    dep_amount = float(input("Please enter the amount you want to deposit. "))
    interest_rate = int(input("Please enter the interest rate. "))
    no_of_years = int(input("Please enter number of years you want to invest. "))
    interest = input("Please enter 'simple' or 'compound' for your interest. ")

    #Do calcuations for simple interest.
    if interest.lower() == "simple":
        simple_interest = dep_amount * (1 + interest_rate * no_of_years)
        print("Your total amount will be R" + str(round(simple_interest, 2)))
    
    #Do calculations for  compound interest
    elif interest.lower() == "compound":
        compound_interest = dep_amount * math.pow((1 + (interest_rate/100)), no_of_years)
        print("Your total amount will be R" + str(round(compound_interest, 2)))
    #invalid inputes
    else:
        print("Invalide interest input please enter 'simple' or 'compound' for your interest. ")

#calcu;atoins if the user chooses bond from the mune
elif investment_bond.lower() == "bond":
    #ask inputs to calculate repayment for bond.
    house_value = float(input("Please enter the value of the house. "))
    rate_interest = int(input("Please enter the interest rate. "))
    no_of_months = int(input("Please enter the number of months you plan to make a repayment. "))

    #calculate repayment
    repayment = (rate_interest * house_value) / (1 - (1 + rate_interest) ** (-no_of_months))
    print("Your repayment will be R" + str(round(repayment, 2)))
#invalid input
else:
    print("Invalide input please enter either 'Investment' or 'Bond' from the menu above to proceed. ")