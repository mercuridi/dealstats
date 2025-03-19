import random
import time

DELAY = 0

def get_money(year: int = 2023):
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

def make_boxes(money: list):
    boxes = {}
    random.shuffle(money)
    for i, val in enumerate(money):
        boxes[i+1] = val
    return boxes

def choose_box(boxes, num):
    return (num, boxes[num])

def fmt_cash(cash):
    return "£{:,.2f}".format(cash)

def show_boxes(boxes):
    print("Here are the boxes still available to choose.")
    print(list(boxes.keys()))

def show_values(boxes, reserved_box):
    print("Here are the values still available in the boxes.")
    vals = list(boxes.values())
    vals.append(reserved_box[1])
    print([fmt_cash(i) for i in sorted(vals)])

def opt_val_choice(boxes, reserved_box, valid_responses, prompter):
    while True:
        print(prompter)
        choice = input("... ").lower()
        if choice in valid_responses:
            return choice
        elif "options" in choice:
            show_boxes(boxes)
        elif "values" in choice:
            show_values(boxes, reserved_box)
        elif "help" in choice:
            print("Type 'options' to see your options again.")
            print("Type 'values' to see the remaining cash values in the boxes.")
            print("Type 'end' to end the game.")
        elif "end" in choice:
            print("You've ended the game.")
            print(f"The Banker gives you {fmt_cash(calc_offer(boxes, reserved_box, random.uniform(0.1, 0.6)) / 4)} for your trouble.")
            print("Goodbye.")
            exit()
        print()

def get_pick(boxes, reserved_box):
    pick = ""
    print("Here are your options: ")
    print(list(boxes.keys()))
    choice = opt_val_choice(
        boxes,
        reserved_box,
        [str(box) for box in boxes.keys()],
        "Please choose a box."
        )
    pick = choose_box(boxes, int(choice))
    del boxes[pick[0]]
    return boxes, pick

def reserve_box(boxes):
    pick = choose_box(boxes, random.randint(1, len(boxes)))
    del boxes[pick[0]]
    return boxes, pick

def reveal_box(picked_box, quartiles):
    (upper_quartile, median, lower_quartile) = quartiles
    print(f"You chose box #{picked_box[0]}.")
    time.sleep(DELAY)
    print("Let's see what's in it...")
    time.sleep(DELAY)
    print(f"Box {picked_box[0]}: {fmt_cash(picked_box[1])}")
    time.sleep(DELAY)
    if picked_box[1] >= upper_quartile:
        print("Ouch...")
    elif picked_box[1] >= median:
        print("Not the best outcome...")
    elif picked_box[1] >= lower_quartile:
        print("Nice one!")
    else:
        print("Great choice!")
    time.sleep(DELAY)

def construct_prompt(offer, last_offer):
    if last_offer:
        return f"The Banker is offering you {fmt_cash(offer)} to walk away now." + \
        f"\nThe Banker's last offer was {fmt_cash(last_offer)}." + \
        "\nDeal or No Deal?"
    else:
        return f"The Banker is offering you {fmt_cash(offer)} to walk away now." + \
        "\nDeal or No Deal?"

def banker_waffle(mult):
    if mult > 1:
        print("BANKER: 'This is a very generous offer.'")
        time.sleep(DELAY*2)
        print("BANKER: 'I advise you take it.")
        time.sleep(DELAY)
    elif mult > 0.7:
        print("BANKER: 'I doubt you'll do much better than this.'")
        time.sleep(DELAY*2)
    else:
        print("BANKER: 'With the skill you've displayed, this is all I can do.'")
        time.sleep(DELAY*2)
        print("BANKER: 'I strongly advise you to take this offer.")
        time.sleep(DELAY)

def banker_offer(boxes, reserved_box, last_offer):
    print()
    print("The phone is ringing...")
    time.sleep(DELAY*2)
    print("The Banker wants to make you an offer.")
    time.sleep(DELAY*2)
    mult = random.uniform(0.4, 1.2)
    banker_waffle(mult)
    offer = calc_offer(boxes, reserved_box, mult)
    time.sleep(DELAY*2)
    prompt = construct_prompt(offer, last_offer)

    while True:
        choice = opt_val_choice(
            boxes,
            reserved_box,
            ("deal", "yes", "true", "no deal", "no", "false"), 
            prompt
            )
        if choice in ("deal", "yes", "true"):
            return True, offer
        elif choice in ("no deal", "no", "false"):
            return False, offer
            
def calc_average(boxes, reserved_box):
    return (sum(boxes.values()) + reserved_box[0]) / len(boxes)

def calc_offer(boxes, reserved_box, mult):
    return round(calc_average(boxes, reserved_box) * mult, 2)

def get_quartiles(boxes, reserved_box):
    vals = list(boxes.values())
    vals.append(reserved_box[1])
    vals.sort()
    n = len(vals)
    # special case if only 2 boxes left
    if len(boxes) == 2:
        return(
            vals[2],
            vals[1],
            vals[1]
        )
    return (
        vals[round((n//2 * 1.5))],
        vals[round((n//2 * 1.0))],
        vals[round((n//2 * 0.5))]
)

def suspense(boxes, reserved_box, final_offer):
    winnings = reserved_box[1]
    (final_num, final_val) = list(boxes.items())[0]
    two_vals = [winnings, final_val]
    random.shuffle(two_vals)
    
    print("You have played all the way to the end of the game.")
    time.sleep(DELAY)
    print("Two boxes remain. Yours and the final box to choose.")
    time.sleep(DELAY)
    print("\nThese two boxes contain the final two values:")
    time.sleep(DELAY)
    print(f"{fmt_cash(two_vals[0])}...")
    time.sleep(DELAY)
    print(f"and {fmt_cash(two_vals[1])}.")
    time.sleep(DELAY)
    print(f"\nThe Banker's final offer to you was {fmt_cash(final_offer)}...")
    time.sleep(DELAY*2)
    print(f"\nThe value in the final box - box {final_num} is...")
    time.sleep(DELAY*3)
    print(f"{fmt_cash(final_val)}!")
    time.sleep(DELAY*3)
    print(f"The value in your box is {fmt_cash(winnings)}!")
    time.sleep(DELAY*3)
    
    if final_val > winnings:
        print("Oh no!")
    else:
        print("Nice!")
    time.sleep(DELAY*2)
    
    print()
    if winnings < final_offer:
        print("This time, the Banker beat you...")
    else:
        print("Congratulations! You have beaten the Banker!")
    time.sleep(DELAY*3)

def print_round(round_num):
    print()
    print(f"Round {(round_num // 3) + 1} | Choice #{round_num}")

def game():
    print("Welcome to Dealgame.")
    print("Type 'help' at any time for assistance.")
    boxes = make_boxes(get_money(2023))
    boxes, reserved_box = reserve_box(boxes)
    print(f"Your reserved box is #{reserved_box[0]}.")

    deal = False
    round_num = 1
    last_offer = 0
    winnings = 0
    all_offers = []

    while (len(boxes) != 1) and not deal:
        print_round(round_num)

        quartiles = get_quartiles(boxes, reserved_box)
        boxes, pick = get_pick(boxes, reserved_box)
        reveal_box(pick, quartiles)

        if (round_num % 3) == 0:
            deal, last_offer = banker_offer(boxes, reserved_box, last_offer)
            all_offers.append(last_offer)
            if deal:
                print("Congratulations! You took the Banker's offer.")
                winnings = last_offer
                break
            else:
                print("No deal! Play on!")
                time.sleep(DELAY)

        round_num += 1

    if not deal:
        winnings = reserved_box[1]
        suspense(boxes, reserved_box, last_offer)
    else:
        time.sleep(DELAY)
        print(f"You're walking away with {fmt_cash(winnings)}!")
        time.sleep(DELAY)
    
    print("\nHere are all the offers the banker made you:")
    print([fmt_cash(offer) for offer in all_offers])
    print()
    
def main():
    choice = True
    while choice:
        game()
        while True:
            print()
            print("Would you like to play again? ")
            choice = input("... ").lower()
            if choice in ("yes"):
                print()
                break
            if choice in ("no"):
                print("Thank you for playing!")
                exit()

if __name__ == "__main__":
    main()