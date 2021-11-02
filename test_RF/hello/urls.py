from django.urls import path
from hello import views


urlpatterns=[
             path("all/",views.all_users),
             path("filter/<str:pk>/",views.specify_user),
             path("update/<str:pk>/",views.update_user),
             path("delete/<str:pk>/",views.delete_user),
             path("new/",views.new_user)

]