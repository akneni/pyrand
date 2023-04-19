import requests
import time
import hashlib
import pyautogui
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
    randbytehash = hashlib.blake2s(randGen.randbytes(100)).hexdigest()
    comp_dif = 0
    counter = 0
    while comp_dif < 0.01:
        randbytehash = hashlib.blake2s(bytes(randbytehash, 'utf-8')).hexdigest()
        end = time.time()
        comp_dif = end-start
        counter += 1
    
    # Note that the screenshot is another source of entropy. The image is not saved anywhere
    img = pyautogui.screenshot()
    pixelvals = ""
    width, height = pyautogui.size()
    for _ in range (100):
        x, y = randGen.randint(0, width), randGen.randint(0, height)
        pixelvals += str(img.getpixel((x, y)))
        
    
    entropyHashes = [randbytehash]

    entropyHashes.append( hashlib.blake2s(bytes(str(req_dif), 'utf-8')).hexdigest() )
    entropyHashes.append( hashlib.blake2s(bytes(str(comp_dif), 'utf-8')).hexdigest() )
    entropyHashes.append( hashlib.blake2s(bytes(data, 'utf-8')).hexdigest() )
    entropyHashes.append( hashlib.blake2s(bytes(str(pyautogui.position()), 'utf-8')).hexdigest() )
    entropyHashes.append( hashlib.blake2s(bytes(str(img), 'utf-8')).hexdigest() )
    entropyHashes.append( hashlib.blake2s(bytes(str(pixelvals), 'utf-8')).hexdigest() )

    finalHash = hashlib.blake2b(bytes("!".join(entropyHashes), 'utf-8')).hexdigest()
    return finalHash

def extendHash(hash, requiredLen):
    if requiredLen <= 125500:
        while (len(hash) < requiredLen):
            salt = str(randGen.randint(0, 100))
            hash += hashlib.blake2s(bytes(hash + salt, 'utf-8')).hexdigest()
    else:
        while (len(hash) < requiredLen):
            salt = str(randGen.randint(0, 100))
            hash += hashlib.blake2s(bytes(hash[-40:] + salt, 'utf-8')).hexdigest()
            hash += hex(int(hash, 16) * randGen.randint(4,9))[2:]    
    return hash
    
def randint(min:int, max:int) -> int:    
    """
    Generates a random integer within the specified range.

    Parameters:
    min (int): The minimum value of the desired integer range (inclusive).
    max (int): The maximum value of the desired integer range (exclusive).

    Returns:
    int: A random integer within the specified range.
    """    
    return hexToInt(genRandHash(), min, max)

def uniform(min:int, max:int) -> float:
    """
    Generates a random float within the specified range.

    Parameters:
    min (float): The minimum value of the desired float range (inclusive).
    max (float): The maximum value of the desired float range (exclusive).

    Returns:
    float: A random float within the specified range.
    """
    return hexToFloat(genRandHash(), min, max)

def random() -> float:
    """
    Generates a random float between 0 and 1.

    Returns:
    float: A random float between 0 and 1.
    """
    return uniform(0, 1)

def choice(lst):
    """
    Returns a random element from the input list.

    Parameters:
    lst (list): The input list to choose a random element from.

    Returns:
    any: A random element from the input list.
    """
    index = randint(0, len(lst))
    return lst[index]

def randintLst(min:int, max:int, length:int) -> list:
    """
    Generates a list of random integers within the specified range.

    Parameters:
    min (int): The minimum value of the desired integer range (inclusive).
    max (int): The maximum value of the desired integer range (exclusive).
    length (int): The length of the list to be generated.

    Returns:
    list: A list of random integers within the specified range.
    """
    hash = genRandHash()
    dif = max-min
    requiredLen = dif * length
    hash = extendHash(hash, requiredLen)
    result = [0 for _ in range(length)]
    for i in range (length):
        result[i] = hexToInt(hash[i:i+(dif)], min, max)
    return result

def uniformLst(min:int, max:int, length:int) -> list:
    """
    Generates a list of random floats within the specified range.

    Parameters:
    min (float): The minimum value of the desired float range.
    max (float): The maximum value of the desired float range.
    length (int): The length of the list to be generated.

    Returns:
    list: A list of random floats within the specified range.
    """
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
    """
    Shuffles the input list using a random hash.

    Parameters:
    lst (list): The input list to be shuffled.

    Returns:
    list: A shuffled version of the input list.
    """
    hash = genRandHash()
    requiredLen = (len(lst)+1)**2 // 8
    hash = extendHash(hash, requiredLen)
    lst = lst.copy()
    
    newLst = []
    counter = 0
    while (len(lst) != 0):
        newLst.append(lst.pop(hexToInt(hash[counter:counter+len(lst)//4], 0, len(lst))))
        counter += len(lst)

    print (requiredLen)
    return newLst

def sample(lst, numSamples) -> list:
    """
    Generates a list of unique elements randomly chosen from the input list.

    Parameters:
    lst (list): The input list to choose elements from.
    numSamples (int): The number of unique elements to choose.

    Returns:
    list: A list of unique elements randomly chosen from the input list.
    """
    lst = list(lst.copy())
    hash = genRandHash()
    
    requiredLen = len(lst) * numSamples
    hash = extendHash(hash, requiredLen)
    
    result = []
    for i in range (numSamples):
        result.append( lst.pop(hexToInt(hash[i:i+len(lst)], 0, len(lst))) )
    return result

