import math
from statistics import mean
import random

# my_dict = {1:1, 2:1, 3:0}

# def avg(d: dict):
#   values = d.values()
#   ev = mean(values)
#   print(values)
#   print(ev)

# avg(my_dict)

# def random_num():
#   activator = random.randint(0, 4)

#   if activator == 0:
#     x = random.uniform(0.11, 0.20)
#   else:
#     x = random.uniform(0.05, 0.10)

#   return round(x, 3)

# print(random_num())


user_choice = ""

while user_choice.replace(" ", "").lower() not in {"deal", "nodeal"}:
    try:
      user_choice = str(input(" "))
    except TypeError:
      print("\n\nInvalid. Please type either 'deal' or 'no deal'.\n")
    except ValueError:
      print("\n\nPlease type either 'deal' or 'no deal'.")

