import traceback
from typing import List
import inquirer
from termcolor import colored
from texttable import Texttable


class PurchaseItem:
    def __init__(self, option):
        self.price = option.p
        self.name = str(option)


def get_total_order_amount(order: List[PurchaseItem]) -> float:
    """
    Calculate the total cost of all items in the order.
    """
    total_amount = sum(item.price for item in order)
    return total_amount


def get_service_charge(order: List[PurchaseItem]) -> float:
    """
    Calculate the service charge based on the total order amount.
    Service charge increases by 1% for every Rs. 100 spent, capped at 20%.
    """
    total_amount = get_total_order_amount(order)
    service_charge_rate = min(20, total_amount // 100)
    service_charge = total_amount * (service_charge_rate / 100)
    return service_charge


class Option:
    def __init__(self, n=None, p=None):
        self.p = float(p) if p is not None else 0.0
        self.n = n

    def __str__(self):
        return f"{self.n} Rs. {self.p}"


MCDONALDS_FOOD_OPTIONS = [
    Option(n="Veg Burger", p=115.00),
    Option(n="Veg Wrap", p=130.00),
    Option(n="Veg Happy Meal", p=215.00),
    Option(n="Chicken Burger", p=175.00),
    Option(n="Chicken Wrap", p=195.00),
    Option(n="No, that's all", p=0.00),
]

MCDONALDS_BEVERAGES_OPTIONS = [
    Option(n="Sprite (M)", p=115.00),
    Option(n="Sprite (L)", p=130.00),
    Option(n="Mango Smoothie", p=215.00),
    Option(n="Chocolate Smoothie", p=175.00),
    Option(n="Chocolate Smoothie w/ Icecream", p=195.00),
    Option(n="No, that's all", p=0.00),
]


def get_option_from_result(result, options):
    for option in options:
        if str(option) == result:
            return option
    raise ValueError("Invalid option selected.")


def print_order(order):
    try:
        total_amount = get_total_order_amount(order)
        service_charge = get_service_charge(order)
        final_amount = total_amount + service_charge

        table = Texttable()
        table.add_row(["Item", "Price (Rs.)"])
        for item in order:
            table.add_row([item.name, f"{item.price:.2f}"])
        table.add_row(["Order Amount", f"{total_amount:.2f}"])
        table.add_row(["Service Charge", f"{service_charge:.2f}"])
        table.add_row(["Final Amount", f"{final_amount:.2f}"])

        print("\n" + colored("Final Order", "green", attrs=["bold"]))
        print(table.draw())

    except Exception as e:
        traceback.print_exc()
        print("Error occurred while generating bill.")


def main():
    order = []

    print(colored("Welcome to McDonalds on your shell :)", "blue", attrs=["bold"]))
    print(colored("Here you can place your order", "blue"))
    print(colored("And then we will show you your bill", "blue"))

    food_choices = [str(option) for option in MCDONALDS_FOOD_OPTIONS]
    while True:
        food_prompt = inquirer.List('food', message="Select a food item (Enter 'No, that's all' to finish)", choices=food_choices)
        food_result = inquirer.prompt([food_prompt])['food']
        if food_result == "No, that's all Rs. 0.0":
            break
        option = get_option_from_result(food_result, MCDONALDS_FOOD_OPTIONS)
        order.append(PurchaseItem(option))
        print(colored(f"{food_result} is added to your order", "green"))

    beverage_choices = [str(option) for option in MCDONALDS_BEVERAGES_OPTIONS]
    while True:
        beverage_prompt = inquirer.List('beverage', message="Select a beverage (Enter 'No, that's all' to finish)", choices=beverage_choices)
        beverage_result = inquirer.prompt([beverage_prompt])['beverage']
        if beverage_result == "No, that's all Rs. 0.0":
            break
        option = get_option_from_result(beverage_result, MCDONALDS_BEVERAGES_OPTIONS)
        order.append(PurchaseItem(option))
        print(colored(f"{beverage_result} is added to your order", "green"))

    print_order(order)


if __name__ == "__main__":
    main()
