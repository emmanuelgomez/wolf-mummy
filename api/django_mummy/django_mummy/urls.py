from django.contrib import admin
from django.urls import path
from core import views


urlpatterns = [
    path('todos/', views.TodoList.as_view(), name='todo-list-view'),
    path('todos/<int:pk>/', views.TodoItem.as_view()),
    path('investors/', views.InvestorList.as_view(), name='investors-list-view'),
    path('investors/<int:pk>/', views.InvestorItem.as_view()),
    path('dashboard/', views.DashboardItem.as_view(), name='dashboard-view'),
    path('admin/', admin.site.urls),
    path('', views.APIRoot.as_view()),
]
