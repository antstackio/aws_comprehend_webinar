from os import path
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
import aws_cdk
from constructs import Construct
from aws_cdk import aws_s3, aws_lambda, aws_lambda_event_sources, aws_ses, aws_iam

class ComprehendWebinarStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.STACKPREFIX = 'sm-webinar'
        
        self.bucket = aws_s3.Bucket(self,
            id=f'{self.STACKPREFIX}-data-store',
            auto_delete_objects=True,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY
        )
        self.request_handler = aws_lambda.Function(self,
            id=f'{self.STACKPREFIX}-client-request',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.from_asset('src'),
            handler='main.handler'
        )
        self.request_handler.add_environment(key='SOURCEBUCKET', value=self.bucket.bucket_name)
        self.request_url = self.request_handler.add_function_url(
            auth_type=aws_lambda.FunctionUrlAuthType.NONE,
            cors=aws_lambda.FunctionUrlCorsOptions(allowed_origins=['*'])
        )
        self.request_handler.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=['s3:PutObject', 's3:GetObject'],
                resources=[f"{self.bucket.bucket_arn}/*"]
            )
        )

        self.invoke_comprehend = aws_lambda.Function(self,
            id=f'{self.STACKPREFIX}-invoke-comprehend',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.from_asset('src'),
            handler='text.handler'
        )
        self.invoke_comprehend.add_event_source(
            source=aws_lambda_event_sources.S3EventSource(self.bucket,
                events=[aws_s3.EventType.OBJECT_CREATED],
                filters=[aws_s3.NotificationKeyFilter(prefix='complaints/')]
            )
        )
        self.invoke_comprehend.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=['s3:GetObject', 's3:List*'],
                resources=[f'{self.bucket.bucket_arn}/*']
            )
        )

