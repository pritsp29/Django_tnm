
from django.urls import path
from . import views
 
urlpatterns = [
    path("employee/", views.EmployeeListSet.as_view()),
    path("employee/<int:pk>/", views.EmployeeRetrieveSet.as_view()),
    path("employee/<int:pk>/department/", views.EmployeeDepartmentListSet.as_view()),
    path("employee/highest-salary/", views.HighestSalary.as_view()),
    path('employees/second-highest-salary/', views.SecondHighestSalaryByDepartmentView.as_view(), name='second-highest-salary'),

    path("department/", views.DepartmentViewSet.as_view()),
    path("department/<int:pk>/", views.DepartmentRetrieveSet.as_view()),
    path('department/total-salary/',views.TotalSalaryByDepartmentView.as_view(), name='highest-salary'),

    path("projects/", views.ProjectViewSet.as_view()),
    path('projects/<int:pk>/', views.ProjectViewSet.as_view(), name='project-detail'),
    path('projects/<int:pk>/add-member/', views.AddMemberToProjectView.as_view(), name='project-add-member'),
    path('projects/<int:pk>/update-status/', views.ProjectViewSet.as_view(), name='project-update-status'),
    path('projects/<int:pk>/budget/', views.ProjectBudgetView.as_view(), name='project-budget'),
    path("projects/new/", views.NewProject.as_view()),
    path("projects/ongoing/", views.OngoingProject.as_view()),
    path("projects/ended/", views.EndedProject.as_view()),
]