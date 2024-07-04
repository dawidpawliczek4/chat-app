from rest_framework import serializers
from .models import Account


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("username", "password")

    def is_valid(self, *, raise_exception=False):
        valid = super().is_valid(raise_exception=raise_exception)
        if valid:
            username = self.validated_data["username"]
            if Account.objects.filter(username=username).exists():
                self._errors["username"] = ["Username already exists"]
                valid = False
        return valid

    def create(self, validated_data):
        user = Account.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("username",)
