"""
Import gspread to access and update data in our spreadsheet
"""

import gspread
import pyfiglet
import pyfiglet.fonts
from google.oauth2.service_account import Credentials
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

data = MENU.get_all_values()


def welcome():
    """
    Function to display home page
    """
    title = "Welcome to the Cafe Beats"
    print(colored(pyfiglet.figlet_format(title, font="big"), "red"))


welcome()