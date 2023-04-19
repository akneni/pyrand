import requests
import time
import hashlib
import random as randGen

def hexToInt(hex_string, min_value, max_value):
    hex_int = int(hex_string, 16)
    max_hex_int = int('F' * len(hex_string), 16)
    normalized_value = hex_int / max_hex_int
    scaled_value = min_value + (max_value - min_value - 0.001) * normalized_value
    return int(scaled_value)

def hexToFloat(hex_string, min_value, max_value):
    hex_int = int(hex_string, 16)
    max_hex_int = int('F' * len(hex_string), 16)
    normalized_value = hex_int / max_hex_int
    scaled_value = min_value + (max_value - min_value) * normalized_value
    return scaled_value

def genRandHash():
    start = time.time()
    data = requests.get('https://www.accuweather.com/').text
    end = time.time()
    req_dif = end-start

    start = time.time()
    randbytehash = hashlib.sha256(randGen.randbytes(100)).hexdigest()
    comp_dif = 0
    counter = 0
    while comp_dif < 0.01:
        randbytehash = hashlib.sha256(bytes(randbytehash, 'utf-8')).hexdigest()
        end = time.time()
        comp_dif = end-start
        counter += 1

    reqhash = hashlib.sha256(bytes(str(req_dif), 'utf-8')).hexdigest()
    comphash = hashlib.sha256(bytes(str(comp_dif), 'utf-8')).hexdigest()
    weatherhash = hashlib.sha256(bytes(data, 'utf-8')).hexdigest()

    finalHash = reqhash = hashlib.sha256(bytes(str(reqhash + comphash + randbytehash + weatherhash), 'utf-8')).hexdigest()
    return finalHash

def extendHash(hash, requiredLen):
    if requiredLen <= 125500:
        while (len(hash) < requiredLen):
            salt = str(randGen.randint(0, 100))
            hash += hashlib.sha256(bytes(hash + salt, 'utf-8')).hexdigest()
    else:
        while (len(hash) < requiredLen):
            salt = str(randGen.randint(0, 100))
            hash += hashlib.sha256(bytes(hash[-40:] + salt, 'utf-8')).hexdigest()
            hash += hex(int(hash, 16) * randGen.randint(4,9))[2:]    
    return hash
    
def randint(min:int, max:int) -> int:        
    return hexToInt(genRandHash(), min, max)

def uniform(min:int, max:int) -> float:
    return hexToFloat(genRandHash(), min, max)

def random() -> float:
    return uniform(0, 1)

def choice(lst):
    index = randint(0, len(lst))
    return lst[index]

def randintLst(min:int, max:int, length:int) -> list:
    hash = genRandHash()
    
    dif = max-min
    requiredLen = dif * length
    hash = extendHash(hash, requiredLen)
    
    result = [0 for _ in range(length)]
    for i in range (length):
        result[i] = hexToInt(hash[i:i+(dif)], min, max)
    
    return result

def uniformLst(min:int, max:int, length:int) -> list:
    hash = genRandHash()
    
    dif = max-min
    requiredLen = dif * length
    while (len(hash) < requiredLen):
        salt = str(randGen.randint(0, 100))
        hash += hashlib.sha256(bytes(hash + salt, 'utf-8')).hexdigest()
    
    result = [0 for _ in range(length)]
    for i in range (length):
        result[i] = hexToFloat(hash[i:i+(dif)], min, max)
    
    return result

def shuffle(lst:list) -> list:
    hash = genRandHash()
    requiredLen = (len(lst)+1)**2 // 2
    hash = extendHash(hash, requiredLen)
    lst = lst.copy()
    
    newLst = []
    while (len(lst) != 0):
        newLst.append(lst.pop(hexToInt(hash[counter:counter+len(lst)], 0, len(lst))))
    return newLst

def sample(lst, numSamples) -> list:
    lst = list(lst.copy())
    hash = genRandHash()
    
    requiredLen = len(lst) * numSamples
    hash = extendHash(hash, requiredLen)
    
    result = []
    for i in range (numSamples):
        result.append( lst.pop(hexToInt(hash[i:i+len(lst)], 0, len(lst))) )
    return result

