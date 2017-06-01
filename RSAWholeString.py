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
    #testStr = "hey";    #the test message.
    
    padInt = 0;

    testb = testStr.encode();   #encode the message to bytes
    testInt = int.from_bytes(testb, sys.byteorder); #bytes to int
    
    #determine whether padding is needed or not
    if(gcd(testInt,nVal) != 1 or (testInt > nVal)):
        #if the test message is not coprime to n
        #or if test message is bigger than mod value
        padInt = pad(testInt,nVal);   #generate the pad needed

    testInt = testInt + padInt;   
    #test = test + padInt;
    print("messsage:",testInt, "(original + ", padInt,")");
    eMsg = pow(testInt,eVal,nVal);     #encrypt the message
    
    dMsgInt = pow(eMsg,dVal,nVal);  #decrypt the message    
    dMsgIntReal = dMsgInt - padInt;   #pad the message before turning into bytes
    
    dMsgb = dMsgIntReal.to_bytes(dMsgInt.bit_length(), sys.byteorder); #convert decrypted int to bytes
    dMsgStr = dMsgb.decode();
    
    
    #************display all the necessary information.***********************
    print("pval: ", pVal, "\nqVal: ", qVal, "\nnVal: ", nVal, "\nPhi(n): ", tot,
         "\npublic key(e, n): (", eVal," ", nVal,
          ")\nprivate key(d, n): (", dVal," ", nVal,")");
    print("initial text: ", testStr);
    print("initial input: ",testInt - padInt);
    print("encrypted input: ",eMsg);
    print("decrypted input: ",dMsgInt - padInt);
    print("decrypted text: ", dMsgStr);
          
main();

