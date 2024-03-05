# Code Analysis
# For each of the following given codes:
# Without executing the code try to read the code and write down what will be the output.
# Use the Python Code Visualizer and execute the code step-by-step. Observe how the variables and statements are executing in each iteration of the loops.

# Code 1
i = 7 #variabele met getal 7
for number in range(1, i + i): #for loop met de variabele number met en range van (1 tot 7+7 = 14)
   print(number) #number uitprinten # hier komen de getallen 1 tot en met 13 uit.
   
# Code 2
i = 1 # var i with number 1
j = 10 # var j with number 10
for number in range(i, j): # for loop with var number in range (i,j) so (1, 10)
   if number > 5:   # if number greater then 5 -> print the number
       print(number)
   else:            # else print hello
       print('Hello') # so for number 1,2,3,4,5 it prints "hello", the rest will print out as the number so 6,7,8,9

# Code 3
sentence = "I just came to say hello!" # a string
count = 0 # a counter
for letter in sentence: # for loop 
   if letter == " ": # if there is a space in the program, the count goes up by 1
       count = count + 1
   elif letter == "a": # if there is an a in the program, the count goes down by 1
       count = count - 1
print(count) # prints the count. In this code there are 5 spaces and 2 a's so 5-2 is 3.

# Code 4
sentence = "I just came to say hello!" # a string
for i in range(0, len(sentence)): # for loop i in range from 0 to the length of the string, in this one it is (24)
	print(sentence[i]) # prints the sentence out from position 0 until the length of the string (24) the [] means the postion with 0 as the starting one.
 
# Code 5
sentence = "I just came to say hello!" # a string
for c in sentence: # c is a variabele, it is exactly the same as code 4 (it does not mean, if c is in the sentence then print a "c")
	print(c) # the whole sentence is printed from position 0 until the end of the sentence
 
###
# Supporting Topics
# Data Formats

###
# Task
# Perform a free (re-)search and explore the answers for the following questions:
###

# Digits in decimal numbers are 0-9. What are the digits in hexadecimal format? What are the digits in binary format?
    #hexadecimal werkt in 16 met 0-9 en A, B, C, D, E, F. Binary gebruikt 0 en 1. bijv: 10 of 1010.
    
# Convert (manually) the following decimal numbers to hexadecimal and binary: 8, 10, 15, 21, 32, 64, 256, 500, 512, 1000.
    # Hexadecimal : 8, A, F, 15, 20, 40, 100, 1F4, 200, 3E8
    # Binary : 1000, 1010, 1111, 10101, 100000, 1000000, 100000000, 111110100, 1000000000, 1111101000
    # Binary werkt met de macht van 2.
    
# How does Python represent these data formats? How can you use Python to convert these data formats to each other?
    # met bin() maak je van een int een binary
    # met hex() maak je van een int een hxadecimal
    # met int(string, base) maak je een decimal (2 of 16 dependent on the type you want to convert)
    
###
# Use Python to:
###

# Convert the decimal number 45 into its binary representation.
binary = bin(45)
print(binary)
# Convert the binary number 1010101 into decimal form.
getal = int("1010101", 2)
print(getal)
# Add the binary numbers 10111 and 1101 and express the result in binary.
a = "10111"
b = "1101"
som = int(a,2) + int(b,2)
print(som)
# Convert the decimal number 255 into its hexadecimal representation.
getal2 = hex(255)
print(getal2)
# Convert the hexadecimal number 2A into decimal form.
getal3 = int("2A", 16)
print(getal3)
# Add the hexadecimal numbers C4 and 3A and express the result in hexadecimal.
som1 = hex(int("C4", 16) + int("3A", 16))
print(som1)
# Convert the binary number 1101 into decimal form.
getal4 = "1101"
print(int(getal4, 2))
# Convert the hexadecimal number F0 into decimal form.
getal5 = "F0"
print(int(getal5, 16))
# Add the decimal numbers 123 and 456.
a1 = 123
b1 = 456
print(a1+b1)
# Convert the decimal number 157 into binary and then into hexadecimal.
getal6 = 157
binary1 = bin(getal6)
hexadecimal = hex(int(binary1, 2))
print(binary1)
print(hexadecimal)
# Convert the binary number 11101101 into decimal and then into hexadecimal.
getal7 = "11101101"
getal8 = int(getal7, 2)
getal9 = hex(getal8)
print(getal8)
print(getal9)
# Convert the hexadecimal number AB4 into decimal and then into binary.
getal10 = "AB4"
getal11 = int(getal10, 16)
getal12 = bin(getal11)
print(getal11)
print(getal12)

###
# Real-life Applications:
###

# Research and identify a real-world example where binary data is used extensively.
    # I think the easiest answer to this is a computer, for example in memory the 0s and 1s it needs to switch on and off.
    
# Investigate how hexadecimal is used in computer memory addressing (CMA).
    # Hexadecimal is used in (CMA) for easy readability and for compact, it does not usse much space.

# Explore how decimal data formats are used in financial calculations or accounting systems.
    # Decimal data is used in financial calculations for its accuracy, a float is not accurate enough.