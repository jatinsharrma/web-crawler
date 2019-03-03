import re
import sys
from time import sleep
#----------------------------------------------------------------------------------------importing extra modules-----------------------------

try:
    from prettytable import PrettyTable
except:
    print ("Pretty table module is not installed in your working environment.")

try: 
    import requests
except:
    print("Requests module is not installed in your working environment.")

try:
    from bs4 import BeautifulSoup
except:
    print("Beautiful Soup module is not installed in your working environment.")

try:
    from colorama import Fore, Back, Style, init, deinit
    init()
except:
    print("Colorama module is not installed in your working environment.")



#-------------------------------------------------------------------------------------function handles get request----------------
def browse(page_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = ("https://www.cricbuzz.com"+page_url)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
        #print(r.text)
    except requests.exceptions.HTTPError as e:
        print ("Error occured while fetching the page")
#------------------------------------------------------------------------------------------END OF BROWSE----------------------------

#------------------------------------------------------------------------------------------Timer function--------------------------
def time_expired():
    
    page_url = "/cricket-match/live-scores"
    soup = browse(page_url)
    ab = soup.findAll("div",{"class":"cb-col cb-col-100 cb-lv-main"})
    links =[]
    data = {}
    curr_score = []    
    j=1

    for i in ab:
        b = i.find("a",{"class":"text-hvr-underline text-bold"}).get_text()[:-1]        
        links.append(b)
        score = i.find("div",{"class":"cb-scr-wll-chvrn"})
        curr_score.append(score)
        temp = []

        for k in i.find("nav",{"class":"cb-col-100 cb-col padt5"}).findAll("a",href= re.compile("(.)")):
            temp.append(k.attrs['href'])
        data[j] = temp
        j+=1
    live_score(curr_score)
#------------------------------------------------------------------------------------------END OF TIME EXPIRED-----------------------------


#----------------------------------------------------------------------------------------function for extracting live score--------------------
def live_score(curr_score):
    try:
        print("[%s]\r"%curr_score[user-1].get_text() ,end="")
        sleep(10)
        time_expired()
    except KeyboardInterrupt:
        print(Fore.RED+"\n\nAborted by user. Exiting.....\n"+Style.RESET_ALL)
#-------------------------------------------------------------------------------------------END OF LIVE_SCORE----------------------------

#----------------------------------------------------------------------------------------Function to extract scorecard------------------------------
def scorecard(soup):
    soup_1 = soup.find("div",{"class":"cb-scrd-lft-col"}).findAll("div",{"class":"cb-ltst-wgt-hdr"})

    #-------------------------------------Batsman 1 Table----------------------------------------------
    print("\n")
    soup = soup_1[0].get_text()
    print(Fore.RED + Style.BRIGHT + soup[:soup.index("Batsman")] + Fore.GREEN  +Style.BRIGHT)
    soup = re.findall(r"([a-zA-Z\s()&\/]*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\.\d*)",soup[soup.index('SR')+2:])
    table = PrettyTable(['Batsman','R','B','4s','6s','SR'])

    for i in soup:
        table.add_row(i)

    print(table)

    #---------------------------------------Bowler 2 Table --------------------------------------------------------
    print("\n")
    soup = soup_1[4].get_text()
    soup = re.findall(r"([a-zA-Z\s()&\/]*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\.\d+)",soup[soup.index('ECO')+3:])
    table = PrettyTable(['Bowler','O','M','R','W','NB','WD','ECO'])

    for i in soup:
        table.add_row(i)

    print(table)

    #--------------------------------------Batsman 2 Table -------------------------------------------
    print("\n")
    soup = soup_1[3].get_text()
    print(Fore.RED + Style.BRIGHT + soup[:soup.index("Batsman")]+Fore.GREEN + Style.BRIGHT)
    soup = re.findall(r"([a-zA-Z\s()&\/]*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\.\d*)",soup[soup.index('SR')+2:])
    table = PrettyTable(['Batsman','R','B','4s','6s','SR'])

    for i in soup:
        table.add_row(i)

    print(table)

    #-------------------------------------Bowler 1 Table -----------------------------------------------------
    print("\n")
    soup = soup_1[1].get_text()
    soup = re.findall(r"([a-zA-Z\s()&\/]*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\.\d+)",soup[soup.index('ECO')+3:])
    table = PrettyTable(['Bowler','O','M','R','W','NB','WD','ECO'])

    for i in soup:
        table.add_row(i)

    print(table)
    print("\n"+Style.RESET_ALL)

    

#-------------------------------------------------------------------------------------------------------------END OF SCORECARD---------------


#-----------------------------------------------------------------------------------------------------MENU 1&2-----------------------
def menu_2(links, data,curr_score,user):
    #----------------user menu -2 --------------------------------------------------------------
        print(Fore.GREEN + Style.BRIGHT + "----------------------------------------------------------------------------")
        print("Current Score ")
        print( "----------------------------------------------------------------------------"+Style.RESET_ALL)
        print(Fore.YELLOW + Style.BRIGHT + curr_score[user-1].get_text() + Style.RESET_ALL)
        print(Fore.GREEN + Style.BRIGHT + "----------------------------------------------------------------------------"+Style.RESET_ALL)
        print(Fore.BLUE + Style.BRIGHT + "\nWhat you want to see? \n1. Live Score \n2. Scorecard  \n3. Exit" + Style.RESET_ALL)
        
        user_1 = int(input( "Enter your choice : " ))

        if user_1 == 3:
            print(Fore.RED + Style.BRIGHT + "\nExiting.....\n" + Style.RESET_ALL)
            sys.exit()

        elif user_1 in range(1,3):

            if user_1 == 1:
                #soup = browse(data[user][user_1-1])
                #soup = live_score(soup)
                live_score(curr_score) 
                sys.exit()           
                #print (data[user][user_1-1])
                #print ("Coming SOON")

            elif user_1 == 2:
                soup = browse(data[user][user_1-1])
                scorecard(soup)
                sys.exit()  
                #print (soup)
        else:
            print ("Wrong Input. Please try again")


def menu_1(links,data,curr_score):
    j=1
    global user
     #---------------user menu -1 --------------------------------------------------------
    print(Fore.MAGENTA + Style.DIM+"\n\n**************************************************")
    print("-------------------User Menu----------------------")
    print("**************************************************\n"+Style.RESET_ALL+Fore.BLUE+Style.BRIGHT)

    for i in links:
        print (j,end=" ")
        print(i)
        j+=1   

    print (Style.RESET_ALL + Fore.RED + Style.BRIGHT+"0 Exit"+Style.RESET_ALL)

    while True:
        user = int(input("\nEnter match number from the above list : "))
        if user == 0:
            print (Fore.RED+Style.BRIGHT+"\nExiting.......\n"+Style.RESET_ALL)
            sys.exit()
        elif user not in range(1,j):
            print (Fore.RED+Style.BRIGHT+"\nYou entered a invalid match number\n"+Style.RESET_ALL)
        else:
            menu_2(links, data,curr_score,user)

#---------------------------------------------------------------------------------------------------END MENU--------------------------


#-----------------------------------------------------------------------------------------------------MAIN FUNCTION-------------------
if __name__ == "__main__":    
    page_url = "/cricket-match/live-scores"
    soup = browse(page_url)
    ab = soup.findAll("div",{"class":"cb-col cb-col-100 cb-lv-main"})
    #print(ab)
    global links
    global data
    global curr_score
    links =[]
    data = {}
    curr_score = []
    
    j=1
    for i in ab:
        b = i.find("a",{"class":"text-hvr-underline text-bold"}).get_text()[:-1]        
        links.append(b)
        score = i.find("div",{"class":"cb-scr-wll-chvrn"})
        curr_score.append(score)
        temp = []

        for k in i.find("nav",{"class":"cb-col-100 cb-col padt5"}).findAll("a",href= re.compile("(.)")):
            temp.append(k.attrs['href'])
        data[j] = temp
        j+=1

    menu_1(links,data,curr_score)        
            
    #print(soup.prettify())
deinit()
#-----------------------------------------------------------------------------------------------------------END--------------------------
