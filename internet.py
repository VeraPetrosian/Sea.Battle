import requests
adress = 'http://127.0.0.1:5000/'

def hit(x, y):
    return requests.get(adress + 'hit?x=' + str(x) + '&y=' + str(y)).text

def status():
    return requests.get(adress + 'status').text

def restart():
    requests.get(adress + 'restart').text

'''is_running = True
while is_running:
    s = input()
    if s == 'q':
        is_running = False
    else:
        print(hit(int(s[0]), int(s[2])))
        print('status is', status())'''
