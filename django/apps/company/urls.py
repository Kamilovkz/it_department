from django.urls import path

from . import views

urlpatterns = [
    path("api/departments/", views.DepartmentAPIView.as_view(), name="department"),
    path("api/employees/", views.EmployeeAPIView.as_view(), name="employee"),
    path(
        "api/employees/<str:department>/", views.EmployeesByDepartmentAPIView.as_view(), name="employees_by_department"
    ),
]
