import chevron
from assistant import run
from bs4 import BeautifulSoup
import json


def genereateCoverLetterMessage(job_description):
    with open('templates/generateCoverLetter.mustache', 'r') as f:
        body = chevron.render(f, {"job_description": job_description})
        return {
            "role": "user",
            "content": body
        }


def getCvMessage():
    with open('templates/cv.mustache', 'r') as f:
        body = chevron.render(f, {})
        return {
            "role": "user",
            "content": f"Poniżej znajduje się moje CV, jego poszczególne sekcje są odzielone za pomocą ++++++ oraz -----:```\n {body} \n```"
        }


def getJobDecription(jobDescriptionURL):
    import requests
    r = requests.get(jobDescriptionURL)
    try:
        return parse(r.text)
    except Exception as err:
        error = f"Error {err=}, {type(err)=}"
        return error

def parse(content):
    soup = BeautifulSoup(content, 'html.parser')
    txt = soup.find("script", type='application/json').getText()
    asJson = json.loads(txt)
    description = asJson["props"]["pageProps"]["offer"]["body"]
    element = BeautifulSoup(description, 'html.parser')
    return element.getText()


def generateCoverLetter(openApiClient, jobDescriptionURL):
    jobDescription = getJobDecription(jobDescriptionURL)
    thread = openApiClient.beta.threads.create(messages=[
        getCvMessage(), genereateCoverLetterMessage(jobDescription)
    ])

    return run(openApiClient, thread.id) | {"content": jobDescription}

