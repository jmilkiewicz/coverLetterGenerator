import json

import chevron
from langchain_community.document_loaders import WebBaseLoader
from assistant import run
from langchain_community.document_loaders import SpiderLoader
from bs4 import BeautifulSoup
import json


def getJobDecription(jobDescriptionURL):
    loader = WebBaseLoader(jobDescriptionURL)
    loader.requests_kwargs = {'verify': False}
    data = loader.load()
    return data[0].page_content


def parse(content):
    soup = BeautifulSoup(content, 'html.parser')
    txt = soup.find("script", type='application/json').getText()
    asJson = json.loads(txt)
    description = asJson["props"]["pageProps"]["offer"]["body"]
    element = BeautifulSoup(description, 'html.parser')

    return element.getText()


def getJobDecription2(jobDescriptionURL):
    crawler_params = {
        'limit': 1,
        'proxy_enabled': False,
        'store_data': False,
        'metadata': False,
        'request': 'http',
        # "return_format": "text"
    }

    api_key = "sk-140d48ef-1373-4554-941d-99fc930b229e"
    loader = SpiderLoader(
        api_key=api_key,
        url=jobDescriptionURL,
        mode="scrape",
        params=crawler_params  # if no API key is provided it looks for SPIDER_API_KEY in env
    )
    content = loader.load()[0].page_content
    try:
        return parse(content)
    except Exception as err:
        error = f"Error {err=}, {type(err)=}"
        return error


def getJobDecription3(jobDescriptionURL):
    import requests
    r = requests.get(jobDescriptionURL)
    return parse(r.text)

print(getJobDecription3("https://justjoin.it/offers/ness-solution-java-developer-warszawa-java"))
# print(getJobDecription2("https://www.espn.com/"))
