def print_request_result(r):
    print("------------------- Code")
    print(r.status_code)
    print("------------------- Headers")
    print(r.headers)
    print("------------------- Text")
    print(r.text)
    print("-------------------")
