class Question:
    lock = ''
    question = ''
    options = []
    outputs = []

    def __init__(self, lock, question):
        self.lock = lock
        self.question = question
        self.options = []
        self.outputs = []

    def addOption(self, option, output):
        self.options.append(option)
        self.outputs.append(output)

    def select(self, number):
        return self.outputs[number]
    
    
    
