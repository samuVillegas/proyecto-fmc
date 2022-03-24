from apps.company.utilities.choose_type.Question import Question
#from Question import Question

def readFile(txt):
    f = open(txt,"r",encoding='utf-8')
    n = int(f.readline())
    questions = []
    while n > 0:
        lock = f.readline().strip()
        question = f.readline().strip()
        image = f.readline().strip()
        quest = Question(lock, question, image)
        option = f.readline().strip()
        while option != '':
            output = f.readline().strip()
            quest.addOption(option, output)
            option = f.readline().strip()
        questions.append(quest)
        n -= 1
    
    return questions


def getQuestions(list):
    questions = readFile('apps/company/utilities/choose_type/Group.txt')
    key = ''
    cont = 0
    for q in questions:
        if key in q.lock:
            if cont == len(list):
                return {'question':q.question,'options':q.options, 'image':q.image,'exist_key':False}
            else:
                selected = q.select(int(list[cont]) - 1)
                cont+=1
                if selected != q.lock:
                    key = selected
    return {'exist_key':True,'key':key}


#Testing
def FindGroup():
    #questions = readFile('apps\\company\\utilities\\choose_type\\Group.txt')
    questions = readFile('Group.txt')
    key = ''
    for q in questions:
        if key in q.lock:
            #Imprimir pregunta
            print(q.question)
            #Imprimir opciones
            for o in q.options:
                print(o)

            # Obtener respuesta
            selected = q.select(int(input()) - 1)

            #Validación de key
            if selected != q.lock:
                key = selected
            print()
    print('Pertenece al grupo ' + key)

#FindGroup()