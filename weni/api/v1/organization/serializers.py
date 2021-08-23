from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from weni.api.v1.fields import TextField
from weni.api.v1.project.validators import CanContributeInOrganizationValidator
from weni.common import tasks
from weni.common.models import (
    Organization,
    OrganizationAuthorization,
    RequestPermissionOrganization,
    BillingPlan,
)


class BillingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingPlan
        fields = [
            "id",
            "cycle",
            "payment_method",
            "next_due_date",
            "termination_date",
            "fixed_discount",
            "payment_method",
            "plan",
            "final_card_number",
            "card_expiration_date",
            "cardholder_name",
            "card_brand",
            "payment_warnings",
            "problem_capture_invoice",
        ]
        ref_name = None

    id = serializers.PrimaryKeyRelatedField(read_only=True, source="pk")
    cycle = serializers.ChoiceField(
        BillingPlan.BILLING_CHOICES,
        label=_("billing cycle"),
    )
    payment_method = serializers.ChoiceField(
        BillingPlan.PAYMENT_METHOD_CHOICES,
        label=_("payment method"),
        default=BillingPlan.PAYMENT_METHOD_CREDIT_CARD,
    )
    fixed_discount = serializers.FloatField(read_only=True)
    termination_date = serializers.DateField(read_only=True)
    next_due_date = serializers.DateField(read_only=True)
    plan = serializers.ChoiceField(
        BillingPlan.PLAN_CHOICES, label=_("plan"), default=BillingPlan.PLAN_FREE
    )
    final_card_number = serializers.CharField(
        read_only=True,
        allow_null=True,
        allow_blank=True,
    )
    card_expiration_date = serializers.CharField(
        read_only=True,
        allow_null=True,
        allow_blank=True,
    )
    cardholder_name = TextField(
        read_only=True,
        allow_null=True,
        allow_blank=True,
    )
    card_brand = serializers.CharField(
        read_only=True,
        allow_null=True,
        allow_blank=True,
    )
    payment_warnings = serializers.ListField()
    problem_capture_invoice = serializers.BooleanField()


class OrganizationSeralizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "uuid",
            "name",
            "description",
            "organization_billing",
            "organization_billing_cycle",
            "organization_billing_payment_method",
            "organization_billing_plan",
            "inteligence_organization",
            "authorizations",
            "authorization",
            "created_at",
            "is_suspended",
        ]
        ref_name = None

    uuid = serializers.UUIDField(style={"show": False}, read_only=True)
    name = serializers.CharField(max_length=40, required=True)
    inteligence_organization = serializers.IntegerField(read_only=True)
    authorizations = serializers.SerializerMethodField(style={"show": False})
    authorization = serializers.SerializerMethodField(style={"show": False})
    organization_billing = BillingPlanSerializer(read_only=True)
    organization_billing_cycle = serializers.ChoiceField(
        BillingPlan.BILLING_CHOICES,
        label=_("billing cycle"),
        source="organization_billing__cycle",
        write_only=True,
        required=True,
    )
    organization_billing_payment_method = serializers.ChoiceField(
        BillingPlan.PAYMENT_METHOD_CHOICES,
        label=_("payment method"),
        source="organization_billing__payment_method",
        write_only=True,
        required=True,
    )
    organization_billing_plan = serializers.ChoiceField(
        BillingPlan.PLAN_CHOICES,
        label=_("plan"),
        source="organization_billing__plan",
        write_only=True,
        required=True,
    )
    is_suspended = serializers.BooleanField(
        label=_("is suspended"),
        default=False,
        required=False,
        help_text=_("Whether this organization is currently suspended."),
    )

    def create(self, validated_data):
        task = tasks.create_organization.delay(  # pragma: no cover
            validated_data.get("name"),
            self.context["request"].user.email,
        )
        if not settings.TESTING:
            task.wait()  # pragma: no cover

        organization = task.result

        validated_data.update({"inteligence_organization": organization.get("id")})

        instance = super(OrganizationSeralizer, self).create(validated_data)

        instance.send_email_organization_create(
            email=self.context["request"].user.email,
            first_name=self.context["request"].user.first_name,
        )

        instance.authorizations.create(
            user=self.context["request"].user, role=OrganizationAuthorization.ROLE_ADMIN
        )

        return instance

    def get_authorizations(self, obj):
        return {
            "count": obj.authorizations.count(),
            "users": [
                {
                    "username": i.user.username,
                    "first_name": i.user.first_name,
                    "last_name": i.user.last_name,
                    "role": i.role,
                    "photo_user": i.user.photo_url,
                }
                for i in obj.authorizations.all()
            ],
        }

    def get_authorization(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None

        data = OrganizationAuthorizationSerializer(
            obj.get_user_authorization(request.user)
        ).data
        return data


class OrganizationAuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationAuthorization
        fields = [
            "uuid",
            "user",
            "user__id",
            "user__username",
            "user__email",
            "user__photo",
            "organization",
            "role",
            "can_read",
            "can_contribute",
            "can_write",
            "is_admin",
            "created_at",
        ]
        read_only = ["user", "user__username", "organization", "role", "created_at"]
        ref_name = None

    user__id = serializers.IntegerField(source="user.id", read_only=True)
    user__username = serializers.SlugRelatedField(
        source="user", slug_field="username", read_only=True
    )
    user__email = serializers.EmailField(
        source="user.email", label=_("Email"), read_only=True
    )
    user__photo = serializers.ImageField(
        source="user.photo", label=_("User photo"), read_only=True
    )


class OrganizationAuthorizationRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationAuthorization
        fields = ["role"]
        ref_name = None

    def validate(self, attrs):
        if attrs.get("role") == OrganizationAuthorization.LEVEL_NOTHING:
            raise PermissionDenied(_("You cannot set user role 0"))
        return attrs


class RequestPermissionOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestPermissionOrganization
        fields = ["id", "email", "organization", "role", "created_by"]
        ref_name = None

    email = serializers.EmailField(max_length=254, required=True)
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects,
        style={"show": False},
        required=True,
        validators=[CanContributeInOrganizationValidator()],
    )
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), style={"show": False}
    )

    def validate(self, attrs):
        if attrs.get("role") == OrganizationAuthorization.LEVEL_NOTHING:
            raise PermissionDenied(_("You cannot set user role 0"))
        return attrs
