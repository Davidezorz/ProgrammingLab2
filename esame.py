

#http://autograding.xyz/

class ExamException(Exception):
    pass

class Diff:

    def __init__ (self, ratio=1):

        #ratio deve essere un numero (int o float) maggiore di zero
        if isinstance(ratio, int)==False and isinstance(ratio, float)==False:
            raise ExamException('ratio not int or float')
        elif ratio==0:
            raise ExamException('impossibile dividere per 0')
        elif ratio<0:
            raise ExamException('ratio negativo non valido')
        else:
            self.ratio = ratio

    def compute (self, lista):

        #la lista deve essere una lista
        if isinstance(lista, list)==False:
            raise ExamException('compute ha in ingresso una lista')
        
        else:
            diff = []
            prev_data = None

            for item in lista:

                #ogni elemento della lista deve essere int o float
                #io il controllo l'ho messo qui, ma sarebbe meglio farlo sopra con un ciclo for dedicato
                if isinstance(item, int)==False and isinstance(item, float)==False:
                    raise ExamException('un elemento della lista nn è int o float')

                #la lunghezza della lista deve essere di almeno due elementi
                elif len(lista)<2:
                    raise ExamException("la lunghezza della lista dev'essere almeno pari a 2")
                   
                else:
                    if prev_data == None:
                        prev_data = item

                    else:
                        a = item - prev_data
                        diff.append(a/self.ratio)
                        prev_data = item
                
            return diff



r = 2
l = [2,4,8,16]
a = Diff(r)

print(a.compute(l))
