import aws_cdk as core
import aws_cdk.assertions as assertions

from llama_sagemaker_inference.llama_sagemaker_inference_stack import LlamaSagemakerInferenceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in llama_sagemaker_inference/llama_sagemaker_inference_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LlamaSagemakerInferenceStack(app, "llama-sagemaker-inference")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
