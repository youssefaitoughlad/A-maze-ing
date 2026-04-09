import random
import ast

test_arr =  [1, 2, 3, 4, 5]

random.seed({" ":2})
print(random.choice(test_arr))


random.seed(None)
print(random.choice(test_arr))
#duplicate done
#seed 
#maze.txt permission done 

s = "Trsdsdp"
value = ast.literal_eval(s)
print(type(value))