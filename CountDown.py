#CountDown2 temp#combinations second try 
#Danny Maclean
import random
import itertools
import copy
import timeit
import time
#global for answer found
answer_found = False
#globals()['answer_found'] = False

class var:
    def __init__(self,value):
        self.value = value
        self.string = None

def temps(number, first, second, appendval):
    temp = number[:]
    temp.remove(first)
    temp.remove(second)
    temp.append(appendval)
    return temp

def guess(thing, numbers, results, first, second):
    if thing == '+':
        add = var(first + second)
        add.string = [first, '+', second] #needs to be saved for later output
        return add.value
    if thing == '-':
        sub = var(first - second)
        sub.string = [first, '-', second] #needs to be saved for later output
        return sub.value
    if thing == '/':
        divide = var(first / second)
        divide.string = [first, '/', second] #needs to be saved for later output
        return divide.value
    if thing == '*':
        multiply = var(first * second)
        multiply.string = [first, '*', second] #needs to be saved for later output
        return multiply.value


def level_five(numbers,result):
    fifth = list(itertools.permutations(numbers, 2))
    global answer_found 
    for thing in fifth:
    #add
        value = guess('+', numbers, result, thing[0], thing[1])
        if value == target:
            answer_found= True
            result = ['(', thing[0], '+', thing[1], ')']
            return result
    #subtract
        if (thing[0] - thing[1]) > 0:
            value = guess('-', numbers, result, thing[0], thing[1])
            if value == target:
                answer_found = True 
                result = ['(', thing[0], '-', thing[1], ')']
                return result
    #multiply
        value = guess('*', numbers, result, thing[0], thing[1])
        if value == target:
            answer_found = True 
            result = ['(', thing[0], '*', thing[1], ')']
            return result
    #divide
        if (thing[1]!=0) or ((thing[0]/thing[1])%1 == 0):
            value = guess('/', numbers, result, thing[0], thing[1])
            if value == target:
                answer_found = True 
                result = ['(', thing[0], '/', thing[1], ')']
                return result
            else:
                return

def level_four(numbers,result):
    global answer_found
    fourth = list(itertools.permutations(numbers, 2))
    for thing in fourth:
    #add
        value = guess('+', numbers, result, thing[0], thing[1])
        if value == target:
            answer_found = True
            result = ['(', thing[0], '+', thing[1], ')']
            return result
        temp = temps(numbers,thing[0],thing[1],value)
        result = level_five(temp, result)
        if answer_found:
            to_insert = ['(', thing[0],'+', thing[1], ')']
            indice = result.index(value)
            result.pop(indice)
            front_half = result[:indice]
            back_half = result[indice:]
            #result.insert(indice, to_insert)
            return (front_half + to_insert + back_half)
    #subtract
        if (thing[0] - thing[1]) > 0:
            value = guess('-', numbers, result, thing[0], thing[1])
            if value == target:
                answer_found = True
                result = ['(', thing[0], '-', thing[1], ')']
                return result
            temp = temps(numbers,thing[0],thing[1],value)
            result = level_five(temp, result)
            if answer_found:
                to_insert = ['(', thing[0],'-', thing[1], ')']
                indice = result.index(value)
                result.pop(indice)
                front_half = result[:indice]
                back_half = result[indice:]
                #result.insert(indice, to_insert)
                return (front_half + to_insert + back_half)
    #multiply
        value = guess('*', numbers, result, thing[0], thing[1])
        if value == target:
            answer_found = True
            result = ['(', thing[0], '*', thing[1], ')'] 
            return result
        temp = temps(numbers,thing[0],thing[1],value)
        result = level_five(temp, result)
        if answer_found:
            to_insert = ['(', thing[0],'*', thing[1], ')']
            indice = result.index(value)
            result.pop(indice)
            front_half = result[:indice]
            back_half = result[indice:]
            #result.insert(indice, to_insert)
            return (front_half + to_insert + back_half)
    #divide
        if (thing[1]!=0) or ((thing[0]/thing[1])%1 == 0):
            value = guess('/', numbers, result, thing[0], thing[1])
            if value == target:
                answer_found = True
                result = ['(', thing[0], '/', thing[1], ')'] 
                return result
            temp = temps(numbers,thing[0],thing[1],value)
            result = level_five(temp, result)
            if answer_found:
                to_insert = ['(', thing[0],'/', thing[1], ')']
                indice = result.index(value)
                result.pop(indice)
                front_half = result[:indice]
                back_half = result[indice:]
                #result.insert(indice, to_insert)
                return (front_half + to_insert + back_half)

def level_three(numbers,result):
    global answer_found
    third = list(itertools.permutations(numbers, 2))
    for thing in third:
        #add
        value = guess('+', numbers, result, thing[0], thing[1])
        if value == target:
            answer_found = True
            result = ['(', thing[0], '+', thing[1], ')']
            return result  
        temp = temps(numbers,thing[0],thing[1],value)
        result = level_four(temp, result)
        if answer_found:
            to_insert = ['(', thing[0],'+', thing[1], ')']
            indice = result.index(value)
            result.pop(indice)
            front_half = result[:indice]
            back_half = result[indice:]
            #result.insert(indice, to_insert)
            return (front_half + to_insert + back_half)
    #subtract
        if (thing[0] - thing[1]) > 0:
            value = guess('-', numbers, result, thing[0], thing[1])
            if value == target:
                answer_found = True 
                result = ['(', thing[0], '-', thing[1], ')']
                return result
            temp = temps(numbers,thing[0],thing[1],value)
            result = level_four(temp, result)
            if answer_found:
                to_insert = ['(', thing[0],'-', thing[1], ')']
                indice = result.index(value)
                result.pop(indice)
                front_half = result[:indice]
                back_half = result[indice:]
                #result.insert(indice, to_insert)
                return (front_half + to_insert + back_half)
    #multiply
        value = guess('*', numbers, result, thing[0], thing[1])
        if value == target:
            answer_found = True 
            result = ['(', thing[0], '*', thing[1], ')']
            return result
        temp = temps(numbers,thing[0],thing[1],value)
        result = level_four(temp, result)
        if answer_found:
            to_insert = ['(', thing[0],'*', thing[1], ')']
            indice = result.index(value)
            result.pop(indice)
            front_half = result[:indice]
            back_half = result[indice:]
            #result.insert(indice, to_insert)
            return (front_half + to_insert + back_half)
    #divide
        if (thing[1]!=0) or ((thing[0]/thing[1])%1 == 0):
            value = guess('/', numbers, result, thing[0], thing[1])
            if value == target:
                answer_found = True 
                result = ['(', thing[0], '/', thing[1], ')']
                return result
            temp = temps(numbers,thing[0],thing[1],value)
            
            result = level_four(temp, result)
            if answer_found:
                to_insert = ['(', thing[0],'/', thing[1], ')']
                indice = result.index(value)
                result.pop(indice)
                front_half = result[:indice]
                back_half = result[indice:]
                #result.insert(indice, to_insert)
                return (front_half + to_insert + back_half)

def level_two(numbers, result):
    global answer_found
    second = list(itertools.permutations(numbers, 2))
    for thing in second:
    #add
        value = guess('+', numbers, result, thing[0], thing[1])
        if value == target:
            answer_found = True
            result = ['(', thing[0], '+', thing[1], ')']
            return result
        temp = temps(numbers,thing[0],thing[1],value)
        result = level_three(temp, result)
        if answer_found:
            to_insert = ['(', thing[0],'+', thing[1], ')']
            indice = result.index(value)
            result.pop(indice)
            front_half = result[:indice]
            back_half = result[indice:]
            #result.insert(indice, to_insert)
            return (front_half + to_insert + back_half)
    #sub    
        if (thing[0] - thing[1]) > 0:
            value = guess('-', numbers, result, thing[0], thing[1])
            if value == target:
                answer_found = True 
                result = ['(', thing[0], '-', thing[1], ')']
                return result
            temp = temps(numbers,thing[0],thing[1],value)
            result = level_three(temp, result)
            if answer_found:
                to_insert = ['(', thing[0],'-', thing[1], ')']
                indice = result.index(value)
                result.pop(indice)
                front_half = result[:indice]
                back_half = result[indice:]
                #result.insert(indice, to_insert)
                return (front_half + to_insert + back_half)
    #multiply
        value = guess('*', numbers, result, thing[0], thing[1])
        if value == target:
            answer_found = True 
            result = ['(', thing[0], '*', thing[1], ')']
            return result
        temp = temps(numbers,thing[0],thing[1],value)
        result = level_three(temp, result)
        if answer_found:
            to_insert = ['(', thing[0],'*', thing[1], ')']
            indice = result.index(value)
            result.pop(indice)
            front_half = result[:indice]
            back_half = result[indice:]
            #result.insert(indice, to_insert)
            return (front_half + to_insert + back_half)
    #divide
        if (thing[1]!=0) or ((thing[0]/thing[1])%1 == 0):
            value = guess('/', numbers, result, thing[0], thing[1])
            if value == target:
                answer_found = True 
                result = ['(', thing[0], '/', thing[1], ')']
                return result
            temp = temps(numbers,thing[0],thing[1],value)
            result = level_three(temp, result)
            if answer_found:
                to_insert = ['(', thing[0],'/', thing[1], ')']
                indice = result.index(value)
                result.pop(indice)
                front_half = result[:indice]
                back_half = result[indice:]
                #result.insert(indice, to_insert)
                return (front_half + to_insert + back_half)


#depth computations 
def level_one(numbers,result):
    global answer_found
    first = list(itertools.permutations(numbers, 2))
    #need new list to pass to level two
    for thing in first:
    #add
        value = guess('+', numbers, result, thing[0], thing[1])
        if value == target:
            answer_found = True
            result = ['(', thing[0], '+', thing[1], ')']
            return result
        temp = temps(numbers,thing[0],thing[1],value)
        result = level_two(temp, result)
        if answer_found:
            to_insert = ['(', thing[0],'+', thing[1], ')']
            indice = result.index(value)
            result.pop(indice)
            front_half = result[:indice]
            back_half = result[indice:]
            #result.insert(indice, to_insert)
            return (front_half + to_insert + back_half)
    #subtract
        if (thing[0] - thing[1]) > 0:
            value = guess('-', numbers, result, thing[0], thing[1])
            if value == target:
                answer_found = True 
                result = ['(', thing[0], '-', thing[1], ')']
                return result
            temp = temps(numbers,thing[0],thing[1],value)
            result = level_two(temp, result)
            if answer_found:
                to_insert = ['(', thing[0],'-', thing[1], ')']
                indice = result.index(value)
                result.pop(indice)
                front_half = result[:indice]
                back_half = result[indice:]
                #result.insert(indice, to_insert)
                return (front_half + to_insert + back_half)
    #multiply
        value = guess('*', numbers, result, thing[0], thing[1])
        if value == target:
            answer_found = True 
            result = ['(', thing[0], '*', thing[1], ')']
            return result
        temp = temps(numbers,thing[0],thing[1],value)
        result = level_two(temp, result)
        if answer_found:
            to_insert = ['(', thing[0],'*', thing[1], ')']
            indice = result.index(value)
            result.pop(indice)
            front_half = result[:indice]
            back_half = result[indice:]
            #result.insert(indice, to_insert)
            return (front_half + to_insert + back_half)
    #divide
        if (thing[1]!=0) or ((thing[0]/thing[1])%1 == 0):
            value = guess('/', numbers, result, thing[0], thing[1])
            if value == target:
                answer_found = True 
                result = ['(', thing[0], '/', thing[1], ')']
                return result
            temp = temps(numbers,thing[0],thing[1],value)
            result = level_two(temp, result)
            if answer_found:
                to_insert = ['(', thing[0],'/', thing[1], ')']
                indice = result.index(value)
                result.pop(indice)
                front_half = result[:indice]
                back_half = result[indice:]
                #result.insert(indice, to_insert)
                return (front_half + to_insert + back_half)

#recieve user input for selection of numbers
small_num = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10] # [x for x in range(1, 11)]*2
large_num = [25,50,75,100]
print("           Welcome to Countdown! I'll be your host, The All Knowing!")
print("*****************************************************************************************")
print("How many large numbers would you like? *Warning: your answer must be between 0-4* ")
while True:
    num_of_large_num=int(input("Answer: "))
    if num_of_large_num > 4: 
        print("Really Now...")
    else: break
print("Your 6 numbers are: ",end='')
numbers = []
result =[]
for x in range(0, (6-num_of_large_num)):
    first = random.randint(0,len(small_num)-1)
    print(small_num[first],end=' ')
    numbers.append(small_num[first])
    del(small_num[first])
for x in range(0, num_of_large_num):
    second = random.randint(0,len(large_num)-1)
    print(large_num[second],end=' ')
    numbers.append(large_num[second])
    del(large_num[second])
print("\nYour target number is....\n\n")
print("           ",end='')
target = random.randint(100,999)
print(target)
print('\n')
input("Hit enter to quit or check your answer against The All Knowing!")
print("One correct answer is...")
start = time.time()
result = level_one(numbers, result)
end = time.time()
print(*result, sep = '')
print('time taken: ', end = '')
print(end - start)
input("well done")
