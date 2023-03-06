"""
Import gspread to access and update data in our spreadsheet
"""
import os
from time import sleep
import random
import gspread
import pyfiglet
import pyfiglet.fonts
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from termcolor import colored

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# To open google sheets after authentication
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Cafe Beats')

# To acces the worksheets in google sheets
MENU = SHEET.worksheet("menu")
ORDER_LIST = SHEET.worksheet("order_list")

MAX_MENU_ITEM = len(MENU.get_all_values()) - 2


# Global variables
user_data = []  # Contains user name, user order id, order type and address

WELCOME_MSG = """
Welcome to The Cafe Beats!
Do you want to start your order now?
[Y] - Yes
[N] - No
"""
ORDER_OPTION_MSG = """
Enter your choice for order type -s
[D] - For Home delivery
[P] - For Pickup:
"""
DISPLAY_MENU_MSG = """
Add item by entering item number.
[P] - To preview your order
[Q] -  To quit
"""


def clear_screen():
    """
    Clears the console
    """
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def tabulate_data(user_info):
    """
    Formats the data in table form
    """
    format_data = tabulate(
        user_info,
        headers=["Item", "Name", "Cost"],
        tablefmt="simple",
        numalign="center",
    )
    print(format_data)


def welcome():
    """
    Function to display home page
    """
    title = "Welcome to The Cafe Beats"
    print(colored(pyfiglet.figlet_format(title, font="standard"), "red"))
    print(colored(WELCOME_MSG, "green"))
    while True:
        start_order = input("\nEnter your choice:\n")
        if start_order.capitalize() == "Y":
            get_user_details()
            break
        elif start_order.capitalize() == "N":
            print(colored("\nThanks for visiting us!\n", "yellow"))
            break
        else:
            print(colored("Invaild input.Enter Y to start.\n", "red"))


def get_user_details():
    """
    Gets user details like user name, order type, address and
    appends them in user data list along with user order Id
    """
    user_data.clear()
    user_name = input("Enter your name:\n")
    user_data.append(user_name)
    user_order_id = random.getrandbits(16)
    user_data.append(user_order_id)
    while user_name == "":
        print(colored("\n***Name is required***\n", "red"))
        user_name = input("Enter your name:\n")
    print(colored(f"\nWelcome {user_name}!\n", "yellow"))
    while True:
        delivery_type = input(ORDER_OPTION_MSG).capitalize()
        if delivery_type not in ("D", "P"):
            print(colored("\nInvalid delivery type. Try again.\n", "red"))
            continue
        if delivery_type == "D":
            order_type = "Home delivery"
            user_data.append(order_type)
            print(
                colored(f"Selected delivery type is: {order_type}\n", "yellow")
            )
            address = input("Enter your Address:\n")
            while address == "":
                print(
                    colored("\n***Enter your full address.***\n", "red")
                )
                address = input("Enter your Address:\n")
            print(
                    colored
                    (f"\nYour provided address is: {address}\n", "yellow")
                )
            user_data.append(address)
        elif delivery_type == "P":
            order_type = "Pickup"
            user_data.append(order_type)
            print(
                colored(f"\nSelected delivery type is: {order_type}", "yellow")
                )
            user_data.append("The Cafe Beats")

        print(colored("\nLoading menu...", "green"))
        sleep(2)
        clear_screen()
        display_menu_list()
        break
    else:
        print(colored("\n***Invalid input.***\n", "red"))


def display_menu_list():
    """
    Fetches the cafe beats menu from google sheets worksheet 'menu' and
    displays it in formatted table form to user.
    """
    display_menu = MENU.get_all_values()
    print(tabulate(display_menu))
    print(DISPLAY_MENU_MSG)
    user_action()


def user_action():
    """
    Display user action after getting the menu items.
    """
    item_number = 0
    while True:
        food_item = input("Please enter a valid input: ")
        if food_item.isdigit():
            food_item = int(food_item)
            if food_item >= 1 and food_item <= (MAX_MENU_ITEM):
                item_number = food_item
                add_item(item_number)
                print(
                    colored(
                        "\nSelected item added to your order list.", "yellow"
                    )
                )
            else:
                print(
                    colored(
                        "\n**Selected item doesn't exist in the menu**.\n",
                        "red"
                    )
                )
        elif food_item.capitalize() == "P":
            if item_number == 0:
                print(colored(
                    "Your order list is empty. please add an item.\n",
                    "red")
                )
            else:
                print(colored("\nLoading preview page....", "green"))
                sleep(2)
                clear_screen()
                break
        elif food_item.capitalize() == "Q":
            print(colored("\nThanks for visiting us!\n", "yellow"))
            sleep(2)
            clear_screen()
            break      


def add_item(item_number):
    """
    Appends user data, order data and order status in google sheets worksheet
    """
    cell = MENU.find(str(item_number))
    order_row = user_data + MENU.row_values(cell.row) + ["Processing"]
    ORDER_LIST.append_row(order_row)


welcome()