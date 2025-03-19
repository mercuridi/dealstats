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
            print(f"The Banker gives you {fmt_cash(calc_offer(boxes, reserved_box) / 4)} for your trouble.")
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

def reveal_box(box):
    print(f"You chose box #{box[0]}.")
    time.sleep(DELAY)
    print("Let's see what's in it...")
    time.sleep(DELAY)
    print(f"Box {box[0]}: {fmt_cash(box[1])}")
    time.sleep(DELAY)

def play_round(boxes, reserved_box, round_num):
    print(f"Welcome to round {round_num}.")
    boxes, pick = get_pick(boxes, reserved_box)
    reveal_box(pick)
    boxes, pick = get_pick(boxes, reserved_box)
    reveal_box(pick)
    return boxes

def banker_offer(boxes, reserved_box):
    print("The phone is ringing...")
    time.sleep(DELAY)
    print("The Banker wants to make you an offer.")
    offer = calc_offer(boxes, reserved_box)
    time.sleep(DELAY)
    while True:
        choice = opt_val_choice(
            boxes,
            reserved_box,
            ("deal", "yes", "true", "no deal", "no", "false"), 
            f"The Banker is offering you {fmt_cash(offer)} to walk away now." +
            "\nDeal or No Deal?"
            )
        if choice in ("deal", "yes", "true"):
            return True, offer
        elif choice in ("no deal", "no", "false"):
            return False, 0
            
def calc_offer(boxes, reserved_box):
    return round(
        ((sum(boxes.values()) + reserved_box[0]) / len(boxes))
        * random.uniform(0.5, 1.1), 2)

def main():
    print("Welcome to Dealstats.")
    print("Type 'help' at any time for assistance.")
    boxes = make_boxes(get_money(2023))
    boxes, reserved_box = reserve_box(boxes)
    print(f"Your reserved box is #{reserved_box[0]}.")
    deal = False
    round_num = 1
    value = 0
    while (len(boxes) != 1) and not deal:
        print()
        print(f"Round {(round_num // 3) + 1} | Choice #{round_num}")
        boxes, pick = get_pick(boxes, reserved_box)
        reveal_box(pick)
        if (round_num % 3) == 0:
            deal, value = banker_offer(boxes, reserved_box)
            if deal:
                print("Congratulations! You took the Banker's offer.")
                time.sleep(DELAY)
                break
            else:
                print("No deal! Play on!")
                time.sleep(DELAY)
        round_num += 1

    if not deal:
        value = reserved_box[1]
        print("Two boxes remain. Yours and the final box to choose.")
        time.sleep(DELAY)
        print("You have played all the way to the end of the game.")
        time.sleep(DELAY)
        print("The value in the final box is...")
        time.sleep(DELAY)
        (final_num, final_val) = boxes.items()
        print(f"#{final_num}: {fmt_cash(final_val)}!")
        time.sleep(DELAY)
        print(f"The value in your box is {fmt_cash(value)}!")

    print(f"You're walking away with {fmt_cash(value)}!")
    print("Please play again!")
        
    

if __name__ == "__main__":
    main()