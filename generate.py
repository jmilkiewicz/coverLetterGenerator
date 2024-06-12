import chevron
from langchain_community.document_loaders import WebBaseLoader
from assistant import run


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
    loader = WebBaseLoader(jobDescriptionURL)
    loader.requests_kwargs = {'verify': False}
    data = loader.load()
    return data[0].page_content


def generateCoverLetter(openApiClient, jobDescriptionURL):
    jobDescription = getJobDecription(jobDescriptionURL)
    thread = openApiClient.beta.threads.create(messages=[
        getCvMessage(), genereateCoverLetterMessage(jobDescription)
    ])

    return run(openApiClient, thread.id) | {"content": jobDescription}

