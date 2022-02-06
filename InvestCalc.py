import argparse
import sys

from InvestmentUtils import InvestmenUtils
from MongodbIO import HandleDBActions

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--rrsp', help="Perform actions on RRSP investments", action="store_true")
    parser.add_argument('-t', '--tfsa', help="Perform actions on TFSA investments", action="store_true")
    parser.add_argument('-v', '--view', help="View the investment calculations and records for the choosen type", action="store_true")
    parser.add_argument('-u', '--update', type=str, help="Update the record for the chosen type")

    args = parser.parse_args()

    if ( args.rrsp or args.tfsa) and not (args.view or args.update):
        print("Error parsing the argument! \nYou need to choose an action to perform. Check help (-h/--help) for the options")
        sys.exit(1)

    inputType = 'RRSP' if args.rrsp else 'TFSA'
    handleDbAction = HandleDBActions(inputType)
    investmentUtils = InvestmenUtils(inputType)

    if args.update:
        if not args.update.lower().endswith('.json'):
            print("Incorrect file type!\nonly JSON file is supported")
            sys.exit(1)

        inputData = investmentUtils.extractFromJson(args.update, inputType)
        currentRecord = handleDbAction.getRecords()
        if currentRecord:
            print(investmentUtils.printInvestment(currentRecord, inputType))
            indx = int(input("Enter contribution index to modify (If there is no contribution, choosing index other than 0 wil update limits and lump sum too) \n"))
        else:
            indx = 0
        opResult = handleDbAction.updateRecord(inputData, indx)
    elif args.view:
        totalInvested = investmentUtils.calculateInvestments()
        print(f"Your total contribution for {inputType} is {totalInvested}")
        currentBalance = float(input(f"Enter current balance for {inputType} >"))
        diff = currentBalance - totalInvested
        if (diff > 0):
            print("Hurray! You are in profit by $%.2f" % diff)
        else:
            print("Ooops! You are in loss by $%.2f" % abs(diff))
