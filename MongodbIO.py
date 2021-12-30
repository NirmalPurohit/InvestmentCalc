from pymongo import MongoClient, collection

class HandleDBActions:
    def __init__(self) -> None:
        self.mongoClient = MongoClient(port=27017)
        self.db = self.mongoClient.investments

    def updateRecord(self, inputType, data):
        investmentCollection = self.db.get_collection('rrsp') if inputType == 'RRSP' else self.db.get_collection('tfsa')
        for transaction in data.contribution:
            record = investmentCollection.update_one({'contribution.start': transaction['start']})
        result = investmentCollection.insert_one()
        
        return result