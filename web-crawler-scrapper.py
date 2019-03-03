import requests
from bs4 import BeautifulSoup
import re
import sys
from prettytable import PrettyTable
from colorama import Fore, Back, Style, init
init()

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


#----------------------------------------------------------------------------------------function for extracting live score--------------------
def live_score(soup):
    soup = soup.find("div",{"class":"cb-mini-col"}).get_text()
    return (soup)
#-------------------------------------------------------------------------------------------END OF LIVE_SCORE----------------------------

#----------------------------------------------------------------------------------------Function to extract scorecard------------------------------
def scorecard(soup):
    soup_1 = soup.find("div",{"class":"cb-scrd-lft-col"}).findAll("div",{"class":"cb-ltst-wgt-hdr"})

    #-------------------------------------Batsman 1 Table----------------------------------------------
    soup = soup_1[0].get_text()
    soup = re.findall(r"([a-zA-Z\s()&\/]*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\.\d*)",soup[soup.index('SR')+2:])
    table = PrettyTable(['Batsman','R','B','4s','6s','SR'])
    for i in soup:
        table.add_row(i)
    print(table)

    #--------------------------------------Batsman 2 Table -------------------------------------------
    soup = soup_1[3].get_text()
    soup = re.findall(r"([a-zA-Z\s()&\/]*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\.\d*)",soup[soup.index('SR')+2:])
    table = PrettyTable(['Batsman','R','B','4s','6s','SR'])
    for i in soup:
        table.add_row(i)
    print(table)

    #-------------------------------------Bowler 1 Table -----------------------------------------------------
    soup = soup_1[1].get_text()
    soup = re.findall(r"([a-zA-Z\s()&\/]*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\.\d+)",soup[soup.index('ECO')+3:])
    table = PrettyTable(['Bolwer','O','M','R','W','NB','WD','ECO'])
    for i in soup:
        table.add_row(i)
    print(table)

    #---------------------------------------Bowler 2 Table --------------------------------------------------------
    soup = soup_1[4].get_text()
    soup = re.findall(r"([a-zA-Z\s()&\/]*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\s*)(\d+\.\d+)",soup[soup.index('ECO')+3:])
    table = PrettyTable(['Bolwer','O','M','R','W','NB','WD','ECO'])
    for i in soup:
        table.add_row(i)
    print(table)

    #-------------------------------------------------------------------------------------------------------------END OF SCORECARD-----------------------------
    

#-----------------------------------------------------------------------------------------------------MAIN FUNCTION-----------------------------------------
if __name__ == "__main__":    
    page_url = "/cricket-match/live-scores"
    soup = browse(page_url)
    ab = soup.findAll("div",{"class":"cb-col cb-col-100 cb-lv-main"})
    #print(ab)
    global links
    global data
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
    j=1

     #---------------user menu -1 --------------------------------------------------------
    print(Fore.MAGENTA + Style.DIM+"\n\n**************************************************")
    print("-------------------User Menu----------------------")
    print("**************************************************\n"+Style.RESET_ALL+Fore.BLUE+Style.BRIGHT)
    for i in links:
        print (j,end=" ")
        print(i)

        j+=1   
    print (Style.RESET_ALL + Fore.RED + Style.BRIGHT+"0 Exit"+Style.RESET_ALL)   
    user = int(input("\nEnter match number from the above list : "))
    if user == 0:
        print (Fore.RED+Style.BRIGHT+"\nExiting.......\n"+Style.RESET_ALL)
        sys.exit()
    elif user not in range(1,j):
        print (Fore.RED+Style.BRIGHT+"\nYou entered a invalid match number\n"+Style.RESET_ALL)
    else:
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
        if user_1 in range(1,3):

            if user_1 == 1:
                soup = browse(data[user][user_1-1])
                soup = live_score(soup)
                #live_score(soup)            
                #print (data[user][user_1-1])
                print (soup)
            elif user_1 == 2:
                soup = browse(data[user][user_1-1])
                scorecard(soup)
                
                #print (soup)
            
    #print(soup.prettify())
#-----------------------------------------------------------------------------------------------------------END--------------------------