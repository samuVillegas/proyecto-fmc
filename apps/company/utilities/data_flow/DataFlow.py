from apps.company.utilities.data_flow.Question import Question, Flow
#from Question import Question, Flow

def readFile(txt):
    f = open(txt,"r",encoding='utf-8')
    n = int(f.readline())
    f.readline()
    fullFlow = []
    while n > 0:
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
    return flow


def getQuestions(list, key):
    fullFlow = readFile('apps/company/utilities/data_flow/Flow.txt')
    flow = []
    references = []
    cont = 0
    for q in fullFlow:
        if key in q.lock:
            if cont == len(list) and isinstance(q,Question):
                return {'question':q.question,'options':q.options,'image':q.image,'exist_flow':False}
            if isinstance(q,Flow):
                flow.append(q.law)
            else:
                flow.append(q.select(int(list[cont])-1))
                cont += 1
            references.append(q.reference)
    return {'exist_flow':True,'flow':flow, 'references':references}

#Testing
def FindGroup(key):
    #fullFlow = readFile('apps\\company\\utilities\\data_flow\\Flow.txt')
    fullFlow = readFile('apps/company/utilities/data_flow/Flow.txt')
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

#FindGroup('C2')