import requests, json

#a function to remove duplicate serial numbers in a list
def remove(duplicate): 
    result = []
    for item in duplicate: 
        if item not in result: 
            result.append(item) 
    return result

#get data needed from firebase
url = 'https://inf551-f307e.firebaseio.com/restaurants.json'
url2 = 'https://inf551-f307e.firebaseio.com/index.json'
restaurants = requests.get(url).json()
index = requests.get(url2).json()

#a function to find serial_numbers of restaurants which have name contained at least one of the keywords from user input
def search(keyword_list):
    serial_no_ls = []
    for keyword in keyword_list:
        keyword = keyword.lower()
        try: serial_no_ls.extend(index[keyword])
        except: continue
    if len(serial_no_ls) == 0: result = None #if no keyword found, return None
    else: result = remove(serial_no_ls)
    return result

#a function to obtain names and scores of restaurants found in the previous function
def get_restaurant_info(keyword_list):
    search_result_d = {}
    serial_no_ls = search(keyword_list)
    
    #if at least one restaurant found, print restaurant's name and score
    if serial_no_ls is not None:
        for serial_no in serial_no_ls:
            search_result_d[serial_no] = restaurants[serial_no]
        result = json.dumps(search_result_d)
        print(json.dumps(search_result_d, indent=4), len(search_result_d))
    else: 
        #if no restaurant's name contain the keywords, print notification and return None
        result = None
        print('Sorry, no restaurant found!') 
    return result
    
#get keywords from user
import sys
keywords = sys.argv[1:]
keyword_list = keywords[0].split(' ')
if len(keyword_list) == 0 : print('Please enter some keywords!')
else: get_restaurant_info(keyword_list)