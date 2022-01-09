from pymongo import MongoClient, collection

NumberTypes = (int, float, complex)

class HandleDBActions:
    def __init__(self, inputType) -> None:
        self.mongoClient = MongoClient(port=27017)
        self.db = self.mongoClient.investments
        self.investmentCollection = self.db.get_collection('rrsp') if inputType == 'RRSP' else self.db.get_collection('tfsa')
        self.first_transaction = self.investmentCollection.find_one()

    def updateRecord(self, data):
        if self.first_transaction is None:
            result = self.investmentCollection.insert_one(data)
        else:
            for key in data.keys():
                if (isinstance(data[key], str) and not "".__eq__(data[key])) or (isinstance(data[key], NumberTypes) and data[key] != 0.0):
                    result = self.investmentCollection.update_one({"first_transaction": self.first_transaction["first_transaction"]}, \
                        {"$set": {key: data[key]}})
                elif isinstance(data[key], list):
                    for doc in data[key]:
                        if self.investmentCollection.find_one({"contribution.start" : doc["start"]}):
                            result = self.investmentCollection.update_one({"contribution.start": doc["start"]}, \
                                {"$set": {"contribution.$": doc}})
                        elif self.investmentCollection.find_one({"contribution.end" : doc["end"]}):
                            result = self.investmentCollection.update_one({"contribution.end": doc["end"]}, \
                                {"$set": {"contribution.$": doc}})
                        elif self.investmentCollection.find_one({"contribution.amount" : doc["amount"]}):
                            result = self.investmentCollection.update_one({"contribution.amount": doc["amount"]}, \
                                {"$set": {"contribution.$": doc}})
                        else:
                            result = self.investmentCollection.update_one({"first_transaction": self.first_transaction["first_transaction"]}, \
                                {"$push": {"contribution": doc}})
        return result

    def getInvestment(self):
        investmentDoc = self.investmentCollection.find_one()
        return investmentDoc