import random

DOLLAR_AMOUNTS = [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750,
                  1000, 5000, 10000, 25000, 50000, 75000, 100000,
                  200000, 300000, 400000, 500000, 750000, 1000000]

def populateCases(d):
  # dictionary to store all the briefcases with dollar amounts in them
  cases = {}
  local_dollar_amounts = list(d)

  # store unique dollar amounts in the dict (no duplicate dollar amounts)
  for _ in range(1, 27):
    cases[_] = random.choice(local_dollar_amounts)
    local_dollar_amounts.remove(cases[_])
  
  return cases

print(populateCases(DOLLAR_AMOUNTS))

print(populateCases(DOLLAR_AMOUNTS).keys())