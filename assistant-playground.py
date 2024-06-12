from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


client = OpenAI()

system_instruction = "Jesteś pomocnym który pomaga mi znaleźć pracę. Szukam dla siebie nowego projektu " \
                      "jako Senior Software Engineer/Engineering Team Lead/Software Architect i pokrewne. " \
                       "Potrzebuję kogoś kto pomoze mi przygotować moje dokumenty takie jak CV, cover letter. " \
                      "Odpowiadaj w języku angielskim."

assistant = client.beta.assistants.create(
    name=" Job apply document generator",
    instructions=system_instruction,
    tools=[],
    model="gpt-4o",
)

print(assistant)