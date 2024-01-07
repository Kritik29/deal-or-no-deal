import random
import time
import sys
import locale

locale.setlocale( locale.LC_ALL, '' )

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

DOLLAR_AMOUNTS = [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750,
                  1000, 5000, 10000, 25000, 50000, 75000, 100000,
                  200000, 300000, 400000, 500000, 750000, 1000000]

def slow_print(s):
  for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)

def populateCases(d):
  # dictionary to store all the briefcases with dollar amounts in them
  cases = {}
  local_dollar_amounts = list(d)

  # store unique dollar amounts in the dict (no duplicate dollar amounts)
  for _ in range(1, 27):
    cases[_] = random.choice(local_dollar_amounts)
    local_dollar_amounts.remove(cases[_])
  
  return cases

slow_print(f'\n\n{bcolors.HEADER}WELCOME TO DEAL OR NO DEAL!{bcolors.ENDC}\n\nPick one of the 26 cases below\n')
cases_in_play = list(populateCases(DOLLAR_AMOUNTS).keys())
print(*cases_in_play)
print(populateCases(DOLLAR_AMOUNTS))
USER_SELECTION = None

while True:
  try:
    USER_SELECTION = int(input("\nYour selection: "))
    if 1 <= USER_SELECTION <= 26:
      break
    else:
      print("\nPlease select a number between 1 and 26.")
  except ValueError:
    print("\nInvalid. Please choose a case number from the above\n")

slow_print(f"\n\nYou selected case: {bcolors.OKGREEN}{USER_SELECTION}{bcolors.ENDC}\n\n")
last_case_to_open = {USER_SELECTION: cases_in_play[USER_SELECTION-1]}
print(last_case_to_open)
del cases_in_play[USER_SELECTION-1]
time.sleep(1)
slow_print(f"{bcolors.YELLOW}Let's play Deal or No Deal!{bcolors.ENDC}\n\nYou will now select 6 cases to open.\n\n")

case_to_open = None

while True:
  try:
    case_to_open = int(input("\nWhat case do you want to open? "))
    if (1 <= case_to_open <= 26) and case_to_open in cases_in_play:
      break
    else:
      print("\nPlease select case between 1 and 26 that is in play.")
  except ValueError:
    print("\nInvalid. Please choose a case number from the above\n")

slow_print(f"\n\nYou picked {bcolors.CYAN}Case Number {case_to_open}{bcolors.ENDC}. Case Number {case_to_open} had:")
slow_print(f"\n\n {bcolors.YELLOW} {locale.currency(cases_in_play[case_to_open-1], grouping=True)} {bcolors.ENDC}")

del cases_in_play[case_to_open-1]

slow_print(f"\n\nThe cases remaining are: \n\n")
print(*cases_in_play)

## TODO: print the current board
## TODO: need to consider dictionary element deletion, the order of the elements changes and this messes up the indexing
## TODO: for some reason, accessing dictionary values from keys doesn't work as expected, need to debug




