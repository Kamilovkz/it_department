from rest_framework import serializers

from django.db.models import Sum

from .models import Department, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")

    class Meta:
        model = Employee
        fields = "__all__"

    def create(self, validated_data):
        department_name = validated_data.pop("department")["name"]
        department, _ = Department.objects.get_or_create(name=department_name)
        validated_data["department"] = department
        return super().create(validated_data)


class DepartmentSerializer(serializers.ModelSerializer):
    num_employees = serializers.SerializerMethodField()
    sum_salary = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = "__all__"

    def get_num_employees(self, obj):
        return obj.employee_set.count()

    def get_sum_salary(self, obj):
        return obj.employee_set.aggregate(total_salary=Sum("salary"))["total_salary"] or 0
