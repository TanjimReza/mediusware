from rest_framework import serializers
from tasks.models import Task  # Import models from your other app


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'  # Or specify fields you want to include
