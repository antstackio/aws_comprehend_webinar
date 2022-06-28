import aws_cdk as core
import aws_cdk.assertions as assertions

from comprehend_webinar.comprehend_webinar_stack import ComprehendWebinarStack

# example tests. To run these tests, uncomment this file along with the example
# resource in comprehend_webinar/comprehend_webinar_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ComprehendWebinarStack(app, "comprehend-webinar")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
