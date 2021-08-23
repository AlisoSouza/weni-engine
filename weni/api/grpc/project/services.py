from django_grpc_framework import generics
from google.protobuf import empty_pb2

from weni import utils
from weni.api.grpc.project.serializers import (
    ClassifierRequestSerializer,
    CreateClassifierRequestSerializer,
    DestroyClassifierRequestSerializer,
    RetrieveClassifierRequestSerializer,
)
from weni.common.models import Project
from weni.protos.connect.project_pb2 import ClassifierResponse


class ProjectService(
    generics.GenericService,
):
    def Classifier(self, request, context):
        serializer = ClassifierRequestSerializer(message=request)

        if serializer.is_valid(raise_exception=True):
            project_uuid = serializer.validated_data.get("project_uuid")

            project = Project.objects.get(uuid=project_uuid)

            grpc_instance = utils.get_grpc_types().get("flow")
            response = grpc_instance.get_classifiers(
                project_uuid=str(project.flow_organization),
                classifier_type="bothub",
                is_active=True,
            )

            for i in response:
                yield ClassifierResponse(
                    authorization_uuid=i.get("authorization_uuid"),
                    classifier_type=i.get("classifier_type"),
                    name=i.get("name"),
                    is_active=i.get("is_active"),
                    uuid=i.get("uuid"),
                )

    def CreateClassifier(self, request, context):
        serializer = CreateClassifierRequestSerializer(message=request)

        if serializer.is_valid(raise_exception=True):
            project_uuid = serializer.validated_data.get("project_uuid")

            project = Project.objects.get(uuid=project_uuid)

            grpc_instance = utils.get_grpc_types().get("flow")
            response = grpc_instance.create_classifier(
                project_uuid=str(project.flow_organization),
                user_email=serializer.validated_data.get("user"),
                classifier_type="bothub",
                classifier_name=serializer.validated_data.get("name"),
                access_token=serializer.validated_data.get("access_token"),
            )

            return ClassifierResponse(
                authorization_uuid=response.get("access_token"),
                classifier_type=response.get("classifier_type"),
                name=response.get("name"),
                is_active=response.get("is_active"),
                uuid=response.get("uuid"),
            )

    def RetrieveClassifier(self, request, context):
        serializer = RetrieveClassifierRequestSerializer(message=request)

        if serializer.is_valid(raise_exception=True):
            classifier_uuid = serializer.validated_data.get("uuid")

            grpc_instance = utils.get_grpc_types().get("flow")
            response = grpc_instance.get_classifier(
                classifier_uuid=str(classifier_uuid),
            )

            return ClassifierResponse(
                authorization_uuid=response.get("access_token"),
                classifier_type=response.get("classifier_type"),
                name=response.get("name"),
                is_active=response.get("is_active"),
                uuid=response.get("uuid"),
            )

    def DestroyClassifier(self, request, context):
        serializer = DestroyClassifierRequestSerializer(message=request)

        if serializer.is_valid(raise_exception=True):
            classifier_uuid = serializer.validated_data.get("uuid")

            grpc_instance = utils.get_grpc_types().get("flow")
            grpc_instance.delete_classifier(
                classifier_uuid=str(classifier_uuid),
            )

            return empty_pb2.Empty()
