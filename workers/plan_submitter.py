from celery import Celery
import requests

app = Celery('plan_submitter', broker='redis://localhost:6379/0')


@app.task
def fetch_url(url):
    resp = requests.get(url)
    #print resp.status_code
    print resp.text


def func(urls):
    for url in urls:
        fetch_url.delay(url)


if __name__ == "__main__":
    func(["http://google.com", "https://amazon.in", "https://facebook.com", "https://twitter.com", "https://alexa.com"])
