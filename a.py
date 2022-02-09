#esame 04/02/2022

class ExamException(Exception):
    pass


class CSVTimeSeriesFile():

    def __init__(self, name):
        
        self.can_read = True

        if isinstance(name, str)==True:
            self.name = name
        else:
            self.can_read = False
        
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except:
            self.can_read = False
            

    def get_data(self):
        
        if self.can_read == False:
            raise ExamException ('file cannot be open')

        else:
            data = []
            my_file = open(self.name, 'r')

            prev_anno = None
            prev_mese = None

            for line in my_file:
                row = line.split(',')
                row[-1] = row[-1].strip()

                i=0
                data_num = []
                anno_mese = []
                check_riga = True

                try:
                    int(row[1])
                except:
                    check_riga = False

                for element in row:
                
                #primo elemento, controllo data
                #------------------------------
                    if i==0 and check_riga == True:
                        i = i + 1
                        anno_mese = element.split('-')
                        
                        try:
                            anno = int(anno_mese[0])
                            mese = int(anno_mese[1])
                        except:
                            check_riga = False
                            continue

                        #il mese è un numero non compreso tra 1 e 12
                        if mese<1 or mese>12:
                            continue
                        #controllo se nella data ci sono altri valori dopo anno e mese, in tal caso i dati aggiuntivi vengono rimossi
                        if len(anno_mese)>2:
                            continue
                            #element=str(anno_mese[0]) + '-' + str(anno_mese[1])
                            #raise ExamException('the date needs to be write in this way: year-month')

                        #prima data
                        if prev_anno == None:
                            prev_anno = anno
                            prev_mese = mese
                            data_num.append(element)
                        #poi controllo consecutività
                        else:
                            #se nello stesso anno
                            if prev_anno==anno:
                                #data non conscutiva
                                
                                if prev_mese >= mese:
                                    raise ExamException('non-conscutive date: {}'.format(row))
                                #mese successivo
                                elif mese == 1+prev_mese:
                                    prev_mese = mese
                                    data_num.append(element)
                                #mesi mancanti
                                else:
                                    for j in range(mese - prev_mese -1):
                                        to_add = []
                                        if prev_mese+1+j < 10:
                                            to_add.append(str(prev_anno) + '-0' + str(prev_mese+1+j))
                                        else:
                                            to_add.append(str(prev_anno) + '-' + str(prev_mese+1+j))
                                        to_add.append(None)
                                        data.append(to_add)
                                    data_num.append(element)
                                    prev_mese = mese
                            
                            #anno nuovo
                            elif prev_anno < anno:
                                if prev_mese == 12 and prev_anno+1==anno and mese ==1:
                                    data_num.append(element)
                                    prev_anno = anno
                                    prev_mese = mese
                                
                                else:
                                    if anno-prev_anno-1!=0:
                                        raise ExamException ('un anno non ha valori')
                                    
                                    #pongo None fino all'elemento di questo anno
                                    for j in range((12*(anno-prev_anno-1))+(12 - prev_mese) + (mese -1)):
                                        to_add = []
                                        prev_mese = prev_mese + 1

                                        if prev_mese == 13:
                                            prev_mese = 1
                                            prev_anno = prev_anno + 1
                                        
                                        if prev_mese <10 :
                                            to_add.append(str(prev_anno) + '-0' + str(prev_mese))
                                        else:
                                            to_add.append(str(prev_anno) + '-' + str(prev_mese))
                                            
                                        to_add.append(None)
                                        data.append(to_add)
                                    data_num.append(element)
                                    prev_mese = mese
                                    prev_anno = anno

                            #anno precedente > anno
                            else:
                                raise ExamException('non-conscutive date: {}'.format(row))
                            
                            #prev_anno = anno
                            #prev_mese = mese
                            
                        
                        
                #il secondo elemento int, sennò None
                #-----------------------
                    elif i==1 and check_riga == True:
                        i = i + 1
                        try:
                            number = int(element)
                            if number >= 0:
                                data_num.append(number)
                            else:
                                data_num.append(None)

                        except:
                            data_num.append(None)
                
                if check_riga == True:
                    data.append(data_num)

            my_file.close()

            return data



#________________________________________________________________________________
#________________________________________________________________________________
#________________________________________________________________________________



def compute_avg_monthly_difference(time_series, first_year, last_year):
    #first_year, last_year str
    #if list_check(time_series) == False:
    #    raise ExamException('the list of "compute_avg_monthly_difference" function should be the list returned by "get_data"')

    if isinstance(first_year, str)==False or isinstance(first_year, str)==False:
        raise ExamException('first_year and last_year are not string')
    try:
        a = int(first_year)
        b = int(last_year)
    except:
        raise ExamException('first_year and last_year are not convertible to int')
    if a >= b:
        raise ExamException('first_year >= last_year')

    is_inside_f = False
    is_inside_l = False

    numerical_data = []

    #first_year, last_year presenti nel file
    for line in time_series:
        data = line[0].split('-')

        #creo un array numerico
        arr = []
        arr.append(int(data[0]))
        arr.append(int(data[1]))
        arr.append(line[1])

        numerical_data.append(arr)

        if data[0] == first_year:
            is_inside_f = True
        
        if data[0] == last_year:
            is_inside_l = True


    if is_inside_f == False or is_inside_l == False:
        raise ExamException('Incorrect ragne of year')
    else:
        list_val_per_year = []
        list_val = []
        
        # list_val_per_year è una lista di liste. Ogni lista inerna rappresenta un anno del file CSV
        #sono presenti controlli per assegnare None in testa e in coda se il file CSV non inizia a gennaio o se non termina a dicembre
        i = False
        last_element = numerical_data[-1]

        for line in numerical_data:
            if i is False:
                first_in_history = line[0]
                if line[1] != 1:
                    for i in range(line[1]-1):
                        list_val.append(None)
                
                list_val.append(line[2])
                i = True
            
            else:
                if line == last_element:
                    #last_in_history = line[0]
                    if len(list_val) != 11:
                        list_val.append(line[2]) 
                        n = 12 - len(list_val)
                        for i in range(n):
                            list_val.append(None)
                        list_val_per_year.append(list_val)
                    else:
                        list_val.append(line[2])
                        list_val_per_year.append(list_val)
                
                elif line[1] != 12:
                    list_val.append(line[2])

                else:
                    list_val.append(line[2])
                    list_val_per_year.append(list_val)

                    list_val = []

        #print('list_val_per_year: ')
        #print(list_val_per_year)

        
        #inizio calcolo
        result = []
        i = 0
        n = b - a
        l = a - first_in_history

        summ = 0

        #per il None
        counter = 0

        #print(list_val_per_year)

        for i in range(12):
        #n (+1 perché voglio un elemento in più, ma -1 perché ho j+1)
            div = n
            for j in range(n):
                if list_val_per_year[l+j][i] == None:
                    div = div - 1

                elif list_val_per_year[l+j+1][i] == None:
                    div = div - 1
                    list_val_per_year[l+j+1][i] = list_val_per_year[l+j][i]
                
                else:
                    summ = summ + list_val_per_year[l+j+1][i] - list_val_per_year[l+j][i]
                    counter = counter + 1
            
            if counter < 1: 
                media = 0
            else:
                media = summ/div
                
            result.append(media)
            summ = 0

        

        return result


    

def list_check (lista):
    value = True
    if isinstance(lista, list) == False:
        value = False

    prev_anno = None
    prev_mese = None
    for line in lista:
        row = []
        try:
            row.append(line[0])
            row.append(line[1])
        except:
            value = False

        if isinstance(row[1], int) == False and isinstance(row[1], None) == False:
            value = False
        anno_mese = row[0].split('-')
        try:
            anno = int(anno_mese[0])
            mese = int(anno_mese[1])
        except:
            value = False

        if prev_mese != None:
            if prev_anno == anno:
                if prev_mese+1 != mese:
                    value = False
            elif prev_anno+1 == anno and prev_mese ==12:
                if mese !=1:
                    value = False
            else:
                value = False          
        prev_anno = anno
        prev_mese = mese
    return value






#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


mio_file = CSVTimeSeriesFile(name='data.csv')
print('Nome del file: "{}"'.format(mio_file.name))
#print(mio_file.get_data())
time_series = mio_file.get_data()

for line in time_series:
    print (line)

first_year = '1950'
last_year = '1953'
print(compute_avg_monthly_difference(time_series, first_year, last_year))