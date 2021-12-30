import argparse
import sys
import json
from DocumentHolder import DocumentHolder

def extractFromJson(jsonFile):
    with open(jsonFile) as inputFile:
            jsonData = json.load(inputFile)
            inputData = DocumentHolder(**jsonData)

    return inputData


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

    if args.update:
        if not args.update.lower().endswith('.json'):
            print("Incorrect file type!\nonly JSON file is supported")
            sys.exit(1)
        
        inputData = extractFromJson(args.update)
    
    inputType = 'RRSP' if args.rrsp else 'TFSA'
