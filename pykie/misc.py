from getpass import getpass


def print_request_result(r):
    print("------------------- Code")
    print(r.status_code)
    print("------------------- Headers")
    print(r.headers)
    print("------------------- Text")
    print(r.text)
    print("-------------------")


def print_banner():
    banner = """

 _  ___         __              _                                     
| |/ (_) ___   / _| ___  _ __  | |__  _   _ _ __ ___   __ _ _ __  ___ 
| ' /| |/ _ \ | |_ / _ \| '__| | '_ \| | | | '_ ` _ \ / _` | '_ \/ __|
| . \| |  __/ |  _| (_) | |    | | | | |_| | | | | | | (_| | | | \__ \\
|_|\_\_|\___| |_|  \___/|_|    |_| |_|\__,_|_| |_| |_|\__,_|_| |_|___/                                                                                                                                                             

powered by requests (www.python-requests.org)
    """
    print(banner)


def force_to_input(items):
    """Forces an user to select an item from a list or exit with 'q'"""
    selected = ""
    while not (selected.isdigit() and 0 <= int(selected) < len(items)) and selected != "q":
        print("\nSelect one [q for quit]")
        for key, val in enumerate(items):
            print("{}: {}".format(key, val))
        selected = input("Choose one: ")

    item = None
    if selected is not "q":
        item = items[int(selected)]

    return item


def request_credentials():
    user = input("Input user [default=kieserver]:")
    password = getpass("Input password [default=kieserver1!]:")
    if len(user) == 0:
        user = "kieserver"
    if len(password) == 0:
        password = "kieserver1!"
    return user, password
