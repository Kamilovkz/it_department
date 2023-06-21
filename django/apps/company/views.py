from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer

# Create your views here.


class CustomEmployeePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class EmployeeAPIView(APIView):
    pagination_class = CustomEmployeePagination

    def get(self, request, format=None):
        employees = Employee.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(employees, request)
        serializer = EmployeeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        employees = Employee.objects.all()
        employees.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentAPIView(APIView):
    def get(self, request, format=None):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        departments = Department.objects.all()
        departments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeesByDepartmentAPIView(APIView):
    def get(self, request, department, format=None):
        departments = Department.objects.filter(name=department)
        department_data = []
        for department in departments:
            employees = department.employee_set.all()  # type: ignore
            serializer = EmployeeSerializer(employees, many=True)
            department_data.append({"department": department.name, "employees": serializer.data})  # noqa: E501
        return Response(department_data)


###################################################################
# I also made using generics, but it a little bit complicated way #
###################################################################


# class EmployeeListAPIView(generics.ListAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer


# class EmployeeDetailAPIView(generics.RetrieveAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     lookup_field = "employee_id"


# class EmployeeCreateAPIView(generics.CreateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer


# class EmployeeDeleteAPIView(generics.DestroyAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     lookup_field = "employee_id"


# class DepartmentListAPIView(generics.ListAPIView):
#     queryset = Department.objects.all()
#     serializer_class = DepartmentSerializer


# class DepartmentCreateAPIView(generics.CreateAPIView):
#     queryset = Department.objects.all()
#     serializer_class = DepartmentSerializer
