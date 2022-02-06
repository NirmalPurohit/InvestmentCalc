import json
from datetime import datetime
from dateutil import rrule
from tabulate import tabulate

from MongodbIO import HandleDBActions


class InvestmenUtils:
    def __init__(self, inputType) -> None:
        self.inputType = inputType

    def extractFromJson(self, jsonFile, inputType):
        with open(jsonFile) as inputFile:
                jsonData = json.load(inputFile)
        return jsonData[inputType]

    def calculateInvestments(self):
        handleDbAction = HandleDBActions(self.inputType)
        doc = handleDbAction.getRecords()
        if doc:
            contributions = doc["contributions"]
            lump_sum = doc["lump sum"]

            totalMonthlyContibution = self.calculateMonthlyContribution(contributions)
            totalInvestment = totalMonthlyContibution + lump_sum

            return totalInvestment
        print("No record found")
        return 0
    
    def calculateMonthlyContribution(self, contributions):
        totalMonthlyContribution = 0
        for contribution in contributions:
            date1 = datetime.strptime(contribution["start"], '%m/%d/%Y').date()
            date2 = datetime.strptime(contribution["end"], '%m/%d/%Y').date()
            if self.inputType == "TFSA":
                months = rrule.rrule(rrule.MONTHLY, dtstart=date1, until=date2)
                totalMonthlyContribution = totalMonthlyContribution + (contribution["amount"] * months.count())
            else:
                weeks = rrule.rrule(rrule.WEEKLY, dtstart=date1, until=date2)
                biWeeklyContirb = (contribution["hourly pay"] * 37.5 * 2) * (contribution["rate"] / 100)
                totalMonthlyContribution += biWeeklyContirb * ((weeks.count() / 2) + 1)
        return totalMonthlyContribution

    def printInvestment(self, investment, inputType):
        print(f"Current limit: {investment['limit']}")
        print(f"Lump sum: {investment['lump sum']}")
        investmentTableHeader = [x for x in investment['contributions'][0].keys()]
        tableData = list()
        for contribution in investment['contributions']:
            rw = list()
            for k in contribution.keys():
                rw.append(contribution[k])
            tableData.append(rw)
        return tabulate(tableData, investmentTableHeader)

