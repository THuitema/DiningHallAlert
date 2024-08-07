from datetime import date
import requests
from bs4 import BeautifulSoup
from db import db_select, db_write
from send_email import send_alert

# Constants for web scraping
BASE_URL = "https://nutrition.umd.edu"
MENU_TAG = "a"
MENU_CLASS = "menu-item-name"


class DiningHall:
    """
    Stores information pertaining to a dining hall and functionality to web scrape menu data

    Attributes
    __________
    name : str
        name of the dining hall
    location_num : int
        identifier used by the dining hall website
    menu: set[str]
        contains items in the menu of the dining hall

    Methods
    _________
    get_url()
        Returns the url to the current dining hall's menu for today
    scrape_menu()
        Web-scrapes the menu of the dining hall for the current day, returning a set of items
    """

    def __init__(self, name: str, location_num: int):
        """
        Initializes the DiningHall object and generates menu
        :param name: name of the dining hall
        :param location_num: identifier used by the dining hall website
        """
        self.name = name
        self.location_num = location_num
        self.url = self.get_url()
        self.menu = self.scrape_menu()

    def get_url(self) -> str:
        """
        :return: url to the current dining hall's menu for today
        """
        month = date.today().month
        day = date.today().day
        year = date.today().year

        return BASE_URL + "/?locationNum=" + str(self.location_num) + "&dtdate=" + str(month) + "/" + str(
            day) + "/" + str(year)

    def scrape_menu(self) -> set[str]:
        """
        Web-scrapes the menu of the dining hall for the current day
        :return: set of items on the menu
        """
        # Set up web scraper
        page = requests.get(self.url, verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        items = set()

        # Iterate through each menu item found in webpage, add to items set
        for line in soup.find_all(MENU_TAG, class_=MENU_CLASS):
            items.add(line.text)

        return items


class Menu:
    """
    Represents the combined menu of all dining halls and interacts with database

    Attributes
    __________
    dining_halls : [DiningHall]
        list of DiningHall objects
    total_menu : {str : Item}
        dictionary mapping menu items to Item objects
    users_to_alert : {int : User}
        dictionary mapping user_ids to User objects

    Methods
    _________
    create_menu()
        Combines menus from each dining hall into one, storing result in total_menu
    update_db_menu(conn)
        Insert new menu items to Menu table and all items to Daily Menu table
    get_alerts(conn)
        Checks with database if there are users to alert, storing result in users_to_alert
    alert_users()
        Send alert emails to users
    """

    def __init__(self, dining_halls):
        """
        Initializes the Menu object

        :param dining_halls: list of DiningHall objects
        """
        self.dining_halls = dining_halls
        self.total_menu = {}
        self.users_to_alert = {}

    def create_menu(self):
        """
        Combines menus from each dining hall into one, storing result in total_menu
        """
        for dining_hall in self.dining_halls:
            for item in dining_hall.menu:
                if item in self.total_menu:
                    # if item has already been seen, add current dining hall to its list
                    self.total_menu[item].dining_halls.append(dining_hall.name)
                else:
                    # otherwise, create new Item object and initialize its list with current dining hall
                    self.total_menu[item] = Item(item)
                    self.total_menu[item].dining_halls = [dining_hall.name]

    def update_db_menu(self, conn):
        """
        Insert new menu items to Menu table and all items to Daily Menu table
        :param conn: PostgreSQL database connection
        """

        for key in self.total_menu.keys():
            # Insert new items to Menu table
            menu_insert_query = '''
                INSERT INTO accounts_menu (item)
                SELECT %s
                WHERE NOT EXISTS (SELECT * FROM accounts_menu WHERE item=%s)
            '''
            db_write(conn, menu_insert_query, key, key)

            # Insert all items to Daily Menu table
            at_y = 'Yahentamitsi' in self.total_menu[key].dining_halls
            at_south = 'South' in self.total_menu[key].dining_halls
            at_251 = '251' in self.total_menu[key].dining_halls

            # Get foreign key for menu item
            get_menu_item_query = '''
                SELECT * 
                FROM accounts_menu
                WHERE item=%s
            '''

            rows = db_select(conn, get_menu_item_query, key)
            menu_item_id = rows[0][0]

            daily_menu_insert_query = '''
                INSERT INTO accounts_dailymenu 
                    (menu_item_id, date, yahentamitsi_dining_hall, south_dining_hall, two_fifty_one_dining_hall)
                VALUES
                    (%s, %s, %s, %s, %s)
            '''

            db_write(conn, daily_menu_insert_query, menu_item_id, date.today(), at_y, at_south, at_251)

        return {'Completed': True}

    def get_alerts(self, conn):
        """
        Appends to users_to_alert users with alerts for the current menu
        :param conn: PostgreSQL database connection
        :return dictionary with key = user id, value = list of alerts
        """
        for item_name, item_obj in self.total_menu.items():
            item_name = item_name.replace("'", "''")

            # Returns rows from Profile table that have alerts for current item
            get_alerts_query = '''
                SELECT *
                FROM accounts_profile
                WHERE id IN (
                    SELECT user_id
                    FROM accounts_alert
                    WHERE menu_item_id in (
                        SELECT id
                        FROM accounts_menu
                        WHERE item=%s
                    )
                )
            '''

            rows = db_select(conn, get_alerts_query, item_name)

            # Append users & alerts to users_to_alert dict
            for row in rows:
                user_id = row[0]
                email = str(row[3])
                receive_email_alerts = row[8]  # == 'True'

                if user_id in self.users_to_alert:
                    self.users_to_alert[user_id].alerts.append(item_obj)
                else:
                    self.users_to_alert[user_id] = User(row, int(user_id), email, receive_email_alerts)
                    self.users_to_alert[user_id].alerts = [item_obj]

        return self.users_to_alert

    def alert_users(self, conn):
        """
        Email users that have alerts for the current day menu
        :param conn: PostgreSQL database connection
        :return list containing each email alerted and their alert message(s)
        """
        alerts_sent = []

        for user_id, user_obj in self.users_to_alert.items():
            if user_obj.receive_email_alerts:
                token = user_obj.get_auth_token(conn)
                response = send_alert(user_obj.email, user_obj.get_alert_list(), token)
                alerts_sent.append([user_obj.email, response.json()])

        return alerts_sent

    def __str__(self):
        """
        Returns each item from menu, along with which dining halls are serving them

        :return: str
        """
        out = ''
        for item_name, obj in self.total_menu.items():
            out += str(obj) + '\n'
        return out


class Item:
    """
    Represents a menu item and dining halls associated with it

    Attributes
    __________
    name : str
        name of the item
    dining_halls : [str]
        names of the dining halls at which the item is being served
    """

    def __init__(self, name: str):
        """
        Initializes Item object

        :param name: str
        """
        self.name = name
        self.dining_halls = []

    def __str__(self):
        """
        Returns item name, along with which dining halls are serving it

        :return: str
        """
        out = '{0} at '.format(self.name)
        out += ', '.join(self.dining_halls)
        return out


class User:
    """
    Represents a User of the app

    Attributes
    __________
    info : object
        any information pertaining to user that is returned by database
    user_id : int
        user id stored in the database
    email : str
        user email
    alerts : [Item]
        list of Item objects that the user should receive an alert for
    receive_email_alerts : bool
        true if user wants to receive email notifications

    Methods
    _________
    get_alert_list()
        get the list of alert messages for user
    get_auth_token(conn)
        Get the user's authentication token
    """

    def __init__(self, info: object, user_id: int, email: str, receive_email_alerts: bool):
        """
        Initializes User object
        :param info: any information pertaining to user, returned by database
        """
        self.info = info
        self.user_id = user_id
        self.email = email
        self.alerts = []
        self.receive_email_alerts = receive_email_alerts

    def get_alert_list(self):
        """
        :return: list of alert messages for user
        """
        alert_list = []
        for alert in self.alerts:
            alert_list.append(str(alert))

        return alert_list

    def get_auth_token(self, conn):
        """
        Get the user's authentication token
        :param conn: PostgreSQL database connection
        :return: Django REST authentication token for user
        """
        get_token_query = '''
            SELECT key
            FROM authtoken_token
            WHERE user_id=%s
        '''

        rows = db_select(conn, get_token_query, self.user_id)

        return rows[0][0]

    def __str__(self):  # use this to alert user by email/sms later?
        """
        Returns the alert(s) for the user

        :return: str
        """
        out = 'Alert(s) for {0}\n'.format(self.email)
        # Calls __str__() of each Item object in alerts
        for alert in self.alerts:
            out += '\t{0}\n'.format(str(alert))
        return out