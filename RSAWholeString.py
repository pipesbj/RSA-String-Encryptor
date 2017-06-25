#   Author: Benjamin Pipes
#
#   The purpose of this assignment is to implement a naive RSA encryption, without using
#   any encryption libraries.
#   The program prompts the user for two prime numbers, p & q
#   from there, it calculates all the values needed for RSA encryption.
#   It encrypts and decrypts an integer "message"
#   once its done, it displays all the necessary info.
#
    #   Used Python 3.5.3, Files needed: 447rsaString.py

from fractions import gcd;
import math;
import random;
import sys;

def isprime(n):
    "check if integer n is a prime"
    n = abs(int(n))
    #check for rudimentary cases
    if n < 2:
        return False
    if n == 2: 
        return True    
    if not n & 1: 
        return False
    #if above cases fail, try all numbers between three and sqrt of the number
    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True

def validE(ep, tot):
    "Determines whether number is a valid candidate for e value"
    "returns zero if true, > 0 if false"

    if(ep > 1 and ep < tot):
        if(gcd(ep,tot) == 1):
            return True;
    else:
        return False;

def pad(msg, cp):
    #input: the message as and int
    #       the target it needs to be coprime with
    #out:   the padding value, ie: the number to add to the message
    origMsg = msg;
    if (msg > cp):
        #if message is larger than mod value
        pad = -2;
        while(msg > cp):
            msg = origMsg   #reset message
            if(msg + (pad - 10000000) > 0):
                #if the message can handle another huge chunk decremented
                pad = pad - 10000000;  #decrement the pad
                msg = msg + pad; #subtract pad from message
            else:
                pad = pad - 1;
                msg = msg + pad;
            #print("msg: ",msg,"pad: ",pad);
        while(gcd(msg,cp) !=1 and msg > 0): #once message is lower than mod value, check for coprime-ness
            msg = msg + pad;    #"add" it to message, making it smaller.
            pad = pad - 1;
            
    else:
        #message is under the mod value, just check from coprime-ness
        pad = 1;
        msg = msg + pad; #initially pad the message
        while(gcd(msg,cp) != 1):
            pad = pad + 1;  #if padding failed, increment the pad
            msg = msg + pad;    #pad the message with new pad
        
    return pad;

#****************************************************************
#                               main
#****************************************************************
def main():
    pvalid = 1;
    qvalid = 1;
    #prompt for p and q values. Checks to make sure user entered prime numbers.
    while(pvalid == 1):
        #while p value is not a prime
        pVal = int(input("Enter p-value: "));
        if(isprime(pVal)):
            #prime p value entered, move on to q
            pvalid = 0;
            while(qvalid == 1):
                #while q value is not a prime
                qVal = int(input("Enter q-value: "));
                if(isprime(qVal) and (qVal != pVal)):
                    qvalid = 0;
                else:
                    qvalid = 1;
                    print("expect q-value to be a prime")
        else:
            pvalid = 1;
            print("expect p-value to be a prime");

    #calculate n and totient
    nVal = pVal * qVal;
    tot = (pVal - 1)*(qVal - 1);

    #generate an e value. Checks if 1 < e < totient and e is a coprime.***
    
    validEp = 1;
    while(validEp == 1):
        eVal = random.randint(2,tot);   #generate a random number between 2 and the totient
        if(isprime(eVal)):
            if(validE(eVal,tot)):       #determine its coprime with the totient
                validEp = 0;
            else:
                validEp = 1;

    #generate a d value, must satisfy d*e mod phi(n) = 1******************
    validD = 1;
    dVal = 200;
    #starts at 200 and increments until relation is satisfied
    
    while(validD == 1):
        
        if(((dVal * eVal) % tot) == 1):
            validD = 0;
        else:
            dVal = dVal + 1;
            validD = 1;

    testStr = str(input("Enter String (6 or less characters): "));
    strArr = list(testStr); #store user input as char array
    
    padInt = 0;
    strLen = len(strArr);

    #traverse the string, turn into byte array
    for i in range(strLen):
        strArr[i] = strArr[i].encode();

    #=======================
   # testb = testStr.encode();   #encode the message to bytes
   # testInt = int.from_bytes(testb, sys.byteorder); #bytes to int
    #========================
    
    strArri = [];   #holds the int values for each byte
    padArri = [];   #holds the pad value for each int
    eMsgArr = [];   #holds the encrypted values for each int
    dMsgArr = [];   #holds the decrypted values for each int
    dMsgArra = [];  #holds the actual values after padding operations
    dMsgArrb = [];  #holds the decrypted values as bytes
    dMsgStr = [];   #holds the decrypted values as chars
    #store the values as ints in an array
    for k in range(strLen):
        padArri.append(0); #fill pad array with zeros
        eMsgArr.append(0); #fill encrypted values with zero
        dMsgArr.append(0); #fill decrypted values with zero;
        dMsgArra.append(0);
        dMsgArrb.append(b'z');
        dMsgStr.append(b'z');
        strArri.append(int.from_bytes(strArr[k], sys.byteorder));

    for j in range(strLen):
        #determine whether padding is needed or not
        if(gcd(strArri[j],nVal) != 1 or (strArri[j] > nVal)):
            #if the test message is not coprime to n
            #or if test message is bigger than mod value
            padArri[j] = pad(strArri[j],nVal);   #generate the pad needed
        strArri[j] = strArri[j] + padArri[j];
        eMsgArr[j] = pow(strArri[j], eVal, nVal); #encrypt the int
        dMsgArr[j] = pow(eMsgArr[j], dVal, nVal); #decrypt the int
        dMsgArra[j] = dMsgArr[j] - padArri[j];     #apply the pad value
        dMsgArrb[j] = dMsgArra[j].to_bytes(dMsgArr[j].bit_length(), sys.byteorder);
        dMsgStr[j] = dMsgArrb[j].decode(); 

        #==============================
    #eMsg = pow(testInt,eVal,nVal);     #encrypt the message
    
    #dMsgInt = pow(eMsg,dVal,nVal);  #decrypt the message    
    #dMsgIntReal = dMsgInt - padInt;   #pad the message before turning into bytes
        #==============================
    
   # dMsgb = dMsgIntReal.to_bytes(dMsgInt.bit_length(), sys.byteorder); #convert decrypted int to bytes
    #dMsgStr = dMsgb.decode();
        #=============================
    
    #************display all the necessary information.***********************
    print("pval: ", pVal, "\nqVal: ", qVal, "\nnVal: ", nVal, "\nPhi(n): ", tot,
         "\npublic key(e, n): (", eVal," ", nVal,
          ")\nprivate key(d, n): (", dVal," ", nVal,")");
    
    print("initial text: ");
    for i in range(strLen):
        print(strArr[i],end=' ');
        
    print("\ninitial input: ");
    for i in range(strLen):
        print(strArri[i] - padArri[j],end=' ');
        
    print("\nencrypted input: ");
    for i in range(strLen):
        print(eMsgArr[i],end=' ');
            
    print("\ndecrypted input: ");
    for i in range(strLen):
        print(dMsgArr[i],end=' ');
        
    print("\ndecrypted text: ");
    for i in range(strLen):
        print(dMsgStr[i],end='');
    
main();
