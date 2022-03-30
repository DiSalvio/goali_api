from rest_framework import serializers
from goali.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "timestamp",
            "completed",
            "updated",
            "removed",
            "goal",
            "user"
        ]
