import argparse

def parseArgVal(args):
    if ( args.rrsp or args.tfsa) and not (args.view or args.update):
        print("You need to choose an action to perform")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--rrsp', help="Perform actions on RRSP investments", action="store_true")
    parser.add_argument('-t', '--tfsa', help="Perform actions on TFSA investments", action="store_true")
    parser.add_argument('-v', '--view', help="View the investment calculations and records for the choosen type", action="store_true")
    parser.add_argument('-u', '--update', help="Update the record for the chosen type")

    args = parser.parse_args()

    parseArgVal(args)
