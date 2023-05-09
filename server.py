import flask
from flask import request, render_template, redirect, url_for
import random

app = flask.Flask(__name__)

adress = "localhost"
port = 5000

size_x = 10
size_y = 10
number_ships = 10
battle_field = [[0 for i in range(size_x)] for i in range(size_y)]
ships_start_x = []
ships_start_y = []
ships_start_dir = []
ships_list = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
ships_left = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
x0 = 0
y0 = 0
res = 'Miss'
score = 0

is_running = True

def show_battle_field():
    for i in range(size_x):
        for j in range(size_y):
            print(battle_field[i][j], end = ' ')
        print('\n')

def hit_result(x, y):
    print('x =', x, 'y =', y)
    global battle_field
    id = battle_field[x][y]
    global score
    if id == 0:
        return 'Miss'
    else:
        battle_field[x][y] *= -1
        score += 1
        if ships_left[id - 1] > 0:
            print('Damaged')
            return 'Damaged'
        else:
            return str(ships_start_x[id - 1]) + str(ships_start_y[id - 1]) + str(ships_start_dir[id - 1]) + str(ships_list[id - 1])

@app.route('/restart')
def restart():
    global battle_field
    global score
    battle_field = [[0 for i in range(size_x)] for i in range(size_y)]
    score = 0
    generate_position()
    return 'restart'

@app.route('/status')
def status():
    print('score', score)
    return str(score)
@app.route('/show')
def show():
    return render_template('base.html', x = x0, y = y0, result = res)

@app.route('/hit', methods = ['GET', 'POST'])
def hit():
    global x0
    global y0
    global res
    x0 = request.args.get('x')
    y0 = request.args.get('y')
    if battle_field[int(x0)][int(y0)] > 0:
        ships_left[battle_field[int(x0)][int(y0)] - 1] -= 1
    res = hit_result(int(x0), int(y0))
    redirect(url_for('show'))
    return res

@app.route('/generate')
def generate_position():
    global battle_field
    global ships_start_x
    global ships_start_y
    global ships_start_dir
    our_sum = 20
    cur_sum = 0
    while cur_sum != our_sum:
        battle_field = [[0 for i in range(size_x)] for i in range(size_y)]
        ships_start_x = []
        ships_start_y = []
        ships_start_dir = []
        for i in range(number_ships):
            len = ships_list[i]
            #2-horizontal
            #1-vertical
            direction = random.randrange(1, 3)
            check_sum = 0
            if direction == 1:
                coor_x = random.randrange(0, size_x + 1 - len)
                coor_y = random.randrange(0, size_y)
                for j in range(len):
                    if coor_y > 0:
                        check_sum += battle_field[coor_x + j][coor_y - 1]
                    if coor_y < 9:
                        check_sum += battle_field[coor_x + j][coor_y + 1]
                if coor_x > 0:
                    check_sum += battle_field[coor_x - 1][coor_y]
                    if coor_y > 0:
                        check_sum += battle_field[coor_x - 1][coor_y - 1]
                    if coor_y < 9:
                        check_sum += battle_field[coor_x - 1][coor_y + 1]
                if coor_x + len < 10:
                    check_sum += battle_field[coor_x  + len][coor_y]
                    if coor_y > 0:
                        check_sum += battle_field[coor_x + len][coor_y - 1]
                    if coor_y < 9:
                        check_sum += battle_field[coor_x + len][coor_y + 1]
            else:
                coor_x = random.randrange(0, size_x)
                coor_y = random.randrange(0, size_y + 1 - len)
                for j in range(len):
                    if coor_x > 0:
                        check_sum += battle_field[coor_x - 1][coor_y + j]
                    if coor_x < 9:
                        check_sum += battle_field[coor_x + 1][coor_y + j]
                if coor_y > 0:
                    check_sum += battle_field[coor_x][coor_y - 1]
                    if coor_x > 0:
                        check_sum += battle_field[coor_x - 1][coor_y - 1]
                    if coor_x < 9:
                        check_sum += battle_field[coor_x + 1][coor_y - 1]
                if coor_y + len < 10:
                    check_sum += battle_field[coor_x][coor_y + len]
                    if coor_x > 0:
                        check_sum += battle_field[coor_x - 1][coor_y + len]
                    if coor_x < 9:
                        check_sum += battle_field[coor_x + 1][coor_y + len]
            if check_sum == 0:
                if direction == 1:
                    for j in range(len):
                        battle_field[coor_x + j][coor_y] = i + 1
                else:
                    for j in range(len):
                        battle_field[coor_x][coor_y + j] = i + 1
                ships_start_x.append(coor_x)
                ships_start_y.append(coor_y)
                ships_start_dir.append(direction)
        cur_sum = 0
        for i in range(size_x):
            for j in range(size_y):
                if battle_field[j][i] > 0:
                    cur_sum += 1


generate_position()
for i in range(10):
    for j in range(10):
        print(battle_field[i][j], end = ' ')
    print('\n')
for i in range(10):
    print(ships_start_x[i], ships_start_y[i], ships_start_dir[i])
'''while is_running:
    s = input()
    if s == 'q':
        is_running = False
    elif s == 'show':
        show_battle_field()
    else:
        print(hit_result(int(s[0]), int(s[2])))'''
if __name__ == '__main__':
    app.run(adress, port, debug=True)
