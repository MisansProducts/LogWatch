#Made by Alex

#======Libraries======
import tkinter as tk
import tkinter.ttk as ttk
import time
from datetime import datetime

#======Main Window======
MainWindow = tk.Tk()
MainWindow.title("Masturbation Prevention") #Window title
MainWindow.configure(background = "#ff0000") #Window background color
MainWindow.geometry("720x480") #Resolution
MainWindow.resizable(0,0) #Disables resizing

#======Variables======
TotalTime = 0 #Total time in seconds
s, m, h, d = 0, 0, 0, 0 #Units of time
bg_color = "#ff0000" #Background color
fg_color = "#0080ff" #Foreground color
ColorRed, ColorGreen, ColorBlue = 255, 0, 0 #RGB values
ColorFlag = 0 #Flag to stop changing colors
file_contents = [] #Contents of the file
score, hscore = 0, 1 #Score and high score
privileges_dict = {} #Creates a dictionary for optional privileges
PrivilegesFlag = 0 #Flag to use privileges

#======Load File======
try: #Tries to find and open file
    with open('masturbation_prevention_info.txt', 'r') as f: #Opens file in read mode
        file_contents = f.readlines() #Puts file contents into a list
except: #Creates file
    with open('masturbation_prevention_info.txt', 'a') as f: #Opens file in append mode
        f.write("======Last Time Masturbated======\n")
        f.write(f"{time.time()}\n") #1 - Last time
        f.write("======Exact Date======\n")
        f.write(f"{datetime.now()}\n") #3 - Last date
        f.write("======High Score======\n")
        f.write("1\n") #5 - High Score
        f.write("======Privileges======\n")
        f.write("\n") #7 - Privileges (Leave empty if none)
        f.write("privileges_end\n") #n - End of privileges
        f.write("======Other Dates Masturbated======") #k - Recent dates

    with open('masturbation_prevention_info.txt', 'r') as f: #Opens file in read mode
        file_contents = f.readlines() #Puts file contents into a list
else: #After opening file
    TotalTime = int(float(time.time()) - float(file_contents[1])) #Total time in seconds calculated
    score, hscore = int((float(time.time()) - float(file_contents[1])) ** 0.5), int(file_contents[5]) #Calculates score and sets high score
    if score >= hscore: #Checks if there is a new high score
        hscore = score #Prevents score from being greater than high score (causes problems with color values if ratio is greater than 1)

#======Functions======
def update_stopwatch(temp = 0): #Updates the stopwatch
    global TotalTime, s, m, h, d

    TotalTime += 1
    s = TotalTime % 60
    m = (TotalTime // 60) % 60
    h = (TotalTime // 3600) % 24
    d = TotalTime // 86400

    counter_string = "" #Grammar correction

    if d == 1: #Days concatenation
        counter_string += f"{d} Day, "
    else:
        counter_string += f"{d} Days, "
    if h == 1: #Hours concatenation
        counter_string += f"{h} Hour, "
    else:
        counter_string += f"{h} Hours, "
    if m == 1: #Minutes concatenation
        counter_string += f"{m} Minute, "
    else:
        counter_string += f"{m} Minutes, "
    if s == 1: #Seconds concatenation
        counter_string += f"and {s} Second"
    else:
        counter_string += f"and {s} Seconds"
        
    counter.config(text = counter_string) #Updates counter text
    
    if temp == 0:
        MainWindow.after(1000, update_stopwatch) #Loops function

def update_color(): #Updates the color
    global ColorRed, ColorGreen, ColorBlue, ColorFlag, hscore, score

    color = int(510 * (score / hscore)) #Choosing a color between (255, 0, 0) and (0, 255, 0)

    if color <= 255: #Variable is less than half of its potential
        ColorRed = 255 #Red is max
        ColorGreen = color #Green is variable
    elif color >= 255: #Variable is more than half of its potential
        ColorRed = 510 - color #Red is variable
        ColorGreen = 255 #Green is max
    
    if ColorFlag != 1: #Flag to change color
        c_hex = '#%02x%02x%02x' % (ColorRed, ColorGreen, ColorBlue) #Hex color calculation

        #Changes backgrounds of all widgets to the new color
        MainWindow.configure(background = c_hex)
        TopFrame.config(bg = c_hex)
        current_score.config(bg = c_hex)
        high_score.config(bg = c_hex)
        BottomFrame.config(bg = c_hex)
        counter_before_label.config(bg = c_hex)
        counter.config(bg = c_hex)
        counter_after_label.config(bg = c_hex)
        counter_reset.config(activebackground = c_hex, bg = c_hex)
        if PrivilegesFlag == 1:
            privileges_label.config(bg = c_hex)
            for privilege in privileges_dict:
                privileges_dict[privilege].config(bg = c_hex)

        MainWindow.after(250, update_color) #Loops function

def update_score(temp = 0): #Updates the current and high score
    global score, hscore, file_contents

    score = int((float(time.time()) - float(file_contents[1])) ** 0.5) #Calculates score
    
    if score >= hscore: #New high score
        hscore = score #Sets high score
        current_score.config(text = "") #User interface accessory
        high_score.config(text = f"New High Score: {hscore}") #Updates label
        if PrivilegesFlag == 1:
            privileges_label.pack_forget() #Gets rid of privileges label
    elif score < hscore: #Old high score
        current_score.config(text = f"Score: {score}") #Updates label
        high_score.config(text = f"High Score: {hscore}") #Updates label

    if hscore > int(file_contents[5]): #Only waste resources on opening files if a change was made to high score
        try: #Handling any potential errors
            with open('masturbation_prevention_info.txt', 'a') as f: #Opens file in append mode
                file_contents[5] = f"{hscore}\n"
                f.seek(0) #Sets stream at the beginning of the file
                f.truncate() #Deletes everything in the file
                f.writelines(file_contents) #Writes each element from the list as lines in the file
        except: #Error opening file
            print("Error opening masturbation_prevention_info.txt") #Prints error

    #Calculates privileges as a bonus
    if PrivilegesFlag == 1:
        x = int(len(privileges_dict) * (score / hscore)) #Chooses the amount of specific privileges to forget corresponding to the score to high score percentage
        for i in range(1, x + 1): #Loops from 1 to the amount of specific privileges
            privileges_dict[f"privileges_label_{i}"].pack_forget() #Forgets specifc privileges

    if temp == 0: #Temporary flag to not loop
        MainWindow.after(1000, update_score) #Loops function

def reset_time(): #Resets the time
    global file_contents, TotalTime, ColorRed, ColorGreen, ColorFlag, score

    file_contents[3] = file_contents[3].strip('\n') #Strips the return at the end of the exact date
    file_contents.append(f"\n{file_contents[3]}") #Appends the exact date at the end of the file
    del file_contents[1], file_contents[2] #Deletes the old time and exact date
    file_contents.insert(1, f"{time.time()}\n"), file_contents.insert(3, f"{datetime.now()}\n") #Writes the new time and exact date

    try: #Handling any potential errors
        with open('masturbation_prevention_info.txt', 'a') as f: #Opens file in append mode
            f.seek(0) #Sets stream at the beginning of the file
            f.truncate() #Deletes everything in the file
            f.writelines(file_contents) #Writes each element from the list as lines in the file
    except: #Error opening file
        print("Error opening masturbation_prevention_info.txt") #Prints error
    else: #After opening file
        TotalTime = 0 #Sets total time to 0
        ColorRed = 255 #Sets red to max
        ColorGreen = 0 #Sets green to min
        ColorFlag = 0 #Flags color changing to 0
        score = 0 #Sets score to 0
        if PrivilegesFlag == 1: #Checks if privileges label is necessary
            privileges_label.pack() #Repacks privileges label
            for i in range(1, len(privileges_dict) + 1): #Goes through the privileges dictionary
                privileges_dict[f"privileges_label_{i}"].pack() #Repacks specific privileges
        update_score(1) #Updates score with a temporary flag parameter
        update_color() #Updates color
        update_stopwatch(1) #Updates stopwatch with a temporary flag parameter

#======Top frame======
TopFrame = tk.Frame(MainWindow, bg = bg_color)
TopFrame.pack(fill = "both")

current_score = tk.Label(TopFrame, text = f"Score: {score}", fg = fg_color, bg = bg_color, font = "Impact 22") #Current Score Label
current_score.pack(side = tk.LEFT)

high_score = tk.Label(TopFrame, text = f"High Score: {score}", fg = fg_color, bg = bg_color, font = "Impact 22") #High Score Label
high_score.pack(side = tk.RIGHT)

#======Bottom frame======
BottomFrame = tk.Frame(MainWindow, bg = bg_color)
BottomFrame.pack(fill = "both")

counter_before_label = tk.Label(BottomFrame, text = "It has been", fg = fg_color, bg = bg_color, font = "Impact 24") #Before Counter
counter_before_label.pack()

counter = tk.Label(BottomFrame, text = f"{d} Days, {h} Hours, {m} Minutes, and {s} Seconds", fg = fg_color, bg = bg_color, font = "Impact 28") #Counter
counter.pack()

counter_after_label = tk.Label(BottomFrame, text = "since you last masturbated.", fg = fg_color, bg = bg_color, font = "Impact 22") #After Counter
counter_after_label.pack()

counter_reset = tk.Button(BottomFrame, text = "Masturbated?", activeforeground = fg_color, activebackground = bg_color, fg = fg_color, bg = bg_color, font = "Impact 22", command = reset_time) #Reset Button
counter_reset.pack()

for line in range(7, len(file_contents)): #Goes through each line in file contents list from 7 to n to check for optional privileges
    if file_contents[line] == "privileges_end\n": #Checks if line is n
        break #Stops writing in dictionary
    elif file_contents[line] == "\n": #Checks if line is whitespace
        continue #Ignores whitepsace
    else: #There are privileges to write
        privileges_dict[f"privileges_label_{line - 6}"] = tk.Label(BottomFrame, text = file_contents[line].strip("\n"), fg = fg_color, bg = bg_color, font = "Impact 16") #Specific Privilege
if privileges_dict: #Checks if privileges label is necessary
    PrivilegesFlag = 1 #Sets flag
    privileges_label = tk.Label(BottomFrame, text = "You are not allowed to:", fg = fg_color, bg = bg_color, font = "Impact 20") #Privileges
    privileges_label.pack() #Packs privileges label
    for privilege in privileges_dict: #Goes through specific privileges
        privileges_dict[privilege].pack() #Packs specific privileges

#======Commands======
update_stopwatch() #Updates stopwatch
update_color() #Updates color
update_score() #Updates score

#======Main Window Loop======
MainWindow.mainloop()