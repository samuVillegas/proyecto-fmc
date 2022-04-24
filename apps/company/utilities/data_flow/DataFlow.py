from apps.company.utilities.data_flow.Question import Question, Flow
#from Question import Question, Flow
import os
import logging
dir = os.path.dirname(os.path.realpath(__file__))

def readFile(txt):
    f = open(txt,"r",encoding='utf-8')
    n = int(f.readline())
    
    fullFlow = []
    while n >= 0:
        type = f.readline().strip()
        if type == 'Pregunta':
            fullFlow.append(typeGroup(f))
        elif type == 'Flujo':
            fullFlow.append(typeFlow(f))
        n -= 1
    
    return fullFlow

def typeGroup(f):
    lock = f.readline().strip()
    reference = f.readline().strip()
    question = f.readline().strip()
    image = f.readline().strip()
    quest = Question(lock, question, reference, image)
    option = f.readline().strip()
    while option != '':
        output = f.readline().strip()
        quest.addOption(option, output)
        option = f.readline().strip()
    return quest

def typeFlow(f):
    lock = f.readline().strip()
    reference = f.readline().strip()
    law = f.readline().strip()
    flow = Flow(lock, reference, law)
    f.readline()
    return flow


def getQuestions(list, law, key):
    fullFlow = readFile(dir + '/Flow' + law + '.txt')
    flow = []
    references = []
    cont = 0
    for q in fullFlow:
        if key in q.lock:
            if cont == len(list) and isinstance(q,Question):
                if len(flow) == 0:
                    flow = ['Ya se cumple la ley ' + law]
                return {'question':q.question,'options':q.options,'image':q.image,'exist_flow':False}
            if isinstance(q,Flow):
                if len(q.law) > 0:
                    flow.append(q.law)
            else:
                selected = q.select(int(list[cont])-1)
                if len(selected) > 0:
                    flow.append(selected)
                cont += 1
            references.append(q.reference)
    if len(flow) == 0:
        flow = ['Ya se cumple la ley ' + law]
    return {'exist_flow':True,'flow':flow, 'references':references}


def getQuestions2(law):
    return readFile(dir + '/Flow' + law + '.txt')

def writeFile(law, dic):
    n = int(dic['size']) - 2
    string = str(n) + '\n\n'

    count = 1
    while count < n + 1:
        type = dic['type' + str(count)]
        string += type + '\n'
        if type == 'Pregunta':
            string += dic['lock' + str(count)] + '\n'
            string += dic['reference' + str(count)] + '\n'
            string += dic['question' + str(count)] + '\n'
            string += dic['image' + str(count)] + '\n'
            count2 = 1
            while 'option' + str(count) + '_' + str(count2) in dic:
                string += dic['option' + str(count) + '_' + str(count2)] + '\n'
                string += dic['output' + str(count) + '_' + str(count2)] + '\n'
                count2 += 1
        elif type == 'Flujo':
            string += dic['lock' + str(count)] + '\n'
            string += dic['reference' + str(count)] + '\n'
            string += dic['law' + str(count)] + '\n'
        count += 1
        string += '\n'
    logging.warning(string)
    f = open(dir + '/Flow' + law + '.txt',"w",encoding='utf-8')
    f.write(string)
    f.close()

#Testing
def FindGroup(law, key):
    fullFlow = readFile(dir + '/Flow' + law + '.txt')
    flow = ''
    for q in fullFlow:
        if key in q.lock:
            if hasattr(q, 'law'):
                flow += q.law + '\n'
            else:
                #Imprimir pregunta
                print(q.question)
                #Imprimir opciones
                for o in q.options:
                    print(o)

                # Obtener respuesta
                selected = q.select(int(input()) - 1)
                flow += selected + '\n'

    print('\n' + flow)

#FindGroup('NSR10','R2') 
#print(getQuestions([2],'NSR10','A1'))
