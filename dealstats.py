import math
import numpy
import pandas
import matplotlib

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

def game_sim():
    