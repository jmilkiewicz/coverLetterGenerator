import chevron


def handler(event, context):
    print("HOME CALLED")
    return build_response()


def build_response():
    with open('templates/home.mustache', 'r') as f:
        body = chevron.render(f,{})
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": body
        }