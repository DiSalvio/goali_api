from rest_framework import serializers
from goali.models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = [
            "id",
            "name",
            "description",
            "timestamp",
            "completed",
            "updated",
            "removed",
            "goal",
            "task",
            "user"
        ]
