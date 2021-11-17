from django.urls import path
from hello import views, views_gen


urlpatterns=[
             path("all/",views_gen.UsersListAPIView.as_view()),
             path("filter/<str:pk>/",views.specify_user),
             path("update/<str:pk>/",views.update_user),
             path("delete/<str:pk>/",views.delete_user),
             path("new/",views.new_user)

]