from rest_framework import serializers
from apps.system.models import DatabaseBackup


class DatabaseBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseBackup
        fields = ['id', 'backup_name', 'backup_date', 'backup_description', 'backup_file']
