from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import time


app = FastAPI()

cache_data = []
last_fetch = 0

@app.get("/news")
def get_news():
    global cache_data, last_fetch

    start =time.time()
    print("-=-=-=-= -start -=-=-",start)
    if time.time() - last_fetch >60:
        print("--=-=-= Fetch data from API -=-=--=-=-=")

        url = "https://news.ycombinator.com/"

        response = requests.get(url)
        print("-=-=-=-= -response  -=-=-",response)
        soup = BeautifulSoup(response.text,"html.parser")
        print("-=-=-=-= -soup -=-=-",soup)

        cache_data = [
            item.text for item in soup.find_all("span", class_ = "titleline")
        ]
        print("-=-=-=-= cache_data -=-=-",cache_data)

        last_fetch = time.time()
        print("-=-=-=-= last_fetch -=-=-",last_fetch)

    else:
        print("usin cathe data")

    end =  time.time()
    print("end",end)
    time_taken = round(end-start,4)

    print("Time Taken:",time_taken)

    return{
        "time_taken":time_taken,
        "data":cache_data[:5]
    }

        