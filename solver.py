import numpy as np
import cv2

def FindBrackets(a):
    """Nalazi prvi dio izraza unutar kojeg nema zagrada; vraca indekse unutar zagrada"""
    m,n = -1, -1
    for r in range(len(a)):
        if a[r] == '15':
            for s in range(r,-1,-1):
                if a[s] == '14':
                    m = s+1
                    break
            n = r-1
            break
    return m,n

def FindOperators(a):
    """Pronalazi indekse na kojima se nalaze operatori ili zagrade"""
    operators = [];
    for r in range(len(a)):
        if a[r] == '10' or a[r] == '11' or a[r] == '12' or a[r] == '13' or a[r] == '14' or a[r] == '15':
            operators.append(r)

    if operators == []:
        operators.append(-1)
    return operators



def create_number( a ):
    """Spaja znamenke u brojeve"""
    number = a[0]
    for i in range(len(a) - 1):
        number = number + a[i+1]

    #popravak brojeva koje bi program inace procitao kao oznaku operatora (10 znaci +, 11 - itd.)
    if number == '10':
        number = '010'
    if number == '11':
        number = '011'
    if number == '12':
        number = '012'
    if number == '13':
        number = '013'
    if number == '14':
        number = '014'
    if number == '15':
        number = '015'    

    return number


def concatenate_digits( a ):
    """Funkcija pronalazi sve znamenke i susjedne spoji u jedan broj"""
    index = FindOperators(a)
    if index[0] == -1:
        number = create_number(a)
        return number

    current_number = a[: index[0] ]
    number = create_number(current_number)
    b = [number]
    b.append(a[index[0]])

    for r in range(len(index)-1):
        if index[r+1] == index[r] + 1:
            continue
        current_number = a[index[r]+1 : index[r+1]]
        number = create_number(current_number)
        b.append(number)
        b.append(a[index[r+1]])
    
    current_number = a[index[len(index)-1] + 1 :]
    number = create_number(current_number)
    b.append(number)
    return b

def find_character( a , operation):
    """Pronalazi indeks na kojem je operacija, input operation je zeljeni znak. Ako ga nema vraca -1"""

    index = -1

    if operation == '*':
        s_character = '12'
    if operation == '/':
        s_character = '13'
    if operation == '+':
        s_character = '10'
    if operation == '-':
        s_character = '11'

    for r in range(len(a)):
        if a[r] == s_character:
            index = r
            break

    return index

def operations(a_input): #nema zagrada
    """Evaluira sve operacije u izrazu bez zagrada s poslozenim prioritetima na *,/"""

    a = a_input

    test = FindOperators(a)

    while( test[0] != -1 ):
        i = find_character( a , '*')
        if i != -1:
            num1 = float( a[i-1])
            num2 = float( a[i+1] )

            result = num1 * num2
            a[i-1 : i+2] = [str(result)]

            test = FindOperators(a)
            continue

        i = find_character( a , '/')
        if i != -1:
            num1 = float( a[i-1])
            num2 = float( a[i+1] )

            result = num1 / num2
            a[i-1 : i+2] = [str(result)]

            test = FindOperators(a)
            continue           

        i = find_character( a , '+')
        if i != -1:
            num1 = float( a[i-1])
            num2 = float( a[i+1] )

            result = num1 + num2
            a[i-1 : i+2] = [str(result)]

            test = FindOperators(a)
            continue

        i = find_character( a , '-')
        if i != -1:
            num1 = float( a[i-1])
            num2 = float( a[i+1] )

            result = num1 - num2
            a[i-1 : i+2] = [str(result)]
            test = FindOperators(a)
            continue

    return a


def my_evaluate( a ):
    """Glavna funkcija za evaluaciju"""
    m,n = FindBrackets(a) #m,n nisu zagrade nego izmedu

    while(m != -1 and n!= -1):
        current = a[m:n+1]
        current = concatenate_digits(current)
        current = operations(current)
        a[m-1 : n+2] = current
        m,n = FindBrackets(a)

    a = concatenate_digits(a)
    a = operations(a)

    return float(a[0])




if __name__ == "__main__":
    a = ["7","10","14","14","1","3","11","1","1","15","12","2","10","4","12","14","2","10","3","15","15","12","2"]

    #a = 7 + ((13-11)*2+4*(2+3))*2

    b = my_evaluate(a)
    print(b)
