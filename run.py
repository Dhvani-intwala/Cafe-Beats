"""
Import gspread to access and update data in our spreadsheet
"""
import os
from time import sleep
from datetime import datetime, timedelta
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

# Global variables
user_data = []  # Contains user name, user order id, order type and address
order_data = []  # Contains item number, item name, item price
# Contains item number, item name, item price for specific user order id
global_individual_user_data = []

WELCOME_MSG = """
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
[R] - To remove an item
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
            # print(colored("\nThanks for visiting us!\n", "yellow"))
            clear_screen()
            thank_you()
            break
        else:
            print(colored("Invaild input.Enter Y to start.\n", "red"))


def take_user_name_input():
    """
    Function to take name input.
    """
    clear_screen()
    user_name = input("Enter your name:\n")
    if user_name == "":
        print(colored("\n***Name is required***\n", "red"))
        return take_user_name_input()
    clear_screen()
    print(pyfiglet.figlet_format(f'Hi {user_name}', font="standard"))
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
    clear_screen()
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
    order_type = take_order_type_input()
    user_data.append(order_type)
    print(
        colored(f"Selected delivery type is: {order_type}\n", "yellow")
    )
    sleep(2)
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


def display_menu_list(is_useraction_required=0, food_item_selected=-1):
    """
    Fetches the cafe beats menu from google sheets worksheet 'menu' and
    displays it in formatted table form to user.
    """
    display_menu = MENU.get_all_values()
    print(tabulate(display_menu))
    print(DISPLAY_MENU_MSG)
    if (is_useraction_required == 0):
        user_action()
    else:
        print(
            colored(
                f'\nYou ordered Item {display_menu[food_item_selected + 1][0]}\
                                     {display_menu[food_item_selected + 1][1]}'
                f' priced at{display_menu[food_item_selected + 1][2]}',
                "green"))


def user_action():
    """
    Display user action after getting the menu items.
    """
    item_number = 0
    while True:
        food_item = input("Please enter a valid input: ")
        if food_item.isdigit() and int(food_item) > 0:
            try:
                food_item = int(food_item)
                clear_screen()
                order_data.append(food_item)
                display_menu_list(1, food_item)
                item_number += 1
            except IndexError:
                clear_screen()
                print(colored(
                    f'\nIm sorry Item "{food_item + 1}" does not exist.'
                    ' Please enter a valid item number', 'yellow'))
            if (food_item >= 1 and food_item <= 20):
                item_number = food_item
                add_item(item_number)
            else:
                print(
                    colored(
                        "\n**Selected item doesn't exist in the menu**.\n",
                        "red"
                    )
                )
                order_data.pop()
                continue
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
        elif food_item.capitalize() == "R":
            if len(order_data) == 0:
                clear_screen()
                print(display_menu_list)
                print(colored('\nNothing to remove, basket'
                              ' is empty', 'yellow'))
            else:
                remove_item()
        elif food_item.capitalize() == "Q":
            # when user enter 'Q' then open thank you message.
            print(colored("\nThanks for visiting us!\n", "yellow"))
            sleep(2)
            clear_screen()
            break
        elif food_item.capitalize() == "C":
            local_user_data = get_individual_user_data()
            # Evaluating order list whether empty or not
            if bool(local_user_data):
                append_order_status(food_item)
                print(colored("\nLoading reciept....", "green"))
                sleep(2)
                clear_screen()
                complete_order()
                break
        else:
            print(colored("\nInvalid input\n", "red"))


def add_item(item_number):
    """
    Appends user data, order data and order status in google sheets worksheet.
    """
    cell = MENU.find(str(item_number))
    order_row = user_data + MENU.row_values(cell.row) + ["Processing"]
    # print(user_data)
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
                row.pop()
                individual_user_data.append(row)
    sleep(2)
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
        if i:
            print(colored("----------Order Preview----------\n", "yellow"))
            # print(local_user_data)
            tabulate_data(local_user_data)
            # print(local_user_data)
            i = False
        preview_option = input(colored(
                '\nPlease press [Y] to return to the order page.\n', 'yellow'))
        preview_option = preview_option.capitalize()
        if preview_option == 'Y':
            clear_screen()
            display_menu_list(1)
            return
        else:
            clear_screen()
            print(
                colored
                (
                    '\nPlease enter "Y"'' to return to order screen.',
                    'yellow'))
            return preview_option

        if preview_option.isdigit():
            preview_option = int(preview_option)
        if preview_option.isdigit():
            preview_option = int(preview_option)
            if (preview_option) >= 1 and (preview_option) <= MAX_MENU_ITEM:
                local_user_data = get_individual_user_data()
                clear_screen()
                tabulate_data(local_user_data)
            else:
                print(colored("\nInvalid item number\n", "red"))


def remove_item():
    """
    Function to pop the last item from the order list.
    """
    clear_screen()
    # print(display_menu_list)
    # removed_item = order_data[-1]
# remove_str = f'\nYou have removed {0}from your order'.format(removed_item)
    # print(colored(remove_str, 'yellow'))
    # order_data.pop()
    # clear_screen()
    # display_menu_list(1)
    worksheet = ORDER_LIST.get_all_values()
    for i, row in enumerate(worksheet):
        for j, item in enumerate(row):
            if (item == str(user_data[0])):
                print(row[j+5], order_data)
                if (row[j+5] == str(order_data[1])):
                    print("success")
                    ORDER_LIST.delete_row(i)
                    break
    removed_item = order_data[-1]
    remove_str = f'\nYou have removed {0} from your order'.format(removed_item)
    print(colored(remove_str, 'yellow'))
    order_data.pop()
    sleep(3)
    clear_screen()
    display_menu_list(1)
     

def complete_order():
    """
    Function to complete order and pass arguments to
    Order class and its functions
    """
    # Display date & time for order receipt
    order_time = datetime.now()
    # delivery_time = order_time + timedelta(hours=1)
    # pickup_time = order_time + timedelta(minutes=30)
    order_time = order_time.strftime("%H:%M:%S  %d-%m-%Y")
    clear_screen()
    order_complete = True
    while complete_order():
        print(colored('Are you ready to complete your order?\n', 'yellow'))
        print('[Y] - Yes\n[N] - No\n')
        order_complete = input('Please enter a vaild input:').strip()
        order_complete = order_complete.capitalize()
        if order_complete == 'Y':
            clear_screen()
            print_receipt()
            break
        elif order_complete == 'N':
            clear_screen()
            display_menu_list()
            order_complete = False
            return
        else:
            clear_screen()
            print(
                colored(f'Im sorry "{order_complete}" is an'
                        ' invalid input\n', 'yellow'))
        while True:
            finish = input(
                colored(
                        "Please press 'Q' to quit. \n", 'green')).strip()
        finish = finish.capitalize()
        if finish == 'Q':
            clear_screen()
            thank_you()
            break
        else:
            print(
                colored(f'Im sorry but {finish} is'
                        ' an invalid input.', 'yellow'))
        break


def print_receipt():
    """
    Function to print a formatted order receipt to the command line.
    """
    print()
    # Display user data
    print(colored("****Your Reciept****\n", "yellow"))
    print(f"User name: {user_data[0]}")
    print(f"Order Id: {user_data[1]}")
    print(f"Order type: {user_data[2]}")
    print(f"Address: {user_data[3]}")
    print()
    print('************** Order Summary **************\n')
    format_order_list()
    print()
    total_order_cost()
    delivery_time()


def delivery_time():
    """
    Function to calculate current time and delivery time.
    """
    current_time = datetime.now()
    order_ready_time = current_time + timedelta(hours=1, minutes=15)
    order_ready_time = order_ready_time.strftime("%H:%M:%S %Y-%m-%d")
    print()


def total_order_cost():
    """
    Function to calculate total order cost as per current order list.
    """


def format_order_list():
    """
    Function to print formatted list of current order
    to the command line.
    """


def thank_you():
    """
    Function to display thank you message
    """
    title = 'Thanks for Visiting!'
    print(pyfiglet.figlet_format(title))
    print('\nCreated by Dhvani Intwala'
          '\n\nGitHub -'
          'https://github.com/Dhvani-intwala'
          '\n\nLinkedIn -'
          'https://www.linkedin.com/in/dhvani-intwala-2716bb235/\n\n')


if __name__ == "__main__":
    welcome()
