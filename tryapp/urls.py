from django.urls import path, include
from tryapp.views import task_list, task_create, task_update, task_delete, signup, login_view, logout_view
from tryapp import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('tasks/', task_list, name='task_list'),  # Task management URLs
    path('task_list/', task_list, name='task_list'),  # Map the URL to the view
    path('categories/', views.category_list, name='category_list'),

    path('tasks/create/', task_create, name='task_create'),
    path('tasks/update/<int:pk>/', task_update, name='task_update'),
    path('tasks/delete/<int:pk>/', task_delete, name='task_delete'),
    path('signup/', signup, name='signup'),  
    path('logout/', logout_view, name='logout'),  # Logout URL

    # path('accounts/', include('django.contrib.auth.urls')),  # Django's built-in auth views
    # This includes /accounts/login/, /accounts/logout/, /accounts/password_reset/, etc.

    path('', views.home, name='home'),  # URL for the landing page

    path('login/', login_view, name='login'),  # Map login_view to 'login'

    path('logout/', logout_view, name='logout'),
    # path('add/', views.add_task, name='add_task'),

    # other urls
     


]
