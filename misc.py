def print_request_result(r):
    print("------------------- Code")
    print(r.status_code)
    print("------------------- Headers")
    print(r.headers)
    print("------------------- Text")
    print(r.text)
    print("-------------------")

def print_banner():
    banner="""

 _  ___         __              _                                     
| |/ (_) ___   / _| ___  _ __  | |__  _   _ _ __ ___   __ _ _ __  ___ 
| ' /| |/ _ \ | |_ / _ \| '__| | '_ \| | | | '_ ` _ \ / _` | '_ \/ __|
| . \| |  __/ |  _| (_) | |    | | | | |_| | | | | | | (_| | | | \__ \\
|_|\_\_|\___| |_|  \___/|_|    |_| |_|\__,_|_| |_| |_|\__,_|_| |_|___/                                                                                                                                                             

powered by requests (www.python-requests.org)
    """
    print(banner)