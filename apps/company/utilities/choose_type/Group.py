from apps.company.utilities.data_flow.Question import Question
#from Question import Question
import os
dir = os.path.dirname(os.path.realpath(__file__))

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


def getQuestions(list, law):
    questions = readFile(dir + '/Group' + law + '.txt')
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

def getQuestionsGroup(law):
    return readFile(dir + '/Group' + law + '.txt')

def writeFileGroup(law, dic):
    n = int(dic['size'])
    string = str(n) + '\n'

    count = 1
    while count < n + 1:
        string += dic['lock' + str(count)] + '\n'
        string += dic['question' + str(count)] + '\n'
        string += dic['image' + str(count)] + '\n'
        count2 = 1
        while 'option' + str(count) + '_' + str(count2) in dic:
            string += dic['option' + str(count) + '_' + str(count2)] + '\n'
            string += dic['output' + str(count) + '_' + str(count2)] + '\n'
            count2 += 1
        count += 1
        string += '\n'
    
    f = open(dir + '/Group' + law + '.txt',"w",encoding='utf-8')
    f.write(string)
    f.close()

#Testing
def FindGroup(law):
    questions = readFile(dir + '/Group' + law + '.txt')
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

#FindGroup('NFPA101')