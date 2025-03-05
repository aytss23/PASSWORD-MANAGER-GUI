from random import choice
from string import ascii_letters, digits

#karakter sözlükleri ve sonuç listesi. 
INCLUDE_DICTIONARY = { 'CHARACTERS' : True, 'SPECIAL_CHARACTERS': True, 'NUMBERS': True }
ASCII_DICTIONARY = { 'CHARACTERS' : ascii_letters, 'SPECIAL_CHARACTERS' : "!#$%&()*+-*/:;><|=@?_[]", 'NUMBERS' : digits }
GENERATE_RESULT = []


def generatePassword(generateLength = 16): #belirli uzunlukta ve belirli karakterleri içeren şifre metinleri oluşturur. 

    if generateLength < 4 or generateLength > 128: generateLength = 16
    
    GENERATE_RESULT.clear()
    
    for generateIndex in range(generateLength): 
        GENERATE_RESULT.append(choice(list(ASCII_DICTIONARY[choice(list({INCLUDES: INCLUDE_VALUE for INCLUDES, INCLUDE_VALUE in INCLUDE_DICTIONARY.items() if INCLUDE_VALUE}))])))
    
    return "".join(map(lambda quoteChar: "*" if quoteChar == '"' else quoteChar, GENERATE_RESULT))