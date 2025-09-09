This code take in a file by the command line and does a cellular life simulator on the input file given. 
It will return the output after a hundred iterations the folder where you ran the file. 
This only works with square matricies, but can take any size.
It will return the time taken to solve each one to with how many processes you used.

You will need to provide two valid command line arguments for the program to function properly:
-i for input file path
-o for output file path (include .txt at the end)

You also can specify the amount of processes you want, if the argument is left out it will be assumed to be one (single threaded):
-p for amount of processes (anything greater than zero is acceptable)


Here are the cellular life rules the program runs by:
Firstly the only acceptable symbols are (X, x, ., o, O) and they have their assosiated values (-3, -1, 0, 1, 3). All of them are dependent on the sum of their neighbors
If the current cell is a O and the sum is in the Fibonacci sequence then it is now dead (.). If the sum is less than 12 it is now a small o.
If the current cell is little O and the sum is less than 0 it is now dead (.). If the sum is greater than 6 it is now a big O.
If the current cell is dead (.) and it is a power of two it will be a little o. If the absolute value is a power of two it will be a little x.
If the current cell is little x and the sum is less than 0 it will now be dead (.). If it's less than -6 it will be a big X.
If the current cell is big X and the absolute value of the sum is prime it will be dead (.). If the sum is greater than -12 it will now be little x.
