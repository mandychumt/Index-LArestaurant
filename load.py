import pandas as pd
import requests,json,sys

#get file name from user

if len(sys.argv[1:]) == 0 : print('Please enter a csv file name!')
elif sys.argv[1][-4:] != '.csv' : print('Please enter a valid csv file!')
else:
    
    file_name = sys.argv[1]
    
    #a function to load data from a csv file
    def get_data_from_csv(file_name):
        data = pd.read_csv(file_name, index_col ="serial_number")[['facility_name', 'score']]
        return data.to_dict(orient='index')

    #get data from a csv file
    restaurant_d = get_data_from_csv(file_name)

    #change the score from integer to string
    for serial_no in restaurant_d:
        restaurant_d[serial_no]['score'] = str(restaurant_d[serial_no]['score'])

    #load restaurant data into firebase
    url = 'https://inf551-f307e.firebaseio.com/restaurants.json'
    restaurant_d_json = json.dumps(restaurant_d)
    requests.put(url, restaurant_d_json)

    #create an inverted index for facility_name
    punctuations = '\'"-&/.,~+?!$:=%;#@()<>'
    index_d = {}
    for serial_no in restaurant_d:
        facility_name = restaurant_d[serial_no]['facility_name']
        #remove all punctuations in each facility name and lowercase
        for punctuation in punctuations:
            facility_name = facility_name.replace(punctuation, '')
        facility_name = facility_name.lower()
    
        #create a dictionary to store unique words and corresponding serial_number
        #key:word  value:list of serial_numbers of restaurants which have name contained this word
        word_list = facility_name.split(' ')
        for word in word_list:
            if len(word) == 0: continue
            elif index_d.get(word,0) == 0: index_d[word] = [serial_no,]
            else: index_d[word].append(serial_no)

    #load index into firebase
    url2 = 'https://inf551-f307e.firebaseio.com/index.json'
    index_d_json = json.dumps(index_d)
    requests.put(url2, index_d_json)

    print(json.dumps(index_d, indent=4))