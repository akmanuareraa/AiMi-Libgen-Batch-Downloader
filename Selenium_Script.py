#modules needed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import urllib.parse as urlparse
from urllib.parse import parse_qs
import wget
import os

#choosing chrome as my browser
driver = webdriver.Chrome() 

#instructions
print(
    '\nIMPORTANT:'
    '\n-----------------------------------------------------------------------------------------------------------------------'
    '\n     *This is Batch Downloader Tool'
    '\n     *You can download either using the title of the book or Publisher name'
    '\n     *You will be able to download in the range of 25, 50 or 100 books every single time you run the script'
    '\n     *Please verify the keyword that you are going to enter with the libgen site'
    '\n     *More precise your keyword the better the results will be'
    '\n     *This script will automatically download books starting from the most latest book to old ones based on the upload time'
    '\n-----------------------------------------------------------------------------------------------------------------------'
)


#to let the program know whether to look for publisher or title

#a variable with any non-zero variable
random_variable_1 = 5
while random_variable_1 != 0:

    #getting input
    search_mode_toggle = int(input("\n\nAre you going to search Publisher wise(1) or Title wise(2): "))

    #sanitizing the input
    if (search_mode_toggle == 1):
        z = 1
        search_mode = 'publisher'
        break
    elif (search_mode_toggle ==2):
        z = 1
        search_mode = 'title'
        break
    else:
        print("\nPlease enter valid response - 1 or 2.")
        continue

#geting the search term 
search_term = input("\nEnter the search term: ")

#to get the total number of books you need

#a variable with non-zero value
random_variable_2 = 5

#sanitizing the input
while random_variable_2 != 0:
    item_count  = int(input('\nHow many books would you like to download?' 
                        '\n(Please enter in multiples of 25)' 
                        '\n(Values must be equal to or greater than 25)'
                        '\n\nEnter Value: '
    ))
    if item_count%25 == 0:
        x = 1
        break
    else:
        print("Please enter valid input (only multiples of 25)")
        continue
#NOTE: I have particularly mentioned "25" because the result page displays a 
#minimum of 25 results per page. So to transverse between the pages, it will 
#be very much comfortable if the count is multiples of "25"

#using this total_pages variable I can iterate through the exact no. of pages using for loop
total_pages = int(item_count/25)

#this loop iterates through a single page at a time
for page in range(1,total_pages+1):
    
    #binding the url along with the search term and search mode to get the exact url
    url = 'http://libgen.rs/search.php?&res=25&req=' + str(search_term) + '&phrase=1&view=detailed&column=' + str(search_mode) + '&sort=year&sortmode=DESC&page=' + str(page)
    
    #drivers navigates to the mentioned url
    driver.get(url)

    #arrays are created to store the links, names and extension of the books
    download_link_array = [0]
    name_array = [0]
    extension_array = [0]

    #this loop iterates through the available books in that particular page to gather the data
    #and append it to the respective array
    #the loop starts from 4 because the very first item(book) in the result page is located in 
    #4th table. So 4+25(total results) = 29
    for i in range(4, 29):

        #a link is merged everytime to iterate between the multiple tables. Because each
        #book is listed in a seperate table tag.
        table_path_merge = "/html/body/table" + "[" + str(i) + "]" + "/tbody/tr[2]/td[3]/b/a"

        #getting the link of the particular page
        link = driver.find_element_by_xpath(table_path_merge).get_attribute('href')

        #getting the format of the file
        extension_1 = '/html/body/table[' + str(i) + ']/tbody/tr[10]/td[4]'

        #getting the text alone
        extension = driver.find_element_by_xpath(extension_1).text

        #merging the md5 hash obtained from the previous url along with the main url
        parsed = urlparse.urlparse(link)
        md5_hash = parse_qs(parsed.query)['md5']
        download_link = "http://library.lol/main/" + str(md5_hash[0])
        download_link_array.append(download_link)
        name = driver.find_element_by_xpath(table_path_merge).text
        name_array.append(name)
        extension = str(extension)
        extension_array.append(extension)

    #now that all the data has been appended into the array, this loopp will iterate through
    #contents in the array
    for i in range(1,26):
        print('\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print("S.No: " + str(i))
        print(name_array[i])

        #navigating to the link
        driver.get(download_link_array[i])

        #getting the link for downloading
        get_link = driver.find_element_by_xpath('//*[@id="info"]/h2/a').get_attribute('href')

        print('Downloading.......' + str(i) + '/25')
        print(get_link)

        #here two different downloading methods are used. If one is facing the error the other 
        #can download
        try:
            filename = wget.download(get_link)
        except:
            try:
                alt_link = "powershell.exe wget.exe " + str(get_link)
                os.system(alt_link)
            except:
                print("Something went wrong. Skipping the download")
