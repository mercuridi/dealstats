import random
import math
import numpy
import pandas
import matplotlib

def get_money(year = 2023):
    money = {
        2023: [
                  0.01,
                  0.10,
                  0.50,
                  1.00,
                  5.00,
                 10.00,
                 50.00,
                100.00,
                250.00,
                500.00,
                750.00,
              1_000.00,
              2_000.00,
              3_000.00,
              4_000.00,
              5_000.00,
              7_500.00,
             10_000.00,
             25_000.00,
             50_000.00,
             75_000.00,
            100_000.00
        ]
    }
    return money[year]

def get_ruleset(year):
    match(year):
        case 2023:
            return (
                get_money(year), # game_money
                get_money(year), # orig_money
                3, # round_length
            )

def game_sim(ruleset = 2023):
    # because computer, no need to implement a "pick"
    # there are 1,124,000,727,777,607,680,000 different permutations 
    # of 22 values - cannot precalculate
    
    # is it faster to:
    # 1. shuffle the list and iterate through it until an endpoint is reached?
    #       ^ some wasted work when early exit
    # 2. pick random smaller ints on demand and never shuffle the list?
    #       ^ no wasted work but maybe difficult logic on re-picked numbers
    # option 2 seems much faster
    
    # TODO when multithreading, orig_money never changes
    # ^ this might be better as a global variable?
    (
        game_money,
        orig_money,
        round_length
    ) = get_ruleset(ruleset)

    n = len(game_money)
    round_num = 1
    deal = False
    winnings = 0
    recent_offer = 0

    while game_money and not deal:
        pick = get_next(game_money)
        if (round_num % round_length) == 0:
            recent_offer = get_offer(game_money, orig_money, round_num)
    
    if deal:
        winnings = recent_offer
    else:
        winnings = pick
    
    return winnings

def rms(lst): 
    return math.sqrt((sum([val**2 for val in lst]) / len(lst)))
    
def get_offer(game_money, orig_money, round_num):
    # according to:
    # https://www.denofgeek.com/tv/deal-or-no-deal-investigating-gameshow-maths/
    # the banker uses a root mean square * ~0.9
    # the deals get better the further in you are with a better result
    # we can simulate this
    
    root_mean_square = rms(game_money)
    # TODO weighting for luck and game length
    return root_mean_square * random.uniform(0.85, 0.95)

def get_next(game_money):
    # TODO can be improved, quite slow
    # consider new data structure
    # problem is O(n) on del for lists
    pick_index = random.randint(0, len(game_money)-1)
    pick = game_money[pick_index]
    del game_money[pick_index]
    return pick

def fmt_cash(cash):
    return "£{:,.2f}".format(cash)

def mean(lst):
    return sum(lst) / len(lst)

def main():
    # 10,000,000 trials with no deal: £12,920.36 EV
    print(mean(get_money()))

if __name__ == "__main__":
    main()