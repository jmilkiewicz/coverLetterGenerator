assistantId = "asst_kdYhdMn7EOcjcvVZCmREuFpQ"


def run(openApiClient, threadId):
    run = openApiClient.beta.threads.runs.create_and_poll(
        thread_id=threadId,
        assistant_id=assistantId,
        instructions="You are a helpful assistant who is helping to prepare personalised documents to apply for a new job or project. "
                     "I am looking for a new project as a Senior Software Engineer, "
                     "Engineering Team Lead, Software Architect, or similar roles. "
                     "I need someone who can assist me in preparing my documents, such as CV, cover letter, "
                     " individual introduction. "
                     "Please respond in English."

    )

    if run.status == 'completed':
        messages = openApiClient.beta.threads.messages.list(
            thread_id=threadId, run_id=run.id
        )
        message = [{"role": m.role, "text": m.content[0].text.value} for m in messages][0]
        result = {
            "threadId": threadId, "coverLetter": message["text"]
        }
        return result
    else:
        raise Exception(f"!!!!!! error !!!!!!! {run.status}")
