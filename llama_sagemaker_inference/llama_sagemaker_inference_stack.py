from aws_cdk import (
    Stack
)

import aws_cdk.aws_iam as iam
import aws_cdk.aws_sagemaker as sagemaker
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_s3_deployment as s3deploy

from constructs import Construct

class LlamaSagemakerInferenceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    def create_model(self, id_:str, model_name: str, image_name: str, s3_url: str) -> sagemaker.CfnModel:
        role = iam.Role(
            self, id=f"{id_}-SageMakerRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
            ]
        )

        '''
        model_artifact_bucket = s3.Bucket(
            self, f"modelartifact",
            bucket_name=f"modelartifact",
        )
        
        artifact_deployment = s3deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3deploy.Source.asset(str(model_artifact_path))],
            destination_bucket=model_artifact_bucket
        )
        '''

        container = sagemaker.CfnModel.ContainerDefinitionProperty(
            container_hostname=image_name,
            image=f"{self.account}.dkr.ecr.{self.region}.amazonaws.com/{image_name}:latest",
            model_data_url=s3_url,
            #environment={"MODEL_SERVER_WORKERS": 1}
        )

        return sagemaker.CfnModel(
            self, id=f"{id_}-SageMakerModel",
            model_name=model_name,
            execution_role_arn=role.role_arn,
            containers=[container],
            
        )
    
    def create_endpoint_configuration(self, id_: str, model_name: str, endpoint_configuration_name: str) -> sagemaker.CfnEndpointConfig:
        return sagemaker.CfnEndpointConfig(
            self, id=f"{id_}-SageMakerEndpointConfiguration",
            endpoint_config_name=endpoint_configuration_name,
            production_variants=[
                sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                    model_name=model_name,
                    initial_instance_count=1,
                    initial_variant_weight=1.0,
                    variant_name="all-traffic",
                    #serverless_config=sagemaker.CfnEndpointConfig.ServerlessConfigProperty(
                    #    max_concurrency=1,
                    #    memory_size_in_mb=3072 #5120
                    #),
                    instance_type="ml.m5.xlarge",
                    volume_size_in_gb=15
                )
            ]
        )
    
    def create_endpoint(
        self,
        id_: str,
        endpoint_configuration_name: str,
        endpoint_name: str,
    ) -> sagemaker.CfnEndpoint:
        return sagemaker.CfnEndpoint(
            self,
            id=f"{id_}-SageMakerEndpoint",
            endpoint_config_name=endpoint_configuration_name,
            endpoint_name=endpoint_name,
        )
