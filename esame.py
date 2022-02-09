#esame 10-02-2022
#versione 2

class ExamException(Exception):
    pass


def check_list (lista, f):
    #controllo input
    if isinstance(lista, list) == False or isinstance(f, int) == False:
        raise ExamException('Error in input of check_list, lista must be list')
    elif len(lista) < 2:
        raise ExamException('lenght of lista must at least 2 in "check_list"  function')
    else:
        result = []
        anno_prima=None
        mese_prima=None

        for row in lista:
            if f == 0:
                try:
                    row[1]=int(row[1]) 
                    anno_mese=row[0].split('-')
                    anno=int(anno_mese[0])
                    mese=int(anno_mese[1])                 
                except:
                    continue
            elif f == 1:
                if isinstance(row[1], int) == False:
                    raise  ExamException('in "compute_avg_monthly_difference" time_series element must be list returned by get_data()')
                try: 
                    anno_mese=row[0].split('-')
                    anno=int(anno_mese[0])
                    mese=int(anno_mese[1])                 
                except:
                    raise ExamException('in "compute_avg_monthly_difference" time_series element must be list returned by get_data()')
            else:
                raise ExamException('wrong value of f')
            #il mese è un mese, non ci sono altri elementi, come il giorno, nella data
            if len(anno_mese)>2 or mese<1 or mese>12:
                continue
                
            #prim anno
            if anno_prima==None:
                anno_prima=anno
                mese_prima=mese
            else:
                if anno_prima<anno:
                    anno_prima=anno
                    mese_prima=mese
                elif anno_prima==anno:
                    if mese_prima<mese:
                        mese_prima=mese
                    else:
                        raise ExamException('non-conscutive date: {}'.format(row))
                else:
                    raise ExamException('non-conscutive date: {}'.format(row))

            result.append(row)
            
    return result



def fill (lista):
    if isinstance(lista, list) == False:
        raise ExamException('lista must be a list in fill function')
    elif len(lista) < 2:
        raise ExamException('lenght of lista must at least 2 in fill function')
    elif lista != check_list(time_series, 1):
        raise ExamException('in "fill" function lista element must be list returned by get_data()') 
    else:
        b = lista[-1]
        a = b[0].split('-')
        last_y = int(a[0])
        last_m = int(a[1])

        ip_anno = None
        ip_mese = None
        result = []
        month_data = []

        continua = True
        i=0
        k=True

        while continua == True:
            try:
                line = lista[i]
                data = line[0].split('-')
                anno = int(data[0])
                mese = int(data[1])
            except:
                pass
            
            if ip_anno == None:
                ip_anno = anno
                ip_mese = 1
            else:           
                if last_y == ip_anno and ip_mese == 12:
                    if k == True:
                        month_data.append(line[1])
                    else:
                        month_data.append(None)
                    continua = False
                    
                elif last_y == ip_anno and last_m <= ip_mese:
                    if ip_mese == mese and ip_anno == anno:
                        month_data.append(line[1])
                    else:
                        month_data.append(None)
                    k = False          
        
                elif ip_mese == mese and ip_anno == anno:
                    month_data.append(line[1])
                    i = i + 1
                else:
                    month_data.append(None)

                ip_mese = ip_mese + 1
                if ip_mese == 13:
                    ip_mese = 1
                    ip_anno = ip_anno + 1
                
                if len(month_data) == 12:
                    result.append(month_data)
                    month_data = []
    
    return result


#---------------------------------------------------------------------------
# funzioni e neccessarie per l'esame
#---------------------------------------------------------------------------

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
            lista = []
            my_file = open(self.name, 'r')
            for line in my_file:
                row = line.split(',')
                row[-1] = row[-1].strip()
                lista.append(row)

            result = check_list (lista, 0)

        my_file.close()
        return result



def compute_avg_monthly_difference(time_series, first_year, last_year):
    #first_year, last_year str
    if isinstance(first_year, str)==False or isinstance(first_year, str)==False:
        raise ExamException('first_year and last_year are not string')
    else:
        try:
            a = int(first_year)
            b = int(last_year)
        except:
            raise ExamException('first_year and last_year are not convertible to int')
        if a >= b:
            raise ExamException('first_year >= last_year')
    
    #range corretto di anni
    is_inside_f = False
    is_inside_l = False

    #salvo il primo anno del file
    first_in_history = None
    
    for line in time_series:
        data = line[0].split('-')
        if first_in_history == None:
            first_in_history = int(data[0])
        if data[0] == first_year:
            is_inside_f = True
        if data[0] == last_year:
            is_inside_l = True

    if is_inside_f == False or is_inside_l == False:
        raise ExamException('Incorrect ragne of year')
    elif time_series != check_list(time_series, 1):
        raise ExamException('in "compute_avg_monthly_difference" time_series element must be list returned by get_data()')    
    
    else:
        lista = fill(time_series)

        for line in lista:
            print(line)
        
        #inizio calcolo della media
        result = []
        n = b - a
        l = a - first_in_history
        #per il None
        for i in range(12):
            counter = 0
            summ = 0
            #n (+1 perché voglio un elemento in più, ma -1 perché ho j+1)
            for j in range(n):
                if lista[l+j][i] == None:
                    pass
                elif lista[l+j+1][i] == None:
                    lista[l+j+1][i] = lista[l+j][i]
                else:
                    summ = summ + lista[l+j+1][i] - lista[l+j][i]
                    counter = counter + 1
            
            if counter < 1: 
                media = 0
            else:
                media = summ/counter
                
            result.append(media)

    return result




    

mio_file = CSVTimeSeriesFile(name='data.csv')
print('Nome del file: "{}"'.format(mio_file.name))

time_series = mio_file.get_data()

for line in time_series:
   print (line)

first_year = '1949'
last_year = '1951'
lista = compute_avg_monthly_difference(time_series, first_year, last_year)
print (lista)