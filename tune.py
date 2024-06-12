import chevron
from langchain_community.document_loaders import WebBaseLoader

from assistant import run


def tuneCoverLetter(openApiClient, params):
    threadId = params["threadId"]
    userMsg = params["feedback"]

    openApiClient.beta.threads.messages.create(
        thread_id=threadId,
        role="user",
        content=userMsg
    )

    return run(openApiClient, threadId)

#
# from openai import OpenAI
#
#
#
#
#
# from dotenv import load_dotenv
# from pathlib import Path
#
# dotenv_path = Path('.env')
# load_dotenv(dotenv_path=dotenv_path)
#
#
# client = OpenAI()
# result = generateCoverLetter(client,"not impoer")
# print(result)
