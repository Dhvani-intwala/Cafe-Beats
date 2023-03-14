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
    clear_screen()
    return print(pyfiglet.figlet_format(f'Hi {user_name}', font="standard"))


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


def display_menu_list(is_useraction_required=0):
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
            'You ordered Item ', order_data)


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
                display_menu_list(1)
                # print("You ordered: ", order_data)
                item_number += 1
                # food_item = input('Please enter a valid input: ')
            except IndexError:
                clear_screen()
                print(colored(
                    f'\nIm sorry Item "{food_item + 1}" does not exist.'
                    ' Please enter a valid item number', 'yellow'))
            if (food_item >= 0 and food_item <= 20):
                item_number = food_item
                add_item(item_number)
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
        if i:
            print(colored("----------Order Preview----------\n", "yellow"))
            tabulate_data(local_user_data)
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
    print(display_menu_list)
    removed_item = order_data[-1]
    remove_str = f'\nYou have removed {0} from your order'.format(removed_item)
    print(colored(remove_str, 'yellow'))
    order_data.pop()
    clear_screen()
    display_menu_list(1)
    return
    # user_action()


def complete_order():
    """
    Function to complete order and pass arguments to
    Order class and its functions
    """
    # Display user data
    print(colored("****Your Reciept****\n", "yellow"))
    print(f"User name: {user_data[0]}")
    print(f"Order Id: {user_data[1]}")
    print(f"Order type: {user_data[2]}")
    print(f"Address: {user_data[3]}")
    # Display date & time for order receipt
    order_time = datetime.now()
    delivery_time = order_time + timedelta(minutes=DELIVERY_TIME)
    pickup_time = order_time + timedelta(minutes=PICKUP_TIME)
    order_time = order_time.strftime("%H:%M:%S  %d-%m-%Y")
    delivery_time = delivery_time.strftime("%H:%M:%S  %d-%m-%Y")
    pickup_time = pickup_time.strftime("%H:%M:%S  %d-%m-%Y")
    print(f"Order time: {order_time}\n")
    total_price = 0  # initialize total price
    local_user_data = get_individual_user_data()
    # Calculating total price for order receipt
    for item in local_user_data:
        price = float(item[2].split('€')[1])
        total_price += price
        display_total_price = "€" + str(round(total_price, 2))
    tabulate_data(local_user_data)
    if user_data[2] == "Home delivery":
        print(
            colored(
                f"\nDelivey Charge: €{float(DELIVERY_CHARGE):.2f}", "yellow"
            )
        )
        display_total_price = "€" + str(total_price + DELIVERY_CHARGE)
        print(
            colored(
                f"Total price of your order: {display_total_price}", "yellow"
            )
        )
    else:
        print(
            colored(
                f"\nTotal price of your order: {display_total_price}", "yellow"
            )
        )
    if user_data[2] == "Home delivery":
        print(
            colored(
                f"Your order will be delivered at {delivery_time}\n", "yellow"
            )
        )
    else:
        print(
            colored(
                f"Your order will be ready for Pickup at {pickup_time}",
                "yellow",
            )
        )
    print(colored("\nThanks for your order. Enjoy your meal!", "green"))
    while True:
        end = input("\nEnter Q to quit:\n")
        if end.capitalize() == "Q":
            clear_screen()
            thank_you()
            sleep(2)
            clear_screen()
            break


def thank_you():
    """
    Function to display thank you message
    """
    title = 'Thanks for Visiting!'
    print(pyfiglet.figlet_format(title))
    print('\nCreated by Dhvani Intwala'
          '\nGitHub -'
          'https://github.com/Dhvani-intwala'
          '\n\nLinkedIn -'
          'https://www.linkedin.com/in/dhvani-intwala-2716bb235/\n\n')


if __name__ == "__main__":
    welcome()
