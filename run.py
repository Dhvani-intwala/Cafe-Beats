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
SHEET = GSPREAD_CLIENT.open('Cafe_Beats')

# To acces the worksheets in google sheets
MENU = SHEET.worksheet("menu")
ORDER_LIST = SHEET.worksheet("order_list")

MAX_MENU_ITEM = len(MENU.get_all_values()) - 2

# Order receipt constants
DELIVERY_CHARGE = 5
DELIVERY_TIME = 30
PICKUP_TIME = 15

# Global variables
user_data = []  # Contains user name, user order id, order type and address
order_data = []  # Contains item number, item name, item price
# Contains item number, item name, item price for specific user order id
global_individual_user_data = []

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
PREVIEW_TEXT = """
[R] - To remove an item
[A] - To add an item
[C] - To confirm order
[Q] - To quit
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
        start_order = input("\nPlease enter a valid input:\n")
        if start_order.capitalize() == "Y":
            get_user_details()
            break
        elif start_order.capitalize() == "N":
            print(colored("\nThanks for visiting us!\n", "yellow"))
            break
        else:
            print(colored("Invaild input.Enter Y to start.\n", "red"))


def take_user_name_input():
    """
    Function to take name input.
    """
    user_name = input("Enter your name:\n")
    if user_name == "":
        print(colored("\n***Name is required***\n", "red"))
        return take_user_name_input()
    return user_name


def take_order_type_input():
    """
    Function to take order type input.
    """
    order_type = input(ORDER_OPTION_MSG).capitalize()
    if order_type not in ("D", "P"):
        print(colored("\nInvalid delivery type. Try again.\n", "red"))
        return take_order_type_input()
    if order_type == "D":
        return "Home delivery"
    elif order_type == "P":
        return "Pickup"


def take_address_input():
    """
    Function to take address input.
    """
    address = input("Enter your Address:\n")
    if address == "":
        print(
            colored("\n***Enter your full address.***\n", "red")
        )
        return take_address_input()
    return address


def get_user_details():
    """
    Gets user details like user name, order type, address and
    appends them in user data list along with user order Id
    """
    user_data.clear()
    user_name = take_user_name_input()
    user_data.append(user_name)
    user_order_id = random.getrandbits(16)
    user_data.append(user_order_id)
    print(colored(f"\nWelcome {user_name}!\n", "yellow"))
    order_type = take_order_type_input()
    user_data.append(order_type)
    print(
        colored(f"Selected delivery type is: {order_type}\n", "yellow")
    )
    if order_type == "Home delivery":
        address = take_address_input()
        print(
                colored
                (f"\nYour provided address is: {address}\n", "yellow")
            )
        user_data.append(address)
    elif order_type == "Pickup":
        user_data.append("The Cafe Beats")
    print(colored("\nLoading menu...", "green"))
    sleep(2)
    clear_screen()
    display_menu_list()


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
            # Validates and adds the item to the order list
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
            # when user enter 'P' without adding an item
            # item_number is used to display order list empty message
            if item_number == 0:
                print(colored(
                    "Your order list is empty. please add an item.\n",
                    "red")
                )
            else:
                print(colored("\nLoading preview page....", "green"))
                sleep(2)
                clear_screen()
                preview_order()
                break
        elif food_item.capitalize() == "Q":
            # when user enter 'Q' then open thank you message.
            print(colored("\nThanks for visiting us!\n", "yellow"))
            sleep(2)
            clear_screen()
            break


def add_item(item_number):
    """
    Appends user data, order data and order status in google sheets worksheet.
    """
    cell = MENU.find(str(item_number))
    order_row = user_data + MENU.row_values(cell.row) + ["Processing"]
    ORDER_LIST.append_row(order_row)


def get_individual_user_data():
    """
    Get individual user's order data from worksheet
    'order_list' with unique order id
    """
    individual_user_data = []
    for row in ORDER_LIST.get_all_values():
        for item in row:
            if item == str(user_data[1]):
                row.pop(7)  # to remove order status
                del row[0:4]  # to remove user data
                individual_user_data.append(row)
    return individual_user_data


def append_order_status(order_request):
    """
    Update order status in worksheet 'order_list'
    when user Confirms / Cancels the order
    """
    cells_list = ORDER_LIST.findall(str(user_data[1]))
    for cell in cells_list:
        # Locating cell for order status corresponding to order id
        confirmation_cell = "H" + str(cell.row)
        if order_request.capitalize() == "C":
            ORDER_LIST.update(confirmation_cell, "Confirmed")
        elif order_request.capitalize() == "Q":
            ORDER_LIST.update(confirmation_cell, "Cancelled")


def preview_order():
    """
    Previews user's order list
    """
    local_user_data = get_individual_user_data()
    i = True
    while True:
        # Tabulate order list when function is called first time
        if i:
            print(colored("----------Order Preview----------\n", "yellow"))
            tabulate_data(local_user_data)
            print(PREVIEW_TEXT)
            i = False
        preview_option = input("Please enter a valid input: ")
        # Evaluating user input for digit and character
        if preview_option.isdigit():
            preview_option = int(preview_option)


def remove_item():
    """
    """


welcome()