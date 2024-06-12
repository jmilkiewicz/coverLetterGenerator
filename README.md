# Generate Cover Letter
This package contains the infrastructure and the code to deploy and run a generate cover letter on AWS lambda. It used 
OpenAPI Assistant API.


## Code organization
### app.py
Contains the infrastructure code written in CDK that will be deployed to AWS

### config.py
Contains the configuration used by the infrastructure and the application code. The current setup expects the API keys to be stored in Secrets Manager under the name `api-keys`. For example, the secrets in the AWS console will look like this:
```json
{
    "openai-api-key": "<api-key-value>"
}
```

## Deploying to AWS

Clone the repository
```bash
git clone ...
```


Install the dependencies; this creates a Conda env named `cover-letter-creator` and activates it.
```bash
conda deactivate
conda env create -f environment.yml # only needed once
conda activate cover-letter-creator
```

### put your cv 
create `cv.mustache` in templates folder where you put your CV in txt format.


### Create assistant 
You just do it once. You can use assistant-playground.py. After generation the id of your assistant must be put in assistant.py
You can review your assistant https://platform.openai.com/assistants

Bundle the code for Lambda deployment.
```bash
./bundle.sh
```

Deploy to your AWS account. These steps require that you must have configured the AWS credentials on your machine using the AWS CLI and using an account that has permissions to deploy and create infrastructure. See the [AWS CLI setup page](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html) and the [CDK guide](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) to learn more.
```bash
cdk bootstrap # Only needed once, if you have not used CDK before in your account
cdk deploy
```
After you run the above commands, you will see a list of assets that this code will generate and you will be asked whether you want to proceed. Enter `y` to go ahead with the deployment. Copy and save the API URL generated from the deployment; this will be used when you create the Slack app.

## Executing the API
Note the api-id from the deployment step. This is the first part in the endpoint URL generated from the deployment. For example, api-id is `xxxxxxx` in the endpoint URL `https://xxxxxxx.execute-api.eu-west-1.amazonaws.com/prod/`.

Get the resource id.
```bash
aws apigateway get-resources --rest-api-id <api-id> --output=text
# you will see an output like this, copy the resource id value, which is 789ai1gbjn in this sample
#ITEMS   2woq7e  m4mmck1fwg      /generate       generate
#ITEMS   m4mmck1fwg              /
#ITEMS   v11sfa  m4mmck1fwg      /tune   tune
#(END)
```

Invoke the  api (easier with GET ,so with resource-id being _m4mmck1fwg_ but it returns HTML here) 
```bash
aws apigateway test-invoke-method --rest-api-id <api-id> \
    --http-method GET \
    --resource-id <resource-id> \
    --output json
```

### Testing
I mostly use it against offers on https://justjoin.it/ so the the job description URL would be `https://justjoin.it/offers/allegro-engineering-team-manager-java-kotlin---tp-o-poznan-java`


