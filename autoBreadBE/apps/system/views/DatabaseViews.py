import os
from datetime import timezone, datetime

from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
import subprocess
from django.conf import settings

from django.core.files.storage import FileSystemStorage
from autoBreadBE.utils.pagination import CustomPagination
from apps.system.models import DatabaseBackup
from apps.system.serializers.DatabaseSerializer import DatabaseBackupSerializer


class DatabaseViewSet(ModelViewSet):
    # 全局配置了验证因此不必写身份验证
    queryset = DatabaseBackup.objects.all()
    serializer_class = DatabaseBackupSerializer

    def list(self, request, page, limit):
        """获取所有用户信息"""
        queryset = self.filter_queryset(self.get_queryset())

        # 使用分页器
        paginator = CustomPagination(request, queryset, DatabaseBackupSerializer, page, limit)
        if not queryset.exists():
            return Response({"code": 404, "message": "找不到备份信息", "data": "null", "ok": False})
        serializer = self.get_serializer(queryset, many=True)
        total = len(serializer.data)

        # 取得分页器返回结果
        result = paginator.get_paginated_data()  # 每页数据
        # print()

        # 获取当页数据
        page_data = result["data"]
        # 获取总页数
        pages = result["pages"]
        return Response({"code": 200, "message": "成功",
                         "data": {"records": page_data,
                                  "total": total,
                                  "size": limit,
                                  "current": page,
                                  "pages": pages}, "ok": True})

    def get_queryset(self):
        queryset = super().get_queryset()
        # 如果请求中包含查询参数，则根据参数进行过滤
        keyword = self.request.query_params.get('backupName', None)
        if keyword:
            queryset = queryset.filter(backup_name__icontains=keyword)
            # print(queryset)
        return queryset

    def create(self, request, *args, **kwargs):
        """保存前端传入的添加备份数据并生成备份文件"""

        # 数据库配置
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']

        # 创建备份文件名，使用当前时间戳
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{db_name}_{timestamp}.sql"
        backup_name = request.data.get('backupName')
        backup_description = request.data.get('backupDesc')

        # 存储目录，不存在则创建一个
        backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups/')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        backup_file_path = os.path.join(backup_dir, backup_filename)

        mysqldump_cmd = [
            'mysqldump',
            '-u', db_user,
            '-p' + db_password,  # 注意：这里为了简洁直接包含了密码，但在生产环境中不推荐这样做
            db_name
        ]
        mysqldump_cmd_with_output = mysqldump_cmd + ['--result-file=' + backup_file_path]

        try:
            backup_true_file = 'backups/' + backup_filename
            # 使用subprocess运行命令，不要使用shell=True，除非你能确保命令是安全的
            subprocess.run(mysqldump_cmd_with_output, check=True, text=True)
            backup_instance = DatabaseBackup(
                backup_name=backup_name,
                backup_description=backup_description,
                backup_file=backup_true_file,  # 注意：这里只保存文件名，Django的FileField会自动处理文件路径
            )
            backup_instance.save()
            backup_data = {
                'id': backup_instance.id,
                'backup_name': backup_instance.backup_name,
                'backup_description': backup_instance.backup_description,
                'backup_file': backup_instance.backup_file.name,  # 注意这只是文件名，不包括完整路径
                # 你可以添加其他需要的字段
            }
        except subprocess.CalledProcessError as e:
            print(f"Error creating database backup: {e.stderr}")
            # 注意：这里返回Response可能不合适，因为这不是在Django视图函数中
            # 在非视图函数的上下文中，你可能想要抛出一个异常或返回一个错误消息
            return Response({"error": "Failed to create database backup"}, status=500)

        return Response({"code": 200, "message": "成功", "data": backup_data, "ok": False})

    def update(self, request, *args, **kwargs):
        """修改前端传入的对象数据并保存到数据库"""
        # 检索要更新的对象
        # print(request.data)
        instance = self.get_object()

        # 序列化要更新的对象，使用请求中的数据
        serializer = self.get_serializer(instance, data=request.data)

        # 验证并保存序列化数据
        result = serializer.is_valid()
        # 如果未通过校验
        if not result:
            return Response({"code": 201, "message": "失败", "data": None, "ok": False})
        serializer.save()
        return Response({"code": 200, "message": "成功", "data": None, "ok": True})

    def perform_destroy(self, instance):
        try:
            instance.backup_file.delete(save=False)
        except Exception as e:
            print(f"错误原因 {e}")
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        """删除前端url中id对应的用户数据"""
        try:
            self.perform_destroy(self.get_object())
            # print(self.get_object().backup_file.path)
            return Response({'code': 200, 'message': '成功', "data": None, "ok": True})
        except Exception as e:
            return Response({'code': 201, 'message': '失败理由为：' + str(e), "data": None, "ok": False})

    def delete_batch(self, request, pk_list):
        """批量删除"""
        id_list = pk_list.split(',')
        try:
            id_list = [int(pk) for pk in id_list]  # 获取要删除的对象的ID列表

            # 逐个删除数据库记录和关联的文件
            for pk in id_list:
                try:
                    instance = DatabaseBackup.objects.get(pk=pk)
                    # 删除文件
                    if instance.backup_file:
                        instance.backup_file.delete(save=False)  # 删除文件，不保存数据库更改（因为我们稍后会批量删除）
                    # 删除数据库记录
                    instance.delete()
                except DatabaseBackup.DoesNotExist:
                    # 如果记录不存在，可以选择记录日志或忽略
                    pass
                except Exception as e:
                    # 如果在删除文件或数据库记录时发生异常，可以记录并继续或选择中断
                    print(f"删除失败的备份ID：原因为：{pk}: {e}")
                    # 可以选择中断或继续，这里我们选择继续

            # 如果需要，可以在这里添加额外的逻辑，比如发送通知等

            return Response({'code': 200, 'message': '批量删除成功', "data": None, "ok": True})
        except Exception as e:
            return Response({'code': 500, 'message': '批量删除失败，原因：' + str(e), "data": None, "ok": False})

    @action(detail=False, methods=['post'])
    def restore(self, request, *args, **kwargs):
        # print("恢复")
        id = request.data.get('id')
        # 数据库配置
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        try:
            obj = DatabaseBackup.objects.get(id=id)
            backup_file_path = obj.backup_file.path  # 假设这是文件在服务器上的完整路径
            print(backup_file_path)
            # 检查文件是否存在
            if not FileSystemStorage().exists(backup_file_path):
                return Response({'code': 404, 'message': '备份文件不存在', "data": None, "ok": False})
            mysql_restore_cmd = f"mysql -u {db_user} -p{db_password} {db_name} < {backup_file_path}"
            try:
                # 注意：使用shell=True时要小心，确保命令字符串是安全的
                subprocess.run(mysql_restore_cmd, shell=True, check=True, stdout=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while executing command: {e}")
                # 恢复成功
            return Response({'code': 200, 'message': '恢复成功', "data": None, "ok": True})

        except DatabaseBackup.DoesNotExist:
            return Response({'code': 404, 'message': '备份记录不存在', "data": None, "ok": False})
        except Exception as e:
            # 处理其他可能的异常
            return Response({'code': 500, 'message': str(e), "data": None, "ok": False})