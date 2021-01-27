import random, time

def main_menu():
    print("MINESWEEPER!")
    print("\n1: Play")
    print("2: Check Statistics")
    print("3: Quit\n")
    while True:
        try:
            choice = int(input("Enter 1, 2, or 3: "))
            if choice == 1 or choice == 2 or choice == 3:
                break
            else:
                print("Invalid input.")
        except ValueError:
            print("Invalid input.")
        
    return choice

def print_field(field, width, height):
    s = ' '
    for x in range(0, height):
        print(s.join(field[x])) 
    print(" ")
  
def create_field():
    
    while True: #Getting input for field size       
        size = input("Enter the width and height of minefield (Example: 20,20): ")
        try:
            list = []
            list = size.split(',')
            width = int(list[0])
            height = int(list[1])
            break
        except ValueError:
            print("Invalid input, use two integers separated by a comma")
        except IndexError:
            print("Invalid input, use two integers separated by a comma")
    field = [] #create field
    for x in range(0, width):
        for y in range(0, height):
            field += [["O"]*(width)]
    revealed_field = [] #create 2nd field (for revealed field to check self)
    for x in range(0, height):
        for y in range(0, width):
            revealed_field += [["O"]*(width)]
    while True:  #Getting number of mines
        try:
            mine_count = int(input("Enter number of mines (Example: 100): "))
            if mine_count == width*height:
                print("Impossible! That will place a mine in every spot!")
            elif mine_count > width*height:
                print("Impossible! There are more mines than spots in the field!")
            else:
                break
        except ValueError:
            print("Please enter an integer number of mines")
    
    #place mines
    for x in range(0, mine_count): 
        x_random = random.randint(0,(width-1))
        y_random = random.randint(0,(height-1))
        while revealed_field[y_random][x_random] == "M":
            x_random = random.randint(0,(width-1))
            y_random = random.randint(0,(height-1))
            print(x_random, y_random)
            if revealed_field[y_random][x_random] == " ":
                break
        revealed_field[y_random][x_random] = "M"

                #check minecount in all spots
    for x in range(0, width):
        for y in range(0, height):
            coord = "{},{}" 
            new_coord = coord.format(str(x), str(y))
            coord_list = [0, x, y]
            if revealed_field[y][x] == "M":
                nothing = 1
            else:
                mines = count_mines(coord_list, revealed_field, width, height)
                if mines > 0:
                    revealed_field[y][x] = str(mines)
                else:
                    revealed_field[y][x] = " "
    return (field, revealed_field, width, height)

def game_instructions(x, y):
    print(" ")
    print("CONTROLS:")
    explanation = "Valid x entries:  to {}. Valid y entries 0 to {}"
    print("To uncover a spot, enter U, then x,y coordinates (Example: U,1,1).")
    print("To flag a mine, enter F, then x,y coordinates (Example: F,1,1).")
    print("To erase a flag, enter E, then x,y cordinates (Example: E,1,1).")
    print("Enter Q to quit the current game.")
    print(explanation.format(x-1, y-1))
    print("Enter ? to get these instructions again.")
    print(" ")

def input_validation(width, height):
    while True:        
        choice = input("Enter U/F/E and x,y coordinates (or Q to quit game): ")
        if choice == "Q" or choice == "q":
            break
        else:
            try:
                choice_list = []
                choice_list = choice.split(',')
                click = choice_list[0]
                x_coord = int(choice_list[1])
                y_coord = int(choice_list[2])
                coord = "{},{}"
                coord = coord.format(str(x_coord), str(y_coord))
                if x_coord < 0 or y_coord < 0 or x_coord >= width or y_coord >= height:
                    result = "The point (x: {}, y: {}) is outside the field!"
                    print(result.format(x_coord, y_coord))
                elif click.find("E") and click.find("e") and click.find("F") and click.find("U") and click.find("f") and click.find("u"): #and click not "U" and click not "f" and click not "u":
                    result = "{} is an invalid input."
                    print(result.format(click))
                else:
                    break
            except ValueError:
                print("Invalid input, enter x and y as integers.")
            except IndexError:
                print("Invalid input")
    if choice == "Q" or choice == "q":
        return "Q"
    else:
        return choice_list

def check_spot(choice_list, revealed_field):
    if revealed_field[int(choice_list[2])][int(choice_list[1])] == "M":
        return 420
    else:
        return 0
    
            
def check_position(choice_list, width, height): #using phone numberpad as position in field
    xcoord = int(choice_list[1])                #Ex. 1 = top left corner, 5 center, 6 right wall
    ycoord = int(choice_list[2])
    if xcoord == ycoord == 0:
        return 1
    elif xcoord == (width-1) and ycoord == (height-1):
        return 9
    elif xcoord == 0 and ycoord == (height-1):
        return 7
    elif xcoord == (width-1) and ycoord == 0:
        return 3
    elif xcoord == 0:
        return 4
    elif xcoord == (width-1):
        return 6
    elif ycoord == 0:
        return 2
    elif ycoord == (height-1):
        return 8
    else:
        return 5
            
def count_mines(choice_list, revealed_field, width, height):
    mine_count = 0
    xcoord = int(choice_list[1])
    ycoord = int(choice_list[2])
    position = check_position(choice_list, width, height)
    coord = "{},{}"
    if position == 5:
        mine_count += count_top(coord, xcoord, ycoord, revealed_field)
        mine_count += count_mid_bt(coord, xcoord, ycoord, revealed_field)
        mine_count += count_bot(coord, xcoord, ycoord, revealed_field)
    elif position == 2:
        mine_count += count_mid_bt(coord, xcoord, ycoord, revealed_field)
        mine_count += count_bot(coord, xcoord, ycoord, revealed_field)
    elif position == 8:
        mine_count += count_top(coord, xcoord, ycoord, revealed_field)
        mine_count += count_mid_bt(coord, xcoord, ycoord, revealed_field)
    elif position == 6:
        mine_count += count_left(coord, xcoord, ycoord, revealed_field)
        mine_count += count_mid_rl(coord, xcoord, ycoord, revealed_field)
    elif position == 4:
        mine_count += count_right(coord, xcoord, ycoord, revealed_field)
        mine_count += count_mid_rl(coord, xcoord, ycoord, revealed_field)
    elif position == 1:
        new_coord = coord.format(xcoord+1, ycoord)
        if revealed_field[ycoord][xcoord+1] == "M":
            mine_count += 1
        new_coord = coord.format(xcoord+1, ycoord+1)
        if revealed_field[ycoord+1][xcoord+1] == "M":
            mine_count += 1
        new_coord = coord.format(xcoord, ycoord+1)
        if revealed_field[ycoord+1][xcoord] == "M":
            mine_count += 1
    elif position == 3:
        new_coord = coord.format(xcoord-1, ycoord)
        if revealed_field[ycoord][xcoord-1] == "M":
            mine_count += 1
        new_coord = coord.format(xcoord-1, ycoord+1)
        if revealed_field[ycoord+1][xcoord-1] == "M":
            mine_count += 1
        new_coord = coord.format(xcoord, ycoord+1)
        if revealed_field[ycoord+1][xcoord] == "M":
            mine_count += 1
    elif position == 7:
        new_coord = coord.format(xcoord+1, ycoord)
        if revealed_field[ycoord][xcoord+1] == "M":
            mine_count += 1
        new_coord = coord.format(xcoord+1, ycoord-1)
        if revealed_field[ycoord-1][xcoord+1] == "M":
            mine_count += 1
        new_coord = coord.format(xcoord, ycoord-1)
        if revealed_field[ycoord-1][xcoord] == "M":
            mine_count += 1
    elif position == 9:
        new_coord = coord.format(xcoord-1, ycoord)
        if revealed_field[ycoord][xcoord-1] == "M":
            mine_count += 1
        new_coord = coord.format(xcoord-1, ycoord-1)
        if revealed_field[ycoord-1][xcoord-1] == "M":
            mine_count += 1
        new_coord = coord.format(xcoord, ycoord-1)
        if revealed_field[ycoord-1][xcoord] == "M":
            mine_count += 1  
    return mine_count
def count_top(coord, xcoord, ycoord, revealed_field):#checks row above number
    mine_count = 0
    for x in range(0, 3):
        new_coord = coord.format(xcoord-1+x, ycoord-1)
        if revealed_field[ycoord-1][xcoord-1+x] == "M":
            mine_count += 1
    return mine_count
def count_bot(coord, xcoord, ycoord, revealed_field):#checks row below number
    mine_count = 0
    for x in range(0, 3):
        new_coord = coord.format(xcoord-1+x, ycoord+1)
        if revealed_field[ycoord+1][xcoord-1+x] == "M":
            mine_count += 1
    return mine_count
def count_mid_rl(coord, xcoord, ycoord, revealed_field):#checks boxes to right and left
    mine_count = 0
    new_coord = coord.format(xcoord, ycoord-1)
    if revealed_field[ycoord-1][xcoord] == "M":
        mine_count += 1
    new_coord = coord.format(xcoord, ycoord+1)
    if revealed_field[ycoord+1][xcoord] == "M":
        mine_count += 1
    return mine_count
def count_right(coord, xcoord, ycoord, revealed_field):#checks column to right
    mine_count = 0
    #print(coord.format(xcoord, ycoord))
    for x in range(0, 3):
        new_coord = coord.format(xcoord+1, ycoord-1+x)
        if revealed_field[ycoord-1+x][xcoord+1] == "M":
            mine_count += 1
            #print(mine_count)
    return mine_count
def count_left(coord, xcoord, ycoord, revealed_field):#checks column to left
    mine_count = 0
    for x in range(0, 3):
        new_coord = coord.format(xcoord-1, ycoord-1+x)
        if revealed_field[ycoord-1+x][xcoord-1] == "M":
            mine_count += 1
    return mine_count
def count_mid_bt(coord, xcoord, ycoord, revealed_field):#checks boxes above and below
    mine_count = 0
    new_coord = coord.format(xcoord-1, ycoord)
    if revealed_field[ycoord][xcoord-1] == "M":
        mine_count += 1
    new_coord = coord.format(xcoord+1, ycoord)
    if revealed_field[ycoord][xcoord+1] == "M":
        mine_count += 1
    return mine_count
    


def flood_fill(field, choice_list, width, height, revealed_field):
    xcoord = int(choice_list[1])
    ycoord = int(choice_list[2])
    coord = "{},{}"
    new_coord = coord.format(choice_list[1], choice_list[2])
    fill_list = [new_coord]
    checked_list = []
    while True:
        try:
            new_coord = fill_list.pop()
            coord_list = new_coord.split(',')
            new_coord_list = [0, coord_list[0], coord_list[1]]
            xcoord = int(new_coord_list[1])
            ycoord = int(new_coord_list[2])
            position = check_position(new_coord_list, width, height)
            right_coord = coord.format(xcoord+1, ycoord)
            top_coord = coord.format(xcoord, ycoord-1)
            bot_coord = coord.format(xcoord, ycoord+1)
            left_coord = coord.format(xcoord-1, ycoord)
            if position == 1:
                checked_list = check_right(revealed_field, fill_list, right_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_bot(revealed_field, fill_list, bot_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
            if position == 2:
                checked_list = check_right(revealed_field, fill_list, right_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_left(revealed_field, fill_list, left_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_bot(revealed_field, fill_list, bot_coord, field) 
                fill_list = checked_list[0]
                field = checked_list[1]
            if position == 3:
                checked_list = check_left(revealed_field, fill_list, left_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_bot(revealed_field, fill_list, bot_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
            if position == 4:
                checked_list = check_right(revealed_field, fill_list, right_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_bot(revealed_field, fill_list, bot_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_top(revealed_field, fill_list, top_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
            if position == 5:
                checked_list = check_right(revealed_field, fill_list, right_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_left(revealed_field, fill_list, left_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_top(revealed_field, fill_list, top_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_bot(revealed_field, fill_list, bot_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
            if position == 6:
                checked_list = check_bot(revealed_field, fill_list, bot_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_left(revealed_field, fill_list, left_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_top(revealed_field, fill_list, top_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
            if position == 7:
                checked_list = check_top(revealed_field, fill_list, top_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_right(revealed_field, fill_list, right_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
            if position == 8:
                checked_list = check_right(revealed_field, fill_list, right_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_left(revealed_field, fill_list, left_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_top(revealed_field, fill_list, top_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
            if position == 9:
                checked_list = check_top(revealed_field, fill_list, top_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
                checked_list = check_left(revealed_field, fill_list, left_coord, field)
                fill_list = checked_list[0]
                field = checked_list[1]
        
        except IndexError:
            nothing = 1
            break
        except IOError:
            nothing = 1
    return field

def replace_w_num(revealed_field, new_coord, xcoord, ycoord, field): 
    field[ycoord][xcoord] = revealed_field[ycoord][xcoord]
    return field

def check_top(revealed_field, fill_list, top_coord, field):
    top_coord_list = top_coord.split(',')
    if revealed_field[int(top_coord_list[1])][int(top_coord_list[0])] == "M":
        nothing = 1
    elif revealed_field[int(top_coord_list[1])][int(top_coord_list[0])] == "1" or revealed_field[int(top_coord_list[1])][int(top_coord_list[0])] == "2" or revealed_field[int(top_coord_list[1])][int(top_coord_list[0])] == "3" or revealed_field[int(top_coord_list[1])][int(top_coord_list[0])] == "4" or revealed_field[int(top_coord_list[1])][int(top_coord_list[0])] == "5" or revealed_field[int(top_coord_list[1])][int(top_coord_list[0])] == "6" or revealed_field[int(top_coord_list[1])][int(top_coord_list[0])] == "7" or revealed_field[int(top_coord_list[1])][int(top_coord_list[0])] == "8" or revealed_field[int(top_coord_list[1])][int(top_coord_list[0])] == "9":
        field = replace_w_num(revealed_field, top_coord, int(top_coord_list[0]), int(top_coord_list[1]), field)
        
    else:
        top_coord_list = top_coord.split(',')
        if field[int(top_coord_list[1])][int(top_coord_list[0])] == "O":
            field = replace_w_num(revealed_field, top_coord, int(top_coord_list[0]), int(top_coord_list[1]), field)
            fill_list.append(top_coord)
    return (fill_list, field)
    
def check_bot(revealed_field, fill_list, bot_coord, field):
    bot_coord_list = bot_coord.split(',')
    if revealed_field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "M":
        nothing = 1
    elif revealed_field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "1" or revealed_field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "2" or revealed_field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "3" or revealed_field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "4" or revealed_field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "5" or revealed_field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "6" or revealed_field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "7" or revealed_field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "8" or revealed_field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "9":
        field = replace_w_num(revealed_field, bot_coord, int(bot_coord_list[0]), int(bot_coord_list[1]), field)
        
    else:
        bot_coord_list = bot_coord.split(',')
        if field[int(bot_coord_list[1])][int(bot_coord_list[0])] == "O":
            field = replace_w_num(revealed_field, bot_coord, int(bot_coord_list[0]), int(bot_coord_list[1]), field)
            fill_list.append(bot_coord)
    return (fill_list, field)
    
    
def check_left(revealed_field, fill_list, left_coord, field):
    left_coord_list = left_coord.split(',')
    if revealed_field[int(left_coord_list[1])][int(left_coord_list[0])] == "M":
        nothing = 1
    elif revealed_field[int(left_coord_list[1])][int(left_coord_list[0])] == "1" or revealed_field[int(left_coord_list[1])][int(left_coord_list[0])] == "2" or revealed_field[int(left_coord_list[1])][int(left_coord_list[0])] == "3" or revealed_field[int(left_coord_list[1])][int(left_coord_list[0])] == "4" or revealed_field[int(left_coord_list[1])][int(left_coord_list[0])] == "5" or revealed_field[int(left_coord_list[1])][int(left_coord_list[0])] == "6" or revealed_field[int(left_coord_list[1])][int(left_coord_list[0])] == "7" or revealed_field[int(left_coord_list[1])][int(left_coord_list[0])] == "8" or revealed_field[int(left_coord_list[1])][int(left_coord_list[0])] == "9":
        field = replace_w_num(revealed_field, left_coord, int(left_coord_list[0]), int(left_coord_list[1]), field)
        
    else:
        left_coord_list = left_coord.split(',')
        if field[int(left_coord_list[1])][int(left_coord_list[0])] == "O":
            field = replace_w_num(revealed_field, left_coord, int(left_coord_list[0]), int(left_coord_list[1]), field)
            fill_list.append(left_coord)
    return (fill_list, field)
    
def check_right(revealed_field, fill_list, right_coord, field):
    right_coord_list = right_coord.split(',')
    if revealed_field[int(right_coord_list[1])][int(right_coord_list[0])] == "M":
        nothing = 1
    elif revealed_field[int(right_coord_list[1])][int(right_coord_list[0])] == "1" or revealed_field[int(right_coord_list[1])][int(right_coord_list[0])] == "2" or revealed_field[int(right_coord_list[1])][int(right_coord_list[0])] == "3" or revealed_field[int(right_coord_list[1])][int(right_coord_list[0])] == "4" or revealed_field[int(right_coord_list[1])][int(right_coord_list[0])] == "5" or revealed_field[int(right_coord_list[1])][int(right_coord_list[0])] == "6" or revealed_field[int(right_coord_list[1])][int(right_coord_list[0])] == "7" or revealed_field[int(right_coord_list[1])][int(right_coord_list[0])] == "8" or revealed_field[int(right_coord_list[1])][int(right_coord_list[0])] == "9":
        field = replace_w_num(revealed_field, right_coord, int(right_coord_list[0]), int(right_coord_list[1]), field)
        
    else:
        right_coord_list = right_coord.split(',')
        if field[int(right_coord_list[1])][int(right_coord_list[0])] == "O":
            field = replace_w_num(revealed_field, right_coord, int(right_coord_list[0]), int(right_coord_list[1]), field)
            fill_list.append(right_coord)
    return (fill_list, field)

def game(field, revealed_field, width, height): 
    import time
    game_instructions(width, height)
    start = time.clock()
    #print_field(revealed_field, width, height)
    while True:
        print_field(field, width, height)
        O_count = [row.count("O") for row in field]
        Empty_count = [row.count("O") for row in revealed_field]
        if O_count == Empty_count:
            end = time.clock()
            time_total = end - start
            end_game = 1
            print("CONGRATS YOU WON!")
            break
        coord = "{},{}"
        try:
            choice_list = input_validation(width, height)
            choice = choice_list[0]
            new_coord = coord.format(choice_list[1], choice_list[2])
            trial_choice_list = [choice_list[0], choice_list[1], choice_list[2]]
            spot = int(check_spot(choice_list, revealed_field))
            if choice == "U" or choice == "u":            
                if spot == 420: #Mine
                    end = time.clock()
                    time_total = end - start
                    end_game = 0
                    print_field(revealed_field, width, height)
                    print("\nEXPLOSION! YOU HIT A MINE!\n")
                    break
                else: #no mine. 
                    mine_count = count_mines(choice_list, revealed_field, width, height)
                    if mine_count == 0:#flood fill
                        field = flood_fill(field, trial_choice_list, width, height, revealed_field)
                    else: #fill with number
                        field[int(choice_list[2])][int(choice_list[1])] = revealed_field[int(choice_list[2])][int(choice_list[1])]
            elif choice == "F" or choice == "f":
                field[int(choice_list[2])][int(choice_list[1])] = "F"
            elif choice == "E" or choice == "e":
                if field[int(choice_list[2])][int(choice_list[1])] == "O":
                    print("That spot doesn't have a flag!")
                else:
                    field[int(choice_list[2])][int(choice_list[1])] = "O"
        except IndexError:
            end = time.clock()
            time_total = end - start
            end_game = 2
            break
    return (round(time_total), end_game)
        
def record_time(game_results):
    import datetime
    now = datetime.datetime.now()
    current_time = str(now.time())
    time_list = current_time.split(':')
    current_time = "{}:{}"
    current_time = current_time.format(time_list[0], time_list[1])
    if str(game_results[1]) == "1":
        date = "{},{},{} {}: Victory in {}."
        with open('Minesweeper_Statistics.txt', mode='a') as target:
            target.write(date.format(now.day, now.month, now.year, current_time, datetime.timedelta(seconds=game_results[0])))
            target.write("\n")
    elif str(game_results[1]) == "0":
        date = "{},{},{} {}: Loss in {}."
        with open('Minesweeper_Statistics.txt', mode='a') as target:
            target.write(date.format(now.day, now.month, now.year, current_time, datetime.timedelta(seconds=game_results[0])))
            target.write("\n")
    else:
        date = "{},{},{} {}: Quit after {}."
        with open('Minesweeper_Statistics.txt', mode='a') as target:
            target.write(date.format(now.day, now.month, now.year, current_time, datetime.timedelta(seconds=game_results[0])))
            target.write("\n")
 
def print_statistics(): 
    print(" ")
    try:
        with open('Minesweeper_Statistics.txt') as target:
            print(target.read())
    except FileNotFoundError:
        print("No games have been played yet!")
        print(" ")
        
def main():    
    while True:
        choice = main_menu()
        if choice == 1: 
            field_info = create_field()
            game_results = game(field_info[0], field_info[1], field_info[2], field_info[3])
            record_time(game_results)
        elif choice == 2:
            print_statistics()
        else:
            print("GOOD BYE")
            break
        
main()