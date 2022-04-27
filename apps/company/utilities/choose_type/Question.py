class Question:
    lock = ''
    question = ''
    image = ''
    options = []
    outputs = []

    def __init__(self, lock, question, image):
        self.lock = lock
        self.question = question
        self.image = image
        self.options = []
        self.outputs = []

    def addOption(self, option, output):
        self.options.append(option)
        self.outputs.append(output)

    def select(self, number):
        return self.outputs[number]
    
    
    
