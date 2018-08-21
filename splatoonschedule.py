from lxml import html
import requests
import datetime

def format_datetime(data):
    date, time = data.split(" ")
    new_time =convert_to_bst(time)

    month, day = date.split("/")

    if "am" in new_time and "pm" in time: 
        day = int(day) + 1
        if day > 31:
            month = int(month) + 1
            if month > 10:
                month = "0" + str(month)
            day = day - 31

    return (new_time + " " + str(day) + "-" + str(month)+ "-" + str(datetime.datetime.now().year))
 
    

def convert_to_bst(time):
    if "am" in time: 
        time = int(time.strip("am")) + 8
    elif "pm" in time: 
        time = int(time.strip("pm")) + 20
    
    if time < 12:
        time = (str(time)+ "am")
    elif time > 12   and time < 24 :
        time = time - 12

        time = (str(time)+ "pm")   
    else:
        time = time - 24
        time = (str(time)+ "am")
    return time

def format_post(start, end, maps, weapons):
    """
    Formats the post to make it more human readable
    """
    return('Start Date: {0} \nEnd Date: {1} \nMap: {2} \nWeapons: {3}'.format(start, end, maps, weapons))

def get_updates():
    page = requests.get('https://twitter.com/grizzcoemployee?lang=en')
    tree = html.fromstring(page.content)

    tweet = tree.xpath('//p[@class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"]/text()')[1]
    parts = tweet.split(". ")

    start,end = parts[0].split("-")

    start = format_datetime(start)
    end = format_datetime(end)

    f = open("splatoon2/eta_time", "w")
    f.write(start + "//" + end)

    return (format_post(start, end, parts[1], parts[2]))
