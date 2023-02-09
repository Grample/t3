from time import time
from multiprocessing import Pool, cpu_count

def factorize(number):
    Results=[]
    i=0
    while i<number:
        i+=1
        if not number % i:
            Results.append(i)
    return Results

def callback_division(Results):
    print(f'dividers is {Results}')

if __name__ == "__main__":
    CurrTime=time()
    with Pool(cpu_count()) as pool:
        pool.map_async(
            factorize,
            [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999],
            callback=callback_division
            )
        pool.close()
        pool.join()
    print(time()-CurrTime)
