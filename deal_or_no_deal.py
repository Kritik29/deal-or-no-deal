import random
import time
import sys
import locale
from statistics import mean

locale.setlocale(locale.LC_ALL, '')

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

ev_offer_ratio = 0.35

def slow_print(s):
  for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)

def slower_print(s):
  for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.25)

def populate_cases(d):
  # dictionary to store all the briefcases with dollar amounts in them
  cases = {}
  local_dollar_amounts = list(d)

  # store unique dollar amounts in the dict (no duplicate dollar amounts)
  for _ in range(1, 27):
    cases[_] = random.choice(local_dollar_amounts)
    local_dollar_amounts.remove(cases[_])
  
  return cases

cases_dict = populate_cases(DOLLAR_AMOUNTS)
# copy of cases_dict used to show the dollar amounts left on the board
cases_dict_copy = dict(cases_dict)
# print(cases_dict)
USER_SELECTION = int
last_case_to_open = {}

def initial_sequence(user_case):
  slow_print(f'\n\n{bcolors.HEADER}WELCOME TO DEAL OR NO DEAL!{bcolors.ENDC}\n\nPick one of the 26 cases below.\n\n')
  print(*list(cases_dict.keys()))

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
  # print(USER_SELECTION)
  user_case = {USER_SELECTION: cases_dict.get(USER_SELECTION)}
  # print(last_case_to_open)
  del cases_dict[USER_SELECTION]
  time.sleep(1)
  slow_print(f"{bcolors.YELLOW}Let's play {bcolors.BOLD}Deal or No Deal!{bcolors.ENDC}{bcolors.ENDC}\n\nYou will now select 6 cases to open.\n\n")
  return user_case

last_case_to_open = initial_sequence(last_case_to_open)

# print(last_case_to_open)

def open_case():
  case_to_open = None

  while True:
    try:
      case_to_open = int(input("\n\nWhat case do you want to open? "))
      if (1 <= case_to_open <= 26) and case_to_open in cases_dict:
        break
      else:
        print("\nPlease select case between 1 and 26 that is in play.")
    except ValueError:
      print("\nInvalid. Please choose a case number from the above\n")

  slow_print(f"\n\nYou selected {bcolors.CYAN}Case Number {case_to_open}{bcolors.ENDC}. Case Number {case_to_open} had:")
  time.sleep(random.uniform(1.0, 2.3))

  if(cases_dict[case_to_open] == 0.01):
    slower_print(f"\n\n{bcolors.YELLOW}{locale.currency(cases_dict[case_to_open], grouping=True)}{bcolors.ENDC}")
  else:
    slower_print(f"\n\n{bcolors.YELLOW}{locale.currency(cases_dict[case_to_open], grouping=True)[:-3]}{bcolors.ENDC}")

  del cases_dict[case_to_open]
  del cases_dict_copy[case_to_open]

def show_remaining_cases():
  slow_print(f"\n\nThe cases remaining are: \n\n")
  print(*list(cases_dict.keys()))

def show_remaining_dollar_amounts():
  slow_print(f"\n\nThe dollar amounts still in play are: \n\n")
  dollar_amounts = sorted(list(cases_dict_copy.values()))
  formatted_dollar_amounts = [f"{bcolors.YELLOW}{locale.currency(_, grouping=True)[:-3]}{bcolors.ENDC}" for _ in dollar_amounts[1:]]
  formatted_dollar_amounts.insert(0, f"{bcolors.YELLOW}{locale.currency(dollar_amounts[0], grouping=True)}{bcolors.ENDC}")
  print(*formatted_dollar_amounts, sep=" | ")

def calculate_expected_value(d: dict):
  values = d.values()
  expected_value = mean(values)
  return expected_value

def dynamic_offer_calculator():
  activator = random.randint(0, 4)

  if activator == 0:
    x = random.uniform(0.11, 0.20)
  else:
    x = random.uniform(0.05, 0.10)

  return round(x, 3)

def banker_offer():
  slow_print("\n☏") 
  slow_print("\nThe Banker's calling and they've made you an offer.")
  slow_print("\nThe Banker's offer is: ")

  global ev_offer_ratio
  offer = round((calculate_expected_value(cases_dict_copy) * ev_offer_ratio), 2)
  ev_offer_ratio += dynamic_offer_calculator()

  slower_print(f"\n\n{bcolors.GREEN}{locale.currency(offer, grouping=True)[:-3]}{bcolors.ENDC}")

def round_1():
  num_cases_to_open = 5
  while num_cases_to_open >= 1:
    open_case()
    show_remaining_cases()
    show_remaining_dollar_amounts()
    
    if num_cases_to_open == 1:
      slow_print("\nFinal case to open in this round.")
      open_case()
      show_remaining_cases()
      show_remaining_dollar_amounts()
      banker_offer()

    num_cases_to_open -= 1

round_1()

## TODO: implement deal or no deal logic
