from pymongo import MongoClient

NumberTypes = (int, float, complex)

class HandleDBActions:
    def __init__(self, inputType) -> None:
        self.mongoClient = MongoClient(port=27017)
        self.db = self.mongoClient.investments
        self.investmentCollection = self.db.get_collection('rrsp') if inputType == 'RRSP' else self.db.get_collection('tfsa')
        self.investmentRecord = self.investmentCollection.find_one()

    def updateRecord(self, data, indx):
        result = None
        if self.investmentRecord is None:
            data['_id'] = 1
            i = 1
            for contrib in data['contributions']:
                contrib['indx'] = i
                i += 1
            result = self.investmentCollection.insert_one(data)
            if result.acknowledged:
                print(f"A new record inserted successfully!")
            else:
                print("Error inserting the record")
        else:
            for key in data.keys():
               if data[key]:
                   if isinstance(data[key], NumberTypes):
                       result = self.investmentCollection.update_one({"_id": 1}, {"$set": {key: data[key]}})
                   else:
                    for contrib in data[key]:
                        for k in contrib.keys():
                            if contrib[k]:
                                result = self.investmentCollection.update_one({"_id": 1, "contributions.indx": indx}, \
                                    {'$set': {f'contributions.$.{k}': contrib[k]}})
            if result.acknowledged:
                print(f"Record updated successfully!\nModified count: {result.modified_count}")
        return result

    def getRecords(self):
        return self.investmentRecord if self.investmentRecord else None