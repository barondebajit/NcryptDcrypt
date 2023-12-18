#Imports
import pyfiglet
import curses
import math
import random

#Initialization
window = curses.initscr()
window.keypad(True)
curses.cbreak()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

#Variables
red = curses.color_pair(1)
green = curses.color_pair(2)
bannertext="Ncrypt/Dcrypt"
banner=pyfiglet.figlet_format(text=bannertext)
garbage=["!","@","#","$","%","^","&","*"]
garbagelen=len(garbage)

#Functions
def NumFactors(a,b):
    count=1
    num = a if a<b else b
    for i in range(2,num+1):
        if a%i==0 and b%i==0:
            count+=1
    return count

def Encrypt(message):
    cipher=""
    msglen=len(message)
    a=random.randint(2,200)
    b=random.randint(4,400)
    key=str(a*b)+"-"+str(a)
    cipher+=garbage[(a*b)%garbagelen]
    for i in range(msglen):
        if message[i].isalpha():
            if message[i] in "aeiouAEIOU":
                cipher+=str(math.factorial(i+1))
                if message[i].isupper():
                    cipher+=chr((ord(message[i])+a*b-65)%26+65)
                elif message[i].islower():
                    cipher+=chr((ord(message[i])+a*b-97)%26+97)
            else:
                cipher+=str(NumFactors(a,b))
                cipher+=str(random.randint(a,a+b))
                cipher+=message[i]
        elif message[i].isdigit():
            cipher+="~"
            if int(message[i])%2==0:
                cipher+=str(int(message[i])+a+b)
            else:
                cipher+=str(abs(int(message[i])-a-b))
        elif message[i]==" ":
            cipher+=";"
        cipher+=garbage[random.randint(0,garbagelen-1)]
    return cipher, key

def Decrypt(cipher,key):
    message=""
    temp=0
    part,a=key.split("-")
    a=int(a)
    b=int(int(part)/int(a))
    while cipher[temp] not in garbage:
        temp+=1
    cipher=cipher[temp+1::]
    temp=len(cipher)-1
    while cipher[temp] not in garbage:
        temp-=1
    cipher=cipher[:temp+1]
    uniquelist=[]
    while True:
        if len(cipher)==0 or cipher=="":
            break
        temp=0
        unique=""
        while cipher[temp] not in garbage:
            unique+=cipher[temp]
            temp+=1
        uniquelist.append(unique)
        cipher=cipher[temp+1::]
    l=[]
    for i in uniquelist:
        if len(i)!=0:
            l.append(i)
    uniquelist=l
    for i in range(len(uniquelist)):
        element=uniquelist[i]
        if element[-1].isalpha():
            if element[:len(element)-1]==str(math.factorial(i+1)):
                if element[-1].isupper():
                    message+=chr((ord(element[-1])-a*b-65)%26+65)
                else:
                    message+=chr((ord(element[-1])-a*b-97)%26+97)
            else:
                message+=element[-1]
        elif element==";":
            message+=" "
        else:
            number=int(element[1::])
            if number<a+b:
                message+=(str(a+b-number))
            else:
                message+=(str(number-a-b))
    return message

def clean(text):
    i=0
    while text[i]!="'":
        i+=1
    text=text[i+1:]
    text=text.rstrip("'")
    return text

def display_menu(window,MENU_TEXT,MENU_OPTIONS,INFO_OPTIONS):
    selectedIndex = 0

    while True:
        window.clear()
        curses.curs_set(0)
        window.addstr(MENU_TEXT, green)
        for i in range(len(MENU_OPTIONS)):
            window.addstr('>',red if i == selectedIndex else green)
            window.addstr(MENU_OPTIONS[i] + '\n', red if i == selectedIndex else green)

        window.addstr(INFO_OPTIONS[selectedIndex],green)

        c = window.getch()
        if c == curses.KEY_UP or c == curses.KEY_LEFT:
            selectedIndex = (selectedIndex - 1 + len(MENU_OPTIONS)) % len(MENU_OPTIONS)
        elif c == curses.KEY_DOWN or c == curses.KEY_RIGHT:
            selectedIndex = (selectedIndex + 1) % len(MENU_OPTIONS)
        elif c == curses.KEY_ENTER or chr(c) in '\r\n':
            return selectedIndex
        else:
            window.addstr("\nThe pressed key '{}' {} is not associated with a menu function.\n".format(chr(c), c))
            window.getch()

#Menu Variables
MAIN_MENU = [
    'Encrypt',
    'Decrypt',
    'Exit',
]
MAIN_OPTIONS = [
    'Encrypt a message using the encrypter',
    'Decrypt a cipher using the decrypter',
    'Exit the program'
]
EXIT_MENU = [
    'Exit',
    'Return'
]
EXIT_OPTIONS = [
    'Exit the program',
    'Return to Menu'
]

#Main
if __name__ == '__main__':
    ext=1
    while ext:
        mainchoice=display_menu(window,banner,MAIN_MENU,MAIN_OPTIONS)
        if mainchoice==0:
            window.clear()
            window.addstr(banner,green)
            window.addstr("Enter the message: ",green)
            message=str(window.getstr())
            message=clean(message)
            result,key=Encrypt(message)
            window.addstr("Cipher: ",green)
            window.addstr(result,red)
            window.addstr("\n",red)
            window.addstr("Key: ",green)
            window.addstr(key,red)
            window.addstr("\n",red)
            window.addstr("Press any key to continue",green)
            window.getch()
        elif mainchoice==1:
            window.clear()
            window.addstr(banner,green)
            window.addstr("Enter the cipher: ",green)
            cipher=str(window.getstr())
            window.addstr("Enter the key: ",green)
            key=str(window.getstr())
            cipher=clean(cipher)
            key=clean(key)
            try:
                result=Decrypt(cipher,key)
                window.addstr(result,red)
            except:
                window.addstr("Invalid cipher",red)
            window.addstr("\n",red)
            window.addstr("Press any key to continue",green)
            window.getch()
        else:
            extchoice=display_menu(window,banner,EXIT_MENU,EXIT_OPTIONS)
            if extchoice==0:
                ext=0
                curses.endwin()
                break
            else:
                continue
