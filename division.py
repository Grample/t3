from time import time

def factorize(*number):
    Results=''
    for numb in number:
        DividersList=[]
        i=0
        while i<numb:
            i+=1    
            if not numb % i:
                DividersList.append(i)
        Results += f'dividers of {numb} is {DividersList}\n'
    return Results

if __name__ == "__main__":
    CurrTime=time()
    print(factorize(1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060))
    print(time()-CurrTime)

    