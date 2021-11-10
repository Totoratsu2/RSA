import numpy as np
import random
import time
import concurrent.futures

from texto import getDiccionario

CARACTERES = getDiccionario()

rd = np.random.default_rng()


def getPrimos():
    # modified version of src: https://stackoverflow.com/questions/3285443/improving-pure-python-prime-sieve-by-recurrence-formula
    n = 5000
    sieve = np.ones(n//3 + (n % 6 == 2), dtype=bool)
    for i in range(1, int(n ** 0.5)//3+1):
        if sieve[i]:
            k = 3*i+1 | 1
            sieve[k*k//3::2*k] = False
            sieve[k*(k-2*(i & 1)+4)//3::2*k] = False
    return random.choices(np.r_[2, 3, ((3*np.nonzero(sieve)[0][1:]+1) | 1)], k=2)


def validateE(e: np.int64, n: np.int64) -> bool:
    numeros = encriptar("áraña", e, n)

    for y in numeros:
        if np.count_nonzero(numeros == y) > 1:
            return False

    return True


def mcdFi(lista: np.ndarray, fi: np.int64, n: np.int64):
    while lista.size == 0:
        e = rd.integers(fi, size=1)[0]

        if np.gcd(e, fi) == 1 and validateE(e, n):
            return e


def getE(fi: np.int64, n: np.int64) -> np.int64:
    e = np.array([], dtype=np.int64)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(mcdFi, e, fi, n)
        res = future.result()
        if res is not None:
            e = res
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(mcdFi, e, fi, n)
        res = future.result()
        if res is not None:
            e = res
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(mcdFi, e, fi, n)
        res = future.result()
        if res is not None:
            e = res

    return e


def getD(fi: np.int64, e: np.int64) -> np.int64:
    for y in range(1, fi+1):
        if (e*y) % fi == 1:
            return y


def desencriptar(encriptado: np.ndarray, d: np.int64, n: np.int64) -> str:
    resultado = ""
    for char in encriptado:
        indice = expMOD(char, d, n) % n
        resultado += CARACTERES[indice]

    return resultado


def encriptar(mensaje: str, e: np.int64, n: np.int64) -> np.int64:
    resultado = np.array([], dtype=np.int64)
    msgLista = np.array([char for char in mensaje])

    for char in msgLista:
        indice = np.where(CARACTERES == char)[0][0]
        resultado = np.append(resultado,  expMOD(indice, e, n) % n)

    return resultado


def expMOD(b: np.int64, exp: np.int64, n: np.int64) -> np.int64:
    # modified version of src: https://stackoverflow.com/questions/57668289/implement-the-function-fast-modular-exponentiation
    res = 1
    while exp > 1:
        if exp & 1:
            res = (res * b) % n
        b = np.power(b, 2) % n
        exp >>= 1
    return (b * res) % n


def genParLlaves():
    p, q = getPrimos()
    n = p*q
    fi = (p-1)*(q-1)

    print(f"p={p}\tq={q}")
    start_time = time.time()
    e = getE(fi, n)
    d = getD(fi, e)
    print("--- e y d %s seconds ---" %
          (time.time() - start_time))

    return [(n, e), (n, d)]
