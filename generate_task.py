import pickle

class S3Task:
    def __init__(self):
        self.payload = "A" * 1000
        self.result = "B" * 1000

    def serialize(self):
        data = {
            "payload": self.payload,
            "result": self.result,
        }

        return pickle.dumps(data)
