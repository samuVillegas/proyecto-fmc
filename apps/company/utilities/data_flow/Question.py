class Question:
    lock = ''
    question = ''
    reference = ''
    image = ''
    options = []
    outputs = []

    def __init__(self, lock, question, reference, image):
        self.lock = lock
        self.question = question
        self.reference = reference
        self.image = image
        self.options = []
        self.outputs = []

    def addOption(self, option, output):
        self.options.append(option)
        self.outputs.append(output)

    def select(self, number):
        return self.outputs[number]
    
class Flow:
    lock = ''
    reference = ''
    law = ''

    def __init__(self, lock, reference, law):
        self.lock = lock
        self.reference = reference
        self.law = law  
    