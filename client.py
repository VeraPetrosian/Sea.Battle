import requests
adress = 'http://127.0.0.1:5000/'

def hit(x, y):
    return requests.get(adress + 'hit?x=' + str(x) + '&y=' + str(y)).text


is_running = True
while is_running:
    s = input()
    if s == 'q':
        is_running = False
    else:
        print(hit(int(s[0]), int(s[2])))
