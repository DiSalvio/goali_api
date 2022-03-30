from rest_framework import serializers
from goali.models import Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            "id",
            "name",
            "description",
            "timestamp",
            "completed",
            "updated",
            "removed",
            "user"
        ]
