#!/usr/bin/python
import math
i = 1
while i < 35:
    n = (math.factorial(39))/(math.factorial(34)*math.factorial(5))
    m = (math.factorial(39-i))/(math.factorial(34-i)*math.factorial(5))
    c = (n-m)/float(n)
    print(str(i)+': '+str(c))
    i += 1