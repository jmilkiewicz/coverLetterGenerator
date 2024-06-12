from aws_cdk import (
    App, Duration, Stack,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_secretsmanager as secretsmanager,
    aws_iam as iam
)
import config


class LangChainApp(Stack):
    def __init__(self, app: App, id: str) -> None:
        super().__init__(app, id)

        api = apigateway.RestApi(self, "generateCoverLetter-api",
                                 rest_api_name="Api for generating cover letter ",
                                 description="Showcases open api assistant"
                                 )

        handler_homePage = lambda_.Function(self, "generateCoverLetterHome",
                                            runtime=lambda_.Runtime.PYTHON_3_12,
                                            code=lambda_.Code.from_asset("dist/lambda.zip"),
                                            handler="lambda/generateCoverLetterHome.handler",
                                            layers=[
                                                lambda_.LayerVersion.from_layer_version_arn(
                                                    self,
                                                    "SecretsExtensionLayer1",
                                                    layer_version_arn=config.config.SECRETS_EXTENSION_ARN
                                                )
                                            ],
                                            timeout=Duration.minutes(5)
                                            )
        api.root.add_method(
            "GET",
            apigateway.LambdaIntegration(handler_homePage)
        )

        handler_generatCoverLetter = lambda_.Function(self, "generateCoverLetter",
                                                      runtime=lambda_.Runtime.PYTHON_3_12,
                                                      code=lambda_.Code.from_asset("dist/lambda.zip"),
                                                      handler="lambda/generateCoverLetter.handler",
                                                      layers=[
                                                          lambda_.LayerVersion.from_layer_version_arn(
                                                              self,
                                                              "SecretsExtensionLayer2",
                                                              layer_version_arn=config.config.SECRETS_EXTENSION_ARN
                                                          )
                                                      ],
                                                      timeout=Duration.minutes(5)
                                                      )

        handler_tuneCoverLetter = lambda_.Function(self, "tuneCoverLetter",
                                                   runtime=lambda_.Runtime.PYTHON_3_12,
                                                   code=lambda_.Code.from_asset("dist/lambda.zip"),
                                                   handler="lambda/tuneCoverLetter.handler",
                                                   layers=[
                                                       lambda_.LayerVersion.from_layer_version_arn(
                                                           self,
                                                           "SecretsExtensionLayer3",
                                                           layer_version_arn=config.config.SECRETS_EXTENSION_ARN
                                                       )
                                                   ],
                                                   timeout=Duration.minutes(5)
                                                   )

        secret = secretsmanager.Secret.from_secret_name_v2(self, 'secret', config.config.API_KEYS_SECRET_NAME)

        secret.grant_read(handler_generatCoverLetter)
        secret.grant_write(handler_generatCoverLetter)

        secret.grant_read(handler_tuneCoverLetter)
        secret.grant_write(handler_tuneCoverLetter)

        generateCoverLetterRequestModel = api.add_model("generateCoverLetterRequestModel",
                                                        content_type="application/json",
                                                        model_name="generateCoverLetterRequestModel",
                                                        description="Schema for generateCoverLetter request payload",
                                                        schema={
                                                            "title": "requestParameters",
                                                            "type": apigateway.JsonSchemaType.OBJECT,
                                                            "properties": {
                                                                "url": {
                                                                    "type": apigateway.JsonSchemaType.STRING,
                                                                    "minLength": 2,
                                                                }
                                                            },
                                                            "required": ["url"]
                                                        }
                                                        )

        tuneCoverLetterRequestModel = api.add_model("tuneCoverLetterRequestModel", content_type="application/json",
                                                    model_name="tuneCoverLetterRequestModel",
                                                    description="Schema for tune CoverLetter request payload",
                                                    schema={
                                                        "title": "requestParameters",
                                                        "type": apigateway.JsonSchemaType.OBJECT,
                                                        "properties": {
                                                            "threadId": {
                                                                "type": apigateway.JsonSchemaType.STRING,
                                                                "minLength": 2,
                                                            },
                                                            "feedback": {
                                                                "type": apigateway.JsonSchemaType.STRING,
                                                                "minLength": 1,
                                                            },

                                                        },
                                                        "required": ["threadId", "feedback"]
                                                    }
                                                    )

        generate = api.root.add_resource("generate")

        generate.add_method(
            "POST",
            apigateway.LambdaIntegration(handler_generatCoverLetter),
            request_models={
                "application/json": generateCoverLetterRequestModel
            },
            request_validator_options={
                "request_validator_name": 'generatePostvalidator',
                "validate_request_body": True,
                "validate_request_parameters": False
            }
        )

        tune = api.root.add_resource("tune")

        tune.add_method(
            "POST",
            apigateway.LambdaIntegration(handler_tuneCoverLetter),
            request_models={
                "application/json": tuneCoverLetterRequestModel
            },
            request_validator_options={
                "request_validator_name": 'tunePostvalidator',
                "validate_request_body": True,
                "validate_request_parameters": False
            }
        )


app = App()
LangChainApp(app, "GenerateCoverLetterApp")
app.synth()
