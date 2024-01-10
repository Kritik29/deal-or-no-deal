## Kritik Kaushal
## Last Updated: Jan 10, 2024

import random
import time
import sys
import locale
from statistics import mean

# set the locale for printing strings with currency format
locale.setlocale(locale.LC_ALL, '')

# colors class for printing in color on Windows terminal
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

# expected value to banker offer ratio, used to calculate banker's offer
# selected 0.35 based on data collected from the actual TV show
ev_offer_ratio = 0.35
cases_to_open = 6

# functions to print text slowly, adds suspense to the game
def slow_print(s):
  for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.04)

def slower_print(s):
  for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.25)

# given an empty dict, populate each case from 1-26 with a random dollar amount
# from the array above
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
USER_SELECTION = int
last_case_to_open = {}

def initial_sequence(user_case):
  slow_print(f'\n\n{bcolors.HEADER}WELCOME TO DEAL OR NO DEAL!{bcolors.ENDC}\n\nPick one of the 26 cases below.\n\n')
  print(*list(cases_dict.keys()))

  # input validation for user case selection
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
  user_case = {USER_SELECTION: cases_dict.get(USER_SELECTION)}
  del cases_dict[USER_SELECTION]
  time.sleep(1)
  slow_print(f"{bcolors.YELLOW}Let's play {bcolors.BOLD}Deal or No Deal!{bcolors.ENDC}{bcolors.ENDC}\n")
  return user_case

# user case will be the last to open
last_case_to_open = initial_sequence(last_case_to_open)

# generic function to open a case
def open_case():
  case_to_open = None

  # user input validation
  while True:
    try:
      case_to_open = int(input("\n\nWhich case do you want to open? "))
      if (1 <= case_to_open <= 26) and case_to_open in cases_dict:
        break
      else:
        print("\nPlease select case between 1 and 26 that is in play.")
    except ValueError:
      print("\nInvalid. Please choose a case number from the above\n")

  slow_print(f"\n\nYou selected {bcolors.CYAN}Case Number {case_to_open}{bcolors.ENDC}. Case Number {case_to_open} had:")
  time.sleep(random.uniform(1.0, 2.3))

  # handling printing of $0.01
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

# based on the TV show, the banker's offer follows a pattern, based on a ratio calculated 
# using the expected value of the dollar amounts in play

# this function dynamically updates the ratio to make the offers feel more "random" and banker-like
def dynamic_ratio_offset_calculator():
  activator = random.randint(0, 2)

  # there is a 1/3 chance the activator == 0. if the activator is 0,
  # the ratio goes up by a random amount between 11% and 20%
  if activator == 0:
    x = random.uniform(0.11, 0.20)
  else:
    x = random.uniform(0.05, 0.10)

  return round(x, 3)

def banker_offer():
  slow_print("\n☏") 
  slow_print("\nThe Banker's calling and they've made you an offer.")
  slow_print("\nThe Banker's offer is: ")

  # based on the current expected value-to-offer ratio, calculate a deal amount
  global ev_offer_ratio
  offer = round((calculate_expected_value(cases_dict_copy) * ev_offer_ratio), 2)
  # update the expected value-to-offer ratio
  ev_offer_ratio += dynamic_ratio_offset_calculator()

  slower_print(f"\n\n{bcolors.GREEN}{locale.currency(offer, grouping=True)[:-3]}{bcolors.ENDC}")

# ask user if they want to cash out their case
def deal_or_no_deal() -> int:
  slow_print("\n\nNow, the question is.....")
  slower_print(f"\n\n{bcolors.YELLOW}{bcolors.BOLD}Deal or No Deal? {bcolors.ENDC}{bcolors.ENDC}")

  user_deal_choice = ""

  # user input validation
  while True:
    user_deal_choice = str(input(""))
    if user_deal_choice.replace(" ", "").lower() in {"deal", "nodeal"}:
      break
    else:
      print("\n\nPlease type either 'deal' or 'no deal'.\n\n")

  if user_deal_choice.lower().replace(" ", "") == "deal":
    return 1
  else:
    return 0

# this function's input is the number of cases to open
# this is a generic function for the game rounds
def game_round(n):
  if n > 1:
    slow_print(f"\n\nIn this round, you will open {n} cases.")
    num_cases_to_open = n-1
    # for a given round, keep opening cases until user opens last case for that round
    while num_cases_to_open >= 1:
      open_case()
      show_remaining_cases()
      show_remaining_dollar_amounts()
      
      # banker makes an offer after opening the final case in the round
      if num_cases_to_open == 1:
        slow_print("\nFinal case to open in this round.")
        open_case()
        show_remaining_cases()
        show_remaining_dollar_amounts()
        banker_offer()

      num_cases_to_open -= 1

  if n == 1:
    slow_print(f"\n\nIn this round, you will open {n} case.")
    open_case()
    show_remaining_cases()
    show_remaining_dollar_amounts()
    banker_offer()

# main game loop

# for rounds with more than 2 cases to open, follow this structure
while cases_to_open >= 2:
  game_round(cases_to_open)
  if deal_or_no_deal() == 1:
    slow_print(f"\n\n{bcolors.BOLD}{bcolors.GREEN}Congrats on your winnings!{bcolors.ENDC}, and thanks for playing!{bcolors.ENDC}")
    break
  else:
    cases_to_open -= 1

# for rounds where only 1 case is opened at a time, follow this structure
while cases_to_open == 1:
  game_round(cases_to_open)
  if deal_or_no_deal() == 1:
    slow_print(f"\n\n{bcolors.BOLD}{bcolors.GREEN}Congrats on your winnings!{bcolors.ENDC}, and thanks for playing!{bcolors.ENDC}")
    break
  # if only 1 case is left on the board, the user can either open their case in hand or swap with the case in play
  if len(cases_dict) == 1:
    slow_print("\n\nNow you have a very important decision to make.")
    slow_print("\nWould you like to open your case now OR swap with the case still left in play (open or swap)? ")

    user_swap_choice = ""
    # user input validation
    while True:
      user_swap_choice = str(input(""))
      if user_swap_choice.replace(" ", "").lower() in {"open", "swap"}:
        break
      else:
        print("\n\nPlease type either 'open' or 'swap'.\n\n")
    
    if user_swap_choice.replace(" ", "").lower() in {"open"}:
      slow_print("\n\nWe will now open the case you selected.")
      slow_print(f"\nYour case, {bcolors.CYAN}case number {next(iter(last_case_to_open))}{bcolors.ENDC} has...")
      slower_print(f"\n\n{bcolors.YELLOW}{locale.currency((last_case_to_open[next(iter(last_case_to_open))]), grouping=True)[:-3]}{bcolors.ENDC}")
      slow_print(f"\n\n{bcolors.BOLD}{bcolors.GREEN}Congrats on your winnings!{bcolors.ENDC}, and thanks for playing!{bcolors.ENDC}")
    else:
      slow_print("\n\nYou chose to swap your case with the one currently in play.")
      slow_print(f"\n\nThe case currently in play is {bcolors.CYAN}case number {next(iter(cases_dict))}{bcolors.ENDC}. This case has...")
      slower_print(f"\n\n{bcolors.YELLOW}{locale.currency((cases_dict[next(iter(cases_dict))]), grouping=True)[:-3]}{bcolors.ENDC}")
      slow_print(f"\n\n{bcolors.BOLD}{bcolors.GREEN}Congrats on your winnings!{bcolors.ENDC}, and thanks for playing!{bcolors.ENDC}")
    break

## TODO: turn it into an exe
## TODO: write README
