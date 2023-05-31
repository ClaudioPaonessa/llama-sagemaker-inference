#!/usr/bin/env python3
import builtins
import os
from pathlib import Path
import typing

import aws_cdk as cdk
from aws_cdk import IPolicyValidationPluginBeta1, IReusableStackSynthesizer

from llama_sagemaker_inference.llama_sagemaker_inference_stack import LlamaSagemakerInferenceStack

class LlamaInferenceApp(cdk.App):
    def __init__(self) -> None:
        super().__init__()

        # https://huggingface.co/vicuna/ggml-vicuna-7b-1.1/blob/main/ggml-vic7b-q4_0.bin
        #model_name = "ggmlvic7bq40"
        #s3_url="s3://llama-model-artifact/ggml-vic7b-q4_0.tar.gz"

        # https://huggingface.co/TheBloke/WizardLM-7B-uncensored-GGML/blob/main/WizardLM-7B-uncensored.ggmlv3.q4_1.bin
        model_name = "wizard7bq4"
        s3_url="s3://llama-model-artifact/wizard-q4_1.tar.gz"

        sagemaker = LlamaSagemakerInferenceStack(
            scope=self,
            construct_id="app-sagemaker-stack"
        )
        model = sagemaker.create_model(
            id_="Llama",
            model_name=model_name,
            image_name="llama-inference",
            s3_url=s3_url
        )
        endpoint_config = sagemaker.create_endpoint_configuration(
            id_="AppEndpointConfiguration",
            model_name=model_name,
            endpoint_configuration_name="app-endpoint-configuration",
        )
        endpoint_config.add_dependency(model)
        endpoint = sagemaker.create_endpoint(
            id_="AppEndpoint",
            endpoint_configuration_name="app-endpoint-configuration",
            endpoint_name="app-endpoint",
        )
        endpoint.add_dependency(endpoint_config)


app = LlamaInferenceApp()
app.synth()
