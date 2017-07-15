from tkinter import *
import random
import time
import winsound
soundfile = "AKB48 - Sugar Rush.wav"
root = Tk()
platform = [{'x': -1, 'y': -1, 'length': -1},
            {'x': -1, 'y': -1, 'length': -1},
            {'x': -1, 'y': -1, 'length': -1},
            {'x': -1, 'y': -1, 'length': -1},
            {'x': -1, 'y': -1, 'length': -1}]
block_xposition = -1
block_yposition = -1
move = 0
lose = 0
level = 1
resetIndex = 0
w = Canvas(root, width=1234, height=595, bg='black')
w.pack(expand = NO, fill = BOTH)
gif1 = PhotoImage(file = 'bkg.gif')
photo = PhotoImage(file = 'fftgame_over_screen.png')
w.create_image(618, 300, image = gif1)

def random_platforms(y,length):
    global level
    w.delete("all")
    w.create_image(618, 300, image=gif1)
    w.grid(row=0, column=0)
    level_label = Label(root, text="Level:  " + str(level), anchor="nw", font=2)
    level_label.grid(row=0, column=0, sticky=NW)
    x = 10
    for i in range(0, len(platform)):
        platform[i]['x'] = x
        platform[i]['y'] = y
        platform[i]['length'] = length
        if i != 4:
            w.create_rectangle(x, y, x + length, y + 10, fill="green")
        else:
            w.create_rectangle(x, y, x + length, y + 10, fill="aqua")
        x += 250
        if x >= 1050:
            break
        y += random.randint(-250, 200)
        if y > 550:
            y -= 200
        elif y < 100:
            y += 200
        length = random.randint(10, 100)
    return y, length

def key(event):
    global move
    if event.char is 'd':
        move = 1
    elif event.char is 'a':
        move = 2
    elif event.char is 'w':
        move = 3

def moving():
    global move
    global block_xposition
    global block_yposition
    global lose
    global level
    block_xposition = 10
    block_yposition = platform[0]['y'] - 5
    rainbow = level % 5
    if rainbow == 0:
        foreground = w.create_oval(block_xposition, block_yposition - 12, block_xposition + 16, block_yposition + 4, fill="red")
    elif rainbow == 1:
        foreground = w.create_oval(block_xposition, block_yposition - 12, block_xposition + 16, block_yposition + 4, fill="black")
    elif rainbow == 2:
        foreground = w.create_oval(block_xposition, block_yposition - 12, block_xposition + 16, block_yposition + 4, fill="white")
    elif rainbow == 3:
        foreground = w.create_oval(block_xposition, block_yposition - 12, block_xposition + 16, block_yposition + 4, fill="violet")
    else:
        foreground = w.create_oval(block_xposition, block_yposition - 12, block_xposition + 16, block_yposition + 4, fill="yellow")
    w.grid(row=0, column=0)
    i = 0
    speed_x = 0
    speed_y = 0
    acc_x = 0
    acc_y = 0
    q=0
    done = 0
    while True:
        w.bind("<Key>", key)
        if move == 1:
            acc_x = 0.2
            move = 0
        elif move == 2:
            acc_x = -0.2
            move = 0
        else:
            acc_x = 0
        if move == 3 and q == 0:
            q = 1
            acc_y = -2
            move = 0
        else:
            acc_y = 0.01
        for i in range(0, len(platform)):
            #if we are about to hit a platform
            if block_xposition >= platform[i]['x'] -8 and block_xposition <= (platform[i]['x'] + platform[i]['length']) and block_yposition < platform[i]['y'] + 5 and block_yposition + speed_y >= platform[i]['y'] - 5:
                speed_y = -(speed_y)
                break
            if block_xposition >= platform[4]['x'] -8 and block_xposition <= (
                platform[4]['x'] + platform[4]['length']) and block_yposition < platform[4][
                'y'] + 5 and block_yposition + speed_y >= platform[4]['y'] - 5:
                done = 1
                level += 1
                break
            if block_xposition <=0:
                speed_x = -(speed_x-7)
            elif block_xposition >= 1234-12:
                speed_x = -(speed_x+7)
            if block_yposition <= 12:
                speed_y = -speed_y
        if done is 1:
            break
        if block_yposition >= 595:
            lose = 1
            break
        w.move(foreground, speed_x, speed_y)
        block_xposition += speed_x
        block_yposition += speed_y
        if speed_x > 0:
            speed_x = max(speed_x - 0.005, 0)
        if speed_x < 0:
            speed_x = min(speed_x + 0.005, 0)
        speed_x = min(speed_x + acc_x, 1)
        speed_x = max(speed_x + acc_x, -1)
        if q==0 and block_xposition >= platform[0]['x'] -8 and block_xposition <= (platform[0]['x'] + platform[0]['length']):
            pass
        else:
            speed_y +=acc_y
        time.sleep(0.01)
        w.grid(row=0, column=0)
        root.update()

def retry():
    global retryIndex
    global lose
    global level
    retryIndex = 1
    lose = 0
    level=1

def quitGame():
    #Closes the program
    root.destroy()
    exit(0)
retry = Button(root, text="Retry", command=retry, bg="black", fg="white" , bd=0)
quitGame = Button(root, text="Quit", command=quitGame, bg="black", fg="white", bd=0)

def startgame():
    winsound.PlaySound(soundfile, winsound.SND_ASYNC)
    global start_game
    global lose
    global retryIndex
    start_game = True
    y = 300
    length = 100
    option_1.grid_forget()
    while start_game is True:
        [y, length] = random_platforms(y, length)
        moving()
        root.update()
        if lose == 1:
            w.delete('all')
            retryIndex = 0
            w.create_image(618, 300, image=photo)
            w.grid(row=0, column=0)
            retry.grid(row=0, column=0, sticky=N)
            quitGame.grid(row=0, column=0, sticky=S)
            while True:
                root.update()
                if retryIndex == 1:
                    y = 300
                    length = 100
                    retry.grid_forget()
                    quitGame.grid_forget()
                    break

start_game = False
w.focus_set()
w.delete('all')
w.create_image(618, 300, image = gif1)
w.grid(row=0, column=0)
option_1 = Button(root, text="Start Game", bg = 'blue', fg = 'violet',
                        activebackground = 'black', activeforeground = 'white',
                  command = startgame )
option_1.grid(row=0, column=0)
root.mainloop()
