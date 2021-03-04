import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

app = Flask("DayEleven")

@app.route("/")
def home():
  return render_template('home.html', subreddits=subreddits)

@app.route("/read")
def read():
  req = request.args  # 선택한 키워드 받아오기
  reading = [i for i in req] # 선택한 키워드들(str)
  reddit_db = [] # 모든 레딧들이 저장될 db
  for topic in reading:
    url = f"https://www.reddit.com/r/{topic}/top/?t=month"
    reddit_req = requests.get(url, headers=headers).text
    soup = BeautifulSoup(reddit_req, "html.parser")
    reddit_box = soup.find(class_="rpBJOHq2PR60pnwJlUyP0")
    reddits = reddit_box.find_all("div", recursive=False)[1:]

    for reddit in reddits:
      try:
        one_reddit = {}
        one_reddit['title'] = reddit.find(class_="_eYtD2XCVieq6emjKBH3m").text
        one_reddit['link'] = reddit.find(class_="SQnoC3ObvgnGjWt90zD9Z")['href']
        one_reddit['vote'] = reddit.find(class_="_1rZYMD_4xY3gRcSS3p8ODO").text
        one_reddit['topic'] = topic
        reddit_db.append(one_reddit)
      except:
        continue

  reddit_db.sort(key=lambda x: int(x['vote']), reverse=True) # vote 내림차순으로 정렬

  return render_template('read.html', reading=reading, reddit_db=reddit_db)

app.run(host="0.0.0.0")