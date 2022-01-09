import json
from MongodbIO import HandleDBActions
from datetime import datetime
from dateutil import rrule


class InvestmenUtils:
    def __init__(self, inputType) -> None:
        self.inputType = inputType

    def extractFromJson(self, jsonFile):
        with open(jsonFile) as inputFile:
                jsonData = json.load(inputFile)
        return jsonData

    def calculateInvestments(self):
        handleDbAction = HandleDBActions(self.inputType)
        doc = handleDbAction.getInvestment()
        contributions = doc["contribution"]
        lump_sum = doc["lump_sum"]

        totalMonthlyContibution = self.calculateMonthlyContribution(contributions)
        totalInvestment = totalMonthlyContibution + lump_sum

        return totalInvestment
    
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
                totalMonthlyContribution = totalMonthlyContribution + (contribution["amount"] * ((weeks.count() / 2) + 1))
        return totalMonthlyContribution